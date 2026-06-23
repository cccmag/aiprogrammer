# AI 應用監控與除錯（2024-2029）

## 透視 LLM 黑盒子

### 前言

傳統應用的監控已經成熟——錯誤率、延遲、吞吐量一目了然。但 AI 應用多了「語意品質」這個維度：回應可能格式正確但內容離譜。2024 年起，開發者開始建立專為 LLM 設計的觀測工具。

### 基礎監控（2024-2025）

最早的 AI 監控只是記錄 API 呼叫：

```python
# 2024：基礎日誌
def monitored_llm(prompt):
    start = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    duration = time.time() - start
    log({
        "prompt": prompt[:100],
        "response": response[:200],
        "tokens": response.usage.total_tokens,
        "latency": duration,
        "model": "gpt-4",
    })
    return response
```

但這種日誌無法幫助診斷「模型胡說八道」的問題。

### 語意監控（2025-2027）

業界開始引入評估模型來監控輸出品質：

```python
# 2026：語意監控
class SemanticMonitor:
    def check(self, prompt, response):
        checks = {
            "relevance": self.relevance_score(prompt, response),
            "hallucination": self.fact_check(response, knowledge_base),
            "toxicity": self.toxicity_filter(response),
            "consistency": self.self_consistency(prompt, response),
        }
        if any(v < threshold for v in checks.values()):
            alert(f"品質異常：{checks}")
        return checks
```

### 追蹤與除錯（2027-2028）

LLM 呼叫鏈的追蹤成為必備：

```python
# 2027：分散式追蹤
@trace(attributes={"service": "rag-pipeline"})
async def rag_answer(question):
    with span("retrieve"):
        docs = await vector_db.search(question)
    with span("generate"):
        response = await llm.generate(question, docs)
    with span("validate"):
        score = await evaluator.score(response, docs)
    return response, score
```

每個 span 記錄了 token 消耗、延遲和中間輸出。

### 自動修復（2028-2029）

AI 應用開始具備自我修復能力：

```python
# 2029：自動修復
class SelfHealingApp:
    async def call(self, request):
        response = await self.model.generate(request)
        if self.monitor.detect_anomaly(response):
            backup_model = self.fallback_router.route(request)
            response = await backup_model.generate(request)
            self.incident_log.record(request, "fallback_used")
        return response
```

### 小結

AI 應用的監控從基礎日誌進化到語意評估、分散式追蹤、自動修復。**看得見不只是回應速度，還有回應品質**。

---

**下一步**：[多模型路由與快取](focus5.md)

## 延伸閱讀

- [LLM Observability Tools](https://www.google.com/search?q=LLM+observability+monitoring+tools+2025)
- [AI Application Debugging](https://www.google.com/search?q=AI+application+debugging+LLM+tracing)
- [Semantic Monitoring Hallucination](https://www.google.com/search?q=semantic+monitoring+hallucination+detection+LLM)
