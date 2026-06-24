# 主題四：SQL 查詢最佳化

## 效能調校技巧

資料庫效能是應用系統回應速度的關鍵。學會分析和最佳化 SQL 查詢，是每個開發者的必備技能。

## 查詢分析

### EXPLAIN 命令

```sql
-- MySQL
EXPLAIN SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.order_date > '2007-01-01';

-- PostgreSQL
EXPLAIN ANALYZE
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.order_date > '2007-01-01';
```

### 解讀執行計畫

```markdown
# EXPLAIN 輸出範例

id: 1
select_type: SIMPLE
table: u
type: const
possible_keys: PRIMARY
key: PRIMARY
rows: 1

# 類型解釋：
# system: 表只有一行（系統表）
# const: 至多一行匹配（使用 PRIMARY 或 UNIQUE 索引）
# eq_ref: 使用 PRIMARY 或 UNIQUE 索引進行等值連接
# ref: 使用非唯一索引
# range: 使用索引範圍掃描
# ALL: 全表掃描（最差）
```

## 常見的最佳化技巧

### 1. 善用索引

```sql
-- 建立適當的索引
CREATE INDEX idx_orders_date ON orders(order_date);

-- 複合索引的欄位順序
-- 查詢：WHERE a = ? AND b = ?
-- 索引：(a, b) 優於 (b, a)

-- 避免在索引欄位上使用函數
-- 不好：
SELECT * FROM orders WHERE YEAR(order_date) = 2007;

-- 好：
SELECT * FROM orders WHERE order_date >= '2007-01-01' AND order_date < '2008-01-01';
```

### 2. 避免 SELECT *

```sql
-- 不好：傳回所有欄位
SELECT * FROM orders;

-- 好：只傳回需要的欄位
SELECT order_id, order_date, total FROM orders;
```

### 3. 使用 LIMIT

```sql
-- 只取需要的筆數
SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;

-- 分頁查詢
SELECT * FROM orders LIMIT 10 OFFSET 20;
```

### 4. 批量操作

```sql
-- 不好：多次插入
INSERT INTO orders (user_id, total) VALUES (1, 100);
INSERT INTO orders (user_id, total) VALUES (1, 200);
INSERT INTO orders (user_id, total) VALUES (1, 300);

-- 好：單次批量插入
INSERT INTO orders (user_id, total) VALUES
    (1, 100),
    (1, 200),
    (1, 300);
```

### 5. 適當使用 EXISTS 取代 IN

```sql
-- 不好：IN 子查詢
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

-- 好：EXISTS
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 1000
);
```

## 效能瓶頸診斷

### 慢查詢日誌

```ini
# MySQL 慢查詢日誌
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
```

```sql
-- PostgreSQL
ALTER DATABASE mydb SET log_min_duration_statement = 1000;
```

### 監控工具

```bash
# MySQL
SHOW PROCESSLIST;          # 當前連線
SHOW STATUS LIKE 'Slow%';  # 慢查詢統計
SHOW INDEX FROM orders;    # 索引資訊

# PostgreSQL
SELECT * FROM pg_stat_activity;
SELECT * FROM pg_stat_user_tables;
```

## 快取策略

### 查詢快取

```ini
# MySQL 查詢快取
query_cache_type = 1
query_cache_size = 64M
query_cache_limit = 2M
```

### 應用層快取

```python
# Python 應用層快取範例
def get_user(user_id):
    cache_key = f"user:{user_id}"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    redis.setex(cache_key, 3600, json.dumps(user))
    return user
```

## 結語

SQL 查詢最佳化是一門藝術，需要理解查詢執行過程、索引原理和資料庫內部機制。透過 EXPLAIN 分析、善用索引、避免全表掃描和適當使用快取，可以大幅提升資料庫效能。

---

*延伸閱讀：*
- [SQL 效能最佳化](https://developers.google.com/search/?q=sql+performance+tuning)
- [資料庫索引](https://developers.google.com/search/?q=database+indexing)*