# INNER JOIN 與 LEFT JOIN

## 為什麼要 JOIN？

在正規化的資料庫中，資料分散在多個表格中。JOIN 讓我們能夠在單一查詢中合併多個表格的資料，這是 SQL 最強大的功能之一。

## 準備範例資料

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    amount REAL NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE
);

INSERT INTO customers VALUES
(1, '王小明', '台北'),
(2, '李小華', '台中'),
(3, '張小英', '高雄'),
(4, '陳小豪', '台北');

INSERT INTO orders VALUES
(101, 1, 'iPhone 17', 35900, '2026-06-01'),
(102, 1, 'AirPods', 6990, '2026-06-02'),
(103, 2, 'MacBook Air', 42900, '2026-06-03'),
(104, 3, 'iPad Pro', 34900, '2026-06-04'),
(105, 5, 'Apple Watch', 14900, '2026-06-05');
-- 注意：客戶 4（陳小豪）沒有訂單
--      訂單 105 的 customer_id=5 沒有對應客戶
```

## INNER JOIN

INNER JOIN 只返回兩個表格中**都有匹配**的記錄。

```sql
SELECT *
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

```
id │ name  │ city  │ id  │ customer_id │ product      │ amount
───┼───────┼───────┼─────┼─────────────┼──────────────┼───────
1  │ 王小明│ 台北  │ 101 │ 1           │ iPhone 17    │ 35900
1  │ 王小明│ 台北  │ 102 │ 1           │ AirPods      │ 6990
2  │ 李小華│ 台中  │ 103 │ 2           │ MacBook Air  │ 42900
3  │ 張小英│ 高雄  │ 104 │ 3           │ iPad Pro     │ 34900
```

**結果分析**：
- 王小明有 2 筆訂單 → 出現 2 次
- 李小華有 1 筆訂單 → 出現 1 次
- 張小英有 1 筆訂單 → 出現 1 次
- 陳小豪（客戶 4）沒有訂單 → 不包含
- 訂單 105（客戶 5）沒有對應客戶 → 不包含

### 實戰：客戶訂單查詢

```sql
-- 查詢特定客戶的訂單
SELECT c.name, c.city, o.product, o.amount, o.order_date
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
WHERE c.name = '王小明'
ORDER BY o.order_date DESC;

-- 分組統計：查詢每個客戶的總消費
SELECT c.name, c.city,
       COUNT(o.id) AS order_count,
       SUM(o.amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id
ORDER BY total_spent DESC;
```

## LEFT JOIN

LEFT JOIN（也稱為 LEFT OUTER JOIN）返回**左表格的所有記錄**，右表格沒有匹配時用 NULL 填充。

```sql
SELECT *
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;
```

```
id │ name  │ city  │ id   │ customer_id │ product      │ amount
───┼───────┼───────┼──────┼─────────────┼──────────────┼───────
1  │ 王小明│ 台北  │ 101  │ 1           │ iPhone 17    │ 35900
1  │ 王小明│ 台北  │ 102  │ 1           │ AirPods      │ 6990
2  │ 李小華│ 台中  │ 103  │ 2           │ MacBook Air  │ 42900
3  │ 張小英│ 高雄  │ 104  │ 3           │ iPad Pro     │ 34900
4  │ 陳小豪│ 台北  │ NULL │ NULL        │ NULL         │ NULL
```

**結果分析**：
- 所有客戶都出現（包括沒有訂單的陳小豪）
- 陳小豪的訂單欄位為 NULL

### 實戰：找出沒有訂單的客戶

```sql
SELECT c.name, c.city
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
-- 結果：陳小豪（4, 台北）
```

## CROSS JOIN

CROSS JOIN 返回兩個表格的笛卡兒乘積——左表格的每筆記錄與右表格的所有記錄配對。

```sql
-- 列出所有客戶與所有產品的組合
SELECT c.name AS customer, p.name AS product
FROM customers c
CROSS JOIN products p;
```

CROSS JOIN 通常不需要，但在某些場景（如生成報表、填充缺失日期）很有用。

## SELF JOIN

表格與自身 JOIN，用於處理同一表格中記錄之間的關聯。

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    manager_id INTEGER
);

INSERT INTO employees VALUES
(1, '執行長', NULL),
(2, '技術長', 1),
(3, '財務長', 1),
(4, '工程經理', 2),
(5, '資深工程師', 4);

-- 查詢每位員工及其主管
SELECT e.name AS employee,
       m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

## 多表格 JOIN

```sql
-- 三表格 JOIN：客戶 → 訂單 → 訂單明細
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
);

INSERT INTO order_items VALUES
(1, 101, 'iPhone 17', 1, 35900),
(2, 102, 'AirPods', 2, 6990);

SELECT c.name, o.id AS order_id,
       oi.product_name, oi.quantity, oi.unit_price
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
ORDER BY c.name, o.id;
```

## JOIN 的執行順序與效能

```sql
-- 提前過濾可以提升 JOIN 效能
SELECT c.name, o.product, o.amount
FROM (SELECT * FROM customers WHERE city = '台北') c
INNER JOIN orders o ON c.id = o.customer_id;

-- 或者直接在 ON 條件中過濾
SELECT c.name, o.product, o.amount
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id AND c.city = '台北';
```

## INNER JOIN vs LEFT JOIN 快速比較

```
INNER JOIN（兩圓交集）        LEFT JOIN（左圓全部）
┌─────────────────────┐     ┌─────────────────────┐
│                     │     │  ◆◆◆◆◆               │
│  ◆◆◆                 │     │  ◆◆INNER◆            │
│  ◆◆  INNER  ◆◆◆      │     │  ◆◆  PART ◆◆◆        │
│  ◆◆◆   PART  ◆◆      │     │  ◆◆◆◆◆◆◆◆◆◆◆        │
│      ◆◆◆◆◆◆◆         │     │                     │
│         ◆◆◆           │     │  LEFT 表格全部記錄  │
└─────────────────────┘     └─────────────────────┘
```

## 選擇建議

| 需求 | 使用 |
|------|------|
| 只要兩邊都有的資料 | INNER JOIN |
| 需要保留左表格的資料，即使右邊為空 | LEFT JOIN |
| 找出左表格中沒有對應右表格的資料 | LEFT JOIN + IS NULL |
| 需要笛卡兒乘積 | CROSS JOIN |

## 參考資料

- [SQL INNER JOIN 教學](https://www.google.com/search?q=SQL+INNER+JOIN+tutorial+examples)
- [SQL LEFT JOIN 教學](https://www.google.com/search?q=SQL+LEFT+JOIN+tutorial)
- [SQL JOIN 型別對比](https://www.google.com/search?q=SQL+JOIN+types+INNER+LEFT+RIGHT+FULL)
