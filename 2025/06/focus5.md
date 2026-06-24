# 聚合函數與 GROUP BY

## 聚合函數

聚合函數（Aggregate Functions）用於對一組記錄進行計算，返回單一值。它們通常與 GROUP BY 搭配使用。

### 常用聚合函數

| 函數 | 說明 | 範例 |
|------|------|------|
| `COUNT()` | 計算記錄數 | `COUNT(*)` 或 `COUNT(column)` |
| `SUM()` | 計算總和 | `SUM(amount)` |
| `AVG()` | 計算平均值 | `AVG(price)` |
| `MAX()` | 找出最大值 | `MAX(score)` |
| `MIN()` | 找出最小值 | `MIN(score)` |

### 基本範例

```sql
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

-- 基本聚合查詢
SELECT COUNT(*) AS 交易筆數,
       SUM(amount * quantity) AS 總銷售額,
       AVG(amount) AS 平均單價,
       MAX(amount) AS 最高單價,
       MIN(amount) AS 最低單價
FROM sales;
```

### COUNT 的細節

```sql
-- COUNT(*) 計算所有記錄數（包含 NULL）
SELECT COUNT(*) FROM sales;  -- 8

-- COUNT(column) 只計算非 NULL 的記錄
SELECT COUNT(region) FROM sales;  -- 8（所有記錄都有 region）

-- COUNT(DISTINCT column) 計算不重複的值
SELECT COUNT(DISTINCT product) FROM sales;  -- 4
SELECT COUNT(DISTINCT region) FROM sales;   -- 3
```

## GROUP BY：分組

GROUP BY 將資料按照指定欄位分組，然後對每個組套用聚合函數。

### 基本語法

```sql
SELECT column1, aggregate_function(column2)
FROM table_name
GROUP BY column1;
```

### 範例

```sql
-- 按產品分組，計算每個產品的銷售統計
SELECT product AS 產品,
       COUNT(*) AS 交易次數,
       SUM(quantity) AS 總數量,
       SUM(amount * quantity) AS 總金額
FROM sales
GROUP BY product;

-- 按地區分組
SELECT region AS 地區,
       COUNT(*) AS 交易次數,
       ROUND(AVG(amount * quantity), 0) AS 平均交易金額
FROM sales
GROUP BY region;

-- 多欄位分組
SELECT product AS 產品,
       region AS 地區,
       SUM(quantity) AS 總數量
FROM sales
GROUP BY product, region;
```

## HAVING：過濾群組

HAVING 類似於 WHERE，但 WHERE 過濾的是記錄，HAVING 過濾的是群組。

```sql
-- 找出總銷售額超過 50000 的產品
SELECT product AS 產品,
       SUM(amount * quantity) AS 總金額
FROM sales
GROUP BY product
HAVING SUM(amount * quantity) > 50000;

-- WHERE 在 GROUP BY 之前，HAVING 在 GROUP BY 之後
SELECT product AS 產品,
       SUM(quantity) AS 總數量
FROM sales
WHERE region = '台北'          -- 先過濾地區
GROUP BY product
HAVING SUM(quantity) >= 2;     -- 再過濾數量
```

### WHERE vs HAVING

| | WHERE | HAVING |
|------|-------|--------|
| 使用時機 | GROUP BY 之前 | GROUP BY 之後 |
| 過濾對象 | 單筆記錄 | 群組結果 |
| 可使用聚合函數 | 不可以 | 可以 |
| 可使用別名 | 不可以 | 可以（部分資料庫） |

## 進階範例

```sql
-- 各月份銷售統計
SELECT strftime('%Y-%m', sale_date) AS 月份,
       COUNT(*) AS 交易次數,
       SUM(amount * quantity) AS 總金額
FROM sales
GROUP BY 月份
ORDER BY 月份;

-- 找出平均單價高於整體平均的產品
SELECT product AS 產品,
       AVG(amount) AS 平均單價
FROM sales
GROUP BY product
HAVING AVG(amount) > (SELECT AVG(amount) FROM sales);
```

## 常見錯誤

### 錯誤 1：SELECT 中混合聚合與非聚合欄位

```sql
-- 錯誤！product 沒有在 GROUP BY 中，也不是聚合函數
SELECT product, SUM(amount * quantity)
FROM sales;

-- 正確：要嘛加入 GROUP BY，要嘛全部使用聚合函數
SELECT product, SUM(amount * quantity)
FROM sales
GROUP BY product;
```

### 錯誤 2：在 WHERE 中使用聚合函數

```sql
-- 錯誤！WHERE 不能使用聚合函數
SELECT product, SUM(quantity)
FROM sales
WHERE SUM(quantity) > 5
GROUP BY product;

-- 正確：使用 HAVING
SELECT product, SUM(quantity)
FROM sales
GROUP BY product
HAVING SUM(quantity) > 5;
```

## 實戰：銷售儀表板

```sql
-- 完整的銷售分析報表
SELECT 
    CASE 
        WHEN GROUPING(product) = 1 THEN '總計'
        ELSE product
    END AS 產品,
    COUNT(*) AS 交易次數,
    SUM(quantity) AS 銷售數量,
    SUM(amount * quantity) AS 銷售金額,
    ROUND(AVG(amount), 0) AS 平均單價
FROM sales
GROUP BY product
ORDER BY 銷售金額 DESC;

-- 各產品在各區域的表現
SELECT product, region,
       SUM(quantity) AS qty,
       RANK() OVER (PARTITION BY product ORDER BY SUM(quantity) DESC) AS rank
FROM sales
GROUP BY product, region;
```

## 查詢邏輯執行順序（完整版）

```
FROM      →  資料來源
WHERE     →  過濾記錄
GROUP BY  →  分組
HAVING    →  過濾群組
SELECT    →  選取欄位/計算
ORDER BY  →  排序
LIMIT     →  限制筆數
```

## 參考資料

- [SQL 聚合函數](https://www.google.com/search?q=SQL+aggregate+functions+COUNT+SUM+AVG)
- [SQL GROUP BY](https://www.google.com/search?q=SQL+GROUP+BY+clause+tutorial)
- [SQL HAVING](https://www.google.com/search?q=SQL+HAVING+clause+tutorial)
