# INSERT、UPDATE、DELETE

## 資料操作語言（DML）

INSERT、UPDATE 和 DELETE 是 SQL 中三個最常用的 DML（Data Manipulation Language）指令，分別負責新增、修改和刪除資料。

## INSERT：新增資料

### 基本語法

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

### 各種插入方式

```sql
-- 插入單一記錄
INSERT INTO products (name, price, stock)
VALUES ('iPhone 17', 35900, 50);

-- 插入多筆記錄
INSERT INTO products (name, price, stock)
VALUES ('MacBook Air', 42900, 30),
       ('iPad Pro', 34900, 40),
       ('AirPods', 6990, 100);

-- 插入時使用運算式
INSERT INTO products (name, price, stock)
VALUES ('Apple Watch', 12900 * 1.05, 25);

-- 插入部分欄位（未指定的欄位使用 DEFAULT）
INSERT INTO products (name, price)
VALUES ('Magic Keyboard', 11900);
-- stock 會使用預設值（如果有的話），否則為 NULL
```

### INSERT INTO ... SELECT

從其他表格查詢結果直接插入：

```sql
-- 將所有庫存為 0 的產品移到 archive 表格
INSERT INTO products_archive (name, price, stock, archived_at)
SELECT name, price, stock, CURRENT_TIMESTAMP
FROM products
WHERE stock = 0;
```

### INSERT OR REPLACE / INSERT OR IGNORE

SQLite 提供衝突處理：

```sql
-- 如果主鍵或唯一約束衝突，則取代該記錄
INSERT OR REPLACE INTO products (id, name, price, stock)
VALUES (1, 'iPhone 17 Pro', 45900, 20);

-- 如果衝突則忽略，不報錯
INSERT OR IGNORE INTO products (id, name, price, stock)
VALUES (1, 'iPhone 17 Ultra', 55900, 10);
```

## UPDATE：修改資料

### 基本語法

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

**重要**：務必加上 WHERE 條件，否則會更新所有記錄！

### 範例

```sql
-- 更新特定產品的價格
UPDATE products
SET price = 33900, updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- 批量更新：所有手機類別的產品降價 5%
UPDATE products
SET price = price * 0.95
WHERE category = '手機';

-- 使用 CASE 條件更新
UPDATE products
SET price = CASE
    WHEN category = '手機' THEN price * 0.9
    WHEN category = '筆電' THEN price * 0.95
    ELSE price * 0.98
END;

-- 更新時使用子查詢
UPDATE products
SET stock = (
    SELECT SUM(quantity)
    FROM inventory
    WHERE inventory.product_id = products.id
)
WHERE id = 1;
```

### UPDATE 的注意事項

```sql
-- 錯誤！忘記 WHERE 條件
UPDATE products SET price = 0;  -- 所有產品的價格都變成 0！

-- 安全寫法：先 SELECT 確認
SELECT * FROM products WHERE id = 1;
-- 確認後再 UPDATE
UPDATE products SET price = 33900 WHERE id = 1;

-- 使用交易保護
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- 如果有任何錯誤，執行 ROLLBACK 取消變更
```

## DELETE：刪除資料

### 基本語法

```sql
DELETE FROM table_name
WHERE condition;
```

### 範例

```sql
-- 刪除特定記錄
DELETE FROM products WHERE id = 10;

-- 刪除符合條件的記錄
DELETE FROM products WHERE stock = 0;

-- 刪除所有記錄（保留表格結構）
DELETE FROM products;

-- 使用子查詢決定刪除哪些記錄
DELETE FROM products
WHERE id IN (
    SELECT product_id
    FROM inventory
    WHERE quantity = 0 AND last_checked < '2026-01-01'
);
```

### DELETE vs DROP vs TRUNCATE

| 指令 | 作用 | 保留結構 | 可復原（交易中） |
|------|------|---------|:-------------:|
| `DELETE` | 刪除記錄 | 是 | 是 |
| `DROP TABLE` | 刪除整個表格 | 否 | 部分資料庫 |
| `TRUNCATE` | 刪除所有記錄（更快） | 是 | 否 |

## 實戰：訂單管理系統

```sql
-- 建立範例資料
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders (customer_name, total) VALUES
('王小明', 1500),
('李小華', 2500),
('張小英', 3200);

-- 更新訂單狀態
UPDATE orders
SET status = 'paid'
WHERE id = 1;

-- 取消訂單（更新狀態和總額）
UPDATE orders
SET status = 'cancelled', total = 0
WHERE id = 2 AND status = 'pending';

-- 清除 30 天前的已取消訂單
DELETE FROM orders
WHERE status = 'cancelled'
  AND created_at < DATE('now', '-30 days');
```

## 安全準則

1. **執行 DELETE/UPDATE 前先用 SELECT 確認**
2. **在交易中執行相關操作**：可 ROLLBACK 復原
3. **備份重要資料**：定期執行備份

```sql
-- 安全更新三步驟
-- 步驟 1：備份
CREATE TABLE products_backup AS SELECT * FROM products;

-- 步驟 2：確認要更新的範圍
SELECT id, name, price FROM products WHERE category = '手機';

-- 步驟 3：在交易中執行
BEGIN TRANSACTION;
UPDATE products SET price = price * 0.9 WHERE category = '手機';
-- 檢查結果
SELECT id, name, price FROM products WHERE category = '手機';
-- 如果錯誤
ROLLBACK;
-- 如果正確
COMMIT;
```

## 參考資料

- [SQL INSERT 語法](https://www.google.com/search?q=SQL+INSERT+INTO+syntax)
- [SQL UPDATE 語法](https://www.google.com/search?q=SQL+UPDATE+statement)
- [SQL DELETE 語法](https://www.google.com/search?q=SQL+DELETE+statement)
- [SQLite INSERT 衝突處理](https://www.google.com/search?q=SQLite+INSERT+OR+REPLACE+OR+IGNORE)
