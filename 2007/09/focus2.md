# 主題二：PostgreSQL 8.3

## 功能豐富的企業級資料庫

PostgreSQL 8.3 在 2008 年初發布，帶來了多項重要的企業級功能，使其成為功能最豐富的開源資料庫。

## PostgreSQL 8.3 新功能

### XML 資料類型

```sql
-- 原生 XML 支援
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content XML NOT NULL
);

-- 插入 XML
INSERT INTO documents (content) VALUES (
    '<doc><title>Example</title><body>Content here</body></doc>'
);

-- XPath 查詢
SELECT xpath('/doc/title', content) FROM documents;

-- XML 函數
SELECT xmlparse(content) FROM documents;
SELECT xmlserialize(content) FROM documents;
```

### UUID 類型

```sql
-- UUID 支援
CREATE EXTENSION "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100)
);

-- 比較 UUID
SELECT * FROM users WHERE id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11';
```

### 陣列類型

```sql
-- 陣列欄位
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    tags TEXT[]
);

-- 插入含陣列的資料
INSERT INTO products (name, tags) VALUES (
    'Laptop',
    ARRAY['electronics', 'computer', 'portable']
);

-- 查詢陣列
SELECT * FROM products WHERE 'electronics' = ANY(tags);
SELECT * FROM products WHERE tags @> ARRAY['computer'];
```

### 全文字搜尋增強

```sql
-- 全文搜尋
ALTER TABLE articles ADD COLUMN fts_vector tsvector;

CREATE INDEX fts_idx ON articles USING GIN(fts_vector);

-- 搜尋
SELECT * FROM articles
WHERE fts_vector @@ to_tsquery('english', 'postgresql & tutorial');

-- 排名
SELECT title, ts_rank(fts_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql') query
WHERE fts_vector @@ query
ORDER BY rank DESC;
```

### ILIKE / LIKE 改進

```sql
-- 不區分大小寫的 pattern matching
SELECT * FROM users WHERE name ILIKE '%john%';

-- SIMILAR TO (POSIX 正規表達式)
SELECT * FROM users WHERE name SIMILAR TO '%(John|Jane)%';
```

## 效能增強

### 線上備份和 Point-in-Time Recovery

```bash
# 設定 WAL 歸檔
archive_mode = on
archive_command = 'cp %p /mnt/archive/%f'
```

### 記憶體管理優化

```sql
-- 檢視記憶體使用
SELECT * FROM pg_settings WHERE name LIKE '%memory%';

-- 設定共享緩衝區
ALTER SYSTEM SET shared_buffers = '1GB';
```

## 結語

PostgreSQL 8.3 以其豐富的功能和強大的擴展性，持續鞏固其在企業級應用中的地位。從 XML 到 UUID，從陣列到全文搜尋，PostgreSQL 提供了幾乎所有需要的功能。

---

*延伸閱讀：*
- [PostgreSQL 官方網站](https://developers.google.com/search/?q=postgresql+official)
- [PostgreSQL 8.3 文件](https://developers.google.com/search/?q=postgresql+8.3+documentation)*