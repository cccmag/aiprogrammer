# 關聯式資料庫基礎：表格、鍵值、關聯

## 前言

關聯式資料庫以表格（Table）為核心，用來表示資料以及資料之間的關係。

## 表格結構

### 基本概念

```sql
-- 建立 users 表格
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```
users 表格結構：
─────────────────

+----+--------+------------------------+------+---------------------+
│ id │  name  │         email          │ age  │    created_at       │
+----+--------+------------------------+------+---------------------+
│ 1  │ 王小明 │ wang@example.com       │ 25   │ 2015-03-01 10:00:00 │
│ 2  │ 李小華 │ lee@example.com        │ 30   │ 2015-03-02 14:30:00 │
+----+--------+------------------------+------+---------------------+
```

### 資料類型

```sql
-- 數值類型
INTEGER, BIGINT, SMALLINT
DECIMAL(p, s), NUMERIC(p, s)
REAL, DOUBLE PRECISION
BOOLEAN

-- 字串類型
CHAR(n), VARCHAR(n)
TEXT

-- 日期時間
DATE, TIME, TIMESTAMP
INTERVAL

-- 其他
UUID, JSON, XML
```

## 主鍵（Primary Key）

### 單一主鍵

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

-- 或明確命名
CREATE TABLE users (
    id INTEGER,
    name VARCHAR(100),
    PRIMARY KEY (id)
);
```

### 複合主鍵

```sql
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

### 自動遞增

```sql
-- PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- MySQL
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- SQLite
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100)
);
```

## 外鍵（Foreign Key）

### 基本語法

```sql
-- 建立 orders 表格，參考 users
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 完整定義

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

### 參考動作

```sql
-- ON DELETE / ON UPDATE 動作：
-- CASCADE：連動刪除/更新
-- SET NULL：設為 NULL
-- SET DEFAULT：設為預設值
-- RESTRICT：阻止刪除/更新
-- NO ACTION：不進行任何動作
```

## 關聯類型

### 一對一（One-to-One）

```sql
-- 使用者與護照資訊
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE passports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    passport_number VARCHAR(20),
    issue_date DATE
);
```

### 一對多（One-to-Many）

```sql
-- 使用者與訂單
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2)
);
```

### 多對多（Many-to-Many）

```sql
-- 學生與課程（需要關聯表）
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- 關聯表
CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id)
);
```

## 實體關係圖（ER Diagram）

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │       │     orders      │       │   order_items   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ *id             │───┐   │ *id             │───┐   │ *order_id       │
│   name          │   │   │   user_id (FK)  │   │   │ *product_id     │
│   email         │   └──►│   total         │   └──►│   quantity      │
│   created_at    │       │   created_at    │       │   price         │
└─────────────────┘       └─────────────────┘       └─────────────────┘
                                                          │
                                                          │
                                                   ┌───────▼───────┐
                                                   │   products    │
                                                   ├───────────────┤
                                                   │ *id           │
                                                   │   name        │
                                                   │   price       │
                                                   └───────────────┘
```

## 索引（Index）

### 建立索引

```sql
-- 單一欄位索引
CREATE INDEX idx_users_email ON users(email);

-- 複合索引
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- 唯一索引
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- 移除索引
DROP INDEX idx_users_email;
```

### 索引類型

```sql
-- B-tree 索引（預設）
CREATE INDEX idx_users_name ON users(name);

-- Hash 索引（僅 PostgreSQL）
CREATE INDEX idx_users_name_hash ON users USING HASH(name);

-- GiST 索引（地理空間搜尋）
CREATE INDEX idx_locations ON locations USING GIST(geom);

-- GIN 索引（JSON/全文搜尋）
CREATE INDEX idx_products_data ON products USING GIN(data);
```

## 結語

關聯式資料庫以表格、鍵值和關聯為基礎，提供了強大而一致的資料建模能力。理解這些基本概念，是學習 SQL 和資料庫設計的起點。

---

## 延伸閱讀

- [關聯式資料庫設計](https://www.google.com/search?q=relational+database+design+primary+foreign+key)
- [SQL 基礎教學](https://www.google.com/search?q=SQL+basics+tutorial)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」歷史回顧系列之一。*