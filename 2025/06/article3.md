# CREATE TABLE 與資料型別

## 建立資料庫的第一步

CREATE TABLE 是 SQL 中最基本的 DDL 指令。一個精心設計的表格結構，是高效能資料庫應用的基礎。

## SQLite 的資料型別

SQLite 使用動態型別系統（Dynamic Typing），與其他資料庫的靜態型別系統不同。

### 五大儲存類別

| 型別 | 說明 | 範例 |
|------|------|------|
| NULL | 空值 | `NULL` |
| INTEGER | 帶號整數（1-8 bytes） | `42`, `-100` |
| REAL | 浮點數（8 bytes IEEE） | `3.14`, `-0.001` |
| TEXT | 文字字串（UTF-8/16） | `'hello'`, `'中文'` |
| BLOB | 二進位資料 | `x'FFD8'` |

### 型別親和性（Type Affinity）

SQLite 的型別親和性決定了當你宣告一個欄位型別時，實際的儲存行為：

```sql
CREATE TABLE example (
    a INTEGER,    -- INTEGER 親和性
    b TEXT,       -- TEXT 親和性
    c REAL,       -- REAL 親和性
    d NUMERIC,    -- NUMERIC 親和性
    e BLOB,       -- BLOB 親和性（無轉換）
    f VARCHAR(10) -- TEXT 親和性（因為包含 CHAR/VARCHAR）
);
```

有趣的是，SQLite 讓你插入任何型別的資料到任何欄位：

```sql
CREATE TABLE flexible (
    value ANY  -- ANY 實際上會變成 NUMERIC 親和性
);

INSERT INTO flexible VALUES (42);
INSERT INTO flexible VALUES ('hello');
INSERT INTO flexible VALUES (3.14);
INSERT INTO flexible VALUES (x'FF');

SELECT value, typeof(value) FROM flexible;
-- 42     | integer
-- hello  | text
-- 3.14   | real
-- □      | blob
```

## 常用約束條件

### PRIMARY KEY

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
```

**重點**：在 SQLite 中，`INTEGER PRIMARY KEY` 會自動成為 `rowid` 的別名，自增行為最佳化。

### NOT NULL 與 DEFAULT

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL DEFAULT 0.0,
    stock INTEGER NOT NULL DEFAULT 0,
    description TEXT DEFAULT '無描述'
);
```

### UNIQUE

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL
);
```

### CHECK

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER CHECK(age >= 18 AND age <= 120),
    salary REAL CHECK(salary > 0),
    department TEXT CHECK(department IN ('工程', '業務', '財務', '人事'))
);
```

### FOREIGN KEY

SQLite 預設不啟用外鍵約束，需要手動開啟：

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
```

`ON DELETE CASCADE` 表示當作者被刪除時，該作者的所有書籍也會被自動刪除。

## 實戰：電商資料庫 Schema

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL CHECK(price >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
    category_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
    total REAL NOT NULL CHECK(total >= 0),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## 修改表格結構

```sql
-- 新增欄位
ALTER TABLE products ADD COLUMN brand TEXT DEFAULT '';

-- 重新命名表格
ALTER TABLE products RENAME TO old_products;

-- 注意：SQLite 不支援 DROP COLUMN（需重建）
-- 修改欄位需要重建表格
CREATE TABLE products_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO products_new SELECT id, name, price FROM products;
DROP TABLE products;
ALTER TABLE products_new RENAME TO products;
```

## 實用建議

1. **總是使用 INTEGER PRIMARY KEY AUTOINCREMENT**：不要信任自然鍵
2. **明確宣告 NOT NULL**：避免意外插入 NULL 值
3. **使用 CHECK 約束驗證資料**：在資料庫層級確保資料品質
4. **啟用外鍵（PRAGMA foreign_keys = ON）**：維護資料完整性
5. **不要在 SQLite 中使用過長的 VARCHAR**：TEXT 沒有效能差異

## 參考資料

- [SQLite CREATE TABLE 文檔](https://www.google.com/search?q=SQLite+CREATE+TABLE+documentation)
- [SQLite 資料型別](https://www.google.com/search?q=SQLite+data+types+affinity)
- [SQL 約束條件](https://www.google.com/search?q=SQL+constraints+PRIMARY+KEY+FOREIGN+KEY)
