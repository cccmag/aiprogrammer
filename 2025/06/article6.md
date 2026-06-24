# ORDER BY 與 LIMIT

## 排序與分頁

ORDER BY 和 LIMIT 是 SQL 查詢中不可或缺的功能。ORDER BY 控制資料的排列順序，LIMIT 控制返回的資料量。兩者結合使用可以實作十分有用的分頁查詢。

## ORDER BY：排序

### 基本語法

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...;
```

- `ASC`：升序（Ascending），小到大，為預設值
- `DESC`：降序（Descending），大到小

### 建立範例資料

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    rating REAL DEFAULT 0
);

INSERT INTO products VALUES
(1, 'iPhone 17', '手機', 35900, 50, 4.8),
(2, 'MacBook Air', '筆電', 42900, 30, 4.6),
(3, 'iPad Pro', '平板', 34900, 40, 4.7),
(4, 'AirPods Pro', '耳機', 7990, 100, 4.5),
(5, 'Apple Watch', '穿戴', 14900, 25, 4.3),
(6, 'Mac Mini', '桌機', 18900, 15, 4.4),
(7, 'iPhone 16', '手機', 29900, 60, 4.6),
(8, 'iPad Air', '平板', 21900, 35, 4.5);
```

### 基本排序

```sql
-- 價格由高到低
SELECT name, price FROM products
ORDER BY price DESC;

-- 價格由低到高（預設 ASC）
SELECT name, price FROM products
ORDER BY price;
-- 等同於 ORDER BY price ASC

-- 字母順序
SELECT name FROM products
ORDER BY name;
```

### 多欄位排序

```sql
-- 先依類別排序，同類別內依價格降序
SELECT name, category, price
FROM products
ORDER BY category, price DESC;

-- 效果：
-- iPad Air    │ 平板 │ 21900
-- iPad Pro    │ 平板 │ 34900
-- iPhone 16   │ 手機 │ 29900
-- iPhone 17   │ 手機 │ 35900
-- MacBook Air │ 筆電 │ 42900

-- 混合升降序
SELECT name, category, price, stock
FROM products
ORDER BY category ASC, price DESC, stock ASC;
```

### 進階排序技巧

```sql
-- 使用運算式排序
SELECT name, price, stock, price * stock AS total_value
FROM products
ORDER BY total_value DESC;

-- 使用 CASE 自訂排序規則
SELECT name, category, price
FROM products
ORDER BY
  CASE category
    WHEN '手機' THEN 1
    WHEN '平板' THEN 2
    WHEN '筆電' THEN 3
    ELSE 4
  END;

-- 使用欄位位置（不建議，可讀性差）
SELECT name, price FROM products
ORDER BY 2 DESC;  -- 依第二個欄位（price）排序

-- NULL 值的排序（SQLite 中 NULL 在升序時排最前）
CREATE TABLE test_nulls (x INTEGER);
INSERT INTO test_nulls VALUES (3), (NULL), (1), (NULL), (2);
SELECT * FROM test_nulls ORDER BY x;
-- NULL, NULL, 1, 2, 3
```

## LIMIT 與 OFFSET：限制結果

### 基本語法

```sql
SELECT column_list
FROM table_name
LIMIT row_count OFFSET offset;
```

### 範例

```sql
-- 只取前 3 筆
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 3;

-- 跳過前 3 筆，取接下來 2 筆
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 2 OFFSET 3;
-- 等同於 LIMIT 3, 2（SQLite 支援）

-- 不同的 LIMIT 語法
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 2, 3;  -- LIMIT <offset>, <count>
```

### 分頁查詢實作

```python
def get_page(page=1, per_page=10):
    offset = (page - 1) * per_page
    query = f"""
        SELECT id, name, price
        FROM products
        ORDER BY id
        LIMIT {per_page} OFFSET {offset}
    """
    return execute_query(query)

# 第 1 頁：LIMIT 10 OFFSET 0  （id 1-10）
# 第 2 頁：LIMIT 10 OFFSET 10 （id 11-20）
# 第 3 頁：LIMIT 10 OFFSET 20 （id 21-30）
```

### 分頁計算

```python
def paginate(query, page=1, per_page=10):
    # 計算總筆數
    count_query = f"SELECT COUNT(*) FROM ({query})"
    total = execute_scalar(count_query)

    # 計算分頁資訊
    total_pages = (total + per_page - 1) // per_page
    offset = (page - 1) * per_page

    # 取得當前頁資料
    data_query = f"{query} LIMIT {per_page} OFFSET {offset}"

    return {
        "data": execute_query(data_query),
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
```

## 實戰組合

```sql
-- 價格最高的 3 個產品
SELECT name, category, price
FROM products
ORDER BY price DESC
LIMIT 3;

-- 每個類別中價格最高的產品
SELECT category, name, price
FROM products
WHERE id IN (
    SELECT id FROM products
    GROUP BY category
    HAVING price = MAX(price)
)
ORDER BY price DESC;

-- 庫存價值最高的前 5 名
SELECT name, stock, price,
       stock * price AS value
FROM products
ORDER BY value DESC
LIMIT 5;

-- 評分最高且庫存充足的產品
SELECT name, rating, stock
FROM products
WHERE stock > 20
ORDER BY rating DESC
LIMIT 5;

-- 隨機選取 3 個產品
SELECT name FROM products
ORDER BY RANDOM()
LIMIT 3;
```

## 注意事項

1. **ORDER BY 的效能**：對大表格排序很昂貴，確保排序欄位有索引
2. **LIMIT 的執行時機**：LIMIT 在 ORDER BY 之後執行，所以排序仍會掃描所有記錄
3. **OFFSET 的效率**：OFTSET 越大效率越差，因為資料庫仍需掃描跳過的記錄
4. **無 ORDER BY 的 LIMIT**：結果不確定，可能每次查詢不同

```sql
-- 不建議：結果不可預期
SELECT * FROM products LIMIT 5;

-- 建議：加上明確的排序
SELECT * FROM products ORDER BY id LIMIT 5;
```

## 參考資料

- [SQL ORDER BY 排序教學](https://www.google.com/search?q=SQL+ORDER+BY+clause+sorting)
- [SQL LIMIT 分頁查詢](https://www.google.com/search?q=SQL+LIMIT+OFFSET+pagination)
- [SQLite SELECT 語法](https://www.google.com/search?q=SQLite+SELECT+ORDER+BY+LIMIT)
