# SQL 查詢實務：常用 SQL 範例

## 概述

本期實作將展示常用的 SQL 查詢範例，涵蓋基本 CRUD 到複雜的 JOIN 和聚合查詢。

## 基本 SQL 語法

```sql
-- 建立表格
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入資料
INSERT INTO users (name, email, age) VALUES ('王小明', 'wang@example.com', 25);
INSERT INTO users (name, email, age) VALUES ('李小華', 'lee@example.com', 30);

-- 查詢
SELECT * FROM users WHERE age >= 18 ORDER BY created_at DESC;

-- 更新
UPDATE users SET age = age + 1 WHERE name = '王小明';

-- 刪除
DELETE FROM users WHERE id = 1;
```

## 進階查詢

```sql
-- JOIN 查詢
SELECT u.name, o.total, o.created_at
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.age >= 18
ORDER BY o.created_at DESC;

-- 聚合查詢
SELECT
    u.country,
    COUNT(*) AS user_count,
    AVG(u.age) AS avg_age,
    SUM(o.total) AS total_sales
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.country
HAVING COUNT(*) > 10
ORDER BY total_sales DESC;
```

## 程式碼展示

本期的程式碼位於 `_code/` 目錄：

- `queries.js` - 常用 SQL 查詢範例

執行方式：

```bash
sqlite3 example.db < queries.js
# 或
node queries.js
```

---

*本期程式實作到此結束。*