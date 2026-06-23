# RAG 管線的可觀測性（2023-2026）

## RAG 的可觀測性挑戰

RAG（Retrieval-Augmented Generation）不是一個單一模型，而是一個由多個元件組成的管線：

1. **查詢處理**：使用者問題的預處理（重寫、擴展）
2. **向量檢索**：從向量資料庫中檢索相關文件
3. **重新排序**：對檢索結果進行精排
4. **上下文構建**：將檢索結果組合成 LLM 的上下文
5. **生成**：LLM 根據上下文生成回答

每個環節都可能出錯，而錯誤會沿著管線傳遞和放大。這就是為什麼 RAG 系統需要端到端的可觀測性。

## RAG 管線追蹤（Tracing with OpenTelemetry）

OpenTelemetry 提供了分散式追蹤的標準機制，讓你能夠追蹤每個請求在 RAG 管線中的完整路徑：

```python
# 使用 OpenTelemetry 追蹤 RAG 管線
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import time

tracer = trace.get_tracer(__name__)

class RAGPipeline:
    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        with tracer.start_as_current_span("retrieve") as span:
            span.set_attribute("query", query)
            span.set_attribute("top_k", top_k)
            start = time.time()
            
            # 模擬向量檢索
            results = self._vector_search(query, top_k)
            
            span.set_attribute("results_count", len(results))
            span.set_attribute("latency_ms", (time.time() - start) * 1000)
            return results
    
    def rerank(self, query: str, results: list[dict]) -> list[dict]:
        with tracer.start_as_current_span("rerank") as span:
            span.set_attribute("input_count", len(results))
            start = time.time()
            
            # 模擬重新排序
            reranked = sorted(results, key=lambda x: x.get("score", 0), reverse=True)
            
            span.set_attribute("output_count", len(reranked))
            span.set_attribute("latency_ms", (time.time() - start) * 1000)
            return reranked
    
    def generate(self, query: str, context: list[dict]) -> str:
        with tracer.start_as_current_span("generate") as span:
            span.set_attribute("context_length", len(context))
            start = time.time()
            
            # 模擬 LLM 生成
            response = self._call_llm(query, context)
            
            span.set_attribute("response_length", len(response))
            span.set_attribute("latency_ms", (time.time() - start) * 1000)
            return response
    
    def run(self, query: str) -> tuple[str, dict]:
        with tracer.start_as_current_span("rag_pipeline") as span:
            span.set_attribute("query", query)
            overall_start = time.time()
            
            docs = self.retrieve(query)
            docs = self.rerank(query, docs)
            answer = self.generate(query, docs)
            
            total_latency = (time.time() - overall_start) * 1000
            span.set_attribute("total_latency_ms", total_latency)
            
            return answer, {"total_latency": total_latency}
```

## 檢索品質監控

檢索階段的品質直接影響最終回答的品質。常用的檢索品質指標：

**MRR（Mean Reciprocal Rank）**：第一個相關結果的排名倒數的平均值。適合只有一個正確答案的場景。

**NDCG（Normalized Discounted Cumulative Gain）**：考慮多個相關結果的排名和相關性等級，更適合有多個相關文件的場景。

**Hit Rate**：前 K 個結果中是否包含至少一個相關文件。簡單直觀，適合快速評估。

```python
# RAG 檢索品質指標
class RetrievalQualityMonitor:
    def mean_reciprocal_rank(self, results: list[list[int]]) -> float:
        """MRR：第一個相關結果的排名倒數的平均值"""
        total = 0.0
        for query_results in results:
            for rank, relevant in enumerate(query_results, 1):
                if relevant:
                    total += 1.0 / rank
                    break
        return total / max(len(results), 1)
    
    def ndcg_at_k(self, relevant: list[int], k: int = 10) -> float:
        """NDCG@K：歸一化折損累計增益"""
        dcg = sum((2**rel - 1) / math.log2(i + 2) 
                  for i, rel in enumerate(relevant[:k]))
        ideal = sorted(relevant, reverse=True)[:k]
        idcg = sum((2**rel - 1) / math.log2(i + 2) 
                   for i, rel in enumerate(ideal))
        return dcg / max(idcg, 1e-10)
    
    def hit_rate_at_k(self, results: list[list[bool]], k: int = 5) -> float:
        """Hit Rate@K：前 K 個結果中包含相關文件的比率"""
        hits = sum(1 for r in results if any(r[:k]))
        return hits / max(len(results), 1)

# 使用範例
monitor = RetrievalQualityMonitor()
mrr = monitor.mean_reciprocal_rank([[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
print(f"MRR: {mrr:.3f}")
```

## 生成品質監控

檢索品質好不代表生成品質好。生成階段的評估需要專門的指標：

**Faithfulness（忠實度）**：模型的回答是否基於檢索到的文件，還是產生了幻覺。這是 RAG 系統最重要的品質指標。

**Answer Relevance（回答相關性）**：回答是否與使用者問題相關。可以反過來問——讓 LLM 根據回答生成問題，然後計算與原始問題的相似度。

```python
# 生成品質監控
class GenerationQualityMonitor:
    def faithfulness_score(self, answer: str, context_docs: list[str]) -> float:
        """評估回答是否忠於檢索文件"""
        # 將答案中的主張與文件進行比對
        answer_claims = self._extract_claims(answer)
        supported = 0
        for claim in answer_claims:
            for doc in context_docs:
                if claim.lower() in doc.lower():
                    supported += 1
                    break
        return supported / max(len(answer_claims), 1)
    
    def _extract_claims(self, text: str) -> list[str]:
        """從回答中提取可驗證的主張"""
        import re
        sentences = re.split(r'[。！？]', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def answer_relevance(self, question: str, answer: str, judge_llm=None) -> float:
        """評估回答與問題的相關性"""
        # 使用 LLM-as-Judge 評估相關性
        prompt = f"""問題：{question}
回答：{answer}
請評估相關性（1-5分）："""
        # 模擬評分
        return 4.2
    
    def hallucination_detection(self, answer: str, context: list[str]) -> list[str]:
        """找出回答中可能幻覺的部分"""
        hallucinations = []
        answer_claims = self._extract_claims(answer)
        for claim in answer_claims:
            found = any(claim.lower() in doc.lower() for doc in context)
            if not found:
                hallucinations.append(claim)
        return hallucinations
```

## 端到端延遲分解分析

RAG 的延遲是各階段的總和。如果不做詳細的延遲分解，你永遠不知道瓶頸在哪裡：

```python
# RAG 延遲分析
class RAGLatencyAnalyzer:
    def __init__(self):
        self.stages = {
            "query_preprocessing": [],
            "vector_search": [],
            "reranking": [],
            "context_building": [],
            "llm_generation": [],
        }
    
    def record_stage_latency(self, stage: str, latency_ms: float):
        if stage in self.stages:
            self.stages[stage].append(latency_ms)
    
    def analyze(self):
        report = {}
        for stage, latencies in self.stages.items():
            if latencies:
                report[stage] = {
                    "p50": sorted(latencies)[len(latencies) // 2],
                    "p99": sorted(latencies)[int(len(latencies) * 0.99)],
                    "avg": sum(latencies) / len(latencies),
                    "total": sum(latencies),
                }
        report["total_p50"] = sum(s["p50"] for s in report.values())
        report["bottleneck"] = max(report.items(), key=lambda x: x[1]["p50"])[0]
        return report
```

典型的 RAG 延遲分布：向量檢索佔 20-30%，LLM 生成佔 60-70%，其他步驟佔 10%。如果檢索佔比異常升高，可能是向量資料庫或索引出了問題。

---

**下一步**：[AI Agent 的行為追蹤](focus6.md)

## 延伸閱讀

- [RAG 系統可觀測性指南](https://www.google.com/search?q=RAG+observability+guide)
- [OpenTelemetry for AI Applications](https://www.google.com/search?q=OpenTelemetry+AI+tracing)
- [RAG 評估指標](https://www.google.com/search?q=RAG+evaluation+metrics+faithfulness)
- [向量檢索品質分析](https://www.google.com/search?q=vector+search+quality+MRR+NDCG)
