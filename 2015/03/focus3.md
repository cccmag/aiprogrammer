# PostgreSQL 詳解：特色功能、效能、擴充

## 前言

PostgreSQL 是功能最強大的開源關聯式資料庫，以其穩定性、標準兼容性和擴充性聞名。

## 特色功能

### 陣列類型

```sql
-- 建立含陣列欄位的表格
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    tags TEXT[]
);

-- 插入含陣列的資料
INSERT INTO products (name, tags)
VALUES ('筆記型電腦', ARRAY['電子', '電腦', '攜帶型']);

-- 查詢陣列
SELECT * FROM products WHERE '電腦' = ANY(tags);

-- 包含查詢
SELECT * FROM products WHERE tags @> ARRAY['電子'];
```

### JSON/JSONB 支援

```sql
-- JSON 欄位
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSON
);

-- 插入 JSON
INSERT INTO events (data) VALUES
    ('{"name": "會議", "participants": ["王小明", "李小華"]}');

-- 查詢 JSON
SELECT data->>'name' FROM events;
SELECT data->'participants'->0 FROM events;

-- JSONB（二進位格式，支援索引）
ALTER TABLE events ADD COLUMN data_b JSONB;
CREATE INDEX idx_events_data ON events USING GIN (data_b);
```

### 範圍類型

```sql
-- 日期範圍
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    room INTEGER,
    period DATERANGE
);

-- 查詢範圍重疊
SELECT * FROM reservations
WHERE period && '[2015-03-01, 2015-03-10)';
```

### 全文搜尋

```sql
-- 建立全文搜尋欄位
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR;

UPDATE articles SET search_vector =
    to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(content, ''));

-- 建立索引
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- 搜尋
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'postgresql & database');
```

## 進階 SQL 功能

### WITH（Common Table Expression）

```sql
-- 遞迴查詢
WITH RECURSIVE subordinates AS (
    -- 基本情況
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 遞迴情況
    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates;

-- 複雜查詢重構
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        SUM(total) AS sales
    FROM orders
    GROUP BY DATE_TRUNC('month', created_at)
),
growth AS (
    SELECT
        month,
        sales,
        LAG(sales) OVER (ORDER BY month) AS prev_sales,
        (sales - LAG(sales) OVER (ORDER BY month)) / LAG(sales) OVER (ORDER BY month) * 100 AS growth_rate
    FROM monthly_sales
)
SELECT * FROM growth;
```

### 視窗函數

```sql
-- 排名
SELECT
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM employees;

-- 分組聚合
SELECT
    department,
    name,
    salary,
    SUM(salary) OVER (PARTITION BY department) AS dept_total,
    salary / SUM(salary) OVER (PARTITION BY department) * 100 AS percentage
FROM employees;

-- 移動平均
SELECT
    date,
    price,
    AVG(price) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM stock_prices;
```

### Upsert（INSERT ... ON CONFLICT）

```sql
-- PostgreSQL 9.5+
INSERT INTO users (id, name, email)
VALUES (1, '王小明', 'wang@example.com')
ON CONFLICT (id) DO UPDATE
  SET name = EXCLUDED.name, email = EXCLUDED.email;

-- 或什麼都不做
INSERT INTO users (id, name, email)
VALUES (1, '王小明', 'wang@example.com')
ON CONFLICT (id) DO NOTHING;
```

### RETURNING

```sql
-- 取得插入的資料
INSERT INTO users (name, email) VALUES ('王小明', 'wang@example.com')
RETURNING id, name;

-- 取得更新的資料
UPDATE users SET age = age + 1 WHERE age < 30
RETURNING id, name, age;

-- 刪除並取得
DELETE FROM users WHERE id = 1
RETURNING *;
```

## 效能優化

### EXPLAIN 分析

```sql
EXPLAIN SELECT * FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.country = 'Taiwan';

-- 更詳細輸出
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE id = 1;
```

### 索引類型

```sql
-- B-tree（預設，通用於 =, <, >, <=, >=）
CREATE INDEX idx_users_email ON users(email);

-- Hash（只用於 =）
CREATE INDEX idx_users_email_hash ON users USING HASH(email);

-- GiST（地理空間、範圍）
CREATE INDEX idx_locations_geom ON locations USING GIST(geom);

-- GIN（JSON、陣列、全文搜尋）
CREATE INDEX idx_products_tags ON products USING GIN(tags);

-- BRIN（適用於大型資料表，按區塊）
CREATE INDEX idx_logs_created ON logs USING BRIN(created_at);
```

### 查詢計畫分析

```sql
-- 查看查詢花費
EXPLAIN (ANALYZE, COSTS, TIMING)
SELECT * FROM users WHERE email = 'test@example.com';

-- 結果分析
Nested Loop (cost=0.00..8.51 rows=1 width=...)
  -> Index Scan using idx_users_email on users
        (cost=0.00..8.01 rows=1 width=...)
        Index Cond: ((email)::text = 'test@example.com'::text)
  -> Index Scan using idx_orders_user_id on orders
        (cost=0.00..0.42 rows=1 width=...)
        Index Cond: (user_id = users.id)
```

## 擴充套件

### 常用擴充

```sql
-- 安裝擴充
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- 模糊搜尋
CREATE EXTENSION IF NOT EXISTS "hstore";   -- 鍵值儲存

-- UUID
SELECT uuid_generate_v4();

-- 模糊搜尋
CREATE INDEX idx_users_name_trgm ON users USING GIN (name gin_trgm_ops);
SELECT * FROM users WHERE name % 'Johan';  -- 相似名稱
```

### 分割表格

```sql
-- 依時間分割
CREATE TABLE logs (
    id SERIAL,
    created_at TIMESTAMP NOT NULL,
    message TEXT
) PARTITION BY RANGE (created_at);

CREATE TABLE logs_2015 PARTITION OF logs
    FOR VALUES FROM ('2015-01-01') TO ('2016-01-01');

CREATE TABLE logs_2016 PARTITION OF logs
    FOR VALUES FROM ('2016-01-01') TO ('2017-01-01');
```

## 結論

PostgreSQL 是功能完整的企業級資料庫。從陣列和 JSON 支援到進階的 CTE 和視窗函數，PostgreSQL 提供了豐富的功能來處理各種資料需求。

---

## 延伸閱讀

- [PostgreSQL 官方文檔](https://www.google.com/search?q=PostgreSQL+documentation)
- [PostgreSQL 效能調校](https://www.google.com/search?q=PostgreSQL+performance+tuning)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」歷史回顧系列之一。*