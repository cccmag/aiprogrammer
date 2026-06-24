# RAG 管線監控實戰

## 前言

RAG（Retrieval-Augmented Generation）已成為 2027 年企業 AI 應用的標準架構。然而，RAG 系統的複雜性遠超單一模型——它是一個由查詢理解、向量檢索、重新排序、上下文構建和 LLM 生成組成的多階段管線。每個環節都可能失敗，而且錯誤會沿著管線累積放大。

這正是 RAG 可觀測性的核心挑戰：你需要知道**哪個環節出了問題**、**問題的影響有多大**、以及**如何自動修復**。

## RAG 管線的可觀測性架構

### 管線階段的標準化追蹤

我們需要為 RAG 的每個階段建立標準化的追蹤點：

```python
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

@dataclass
class RAGSpan:
    span_id: str
    parent_id: str | None
    stage: str          # query_preprocessing, retrieval, reranking, context_building, generation
    start_time: float
    end_time: float | None = None
    input: Any = None
    output: Any = None
    metadata: dict = field(default_factory=dict)
    error: str | None = None
    children: list["RAGSpan"] = field(default_factory=list)

class RAGTracer:
    def __init__(self):
        self.traces: dict[str, list[RAGSpan]] = {}

    def start_trace(self, query: str) -> str:
        trace_id = f"rag_{uuid.uuid4().hex[:8]}"
        self.traces[trace_id] = []
        return trace_id

    def start_span(self, trace_id: str, stage: str,
                   parent_id: str | None = None) -> str:
        span_id = f"{stage}_{uuid.uuid4().hex[:6]}"
        span = RAGSpan(
            span_id=span_id,
            parent_id=parent_id,
            stage=stage,
            start_time=time.time()
        )
        self.traces[trace_id].append(span)
        return span_id

    def end_span(self, trace_id: str, span_id: str,
                 output: Any = None, error: str | None = None):
        for span in self.traces[trace_id]:
            if span.span_id == span_id:
                span.end_time = time.time()
                span.output = output
                span.error = error
                break

    def get_trace_report(self, trace_id: str) -> dict:
        spans = self.traces.get(trace_id, [])
        stages = {}
        for span in spans:
            if span.end_time:
                latency = (span.end_time - span.start_time) * 1000
                stages[span.span_id] = {
                    "stage": span.stage,
                    "latency_ms": round(latency, 2),
                    "error": span.error,
                }
        return {
            "trace_id": trace_id,
            "total_latency_ms": sum(
                s["latency_ms"] for s in stages.values()
            ),
            "stages": stages,
            "has_errors": any(s["error"] for s in stages.values()),
        }
```

### 實際的 RAG 管線

```python
class MonitoredRAGPipeline:
    def __init__(self, vector_store, llm_client, tracer: RAGTracer):
        self.vector_store = vector_store
        self.llm = llm_client
        self.tracer = tracer
        # 品質監控器
        self.quality_monitor = RetrievalQualityMonitor()
        self.generation_monitor = GenerationQualityMonitor()

    def query(self, user_query: str) -> tuple[str, dict]:
        trace_id = self.tracer.start_trace(user_query)

        # 階段 1：查詢預處理
        span_id = self.tracer.start_span(trace_id, "query_preprocessing")
        processed_query = self._preprocess(user_query)
        self.tracer.end_span(trace_id, span_id, output=processed_query)

        # 階段 2：向量檢索
        span_id = self.tracer.start_span(trace_id, "retrieval")
        retrieved_docs = self.vector_store.similarity_search(
            processed_query, k=5
        )
        retrieval_quality = self.quality_monitor.evaluate_retrieval(
            query=processed_query,
            results=retrieved_docs
        )
        self.tracer.end_span(
            trace_id, span_id,
            output={"count": len(retrieved_docs), "quality": retrieval_quality}
        )

        # 階段 3：重新排序
        span_id = self.tracer.start_span(trace_id, "reranking")
        reranked_docs = self._rerank(processed_query, retrieved_docs)
        self.tracer.end_span(trace_id, span_id, output={"count": len(reranked_docs)})

        # 階段 4：上下文構建
        span_id = self.tracer.start_span(trace_id, "context_building")
        context = self._build_context(reranked_docs)
        context_stats = {
            "doc_count": len(reranked_docs),
            "total_tokens": len(context.split())
        }
        self.tracer.end_span(trace_id, span_id, output=context_stats)

        # 階段 5：生成
        span_id = self.tracer.start_span(trace_id, "generation")
        try:
            response = self.llm.generate(
                system_prompt="根據以下文件回答使用者問題。",
                context=context,
                query=user_query
            )
            gen_quality = self.generation_monitor.evaluate_generation(
                query=user_query,
                response=response,
                context_docs=reranked_docs
            )
            self.tracer.end_span(
                trace_id, span_id,
                output={"response_length": len(response), "quality": gen_quality}
            )
        except Exception as e:
            self.tracer.end_span(trace_id, span_id, error=str(e))
            response = ""

        report = self.tracer.get_trace_report(trace_id)
        report["retrieval_quality"] = retrieval_quality
        report["generation_quality"] = gen_quality if 'gen_quality' in dir() else {}

        return response, report

    def _preprocess(self, query: str) -> str:
        """查詢預處理：去除停用詞、查詢重寫"""
        return query.strip()

    def _rerank(self, query: str, docs: list) -> list:
        """重新排序：可以基於交叉編碼器或 LLM"""
        return sorted(docs, key=lambda x: x.get("score", 0), reverse=True)

    def _build_context(self, docs: list) -> str:
        return "\n\n".join(d.get("content", "") for d in docs)
```

## 檢索品質監控

檢索品質是 RAG 系統的瓶頸——差的檢索必然導致差的生成：

```python
class RetrievalQualityMonitor:
    def evaluate_retrieval(self, query: str, results: list,
                           relevance_labels: list[bool] | None = None) -> dict:
        """評估檢索品質"""
        metrics = {
            "result_count": len(results),
            "avg_score": sum(r.get("score", 0) for r in results) / max(len(results), 1),
            "score_distribution": self._score_distribution(results),
        }

        if relevance_labels:
            metrics.update(self._calculate_ranking_metrics(
                results, relevance_labels
            ))

        return metrics

    def _score_distribution(self, results: list) -> dict:
        scores = [r.get("score", 0) for r in results]
        if not scores:
            return {"min": 0, "max": 0, "mean": 0}
        return {
            "min": min(scores),
            "max": max(scores),
            "mean": sum(scores) / len(scores),
            "std": (sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores))**0.5
        }

    def _calculate_ranking_metrics(self, results: list,
                                    relevance: list[bool]) -> dict:
        """計算 MRR 與 Precision@K"""
        # MRR
        mrr = 0.0
        for i, rel in enumerate(relevance):
            if rel:
                mrr = 1.0 / (i + 1)
                break

        # Precision@K
        precisions = {}
        for k in [1, 3, 5]:
            if k <= len(relevance):
                precisions[f"p@{k}"] = sum(relevance[:k]) / k

        return {"mrr": mrr, **precisions}
```

## 生成品質監控

生成階段的評估需要專門的 RAG 指標：

```python
class GenerationQualityMonitor:
    def evaluate_generation(self, query: str, response: str,
                             context_docs: list) -> dict:
        """評估生成品質"""
        return {
            "faithfulness": self._check_faithfulness(response, context_docs),
            "relevance": self._check_relevance(query, response),
            "hallucination_score": self._detect_hallucinations(response, context_docs),
            "response_stats": self._response_statistics(response),
        }

    def _check_faithfulness(self, response: str, docs: list) -> float:
        """檢查回覆是否忠於檢索文件"""
        # 簡單實作：檢查回覆中的句子是否可在文件中找到支援
        sentences = [s.strip() for s in response.split("。") if len(s.strip()) > 5]
        if not sentences:
            return 1.0

        supported = 0
        doc_text = " ".join(d.get("content", "") for d in docs).lower()

        for sentence in sentences:
            key_phrases = sentence.split("是")[-1].split()[:3]
            if any(phrase.lower() in doc_text for phrase in key_phrases):
                supported += 1

        return supported / len(sentences)

    def _check_relevance(self, query: str, response: str) -> float:
        """檢查回覆與問題的相關性"""
        query_tokens = set(query.lower().split())
        response_tokens = set(response.lower().split())
        overlap = query_tokens & response_tokens
        return len(overlap) / max(len(query_tokens), 1)

    def _detect_hallucinations(self, response: str, docs: list) -> float:
        """檢測可能幻覺的比例"""
        doc_text = " ".join(d.get("content", "") for d in docs).lower()
        sentences = [s.strip() for s in response.split("。") if len(s.strip()) > 10]
        if not sentences:
            return 0.0

        hallucinated = 0
        for s in sentences:
            # 簡單的幻覺檢測：關鍵名詞是否在文件中出現
            nouns = [w for w in s.split() if len(w) > 3]
            found = sum(1 for n in nouns if n.lower() in doc_text)
            if found / max(len(nouns), 1) < 0.3:
                hallucinated += 1

        return hallucinated / len(sentences)

    def _response_statistics(self, response: str) -> dict:
        return {
            "length_chars": len(response),
            "sentence_count": len(response.split("。")),
            "has_citations": "[" in response and "]" in response,
        }
```

## 端到端延遲與成本分析

RAG 監控的最後一塊拼圖是延遲與成本的可視化：

```python
class RAGAnalyticsDashboard:
    def __init__(self):
        self.traces: list[dict] = []

    def record_query(self, trace_report: dict):
        self.traces.append(trace_report)

    def hourly_report(self) -> dict:
        if not self.traces:
            return {}

        latencies = [t["total_latency_ms"] for t in self.traces]
        errors = [t for t in self.traces if t.get("has_errors")]

        # 各階段延遲分析
        stage_latencies = {}
        for t in self.traces:
            for span_id, info in t.get("stages", {}).items():
                stage = info["stage"]
                if stage not in stage_latencies:
                    stage_latencies[stage] = []
                stage_latencies[stage].append(info["latency_ms"])

        stage_report = {}
        for stage, lats in stage_latencies.items():
            sorted_lats = sorted(lats)
            stage_report[stage] = {
                "p50": sorted_lats[len(sorted_lats) // 2],
                "p95": sorted_lats[int(len(sorted_lats) * 0.95)],
                "p99": sorted_lats[int(len(sorted_lats) * 0.99)],
                "avg": sum(lats) / len(lats),
            }

        # 找出瓶頸階段
        bottleneck = None
        if stage_report:
            bottleneck = max(
                stage_report.items(),
                key=lambda x: x[1]["p50"]
            )[0]

        # 品質趨勢（最近 100 筆）
        recent = self.traces[-100:]
        retrieval_quality = [
            t.get("retrieval_quality", {}).get("avg_score", 0)
            for t in recent
        ]
        generation_quality = [
            t.get("generation_quality", {}).get("faithfulness", 0)
            for t in recent
        ]

        return {
            "total_queries": len(self.traces),
            "error_rate": len(errors) / max(len(self.traces), 1),
            "latency": {
                "p50": sorted(latencies)[len(latencies) // 2],
                "p95": sorted(latencies)[int(len(latencies) * 0.95)],
                "p99": sorted(latencies)[int(len(latencies) * 0.99)],
            },
            "stage_breakdown": stage_report,
            "bottleneck_stage": bottleneck,
            "quality_trends": {
                "avg_retrieval_score": sum(retrieval_quality) / max(len(retrieval_quality), 1),
                "avg_faithfulness": sum(generation_quality) / max(len(generation_quality), 1),
            },
        }
```

## 實戰建議

1. **從第一天就加入追蹤**：不要在 RAG 系統上線後才補可觀測性
2. **設定品質 SLO**：例如 faithfulness > 0.8, p95 latency < 2s
3. **自動觸發警報**：當檢索品質下降或幻覺率上升時立即通知團隊
4. **取樣儲存完整軌跡**：100% 記錄中繼資料，5% 記錄完整輸入輸出
5. **儀表板視覺化**：使用 Grafana 建立 RAG 專用儀表板，一目瞭然各階段狀態

## 參考資源

- [RAG Observability Guide](https://www.google.com/search?q=RAG+observability+monitoring+guide)
- [OpenTelemetry for RAG Pipelines](https://www.google.com/search?q=OpenTelemetry+RAG+tracing)
- [RAG Evaluation Metrics](https://www.google.com/search?q=RAG+faithfulness+relevance+evaluation)
- [Grafana RAG Dashboard](https://www.google.com/search?q=Grafana+RAG+monitoring+dashboard)
