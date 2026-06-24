# 子查詢實戰

## 子查詢的力量

子查詢（Subquery）讓你可以在一個查詢的內部嵌入另一個查詢，實現更複雜的資料檢索。子查詢可以出現在 SELECT、FROM、WHERE、HAVING 等任何子句中。

## 標量子查詢

返回單一值的子查詢，像普通值一樣使用。

```sql
-- 每個員工的薪資與平均薪資的比較
SELECT name, salary,
       (SELECT ROUND(AVG(salary), 0) FROM employees) AS avg_salary,
       salary - (SELECT ROUND(AVG(salary), 0) FROM employees) AS diff
FROM employees;

-- 找出薪資高於平均的員工
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;

-- 最新的訂單
SELECT * FROM orders
WHERE order_date = (SELECT MAX(order_date) FROM orders);
```

## 列子查詢

返回單列多行的子查詢，通常與 IN、ANY、ALL 搭配。

```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    min_salary REAL
);

INSERT INTO departments VALUES
(1, '工程', 50000),
(2, '業務', 40000),
(3, '財務', 45000);

-- 找出薪資高於所有業務部門員工的人
SELECT name, salary FROM employees
WHERE salary > ALL (
    SELECT salary FROM employees
    WHERE department = '業務'
);

-- 找出薪資高於任一工程部門員工的人
SELECT name, salary FROM employees
WHERE salary > ANY (
    SELECT salary FROM employees
    WHERE department = '工程'
);

-- 找出在所有部門最低薪資範圍內的員工
SELECT name, salary FROM employees
WHERE salary >= ALL (
    SELECT min_salary FROM departments
);

-- NOT IN 子查詢
SELECT name FROM customers
WHERE id NOT IN (
    SELECT DISTINCT customer_id FROM orders
);
```

## FROM 子句中的子查詢（Derived Table）

```sql
-- 找出生產最多產品的類別
SELECT category, product_count
FROM (
    SELECT category, COUNT(*) AS product_count
    FROM products
    GROUP BY category
)
WHERE product_count = (
    SELECT MAX(product_count)
    FROM (
        SELECT COUNT(*) AS product_count
        FROM products
        GROUP BY category
    )
);

-- 各部門薪資統計排名
SELECT department, avg_salary, rank
FROM (
    SELECT department,
           ROUND(AVG(salary), 0) AS avg_salary,
           RANK() OVER (ORDER BY AVG(salary) DESC) AS rank
    FROM employees
    GROUP BY department
)
WHERE rank <= 3;
```

## 關聯子查詢

關聯子查詢（Correlated Subquery）引用外部查詢的欄位，對外部查詢的每一筆記錄執行一次。

```sql
-- 找出每個分類中價格最高的產品
SELECT p1.name, p1.category, p1.price
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
    SELECT MAX(o2.order_date)
    FROM orders o2
    WHERE o2.customer_id = c.id
);

-- 找出訂單金額高於客戶平均訂單金額的訂單
SELECT o1.id, o1.customer_id, o1.total
FROM orders o1
WHERE o1.total > (
    SELECT AVG(o2.total)
    FROM orders o2
    WHERE o2.customer_id = o1.customer_id
);
```

### EXISTS 與 NOT EXISTS

```sql
-- 找出有訂單的客戶
SELECT name FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id
);

-- 找出從未訂購 iPhone 的客戶
SELECT name FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id
      AND o.product LIKE '%iPhone%'
);

-- EXISTS vs IN 效能
-- 通常 EXISTS 在大表格時效能更好
-- 因為找到第一筆符合記錄後就會停止
```

## 巢狀子查詢

子查詢可以多層嵌套，但過深會影響可讀性。

```sql
-- 找出訂購了價格最高產品的客戶
SELECT c.name
FROM customers c
WHERE c.id IN (
    SELECT o.customer_id
    FROM orders o
    WHERE o.product_id = (
        SELECT p.id
        FROM products p
        ORDER BY p.price DESC
        LIMIT 1
    )
);

-- 更好的寫法：使用 CTE
WITH best_product AS (
    SELECT id, name, price
    FROM products
    ORDER BY price DESC
    LIMIT 1
),
buyers AS (
    SELECT DISTINCT o.customer_id
    FROM orders o
    INNER JOIN best_product bp ON o.product_id = bp.id
)
SELECT c.name
FROM customers c
INNER JOIN buyers b ON c.id = b.customer_id;
```

## 子查詢的效能考量

```sql
-- 有時 JOIN 比子查詢更高效
-- 子查詢寫法
SELECT * FROM products
WHERE id IN (
    SELECT product_id FROM order_items
    WHERE quantity >= 10
);

-- JOIN 寫法（通常更快）
SELECT DISTINCT p.*
FROM products p
INNER JOIN order_items oi ON p.id = oi.product_id
WHERE oi.quantity >= 10;
```

### 使用策略

| 情境 | 建議 |
|------|------|
| 簡單的聚合比較 | 標量子查詢 |
| 集合成員測試 | IN / NOT IN |
| 存在性測試 | EXISTS / NOT EXISTS |
| 複雜多步驟查詢 | CTE（下一篇） |
| 大量資料的關聯查詢 | JOIN 通常更佳 |

## 實戰範例

```sql
-- 找出連續兩天都有銷售記錄的產品
SELECT DISTINCT s1.product
FROM sales s1
WHERE EXISTS (
    SELECT 1 FROM sales s2
    WHERE s2.product = s1.product
      AND s2.sale_date = DATE(s1.sale_date, '+1 day')
);

-- 找出銷售成長最顯著的產品
SELECT product,
       current_month_sales,
       prev_month_sales,
       ROUND((current_month_sales - prev_month_sales) / prev_month_sales * 100, 1) AS growth_pct
FROM (
    SELECT product,
           SUM(CASE WHEN strftime('%m', sale_date) = '06' THEN amount * quantity END) AS current_month_sales,
           SUM(CASE WHEN strftime('%m', sale_date) = '05' THEN amount * quantity END) AS prev_month_sales
    FROM sales
    WHERE sale_date >= '2026-05-01' AND sale_date < '2026-07-01'
    GROUP BY product
)
WHERE current_month_sales IS NOT NULL
  AND prev_month_sales IS NOT NULL
ORDER BY growth_pct DESC;
```

## 參考資料

- [SQL 子查詢教學](https://www.google.com/search?q=SQL+subquery+tutorial+SELECT+FROM+WHERE)
- [SQL 關聯子查詢](https://www.google.com/search?q=SQL+correlated+subquery+examples)
- [SQL EXISTS 用法](https://www.google.com/search?q=SQL+EXISTS+and+NOT+EXISTS)
