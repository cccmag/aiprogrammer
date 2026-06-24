# 子查詢與 CTE

## 什麼是子查詢？

子查詢（Subquery）是嵌套在另一個 SQL 查詢內部的查詢。子查詢的特點是：

1. 用括號 `()` 包圍
2. 可以返回單一值、一列值或一個表格
3. 可以在 SELECT、FROM、WHERE 等子句中使用

## 標量子查詢

返回單一值的子查詢，可以像普通值一樣使用。

```sql
-- 找出價格高於平均價格的商品
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- 顯示每個產品的價格與平均價格的差異
SELECT name, price,
       (SELECT AVG(price) FROM products) AS avg_price,
       price - (SELECT AVG(price) FROM products) AS diff
FROM products;
```

## 列子查詢

返回一列值的子查詢，通常與 IN、ANY、ALL 搭配使用。

```sql
-- 找出有訂單的客戶
SELECT name FROM customers
WHERE id IN (SELECT DISTINCT customer_id FROM orders);

-- 找出價格高於任一 iPhone 產品的商品
SELECT name, price FROM products
WHERE price > ANY (SELECT price FROM products WHERE category = '手機');

-- 找出價格高於所有 iPhone 產品的商品
SELECT name, price FROM products
WHERE price > ALL (SELECT price FROM products WHERE category = '手機');
```

## 表格子查詢

返回一個表格的子查詢，通常用在 FROM 子句中（稱為 Derived Table）。

```sql
-- 找出每個產品類別中價格最高的產品
SELECT p.category, p.name, p.price
FROM products p
INNER JOIN (
    SELECT category, MAX(price) AS max_price
    FROM products
    GROUP BY category
) max_p ON p.category = max_p.category AND p.price = max_p.max_price;

-- 計算每個客戶的訂單總金額
SELECT c.name, o.total_spent
FROM customers c
INNER JOIN (
    SELECT customer_id, SUM(total) AS total_spent
    FROM orders
    GROUP BY customer_id
) o ON c.id = o.customer_id;
```

## 關聯子查詢

子查詢參考外部查詢的欄位，對於外部查詢的每一筆記錄執行一次。

```sql
-- 找出每個分類中價格最高的產品
SELECT name, category, price
FROM products p1
WHERE price = (
    SELECT MAX(price)
    FROM products p2
    WHERE p2.category = p1.category
);

-- 找出每個客戶的最新訂單
SELECT c.name, o.order_date, o.total
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
WHERE o.order_date = (
    SELECT MAX(order_date)
    FROM orders
    WHERE customer_id = c.id
);
```

### EXISTS 與 NOT EXISTS

```sql
-- 找出有下訂單的客戶
SELECT name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id
);

-- 找出從未下訂單的客戶
SELECT name FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id
);
```

## CTE（Common Table Expression）

CTE 是用 WITH 子句定義的臨時命名查詢，可以在主查詢中多次引用。CTE 讓複雜查詢更易讀、更易維護。

### 基本語法

```sql
WITH cte_name AS (
    SELECT query
)
SELECT * FROM cte_name;
```

### 範例

```sql
WITH regional_sales AS (
    SELECT region, SUM(amount * quantity) AS total_sales
    FROM sales
    GROUP BY region
),
top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > 100000
)
SELECT s.product, s.region, SUM(s.amount * s.quantity) AS sales
FROM sales s
WHERE s.region IN (SELECT region FROM top_regions)
GROUP BY s.product, s.region;
```

### CTE 的優點

```sql
-- 不使用 CTE 的寫法（嵌套深，不易讀）
SELECT c.name, o.total_spent
FROM customers c
INNER JOIN (
    SELECT customer_id, SUM(total) AS total_spent
    FROM orders
    GROUP BY customer_id
) o ON c.id = o.customer_id
WHERE o.total_spent > (
    SELECT AVG(total_spent)
    FROM (
        SELECT customer_id, SUM(total) AS total_spent
        FROM orders
        GROUP BY customer_id
    )
);

-- 使用 CTE 的寫法（清晰易懂）
WITH customer_spending AS (
    SELECT customer_id, SUM(total) AS total_spent
    FROM orders
    GROUP BY customer_id
),
avg_spending AS (
    SELECT AVG(total_spent) AS avg_amount
    FROM customer_spending
)
SELECT c.name, cs.total_spent
FROM customers c
INNER JOIN customer_spending cs ON c.id = cs.customer_id
CROSS JOIN avg_spending
WHERE cs.total_spent > avg_spending.avg_amount;
```

### 遞迴 CTE

部分資料庫（如 PostgreSQL、SQLite）支援遞迴 CTE，用於處理樹狀或圖形結構的資料。

```sql
-- 建立組織結構表
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

INSERT INTO employees VALUES
(1, '執行長', NULL),
(2, '技術長', 1),
(3, '財務長', 1),
(4, '工程經理', 2),
(5, '資深工程師', 4),
(6, '初級工程師', 4);

-- 遞迴 CTE：找出所有直屬與間接下屬
WITH RECURSIVE org_chart AS (
    -- 基礎情況：直接下屬
    SELECT id, name, manager_id, 0 AS level
    FROM employees
    WHERE manager_id = 2  -- 技術長的下屬

    UNION ALL

    -- 遞迴情況：下屬的下屬
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    INNER JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, id;
```

## 子查詢 vs CTE  vs JOIN

| 特性 | 子查詢 | CTE | JOIN |
|------|--------|-----|------|
| 可讀性 | 嵌套深時較差 | 良好 | 良好 |
| 可重複使用 | 不可 | 可在同一查詢中多次引用 | N/A |
| 遞迴支援 | 不支援 | 支援（遞迴 CTE） | 不支援 |
| 效能 | 取決於資料庫最佳化器 | 通常與子查詢相似 | 通常最佳 |

## 實戰建議

1. **簡單查詢用子查詢**：當子查詢只使用一次且邏輯簡單時
2. **複雜查詢用 CTE**：當查詢邏輯複雜或需要多次引用相同子查詢時
3. **關聯查詢優先考慮 JOIN**：大多數情況下 JOIN 效能優於關聯子查詢
4. **避免過深嵌套**：超過 3 層的子查詢應該重構為 CTE 或拆分為多個查詢

## 參考資料

- [SQL 子查詢](https://www.google.com/search?q=SQL+subquery+tutorial)
- [SQL CTE 公用表格表達式](https://www.google.com/search?q=SQL+Common+Table+Expression+CTE+tutorial)
- [SQL 遞迴查詢](https://www.google.com/search?q=SQL+recursive+query+CTE)
