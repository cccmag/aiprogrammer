# 混合搜尋：關鍵字 + 向量 + 重新排序

## 1. 為什麼需要混合搜尋？

純向量搜尋擅長捕捉語義相似性，但對精確關鍵字匹配較弱。例如搜尋「Python 程式設計」，向量搜尋可能會返回「Java 開發指南」（因為語義相近），卻錯過了專門討論 Python 語法的文章。混合搜尋將多種檢索策略的優點結合，顯著提升搜尋品質。

## 2. 混合搜尋的三階段架構

```
查詢 → 第一階段檢索（關鍵字 + 向量）→ 第二階段融合 → 第三階段重新排序
```

### 2.1 第一階段：多路檢索

同時執行稀疏檢索（關鍵字/BM25）和密集檢索（向量搜尋）：

```python
import numpy as np
from rank_bm25 import BM25Okapi
from openai import OpenAI

class HybridRetriever:
    def __init__(self):
        self.client = OpenAI()
        self.documents = []
        self.bm25 = None

    def index(self, documents):
        self.documents = documents
        tokenized = [doc["content"].split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query, top_k=20):
        # 向量檢索
        resp = self.client.embeddings.create(
            model="text-embedding-3-small", input=query
        )
        q_vec = resp.data[0].embedding
        vec_scores = []
        for doc in self.documents:
            sim = np.dot(q_vec, doc["embedding"])
            vec_scores.append(sim)

        # 關鍵字檢索（BM25）
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # 取 top_k 候選
        combined = list(zip(range(len(self.documents)),
                           vec_scores, bm25_scores))
        # 每種策略取 top_k 合併
        vec_top = set(sorted(combined, key=lambda x: -x[1])[:top_k])
        bm25_top = set(sorted(combined, key=lambda x: -x[2])[:top_k])
        candidates = vec_top | bm25_top
        return [self.documents[i[0]] for i in candidates]
```

### 2.2 第二階段：分數融合

使用 **RRF**（Reciprocal Rank Fusion）將多個排名合併成單一排名：

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for rank_list in rankings:
        for rank, doc_id in enumerate(rank_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores.items(), key=lambda x: -x[1])
```

RRF 的優勢在於它只依賴排名而非分數，避免了不同檢索策略分數量級不一致的問題。參數 `k` 控制融合的平滑程度（通常設為 60）。

### 2.3 第三階段：重新排序

使用 Cross-encoder 模型對候選文件進行精細排序。Cross-encoder 同時處理 query 和 document，能捕捉更複雜的語義關係：

```python
from sentence_transformers import CrossEncoder

class ReRanker:
    def __init__(self):
        self.model = CrossEncoder(
            "BAAI/bge-reranker-v2-m3"
        )

    def rerank(self, query, candidates, top_k=10):
        pairs = [(query, doc["content"])
                 for doc in candidates]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(candidates, scores),
                       key=lambda x: -x[1])
        return ranked[:top_k]
```

BGE ReRanker v2 在中文和英文場景都有出色表現，將 top-20 重新排序為 top-10 可以將 NDCG@10 提升 5-10%。

## 3. 完整混合搜尋管線

```python
def hybrid_search(query, retriever, reranker, top_k=10):
    # 第一階段：多路檢索
    candidates = retriever.retrieve(query, top_k=20)

    # 第二階段：RRF 融合
    vec_ranking = [(doc["id"], doc["vec_score"])
                   for doc in candidates]
    bm25_ranking = [(doc["id"], doc["bm25_score"])
                    for doc in candidates]
    fused = reciprocal_rank_fusion(
        [[r[0] for r in vec_ranking],
         [r[0] for r in bm25_ranking]]
    )

    # 第三階段：重新排序
    reranked = reranker.rerank(query, candidates, top_k)
    return reranked
```

## 4. 實戰調校技巧

- **關鍵字權重**：對程式碼、產品名稱等場景，提高 BM25 權重
- **快取常見查詢**：熱門查詢的混合搜尋結果可以快取 5-10 分鐘
- **非同步檢索**：向量和關鍵字檢索可以平行執行
- **動態融合策略**：短查詢（< 5 字）偏向關鍵字，長查詢偏向向量

## 5. 使用情境建議

| 場景 | 向量權重 | 關鍵字權重 | 重新排序 |
|------|---------|-----------|---------|
| 客服問答 | 0.8 | 0.2 | 必要 |
| 技術文件搜尋 | 0.5 | 0.5 | 建議 |
| 產品目錄 | 0.3 | 0.7 | 可選 |
| 學術論文搜尋 | 0.7 | 0.3 | 必要 |

## 參考資料

- [RRF 演算法](https://www.google.com/search?q=reciprocal+rank+fusion+information+retrieval)
- [Cross-encoder 重新排序](https://www.google.com/search?q=cross+encoder+re+ranking+sentence+transformers)
- [混合搜尋最佳實務](https://www.google.com/search?q=hybrid+search+best+practices+rag)
