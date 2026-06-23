# pgvector 實戰：PostgreSQL 向量搜尋

## 1. 為什麼選擇 pgvector？

多數專案已經在使用 PostgreSQL。與其引入額外的向量資料庫增加系統複雜度，不如直接在 Postgres 中加入向量搜尋能力。pgvector 擴展讓你可以在熟悉的 SQL 環境中進行向量相似度搜尋，無需管理兩個資料庫系統。

## 2. 安裝與設定

```bash
# 透過 apt 或 brew 安裝
sudo apt install postgresql-16-pgvector
# 或從原始碼編譯
git clone https://github.com/pgvector/pgvector.git
cd pgvector && make && sudo make install
```

在資料庫中啟用擴展：

```sql
CREATE EXTENSION vector;
```

## 3. 建立向量表

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    embedding VECTOR(768),  -- 768 維向量
    created_at TIMESTAMP DEFAULT NOW(),
    category TEXT
);

-- 建立索引加速搜尋
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

pgvector 支援三種索引類型：
- **IVFFlat**（預設）：近似搜尋，速度快但召回率較低
- **HNSW**（pgvector 0.7+）：更準確的近似搜尋
- 無索引：暴力搜尋，資料量小時可用

## 4. 基本 CRUD 與搜尋

### 插入資料

```python
import psycopg2
from openai import OpenAI

client = OpenAI()
conn = psycopg2.connect("dbname=vectordb user=postgres")

def add_document(title, content, category):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=content
    )
    embedding = response.data[0].embedding
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (title, content, embedding, category) "
        "VALUES (%s, %s, %s, %s)",
        (title, content, embedding, category)
    )
    conn.commit()
```

### 向量搜尋

```python
def search_similar(query, category=None, top_k=5):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    q_vec = response.data[0].embedding
    cur = conn.cursor()
    if category:
        sql = """
            SELECT id, title, content,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM documents
            WHERE category = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """
        cur.execute(sql, (q_vec, category, q_vec, top_k))
    else:
        sql = """
            SELECT id, title, content,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """
        cur.execute(sql, (q_vec, q_vec, top_k))
    return cur.fetchall()
```

`<=>` 是餘弦距離運算子。pgvector 也支援 `<->`（L2 距離）和 `<#>`（內積距離）。

## 5. HNSW 索引設定（pgvector 0.7+）

```sql
-- HNSW 索引提供更好的召回率
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 200);
```

HNSW 索引在建置時需要更多記憶體和時間，但搜尋速度更快、召回率更高，特別適合大型資料集。

## 6. 混合搜尋：全文檢索 + 向量

pgvector 在單一 SQL 查詢中即可結合傳統全文檢索與向量搜尋：

```sql
SELECT id, title, content,
    -- 向量相似度分數（權重 0.7）
    0.7 * (1 - (embedding <=> %s::vector)) +
    -- 全文檢索分數（權重 0.3）
    0.3 * ts_rank(to_tsvector('english', content), plainto_tsquery('english', %s))
    AS combined_score
FROM documents
WHERE to_tsvector('english', content) @@ plainto_tsquery('english', %s)
    OR 1 - (embedding <=> %s::vector) > 0.7
ORDER BY combined_score DESC
LIMIT 10;
```

這種混合方法在實際應用中往往比純向量搜尋效果更好，因為它可以同時捕捉語義相似性和關鍵字精確匹配。

## 7. 效能調校

- **lists 參數**：IVFFlat 的 `lists` 設為 `sqrt(n)`，例如 100 萬筆設 1000
- **m 與 ef_construction**：HNSW 的 `m=16`、`ef_construction=200` 是良好的起點
- **真空維護**：定期執行 `VACUUM ANALYZE documents`
- **平行查詢**：PostgreSQL 16+ 支援平行順序掃描

## 8. 限制與替代方案

pgvector 適合數百萬級別的向量量。當規模達到數千萬或數億時，建議考慮專用向量資料庫如 Qdrant 或 Milvus。此外，pgvector 不支援即時向量索引更新——新增大量資料後需要重建索引。

## 參考資料

- [pgvector GitHub](https://www.google.com/search?q=pgvector+github)
- [PostgreSQL 向量搜尋最佳實務](https://www.google.com/search?q=pgvector+best+practices)
- [pgvector vs 專用向量資料庫](https://www.google.com/search?q=pgvector+vs+dedicated+vector+database)
