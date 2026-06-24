# SQL 查詢語法：SELECT、WHERE、JOIN

## 前言

SQL（Structured Query Language）是用於操作關聯式資料庫的標準語言。本篇介紹最常用的 SQL 查詢語法。

## 基本查詢

### SELECT

```sql
-- 查詢所有欄位
SELECT * FROM users;

-- 查詢特定欄位
SELECT name, email FROM users;

-- 查詢並重新命名
SELECT name AS "使用者名稱", email AS "電子郵件" FROM users;

-- DISTINCT 去重
SELECT DISTINCT country FROM users;
```

### WHERE 條件

```sql
-- 單一條件
SELECT * FROM users WHERE age >= 18;

-- 多條件（AND）
SELECT * FROM users WHERE age >= 18 AND country = 'Taiwan';

-- 多條件（OR）
SELECT * FROM users WHERE country = 'Taiwan' OR country = 'Japan';

-- NOT 否定
SELECT * FROM users WHERE NOT country = 'USA';

-- IN 列表
SELECT * FROM users WHERE country IN ('Taiwan', 'Japan', 'Korea');

-- BETWEEN 範圍
SELECT * FROM users WHERE age BETWEEN 18 AND 30;

-- LIKE 模糊查詢
SELECT * FROM users WHERE name LIKE '王%';    -- 開頭是王的
SELECT * FROM users WHERE email LIKE '%@gmail.com'; -- gmail 用戶
SELECT * FROM users WHERE name LIKE '_小%';  -- 第二個字是小
```

### ORDER BY 排序

```sql
-- 遞增排序（預設）
SELECT * FROM users ORDER BY created_at;

-- 遞減排序
SELECT * FROM users ORDER BY created_at DESC;

-- 多欄位排序
SELECT * FROM users ORDER BY country, age DESC;

-- NULL 排在最後
SELECT * FROM users ORDER BY age NULLS LAST;
```

### LIMIT 分頁

```sql
-- 取前 10 筆
SELECT * FROM users LIMIT 10;

-- 跳過前 20 筆，取 10 筆
SELECT * FROM users LIMIT 10 OFFSET 20;

-- MySQL 語法
SELECT * FROM users LIMIT 20, 10;
```

## 聚合函數

### 基本聚合

```sql
-- 計數
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM users WHERE age >= 18;

-- 總和
SELECT SUM(total) FROM orders;

-- 平均
SELECT AVG(age) FROM users;

-- 最大/最小
SELECT MAX(age), MIN(age) FROM users;

-- 去重計數
SELECT COUNT(DISTINCT country) FROM users;
```

### GROUP BY 分組

```sql
-- 依國家分組
SELECT country, COUNT(*) FROM users GROUP BY country;

-- 依國家分組並過濾
SELECT country, COUNT(*) FROM users GROUP BY country HAVING COUNT(*) > 10;

-- 多欄位分組
SELECT country, gender, AVG(age) FROM users
GROUP BY country, gender;
```

### 聚合範例

```sql
-- 每個國家的訂單統計
SELECT
    u.country,
    COUNT(o.id) AS order_count,
    SUM(o.total) AS total_sales,
    AVG(o.total) AS avg_order
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.country
ORDER BY total_sales DESC;
```

## JOIN 關聯查詢

### INNER JOIN

```sql
-- 基本語法
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 多表關聯
SELECT u.name, o.total, p.name AS product
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id;
```

```
INNER JOIN 結果：
─────────────────

users          orders         result
┌────┐        ┌────┐         ┌────┐
│ 1  │        │ 1  │         │ 1  │
└────┘        └────┘         └────┘
   │    JOIN    │      →        │
┌────┐        ┌────┐         ┌────┐
│ 2  │        │ 2  │         │ 2  │
└────┘        └────┘         └────┘
   │    JOIN    │      →        │
┌────┐        ┌────┐         ┌────┐
│ 3  │        │ 5  │         │ 3  │  ← 只取兩邊都有對應的
└────┘        └────┘         └────┘
```

### LEFT JOIN

```sql
-- 包含所有左表資料
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

```
LEFT JOIN 結果：
─────────────────

users          orders         result
┌────┐        ┌────┐         ┌────┐
│ 1  │        │ 1  │         │ 1  │ ← 有對應
└────┘        └────┘         └────┘
   │    JOIN    │      →
┌────┐        ┌────┐         ┌────┐
│ 2  │        │ 2  │         │ 2  │ ← 有對應
└────┘        └────┘         └────┘
   │    JOIN    │      →
┌────┐           ○           ┌────┐
│ 3  │                      │ 3  │ NULL ← 無對應，仍保留
└────┘                      └────┘
```

### RIGHT JOIN / FULL OUTER JOIN

```sql
-- RIGHT JOIN（包含所有右表）
SELECT u.name, o.total
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- FULL OUTER JOIN（兩邊都保留）
SELECT u.name, o.total
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;
```

## 子查詢

### 簡單子查詢

```sql
-- 在 WHERE 中使用
SELECT * FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- 在 FROM 中使用
SELECT country, avg_age
FROM (SELECT country, AVG(age) AS avg_age FROM users GROUP BY country) sub;
```

### EXISTS / IN

```sql
-- 有訂單的使用者
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- 購買過特定商品的用戶
SELECT * FROM users
WHERE id IN (
    SELECT user_id FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    WHERE oi.product_id = 123
);
```

## UNION / INTERSECT

```sql
-- 合併結果（自動去重）
SELECT name FROM users
UNION
SELECT name FROM admins;

-- 合併結果（保留重複）
SELECT name FROM users
UNION ALL
SELECT name FROM admins;

-- 交集
SELECT name FROM users
INTERSECT
SELECT name FROM admins;

-- 差集（PostgreSQL）
SELECT name FROM users
EXCEPT
SELECT name FROM admins;
```

## CASE 表達式

```sql
-- 簡單 CASE
SELECT
    name,
    age,
    CASE age
        WHEN < 18 THEN '未成年'
        WHEN < 30 THEN '青年'
        WHEN < 60 THEN '中年'
        ELSE '老年'
    END AS age_group
FROM users;

-- 搜尋 CASE
SELECT
    name,
    CASE
        WHEN age < 18 THEN '未成年'
        WHEN age >= 18 AND age < 30 THEN '青年'
        ELSE '其他'
    END AS category
FROM users;
```

## 常用函數

```sql
-- 字串函數
SELECT UPPER(name), LOWER(email) FROM users;
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;
SELECT SUBSTRING(phone, 1, 3) AS area_code FROM users;
SELECT TRIM(name), LENGTH(name) FROM users;

-- 數值函數
SELECT ABS(-10), ROUND(3.14159, 2), CEIL(3.1), FLOOR(3.9);

-- 日期函數
SELECT NOW(), CURRENT_DATE, CURRENT_TIME;
SELECT EXTRACT(YEAR FROM created_at) FROM users;
SELECT DATE_TRUNC('month', created_at) FROM users;
SELECT age, INTERVAL '1 month' FROM users;

-- NULL 處理
SELECT COALESCE(phone, '無電話') FROM users;
SELECT NULLIF(age, 0) FROM users;
```

## 結語

SQL 是操作關聯式資料庫的強大工具。熟練掌握 SELECT、WHERE、JOIN、聚合和子查詢，就能應對大多數的資料查詢需求。

---

## 延伸閱讀

- [SQL 查詢教學](https://www.google.com/search?q=SQL+SELECT+JOIN+tutorial)
- [SQL 語法參考](https://www.google.com/search?q=SQL+reference+manual)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」歷史回顧系列之一。*