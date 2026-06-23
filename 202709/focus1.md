# 從關聯式資料庫到 AI 原生資料庫（1970-2026）

## 資料庫的三大演化階段

### 1970-2000：關聯式時代

1970 年 Codd 提出關聯模型，Oracle、DB2、MySQL、PostgreSQL 相繼誕生。關聯式資料庫的核心是**結構化查詢（SQL）**和**ACID 事務**，資料必須先有 schema 才能存入。

```sql
-- 關聯式查詢：精確匹配
SELECT * FROM products WHERE price < 100;
```

缺點是對非結構化資料（文字、圖片、向量）無能為力。

### 2000-2020：NoSQL 時代

文件資料庫（MongoDB）、鍵值儲存（Redis）、圖資料庫（Neo4j）崛起。它們放棄了嚴格的 schema 約束，換取水平擴展和靈活性。但搜尋仍然依賴精確匹配或簡單的全文索引。

### 2020-2026：AI 原生資料庫

AI 原生資料庫的核心差異在於**資料以向量形式儲存**，查詢時透過**語義相似度**而非精確值。這徹底改變了資料庫的設計哲學：

| 特性 | 關聯式 | NoSQL | AI 原生 |
|------|--------|-------|---------|
| 查詢方式 | SQL 精確匹配 | Key/文件查詢 | 向量相似度 |
| 資料型態 | 結構化 | 半結構化 | 向量+結構化 |
| 索引 | B+ Tree | LSM Tree | HNSW/IVF |
| 查詢範例 | price < 100 | get(key) | find_similar(emb) |

### 向量資料庫的誕生

2019 年 Pinecone 作為首個雲端向量資料庫問世，隨後 Weaviate（2020）、Qdrant（2020）、Chroma（2022）陸續出現。2023 年 pgvector 將向量支援引入 PostgreSQL，讓傳統關聯式資料庫也能進行語義搜尋。

```python
# AI 原生資料庫的查詢方式
import numpy as np

def semantic_search(db, query_embedding, top_k=5):
    """在向量資料庫中進行語義搜尋"""
    results = db.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return results
```

### AI 原生資料庫的定義

一個 AI 原生資料庫應具備：

1. **向量儲存與索引**：支援高維向量（128-1536 維）的高效儲存與索引
2. **語義查詢**：以相似度而非精確值作為查詢條件
3. **混合搜尋**：同時支援向量搜尋與結構化過濾
4. **嵌入整合**：內建或易於整合 embedding API
5. **AI 管線**：支援 RAG、自動分類、資料標註等 AI 工作流程

### 從 2026 看未來

2026 年，AI 原生資料庫不再是 niche 產品。幾乎所有主流資料庫都內建了向量支援：PostgreSQL（pgvector）、SQLite（sqlite-vec）、MongoDB（Atlas Vector Search）、Redis（RediSearch）。下一個階段是**自主資料庫**——由 AI 自動管理 schema、索引和查詢最佳化。

---

**下一步**：[向量嵌入與語義搜尋](focus2.md)

## 延伸閱讀

- [從 SQL 到向量的資料庫演化](https://www.google.com/search?q=database+evolution+relational+to+vector)
- [Pinecone 發展歷史](https://www.google.com/search?q=Pinecone+vector+database+history)
