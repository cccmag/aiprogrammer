# 資料過濾與排序

## WHERE 子句

WHERE 子句用於過濾資料，只返回符合條件的記錄。它是 SQL 查詢中最常用的功能。

### 基本語法

```sql
SELECT column1, column2, ...
FROM table_name
WHERE condition;
```

### 比較運算子

| 運算子 | 說明 | 範例 |
|--------|------|------|
| `=` | 等於 | `WHERE age = 20` |
| `<>` 或 `!=` | 不等於 | `WHERE age <> 20` |
| `>` | 大於 | `WHERE price > 100` |
| `<` | 小於 | `WHERE stock < 10` |
| `>=` | 大於等於 | `WHERE age >= 18` |
| `<=` | 小於等於 | `WHERE price <= 500` |

### 邏輯運算子

```sql
-- AND：所有條件都必須成立
SELECT * FROM products
WHERE category = '手機' AND price < 20000;

-- OR：任一條件成立即可
SELECT * FROM products
WHERE category = '手機' OR category = '平板';

-- NOT：反轉條件
SELECT * FROM products
WHERE NOT category = '手機';

-- 組合使用（建議使用括號明確優先順序）
SELECT * FROM products
WHERE (category = '手機' OR category = '筆電')
  AND price < 30000;
```

### 特殊條件

```sql
-- BETWEEN：範圍查詢
SELECT * FROM products
WHERE price BETWEEN 10000 AND 30000;

-- IN：符合集合中的任一值
SELECT * FROM products
WHERE category IN ('手機', '平板', '穿戴裝置');

-- LIKE：模糊匹配
SELECT * FROM products
WHERE name LIKE '%iPhone%';  -- 包含 iPhone
-- % 代表任意長度的字串
-- _ 代表單一字元

-- IS NULL：檢查空值
SELECT * FROM products
WHERE category IS NULL;

-- IS NOT NULL：檢查非空值
SELECT * FROM products
WHERE category IS NOT NULL;
```

## ORDER BY：排序

### 基本語法

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...;
```

- `ASC`：升序（預設，小到大）
- `DESC`：降序（大到小）

### 範例

```sql
-- 單一欄位排序
SELECT name, price FROM products
ORDER BY price DESC;

-- 多欄位排序（先依類別排序，同類別依價格排序）
SELECT name, category, price FROM products
ORDER BY category ASC, price DESC;

-- 使用別名排序
SELECT name, price * 1.05 AS price_with_tax
FROM products
ORDER BY price_with_tax DESC;

-- 使用欄位位置排序
SELECT name, price, stock FROM products
ORDER BY 3 DESC;  -- 依第三個欄位（stock）排序
```

## LIMIT 與 OFFSET：分頁

### 基本語法

```sql
SELECT column1, column2, ...
FROM table_name
LIMIT row_count OFFSET offset_value;
```

LIMIT 限制返回的記錄數，OFFSET 指定跳過多少筆記錄。

### 範例

```sql
-- 只取前 5 筆
SELECT * FROM products
ORDER BY price DESC
LIMIT 5;

-- 跳過前 10 筆，取接下來的 5 筆（第 11-15 筆）
SELECT * FROM products
ORDER BY price DESC
LIMIT 5 OFFSET 10;

-- 簡寫：LIMIT 5 OFFSET 10 等同於 LIMIT 10, 5
SELECT * FROM products
ORDER BY price DESC
LIMIT 10, 5;
```

### 分頁實戰

```python
# Python 分頁查詢範例
def get_page(page_num, page_size=10):
    offset = (page_num - 1) * page_size
    query = f"""
    SELECT * FROM products
    ORDER BY id
    LIMIT {page_size} OFFSET {offset};
    """
    return execute_query(query)

# 第 1 頁：LIMIT 10 OFFSET 0
# 第 2 頁：LIMIT 10 OFFSET 10
# 第 3 頁：LIMIT 10 OFFSET 20
```

## 綜合範例

```sql
-- 建立銷售資料表
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    amount REAL NOT NULL,
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    region TEXT
);

INSERT INTO sales VALUES
(1, 'iPhone 17', 35900, 2, '2026-06-01', '台北'),
(2, 'MacBook Air', 42900, 1, '2026-06-01', '台北'),
(3, 'iPad Pro', 34900, 3, '2026-06-02', '台中'),
(4, 'iPhone 17', 35900, 1, '2026-06-02', '高雄'),
(5, 'AirPods', 6990, 5, '2026-06-03', '台北'),
(6, 'MacBook Air', 42900, 2, '2026-06-03', '台中'),
(7, 'iPad Pro', 34900, 1, '2026-06-04', '台北'),
(8, 'AirPods', 6990, 3, '2026-06-04', '高雄');

-- 查詢台北地區、金額大於 10000 的銷售記錄
SELECT * FROM sales
WHERE region = '台北' AND amount * quantity > 10000;

-- 按日期排序，顯示前 3 筆
SELECT product, quantity, amount * quantity AS total
FROM sales
ORDER BY sale_date ASC
LIMIT 3;

-- 查詢總金額最高的前 5 筆交易
SELECT product, region, quantity, amount,
       quantity * amount AS total
FROM sales
ORDER BY total DESC
LIMIT 5;
```

## 查詢執行順序

SQL 查詢的邏輯執行順序：

```
FROM      →  選取資料來源
WHERE     →  過濾記錄
GROUP BY  →  分組（下期介紹）
HAVING    →  過濾群組（下期介紹）
SELECT    →  選取欄位
ORDER BY  →  排序
LIMIT     →  限制返回筆數
```

了解這個順序對於撰寫正確的 SQL 非常重要。例如，你不能在 WHERE 中使用 SELECT 中定義的別名，因為 WHERE 在 SELECT 之前執行。

## 參考資料

- [SQL WHERE 子句](https://www.google.com/search?q=SQL+WHERE+clause+tutorial)
- [SQL ORDER BY 排序](https://www.google.com/search?q=SQL+ORDER+BY+tutorial)
- [SQL LIMIT 分頁](https://www.google.com/search?q=SQL+LIMIT+OFFSET+pagination)
