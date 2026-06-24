# 資料庫效能調校

## 前言

效能調校是資料庫管理的重要課題，本篇介紹常見的優化方法。

## 索引優化

```sql
-- 建立合適的索引
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- 避免過多索引
-- 每個索引都會影響寫入效能

-- 使用 EXPLAIN 分析
EXPLAIN SELECT * FROM orders WHERE user_id = 1;
```

## 查詢優化

```sql
-- 避免 SELECT *
SELECT id, name FROM users WHERE id = 1;

-- 使用 LIMIT
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;

-- 避免 LIKE %
SELECT * FROM users WHERE email LIKE '%@gmail.com';  -- 無法使用索引
SELECT * FROM users WHERE email LIKE 'gmail%';        -- 可使用索引
```

## 設定調優

```sql
-- PostgreSQL
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';

-- MySQL
SET GLOBAL innodb_buffer_pool_size = 4294967296;
```

## 慢查詢分析

```sql
-- PostgreSQL
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- 1 秒

-- MySQL
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
```

---

## 延伸閱讀

- [Database Performance Tuning](https://www.google.com/search?q=database+performance+tuning+guide)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*