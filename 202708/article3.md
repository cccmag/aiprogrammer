# 記憶系統設計：從短期到長期記憶

## 前言

記憶是 AI Agent 從「無狀態工具」進化為「持續學習系統」的關鍵。本文將探討三層記憶架構（短期、長期、共享），並提供 Python 實作模式，以及 MemGPT/Letta 等前沿專案的設計理念。

---

## 一、三層記憶架構

### 1.1 記憶類型總覽

| 記憶類型 | 儲存方式 | 持久性 | 容量 | 存取速度 | 用途 |
|---------|---------|--------|------|---------|------|
| 短期記憶 | LLM Context Window | 單次對話 | 小（4K–200K tokens） | 即時 | 當前對話上下文 |
| 長期記憶 | Vector Database | 永久 | 大（百萬級） | 中等 | 跨對話知識保留 |
| 共享記憶 | 共享資料庫/檔案 | 永久 | 大 | 中等 | Agent 間資訊交換 |

### 1.2 短期記憶（Conversation Buffer）

短期記憶最簡單的實作就是維護對話歷史列表：

```python
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ShortTermMemory:
    messages: List[Dict] = field(default_factory=list)
    max_tokens: int = 4096

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._trim()

    def _trim(self):
        # 簡單實作：保留最近 N 條訊息
        if len(self.messages) > 20:
            self.messages = self.messages[-20:]

    def get_context(self) -> List[Dict]:
        return self.messages

    def clear(self):
        self.messages = []
```

進階的短期記憶管理需要考慮 Token 預算，使用 `tiktoken` 進行精確控制：

```python
import tiktoken

class TokenAwareShortTermMemory:
    def __init__(self, model: str = "gpt-4", max_tokens: int = 6000):
        self.encoder = tiktoken.encoding_for_model(model)
        self.messages = []
        self.max_tokens = max_tokens

    def add(self, message: dict):
        self.messages.append(message)
        self._trim_to_token_budget()

    def _trim_to_token_budget(self):
        while self._count_tokens() > self.max_tokens and self.messages:
            self.messages.pop(0)

    def _count_tokens(self) -> int:
        return sum(len(self.encoder.encode(m.get("content", "")))
                   for m in self.messages)
```

---

## 二、長期記憶：基於 RAG 的實作

### 2.1 向量資料庫整合

長期記憶的核心是 Retrieval-Augmented Generation（RAG），將資訊向量化儲存並在需要時檢索：

```python
import numpy as np
from typing import List, Optional

class VectorMemory:
    def __init__(self, embedder, db_path: str = "memory.db"):
        self.embedder = embedder  # 嵌入模型
        self.vectors: List[np.ndarray] = []
        self.texts: List[str] = []
        self.metadata: List[dict] = []

    def add(self, text: str, metadata: Optional[dict] = None):
        vector = self.embedder.embed(text)
        self.vectors.append(vector)
        self.texts.append(text)
        self.metadata.append(metadata or {})

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        query_vec = self.embedder.embed(query)
        scores = [
            self._cosine_similarity(query_vec, v) for v in self.vectors
        ]
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [
            {
                "text": self.texts[i],
                "score": scores[i],
                "metadata": self.metadata[i],
            }
            for i in top_indices
        ]

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

### 2.2 記憶管理策略

長期記憶需要管理機制來控制品質和相關性：

```python
class LongTermMemory:
    def __init__(self, vector_memory: VectorMemory):
        self.vm = vector_memory
        self.importance_threshold = 0.6

    def consolidate(self, short_term: ShortTermMemory):
        """將短期記憶中的重要內容整合到長期記憶"""
        for msg in short_term.messages:
            importance = self._assess_importance(msg["content"])
            if importance > self.importance_threshold:
                self.vm.add(
                    text=msg["content"],
                    metadata={"importance": importance, "role": msg["role"]}
                )

    def _assess_importance(self, text: str) -> float:
        # 基於規則的簡單重要性評估
        keywords = ["專案", "客戶", "設定", "密碼", "API", "版本"]
        score = sum(1 for kw in keywords if kw in text) / len(keywords)
        return min(score + 0.3, 1.0)

    def recall(self, query: str, top_k: int = 3) -> str:
        results = self.vm.search(query, top_k=top_k)
        if not results:
            return "（記憶中找不到相關資訊）"
        return "\n".join(
            f"[相關性 {r['score']:.2f}] {r['text']}"
            for r in results
        )
```

---

## 三、共享記憶：Agent 間協作

在多 Agent 系統中，共享記憶讓 Agent 之間可以交換知識：

```python
import json
import os
from datetime import datetime

class SharedMemory:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.file = f"shared_memory_{namespace}.json"
        self._load()

    def _load(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"notes": [], "decisions": []}

    def _save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def write_note(self, agent: str, key: str, content: str):
        self.data["notes"].append({
            "agent": agent,
            "key": key,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        self._save()

    def read_notes(self, key: str) -> List[str]:
        return [
            n["content"] for n in self.data["notes"]
            if n["key"] == key
        ]

    def record_decision(self, agent: str, decision: str, rationale: str):
        self.data["decisions"].append({
            "agent": agent,
            "decision": decision,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat(),
        })
        self._save()
```

---

## 四、MemGPT / Letta 架構啟發

MemGPT（現名 Letta）是記憶管理最具代表性的系統之一。其核心創新在於：

1. **分層記憶管理**：將記憶分為工作記憶（working memory）和外部記憶（external memory），類似作業系統的虛擬記憶體
2. **記憶封存（Archival）**：Context Window 滿時，自動將較舊且不重要的內容寫入外部儲存
3. **記憶回顧（Recall）**：根據當前對話上下文自動檢索相關記憶
4. **自我更新**：Agent 可以在對話過程中主動更新自己的系統提示（system prompt），實現「學習」

---

## 結語

良好的記憶系統設計是 Agent 從一次性工具進化為持久智慧體的關鍵。短期記憶提供對話的連貫性，長期記憶保存跨對話的知識，共享記憶促進 Agent 間的協作。在實作時，需要根據應用場景在記憶容量、檢索速度、相關性之間取得平衡。

---

**參考資料**

- Letta（原 MemGPT）：https://www.letta.com/
- "MemGPT: Towards LLMs as Operating Systems", https://arxiv.org/abs/2310.08560
- RAG 最佳實踐：https://docs.llamaindex.ai/en/stable/understanding/rag/
- Pinecone 向量資料庫：https://www.pinecone.io/
