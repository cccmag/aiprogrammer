# 向量資料庫選型指南（2020-2026）

## 六款主流向量資料庫深度比較

### Pinecone

雲端原生，完全託管。零運維、自動擴展，但封閉源碼且成本較高。

```python
import pinecone
pinecone.init(api_key="your-key")
index = pinecone.Index("my-index")
index.upsert([("id1", [0.1, 0.2], {"text": "hello"})])
results = index.query(vector=[0.1, 0.2], top_k=5)
```

### Weaviate

開源，支援 GraphQL 和內建混合搜尋。

```python
import weaviate
client = weaviate.Client("http://localhost:8080")
result = client.query.get("Document", ["title"]) \
    .with_near_vector({"vector": query_emb}) \
    .with_where({"path": ["category"], "operator": "Equal", "valueString": "tech"}).do()
```

### Qdrant

Rust 實作，性能優秀，支援精確和近似搜尋。獨特的 payload 過濾器設計在大量點上仍保持高效。

**適合**：對延遲敏感的即時應用。

```python
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
client.upsert(
    collection_name="products",
    points=[{"id": 1, "vector": [0.1, 0.2, 0.3], 
             "payload": {"price": 100, "category": "electronics"}}]
)
results = client.search(
    collection_name="products",
    query_vector=[0.1, 0.2],
    limit=10,
    query_filter={"must": [{"key": "price", "range": {"lte": 500}}]}
)
```

### Chroma

輕量級，嵌入開發者體驗。支援記憶體內和持久化模式，提供 Python 原生 API。

**適合**：開發測試、教學、小型專案。

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("docs")
collection.add(
    documents=["This is a document", "This is another"],
    embeddings=[[1.1, 2.3], [4.5, 6.7]],
    ids=["doc1", "doc2"]
)
results = collection.query(query_embeddings=[[1.1, 2.3]], n_results=5)
```

### pgvector

PostgreSQL 擴展，讓傳統關聯式資料庫具備向量搜尋能力。優點是無需新資料庫、完整的 SQL 支援、ACID 保證。

**適合**：已使用 PostgreSQL 的團隊、需要向量搜尋結合複雜 SQL 查詢。

```python
import psycopg2

conn = psycopg2.connect("dbname=test")
cur = conn.cursor()
cur.execute("CREATE EXTENSION vector")
cur.execute("CREATE TABLE items (id bigserial, embedding vector(768))")
cur.execute("INSERT INTO items (embedding) VALUES (%s)", ([0.1, 0.2],))
# 向量搜尋 (使用 pgvector IVFFlat 索引)
cur.execute("SELECT * FROM items ORDER BY embedding <-> %s LIMIT 10", ([0.1, 0.2],))
```

### Milvus

分散式向量資料庫，專為大規模設計。支援 GPU 加速、多種索引類型、雲端原生架構。

**適合**：億級以上向量、需要 GPU 加速的場景。

### 選型決策樹

```
規模 < 100 萬向量 → Chroma 或 pgvector
100 萬 - 1000 萬 → pgvector 或 Qdrant
1000 萬 - 1 億   → Qdrant 或 Milvus
1 億以上         → Milvus 或 Pinecone

需要複雜過濾 → Weaviate 或 Qdrant
需要 SQL 整合 → pgvector
不想管伺服器 → Pinecone
預算有限     → Chroma 或 pgvector
```

### 2026 年的市場格局

向量資料庫的市場正在整合：大型雲端廠商（AWS OpenSearch、Azure AI Search）開始內建向量支援；PostgreSQL 生態圈持續擴大。選擇的關鍵不再是功能，而是與現有技術棧的整合度。

---

**下一步**：[AI 輔助資料庫開發](focus7.md)

## 延伸閱讀

- [向量資料庫效能評測](https://www.google.com/search?q=vector+database+benchmark+comparison+2026)
- [pgvector vs 專用向量資料庫](https://www.google.com/search?q=pgvector+vs+dedicated+vector+database)
