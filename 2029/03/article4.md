# LLM 呼叫快取策略

## 前言

LLM API 呼叫既是成本主要來源，也是延遲瓶頸。合理的快取策略能降低 40-60% 的 API 成本並顯著提升回應速度。

## 語義快取

傳統的 exact-match 快取對 LLM 應用幫助有限，因為使用者提問很少完全一致。語義快取基於嵌入相似度判斷快取命中：

```python
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional
import numpy as np

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.92, ttl: int = 3600):
        self.threshold = similarity_threshold
        self.ttl = ttl
        self._entries: list[dict] = []

    async def get(self, query: str, embedding: list[float]) -> Optional[str]:
        now = datetime.now()
        for entry in self._entries:
            if now - entry["timestamp"] > timedelta(seconds=self.ttl):
                continue
            sim = self.cosine_similarity(embedding, entry["embedding"])
            if sim >= self.threshold:
                entry["hits"] += 1
                return entry["response"]
        return None

    async def set(self, query: str, embedding: list[float], response: str):
        self._entries.append({
            "query": query,
            "embedding": embedding,
            "response": response,
            "timestamp": datetime.now(),
            "hits": 0,
        })

    @staticmethod
    def cosine_similarity(a: list[float], b: list[float]) -> float:
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

## 多層快取

```python
import diskcache as dc

class MultiLevelCache:
    def __init__(self):
        self.memory_cache: dict[str, str] = {}
        self.disk_cache = dc.Cache("./llm_cache")
        self.semantic_cache = SemanticCache()

    async def get(self, query: str, embedding: list[float]) -> Optional[str]:
        exact_key = hashlib.sha256(query.encode()).hexdigest()
        if exact_key in self.memory_cache:
            return self.memory_cache[exact_key]

        if exact_key in self.disk_cache:
            self.memory_cache[exact_key] = self.disk_cache[exact_key]
            return self.disk_cache[exact_key]

        semantic_result = await self.semantic_cache.get(query, embedding)
        if semantic_result:
            self.memory_cache[exact_key] = semantic_result
            return semantic_result

        return None

    async def set(self, query: str, embedding: list[float], response: str):
        exact_key = hashlib.sha256(query.encode()).hexdigest()
        self.memory_cache[exact_key] = response
        self.disk_cache[exact_key] = response
        await self.semantic_cache.set(query, embedding, response)
```

## 快取失效策略

```python
from enum import Enum

class InvalidationStrategy(Enum):
    TTL = "time_to_live"
    LRU = "least_recently_used"
    MANUAL = "manual"

class CacheManager:
    def __init__(self, strategy: InvalidationStrategy, max_size: int = 10000):
        self.strategy = strategy
        self.max_size = max_size
        self._access_order: list[str] = []

    def should_evict(self) -> bool:
        return len(self._access_order) > self.max_size

    def record_access(self, key: str):
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

    def evict(self) -> Optional[str]:
        if self.strategy == InvalidationStrategy.LRU:
            return self._access_order.pop(0) if self._access_order else None
        return None

    def invalidate_by_prefix(self, key_prefix: str):
        self._access_order = [
            k for k in self._access_order
            if not k.startswith(key_prefix)
        ]
```

## 使用範例

```python
cache = MultiLevelCache()

async def cached_llm_call(query: str) -> str:
    embedding = await get_embedding(query)
    cached = await cache.get(query, embedding)
    if cached:
        return cached

    response = await call_llm(query)
    await cache.set(query, embedding, response)
    return response
```

## 結語

語義快取是 LLM 應用最有效的優化手段之一。搭配多層快取結構和適當的失效策略，可以在不影響回答品質的前提下大幅降低成本與延遲。

---

**延伸閱讀**

- [Semantic Caching for LLMs](https://www.google.com/search?q=semantic+caching+LLM)
- [快取策略比較](https://www.google.com/search?q=caching+strategies+LLM+applications)
- [LLM 成本優化](https://www.google.com/search?q=LLM+cost+optimization+caching)
