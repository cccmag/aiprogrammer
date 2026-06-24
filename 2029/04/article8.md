# 多模態記憶管理

## 1. 記憶的類型

多模態 Agent 的記憶不僅是文字，還包括圖像、語音等非結構化數據。

| 類型 | 儲存 | 檢索 |
|------|------|------|
| 短期 | 當前 session 交互 | 順序存取 |
| 長期 | 跨 session 資訊 | 語義檢索 |
| 工作 | 當前任務暫存 | 直接引用 |

## 2. 多模態記憶儲存

```python
import hashlib, json
from datetime import datetime
import chromadb
from sentence_transformers import SentenceTransformer

class Memory:
    def __init__(self):
        self.db = chromadb.Client().create_collection("mem")
        self.enc = SentenceTransformer("all-MiniLM-L6-v2")
        self.short = []

    def add(self, modality, content):
        mid = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]
        text = f"[{modality}] {str(content)[:200]}"
        self.db.add(embeddings=[self.enc.encode(text).tolist()], documents=[text], ids=[mid])
        self.short.append({"id": mid, "modality": modality, "content": content})
        if len(self.short) > 50: self.short.pop(0)

    def search(self, query, k=5):
        r = self.db.query(query_embeddings=[self.enc.encode(query).tolist()], n_results=k)
        return r["documents"][0]
```

## 3. 記憶壓縮

長時間運行需要壓縮記憶以減少 token 消耗：

```python
class MemoryCompressor:
    def compress(self, items, llm, max_tokens=500):
        raw = "\n".join([f"[{i['modality']}] {str(i['content'])[:100]}" for i in items])
        r = llm.chat.completions.create(model="gpt-4o", messages=[{
            "role": "user", "content": f"壓縮以下多模態記憶（{max_tokens} tokens）：\n{raw}"}])
        return r.choices[0].message.content
```

## 4. 遺忘機制

```python
class Forgetting:
    def apply(self, memory, days=30):
        from datetime import timedelta
        limit = datetime.now() - timedelta(days=days)
        memory.short = [m for m in memory.short if datetime.fromisoformat(m.get("ts", datetime.now().isoformat())) > limit]
```

## 5. 結語

記憶管理是 Agent 持續學習的基礎。壓縮與檢索的平衡決定長期任務的表現上限。

- https://www.google.com/search?q=agent+memory+management+multimodal
- https://www.google.com/search?q=chromadb+multimodal+embedding
