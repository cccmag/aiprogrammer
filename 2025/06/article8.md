# COUNT、SUM、AVG 聚合

## 從原始資料到洞察

聚合函數是 SQL 中將原始資料轉化為商業洞察的關鍵工具。它們對一組記錄執行計算，返回單一的彙總值。

## 建立範例資料

```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    category TEXT,
    amount REAL NOT NULL,
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    region TEXT
);

INSERT INTO sales VALUES
(1, 'iPhone 17', '手機', 35900, 2, '2026-06-01', '台北'),
(2, 'MacBook Air', '筆電', 42900, 1, '2026-06-01', '台北'),
(3, 'iPad Pro', '平板', 34900, 3, '2026-06-02', '台中'),
(4, 'iPhone 17', '手機', 35900, 1, '2026-06-02', '高雄'),
(5, 'AirPods', '耳機', 6990, 5, '2026-06-03', '台北'),
(6, 'MacBook Air', '筆電', 42900, 2, '2026-06-03', '台中'),
(7, 'iPad Pro', '平板', 34900, 1, '2026-06-04', '台北'),
(8, 'AirPods', '耳機', 6990, 3, '2026-06-04', '高雄'),
(9, 'iPhone 17', '手機', 35900, 1, '2026-06-05', '台中'),
(10, 'Apple Watch', '穿戴', 14900, 2, '2026-06-05', '台北');
```

## COUNT：計數

### 使用方式

```sql
-- 計算所有記錄
SELECT COUNT(*) FROM sales;  -- 10

-- 計算非 NULL 值（此範例所有欄位皆有值）
SELECT COUNT(region) FROM sales;  -- 10

-- 計算不重複的值
SELECT COUNT(DISTINCT product) FROM sales;  -- 5
SELECT COUNT(DISTINCT region) FROM sales;   -- 3
```

### COUNT 的細節

```sql
-- COUNT(*) 和 COUNT(1) 效能相同
SELECT COUNT(*) FROM sales;  -- 標準寫法
SELECT COUNT(1) FROM sales;  -- 某些資料庫偏好此寫法
-- 兩者在 SQLite 中無效能差異

-- COUNT 與 NULL 的互動
SELECT COUNT(column_name) FROM sales;
-- 只計算 column_name 非 NULL 的記錄
```

## SUM：總和

```sql
-- 總銷售金額
SELECT SUM(amount * quantity) AS total_revenue
FROM sales;  -- 364,730

-- 各分類總銷售
SELECT category,
       SUM(quantity) AS total_units,
       SUM(amount * quantity) AS total_revenue
FROM sales
GROUP BY category;

-- 條件加總
SELECT SUM(amount * quantity) AS taipei_revenue
FROM sales
WHERE region = '台北';
```

## AVG：平均值

```sql
-- 平均單價
SELECT AVG(amount) AS avg_unit_price
FROM sales;  -- 約 27,608

-- 各產品平均銷售數量
SELECT product,
       AVG(quantity) AS avg_quantity
FROM sales
GROUP BY product;

-- AVG 會忽略 NULL
SELECT AVG(amount) FROM sales;
-- 等同於 SUM(amount) / COUNT(amount)
-- 而不是 SUM(amount) / COUNT(*)
```

## MAX 與 MIN

```sql
-- 最高與最低單價
SELECT MAX(amount) AS max_price,
       MIN(amount) AS min_price
FROM sales;

-- 各分類最高單價
SELECT category,
       MAX(amount) AS max_price,
       MIN(amount) AS min_price
FROM sales
GROUP BY category;

-- 第一次與最後一次銷售日期
SELECT MIN(sale_date) AS first_sale,
       MAX(sale_date) AS last_sale
FROM sales;
```

## 與 GROUP BY 搭配使用

### 單欄位分組

```sql
SELECT product,
       COUNT(*) AS transactions,
       SUM(quantity) AS units_sold,
       SUM(amount * quantity) AS revenue,
       ROUND(AVG(amount), 0) AS avg_price
FROM sales
GROUP BY product;
```

### 多欄位分組

```sql
SELECT category, region,
       COUNT(*) AS transactions,
       SUM(quantity) AS units_sold,
       SUM(amount * quantity) AS revenue
FROM sales
GROUP BY category, region
ORDER BY category, region;
```

### 使用 HAVING 過濾群組

```sql
SELECT product,
       SUM(quantity) AS total_units,
       SUM(amount * quantity) AS revenue
FROM sales
GROUP BY product
HAVING SUM(amount * quantity) > 50000
ORDER BY revenue DESC;
```

## 進階聚合技巧

### 多層聚合

```sql
-- 各類別/產品/地區的銷售彙總
SELECT category, product, region,
       SUM(amount * quantity) AS revenue
FROM sales
GROUP BY category, product, region;

-- 使用 ROLLUP 產生小計與總計（SQLite 3.39+）
SELECT category, product,
       SUM(amount * quantity) AS revenue
FROM sales
GROUP BY ROLLUP(category, product);
```

### 條件聚合

```sql
-- 各產品的台北與非台北銷售
SELECT product,
       SUM(CASE WHEN region = '台北'
           THEN amount * quantity ELSE 0 END) AS taipei_sales,
       SUM(CASE WHEN region != '台北'
           THEN amount * quantity ELSE 0 END) AS other_sales
FROM sales
GROUP BY product;
```

### 視窗函數（Window Functions）

```sql
-- 排名（SQLite 3.25+）
SELECT product,
       SUM(amount * quantity) AS revenue,
       RANK() OVER (ORDER BY SUM(amount * quantity) DESC) AS rank
FROM sales
GROUP BY product;
```

## 常見錯誤與陷阱

```sql
-- 錯誤：混用聚合與非聚合
SELECT product, SUM(quantity)
FROM sales;
-- 錯誤！product 不在 GROUP BY 中

-- 正確
SELECT product, SUM(quantity)
FROM sales
GROUP BY product;

-- 陷阱：SUM 對 NULL 的處理
-- 如果 quantity 為 NULL，SUM 會忽略它
-- 使用 COALESCE 處理
SELECT SUM(COALESCE(quantity, 0)) FROM sales;

-- 陷阱：AVG 不等於 SUM/COUNT(*)
SELECT AVG(amount),
       SUM(amount) / COUNT(*) AS wrong_avg,
       SUM(amount) / COUNT(amount) AS correct_avg
FROM sales;
-- AVG 只使用非 NULL 值計算分母
```

## 實戰：銷售儀表板查詢

```sql
-- 整體營運指標
SELECT
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT product) AS products_sold,
    SUM(quantity) AS total_units,
    SUM(amount * quantity) AS total_revenue,
    ROUND(AVG(amount * quantity), 0) AS avg_order_value,
    ROUND(SUM(amount * quantity) / SUM(quantity), 0) AS avg_unit_price
FROM sales;

-- 每日銷售趨勢
SELECT sale_date,
       COUNT(*) AS orders,
       SUM(amount * quantity) AS revenue
FROM sales
GROUP BY sale_date
ORDER BY sale_date;

-- 前三大暢銷產品
SELECT product, SUM(quantity) AS total_qty
FROM sales
GROUP BY product
ORDER BY total_qty DESC
LIMIT 3;
```

## 參考資料

- [SQL COUNT、SUM、AVG 聚合函數](https://www.google.com/search?q=SQL+aggregate+functions+COUNT+SUM+AVG+MAX+MIN)
- [SQL GROUP BY 與聚合](https://www.google.com/search?q=SQL+GROUP+BY+aggregate+functions+tutorial)
- [SQL HAVING 子句](https://www.google.com/search?q=SQL+HAVING+clause+with+aggregate)
