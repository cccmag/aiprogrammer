# PostgreSQL 9.5 新功能

## 前言

PostgreSQL 9.5 帶來了多項企業級功能，讓 PostgreSQL 在企業應用中更加實用。

## 主要新功能

### BRIN 索引

```sql
-- BRIN 索引：區塊範圍索引
-- 適合大型資料表、資料有序

CREATE INDEX idx_logs_created ON logs USING BRIN(created_at);

-- 查詢效能
EXPLAIN SELECT * FROM logs
WHERE created_at BETWEEN '2015-01-01' AND '2015-01-31';
```

### Upsert（INSERT ... ON CONFLICT）

```sql
INSERT INTO users (id, name, email)
VALUES (1, '王小明', 'wang@example.com')
ON CONFLICT (id) DO UPDATE
  SET name = EXCLUDED.name, email = EXCLUDED.email;
```

### 進階分析功能

```sql
-- CUBE：所有組合聚合
SELECT country, product, SUM(sales)
FROM sales
GROUP BY CUBE(country, product);

-- ROLLUP：階層聚合
SELECT year, month, SUM(sales)
FROM sales
GROUP BY ROLLUP(year, month);

-- GROUPING SETS：指定聚合組合
SELECT country, product, SUM(sales)
FROM sales
GROUP BY GROUPING SETS((country), (product), ());
```

---

## 延伸閱讀

- [PostgreSQL 9.5 發布說明](https://www.google.com/search?q=PostgreSQL+9.5+release+notes)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*