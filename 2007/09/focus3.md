# 主題三：關聯式資料庫基礎

## 表格、索引與正規化

關聯式資料庫是現代資訊系統的基石。理解其核心概念，對於設計和最佳化資料庫至關重要。

## 關聯式模型

### 核心概念

```python
"""
關聯式資料庫核心概念
"""

def rdbms_concepts():
    concepts = {
        "資料表 (Table)": "以行列組織的資料集合",
        "列 (Row/Tuple)": "一筆完整的資料記錄",
        "欄位 (Column/Attribute)": "資料的特定屬性",
        "主鍵 (Primary Key)": "唯一識別每一列",
        "外鍵 (Foreign Key)": "建立資料表之間的關聯",
        "索引 (Index)": "加速資料查詢的結構",
        "視圖 (View)": "虛擬的資料表",
    }

    print("關聯式資料庫核心概念：")
    for concept, desc in concepts.items():
        print(f"  {concept}: {desc}")

rdbms_concepts()
```

### ER 圖範例

```markdown
# 電子商務資料庫 ER 圖

Users (使用者)
├── user_id (PK)
├── name
├── email
└── created_at

Orders (訂單)
├── order_id (PK)
├── user_id (FK)
├── order_date
└── total

OrderItems (訂單項目)
├── item_id (PK)
├── order_id (FK)
├── product_id (FK)
├── quantity
└── price

Products (產品)
├── product_id (PK)
├── name
├── description
└── price
```

## 建立資料表

```sql
-- 使用者資料表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 訂單資料表
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    total DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 訂單項目資料表
CREATE TABLE order_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

## 正規化

### 第一正規化 (1NF)

```sql
-- 問題：重複群組
-- 解決：每個欄位只能有單一值

-- 不符合 1NF
CREATE TABLE orders_bad (
    order_id INT,
    product_ids VARCHAR(100)  -- "1,2,3" 多值
);

-- 符合 1NF
CREATE TABLE orders_good (
    order_id INT,
    product_id INT
);
```

### 第二正規化 (2NF)

```sql
-- 問題：部分相依
-- 解決：移除只相依於主鍵一部分的欄位

-- 不符合 2NF（假設 order_id + product_id 是主鍵）
CREATE TABLE order_items_bad (
    order_id INT,
    product_id INT,
    order_date DATE,  -- 只相依於 order_id
    PRIMARY KEY (order_id, product_id)
);

-- 符合 2NF：移除 order_date 到獨立的 orders 表
```

### 第三正規化 (3NF)

```sql
-- 問題：轉移相依
-- 解決：移除不直接相依於主鍵的欄位

-- 不符合 3NF
CREATE TABLE orders_bad (
    order_id INT PRIMARY KEY,
    user_id INT,
    user_city VARCHAR(50)  -- 轉移相依於 user_id
);

-- 符合 3NF：移除 user_city 到獨立的 users 表
```

## 索引

### 索引類型

```sql
-- 單一欄位索引
CREATE INDEX idx_users_email ON users(email);

-- 複合索引（欄位順序很重要）
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- 唯一索引
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- 全文索引（MySQL）
CREATE FULLTEXT INDEX idx_products_name ON products(name);
```

### 索引的代價

```markdown
# 索引的優點
- 大幅加速查詢
- 強制唯一性
- 減少鎖定

# 索引的代價
- 佔用儲存空間
- 降低寫入效能
- 增加維護成本
```

## 資料完整性約束

```sql
-- NOT NULL
CREATE TABLE users (
    name VARCHAR(100) NOT NULL
);

-- UNIQUE
CREATE TABLE users (
    email VARCHAR(255) UNIQUE
);

-- CHECK
CREATE TABLE products (
    price DECIMAL(10,2) CHECK (price >= 0)
);

-- DEFAULT
CREATE TABLE users (
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 結語

掌握關聯式資料庫的基礎概念，是成為優秀資料庫設計師的第一步。透過正規化設計、合理的索引策略和適當的約束，可以建立高效、可靠的資料庫系統。

---

*延伸閱讀：*
- [關聯式資料庫基礎](https://developers.google.com/search/?q=relational+database+fundamentals)
- [資料庫正規化](https://developers.google.com/search/?q=database+normalization)*