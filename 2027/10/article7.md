# 多模態檢索增強生成（MM-RAG）

## 前言

檢索增強生成（RAG）透過從外部知識庫檢索相關文件來提升 LLM 的回應品質。多模態 RAG（MM-RAG）將這個概念擴展到圖片、音訊、影片等多種模態。本文將介紹 MM-RAG 的架構設計、實作方式以及效能調校技巧。

---

## 一、從 RAG 到 MM-RAG

傳統 RAG 只處理文字，MM-RAG 將檢索與生成擴展到多模態：

```python
# 傳統 RAG：文字 → 文字
# MM-RAG：文字/圖片/音訊 → 文字 + 圖片 + 音訊
```

## 二、MM-RAG 系統架構

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MultiModalChunk:
    id: str
    modality: str       # "text" | "image" | "audio"
    content: str        # 文字內容或檔案路徑
    embedding: np.ndarray = field(repr=False)
    metadata: dict = field(default_factory=dict)

class MultiModalVectorStore:
    def __init__(self):
        self.chunks: List[MultiModalChunk] = []

    def add(self, chunk: MultiModalChunk):
        self.chunks.append(chunk)

    def search(self, query_emb: np.ndarray, k: int = 5,
               modality: Optional[str] = None) -> List[MultiModalChunk]:
        scored = []
        for chunk in self.chunks:
            if modality and chunk.modality != modality:
                continue
            sim = np.dot(query_emb, chunk.embedding)
            scored.append((sim, chunk))
        scored.sort(key=lambda x: -x[0])
        return [chunk for _, chunk in scored[:k]]
```

## 三、多模態檢索策略

### 3.1 跨模態檢索

使用統一的嵌入模型（如 CLIP）將所有模態映射到同一空間：

```python
class UnifiedRetriever:
    def __init__(self, embedder, store: MultiModalVectorStore):
        self.embedder = embedder
        self.store = store

    def retrieve(self, query: str, modality: Optional[str] = None, k: int = 5):
        query_emb = self.embedder.embed(query)
        return self.store.search(query_emb, k, modality)

    def retrieve_by_image(self, image_path: str, k: int = 5):
        query_emb = self.embedder.embed_image(image_path)
        return self.store.search(query_emb, k)
```

### 3.2 分層檢索（Hibrid Search）

先進行關鍵字檢索，再進行語義檢索，最後融合結果：

```python
class HybridRetriever:
    def __init__(self, semantic_retriever, bm25_index, alpha=0.5):
        self.semantic = semantic_retriever
        self.bm25 = bm25_index
        self.alpha = alpha

    def retrieve(self, query: str, k: int = 5):
        semantic_results = self.semantic.retrieve(query, k=k * 2)
        bm25_results = self.bm25.search(query, k=k * 2)

        # 融合評分
        scores = {}
        for i, chunk in enumerate(semantic_results):
            scores[chunk.id] = self.alpha * (1 - i / len(semantic_results))

        for i, chunk in enumerate(bm25_results):
            scores[chunk.id] = scores.get(chunk.id, 0) + (1 - self.alpha) * (1 - i / len(bm25_results))

        ranked = sorted(scores.items(), key=lambda x: -x[1])
        return [self.semantic.store.get(cid) for cid, _ in ranked[:k]]
```

## 四、多模態提示組裝

檢索到多模態文件後，需要將它們組裝成 LLM 可理解的提示：

```python
def assemble_multimodal_prompt(query, text_chunks, image_paths):
    prompt = f"用戶問題：{query}\n\n"

    if text_chunks:
        prompt += "相關文字資料：\n"
        for i, chunk in enumerate(text_chunks):
            prompt += f"[{i+1}] {chunk.content}\n"

    if image_paths:
        prompt += "\n相關圖片：\n"
        # 對 GPT-4V 等模型，圖片以 image_url 形式傳入
        for path in image_paths:
            prompt += f"![圖片]({path})\n"

    prompt += "\n請根據以上多模態資訊回答問題。\n"
    return prompt
```

## 五、評估 MM-RAG 系統

```python
def evaluate_mmrag(retriever, test_queries, relevant_items):
    """使用 Recall@K 和 MRR 評估"""
    recall_scores = []
    mrr_scores = []

    for query, relevant_ids in zip(test_queries, relevant_items):
        results = retriever.retrieve(query, k=10)
        retrieved_ids = [r.id for r in results]

        # Recall@K
        hits = sum(1 for r in retrieved_ids if r in relevant_ids)
        recall_scores.append(hits / len(relevant_ids))

        # MRR
        for rank, r_id in enumerate(retrieved_ids, 1):
            if r_id in relevant_ids:
                mrr_scores.append(1 / rank)
                break
        else:
            mrr_scores.append(0)

    print(f"Mean Recall@10: {np.mean(recall_scores):.4f}")
    print(f"Mean MRR: {np.mean(mrr_scores):.4f}")
    return recall_scores, mrr_scores
```

## 六、MM-RAG 的最佳實踐

1. **模態感知的 chunking**：不同模態適用不同的切分策略，圖片應保持完整性
2. **嵌入模型選擇**：CLIP 適合跨模態檢索，但 domain-specific 場景需要微調
3. **重新排序**：檢索後使用跨模態注意力重新排序，提升準確率
4. **多輪檢索**：根據 LLM 的初步回答進行二次檢索，類似 ReAct 模式

---

## 結語

MM-RAG 將 RAG 從純文字擴展到多模態世界，讓 AI 系統能夠利用圖片、圖表、音訊等豐富的資訊來源。隨著多模態嵌入模型的成熟和向量資料庫的發展，MM-RAG 正在成為企業級 AI 應用的標準架構。

---

**參考資料**

- RAG 論文：https://arxiv.org/abs/2005.11401
- MM-RAG 架構：https://www.google.com/search?q=multimodal+RAG+retrieval+augmented+generation
- LangChain 多模態 RAG 文檔：https://python.langchain.com/docs/use_cases/multimodal
- CLIP 嵌入檢索：https://github.com/openai/CLIP
