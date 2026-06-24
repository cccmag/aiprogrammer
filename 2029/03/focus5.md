# 多模型路由與快取（2025-2029）

## 聰明選擇，減少浪費

### 前言

2025 年，多數應用只用一個模型。問題是：簡單任務用昂貴的大模型，複雜任務用小模型又不夠力。2029 年，模型路由和語意快取成為 AI 原生的基礎設施。

### 靜態路由（2025-2026）

第一代路由根據任務類型硬編碼：

```python
# 2025：靜態路由
def route(intent: str) -> str:
    if intent in ["greeting", "faq"]:
        return "gpt-4o-mini"   # 便宜快速
    elif intent in ["code_gen", "analysis"]:
        return "gpt-4o"        # 強大昂貴
    else:
        return "claude-3-haiku"
```

### 動態路由（2026-2027）

路由開始根據輸入複雜度動態決策：

```python
# 2026：動態路由
class DynamicRouter:
    async def select(self, task) -> str:
        complexity = await self.complexity_estimator(task)
        if complexity < 0.3:
            return "gemini-2-flash"
        elif complexity < 0.7:
            return "gpt-4o"
        else:
            return "claude-4-opus"
```

### 語意快取（2025-2027）

語意快取是與路由搭配的關鍵技術：

```python
# 2026：語意快取
class SemanticCache:
    async def lookup(self, query) -> str | None:
        similar = await self.vector_db.search(
            query, threshold=0.92
        )
        if similar:
            return similar[0].response
        return None

    async def store(self, query, response):
        embedding = await self.embed(query)
        await self.vector_db.insert(query, response, embedding)
```

語意快取對重複率高的查詢可減少 40-60% 的 API 成本。

### 成本感知路由（2028-2029）

路由加入成本與延遲權衡：

```python
# 2029：成本感知路由
class CostAwareRouter:
    async def route(self, task, budget):
        candidates = [
            ("gpt-4o-mini", 0.002, 0.5),
            ("gpt-4o", 0.03, 0.2),
            ("claude-4", 0.05, 0.15),
        ]
        for model, cost, quality in candidates:
            if self.quality_sufficient(task, quality):
                if cost <= budget["per_request"]:
                    return model
        return "gpt-4o"  # 預設最強模型
```

### 小結

多模型路由從靜態映射進化為動態感知決策，搭配語意快取大幅降低成本。**核心思維是：每個任務用最適合的模型，不做過度推理**。

---

**下一步**：[AI 應用安全設計](focus6.md)

## 延伸閱讀

- [LLM Routing Strategies](https://www.google.com/search?q=LLM+model+routing+strategies+cost+optimization)
- [Semantic Cache for LLM](https://www.google.com/search?q=semantic+cache+LLM+vector+database)
- [Cost Optimization Multi Model](https://www.google.com/search?q=cost+optimization+multi+model+LLM+routing)
