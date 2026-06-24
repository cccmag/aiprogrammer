# PostgreSQL 8.3：企業級資料庫

PostgreSQL 8.3 在 2008 年初發布，帶來了多項重要的企業級功能。

## 新功能一覽

### 向量索引

```sql
-- 全文搜尋改進
ALTER TABLE documents ADD COLUMN fts_vector tsvector;
CREATE INDEX fts_idx ON documents USING GIN(fts_vector);
```

### UUID 支援

```sql
-- 原生 UUID 類型
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100)
);
```

### XML 資料類型

```sql
-- XML 原生支援
CREATE TABLE docs (
    id SERIAL PRIMARY KEY,
    content XML
);

INSERT INTO docs (content) VALUES ('<doc><title>Test</title></doc>');
```

## 結語

PostgreSQL 8.3 的這些功能使其在企業級應用中更具競爭力。

---

*延伸閱讀：[PostgreSQL 官方網站](https://developers.google.com/search/?q=postgresql+official)*