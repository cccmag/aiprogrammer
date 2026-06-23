# 向量資料庫實戰：Chroma vs Qdrant vs Pinecone

## 前言

向量資料庫是 RAG 系統的核心基礎設施。它負責儲存文字片段的向量嵌入，並支援高效的相似性搜尋。市場上有數十個向量資料庫方案，本文將深入比較 Chroma、Qdrant 與 Pinecone 三種主流方案，從安裝設定到生產部署提供完整實作指引。

## 向量資料庫的核心概念

向量資料庫的核心操作是近似最近鄰（ANN）搜尋。主要評估指標包括：

- **Recall@k**：檢索的準確率
- **QPS**：每秒查詢數
- **延遲**：單次查詢回應時間
- **索引速度**：建立索引的時間

## Chroma：輕量級嵌入式資料庫

Chroma 是開源的輕量級向量資料庫，適合原型開發與小型專案：

```python
# 安裝：pip install chromadb
import chromadb
from chromadb.config import Settings

# 用戶端初始化
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_data"
))

# 建立集合（Collection）
collection = client.create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}  # 距離計算方式
)

# 加入向量
collection.add(
    documents=["Transformer 使用注意力機制", "RNN 使用遞迴結構"],
    metadatas=[{"source": "wiki"}, {"source": "wiki"}],
    ids=["doc1", "doc2"],
    embeddings=embedding_model.encode(["Transformer...", "RNN..."])
)

# 檢索
results = collection.query(
    query_embeddings=embedding_model.encode(["什麼是注意力機制？"]),
    n_results=3
)
```

優點：零設定、記憶體模式、Python 原生。缺點：不適合大規模生產環境。

## Qdrant：高效能開源方案

Qdrant 是 Rust 實現的高效能向量資料庫，支援過濾、分組、與即時更新：

```python
# 安裝：pip install qdrant-client
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# 連線（可 Docker 部署）
client = QdrantClient(
    url="http://localhost:6333",
    api_key="your_api_key"  # 自託管可省略
)

# 建立集合
client.recreate_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE
    )
)

# 批次寫入
points = [
    PointStruct(
        id=i,
        vector=embedding,
        payload={"text": doc, "source": "pdf"}
    )
    for i, (doc, embedding) in enumerate(zip(docs, embeddings))
]
client.upsert(collection_name="documents", points=points)

# 進階檢索：帶過濾條件
from qdrant_client.models import Filter, FieldCondition, MatchValue

results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="source",
                match=MatchValue(value="pdf")
            )
        ]
    ),
    limit=5,
    with_payload=True
)
```

Qdrant 支援多種索引類型（HNSW、IVF）與量化壓縮，可根據資料規模調整。

## Pinecone：全託管雲端服務

Pinecone 是 SaaS 形式的向量資料庫，無需自行管理基礎設施：

```python
# 安裝：pip install pinecone-client
import pinecone

# 初始化（需註冊取得 API Key）
pinecone.init(
    api_key="your-pinecone-api-key",
    environment="us-west1-gcp"
)

# 建立索引
pinecone.create_index(
    name="rag-knowledge",
    dimension=768,
    metric="cosine",
    pods=1,           # 基本方案 1 個 pod
    pod_type="p1.x1"  # 規格選擇
)

index = pinecone.Index("rag-knowledge")

# 批次寫入（每次最多 100 筆）
batch_size = 100
for i in range(0, len(docs), batch_size):
    batch = [
        (str(j), embedding, {"text": doc})
        for j, (doc, embedding) in enumerate(
            zip(docs[i:i+batch_size], embeddings[i:i+batch_size])
        )
    ]
    index.upsert(vectors=batch)

# 檢索
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)
```

## 混合搜尋：向量 + 關鍵字

結合向量相似度與關鍵字匹配的混合搜尋策略：

```python
import numpy as np

class HybridSearch:
    def __init__(self, vector_db, bm25_index, alpha=0.7):
        self.vector_db = vector_db
        self.bm25 = bm25_index
        self.alpha = alpha

    def search(self, query, k=5):
        # 向量檢索
        vec_results = self.vector_db.similarity_search(query, k=k*2)
        vec_scores = {doc.id: doc.score for doc in vec_results}

        # 關鍵字檢索
        bm25_results = self.bm25.get_top_n(query, k=k*2)
        bm25_scores = {doc.id: score for doc, score in bm25_results}

        # 分數融合（RRF 或加權平均）
        all_ids = set(vec_scores.keys()) | set(bm25_scores.keys())
        fusion_scores = {}
        for doc_id in all_ids:
            v = vec_scores.get(doc_id, 0.0)
            b = bm25_scores.get(doc_id, 0.0)
            fusion_scores[doc_id] = self.alpha * v + (1 - self.alpha) * b

        return sorted(fusion_scores.items(), key=lambda x: x[1], reverse=True)[:k]
```

## 比較總結

| 特性 | Chroma | Qdrant | Pinecone |
|------|--------|--------|----------|
| 開源 | 是 | 是 | 否 |
| 部署方式 | 嵌入式/Docker | Docker/雲端 | 全託管 |
| 延遲 | <5ms | <10ms | <20ms |
| 規模上限 | 百萬級 | 億級 | 億級 |
| 過濾支援 | 有限 | 完整 | 完整 |
| 成本 | 免費 | 自管免費 | 按量計費 |

## 選擇建議

- **原型開發**：Chroma（快速迭代）
- **中型生產**：Qdrant（開源可控、高效能）
- **大型企業**：Pinecone（免運維、SLA 保證）
- **混合需求**：Qdrant + 自建 BM25

## 參考資源

- [Chroma 官方文件](https://www.google.com/search?q=chromadb+documentation)
- [Qdrant 官方文件](https://www.google.com/search?q=qdrant+vector+database+documentation)
- [Pinecone 官方教學](https://www.google.com/search?q=pinecone+vector+database+getting+started)
- [ANN 演算法比較](https://www.google.com/search?q=approximate+nearest+neighbor+algorithms+comparison)
