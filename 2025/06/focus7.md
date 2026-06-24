# 資料庫正規化與設計

## 為什麼需要正規化？

正規化（Normalization）是一組用於設計資料庫表格的指導原則，目的是：

1. **減少資料重複**：避免同一個資料在多個地方儲存
2. **避免更新異常**：修改一筆資料時，不需要修改多個地方
3. **避免插入異常**：新增資料時，不需要先有不相關的資料
4. **避免刪除異常**：刪除資料時，不會意外刪除其他相關資料

### 未正規化的範例

```sql
CREATE TABLE orders_bad (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    product1 TEXT,
    product1_price REAL,
    product2 TEXT,
    product2_price REAL
    -- 問題：欄位數量固定，無法彈性擴充
);
```

## 第一正規化（1NF）

**定義**：每個欄位都只能包含一個值（atomic value），不可包含重複的群組。

### 違反 1NF 的表格

```
order_id │ customer │ products
1        │ 王小明   │ iPhone 17, MacBook Air
2        │ 李小華   │ iPad Pro
```

`products` 欄位包含多個值，違反 1NF。

### 修正為 1NF

```
order_id │ customer │ product
1        │ 王小明   │ iPhone 17
1        │ 王小明   │ MacBook Air
2        │ 李小華   │ iPad Pro
```

```sql
CREATE TABLE orders_1nf (
    order_id INTEGER,
    customer TEXT NOT NULL,
    product TEXT NOT NULL,
    PRIMARY KEY (order_id, product)
);
```

## 第二正規化（2NF）

**定義**：滿足 1NF，且所有非主鍵欄位都**完全依賴於主鍵**（而非部分主鍵）。

### 違反 2NF 的表格

假設主鍵是 `(order_id, product)`：

```
order_id │ product    │ customer  │ customer_email │ price
1        │ iPhone 17  │ 王小明    │ wang@test.com  │ 35900
1        │ MacBook Air│ 王小明    │ wang@test.com  │ 42900
2        │ iPad Pro   │ 李小華    │ lee@test.com   │ 34900
```

`customer` 和 `customer_email` 只依賴於 `order_id`（部分主鍵），而非整個主鍵。

### 修正為 2NF

```sql
-- 訂單表格
CREATE TABLE orders_2nf (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE
);

-- 訂單明細表格
CREATE TABLE order_items_2nf (
    order_id INTEGER,
    product TEXT,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY (order_id, product),
    FOREIGN KEY (order_id) REFERENCES orders_2nf(order_id)
);

-- 客戶表格
CREATE TABLE customers_2nf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);
```

## 第三正規化（3NF）

**定義**：滿足 2NF，且所有非主鍵欄位**不傳遞依賴**於主鍵。

### 違反 3NF 的表格

```
product_id │ product_name │ category_id │ category_name
1          │ iPhone 17    │ 1           │ 手機
2          │ MacBook Air  │ 2           │ 筆電
3          │ iPad Pro     │ 1           │ 手機
```

`category_name` 依賴於 `category_id`，而 `category_id` 依賴於 `product_id`——這是傳遞依賴。

### 修正為 3NF

```sql
CREATE TABLE products_3nf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories_3nf(id)
);

CREATE TABLE categories_3nf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
```

## BCNF（Boyce-Codd Normal Form）

BCNF 是 3NF 的強化版本。**定義**：對於所有函數依賴 X → Y，X 必須是候選鍵（superkey）。

在大多數實際案例中，滿足 3NF 就等同於滿足 BCNF。BCNF 主要處理一些 3NF 無法處理的特殊情況。

## 反正規化

有時候為了查詢效能，我們會故意違反正規化原則，這就是反正規化（Denormalization）。

```sql
-- 反正規化範例：在訂單中直接儲存客戶名稱（避免頻繁 JOIN）
CREATE TABLE orders_denormalized (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,  -- 反正規化！
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE
);
```

### 何時使用反正規化

| 優點 | 缺點 |
|------|------|
| 查詢速度快（減少 JOIN） | 資料重複 |
| 實作簡單 | 更新需維護多處 |
| 適合大量讀取場景 | 佔用更多儲存空間 |

## 實務設計步驟

### 1. 需求分析

了解業務需求，識別實體（Entity）和關係（Relationship）。

```
範例：圖書館系統
實體：書籍、作者、讀者、借閱記錄
關係：書籍由作者撰寫（多對一）
      讀者借閱書籍（多對多，借閱記錄為中間表）
```

### 2. 概念設計

繪製 Entity-Relationship Diagram（ERD）。

```
[作者]──1:N──[書籍]──N:M──[讀者]
                    │
                    └── 借閱記錄（中間表）
```

### 3. 邏輯設計

將 ERD 轉換為表格定義，進行正規化。

```sql
CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_year INTEGER
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    isbn TEXT UNIQUE,
    published_year INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE readers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    reader_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (reader_id) REFERENCES readers(id)
);
```

### 4. 效能最佳化

根據查詢模式加入索引（Index）：

```sql
CREATE INDEX idx_loans_due ON loans(due_date);
CREATE INDEX idx_books_author ON books(author_id);
```

## 設計原則總結

1. **每個表格代表一個實體**：不要在同一個表格中混合不同型別的資料
2. **每個記錄有唯一標識**：使用 PRIMARY KEY
3. **使用外鍵建立關聯**：不要在同一欄位中儲存多個 ID
4. **適度正規化**：通常 3NF 是好的平衡點
5. **為效能索引**：為常用查詢的欄位建立索引
6. **必要時反正規化**：但要有意識地做，並維護資料一致性

## 參考資料

- [資料庫正規化教學](https://www.google.com/search?q=database+normalization+1NF+2NF+3NF+tutorial)
- [BCNF 正規化](https://www.google.com/search?q=BCNF+Boyce+Codd+normal+form)
- [資料庫設計最佳實務](https://www.google.com/search?q=database+design+best+practices)
- [ERD 實體關係圖](https://www.google.com/search?q=Entity+Relationship+Diagram+tutorial)
