# 資料庫設計原則：正規化、索引、視圖

## 前言

良好的資料庫設計是效能和可維護性的基礎。本篇介紹正規化理論、索引設計和進階資料庫物件。

## 正規化理論

### 為什麼需要正規化？

```
正規化目的：
───────────
1. 消除資料冗余
2. 確保資料完整性
3. 簡化資料更新
4. 提供一致的資料結構
```

### 第一正規化（1NF）

```
要求：每個欄位都是不可分割的原子值
```

```sql
-- 違反 1NF（電話有多個值）
┌────┬────────────────────┐
│ id │      phones        │
├────┼────────────────────┤
│ 1  │ 0912-345-678       │
│ 2  │ 0987-654-321, 0900 │
└────┴────────────────────┘

-- 符合 1NF（拆分為多列）
┌────┬───────────────┐
│ id │     phone     │
├────┼───────────────┤
│ 1  │ 0912-345-678  │
│ 2  │ 0987-654-321  │
│ 2  │ 0900-111-222  │
└────┴───────────────┘
```

### 第二正規化（2NF）

```
要求：符合 1NF，且非主鍵欄位完全依賴主鍵（無部分依賴）
```

```sql
-- 違反 2NF（課程名稱依賴課程 ID，不完全依賴主鍵）
┌──────────┬───────────┬────────────┐
│ 學生ID   │ 課程ID    │ 課程名稱    │
├──────────┼───────────┼────────────┤
│ 1        │ CS101     │ 資料庫      │
│ 2        │ CS101     │ 資料庫      │  ← 課程名稱重複
└──────────┴───────────┴────────────┘

-- 拆分為兩個表格
┌────────┬────────┐      ┌─────────┬──────────┐
│ 學生ID │ 課程ID │      │ 課程ID  │ 課程名稱 │
├────────┼────────┘      ├─────────┼──────────┤
│ 1      │ CS101         │ CS101   │ 資料庫    │
│ 2      │ CS101         │ MATH101 │ 數學      │
└────────┴───────────┘      └─────────┴──────────┘
```

### 第三正規化（3NF）

```
要求：符合 2NF，且非鍵欄位之間沒有傳遞依賴
```

```sql
-- 違反 3NF（城市依賴郵遞區號，傳遞依賴學生）
┌────┬────┬───────────┬──────────┐
│ ID │姓名│ 郵遞區號  │ 城市      │
├────┼────┼───────────┼──────────┤
│ 1  │王小│ 100       │ 台北市    │
│ 2  │李小│ 100       │ 台北市    │  ← 城市重複
└────┴────┴───────────┴──────────┘

-- 拆分為兩個表格
┌────┬────┬───────────┐      ┌───────────┬──────────┐
│ ID │姓名│ 郵遞區號  │      │ 郵遞區號  │ 城市      │
├────┼────┼───────────┘      ├───────────┼──────────┤
│ 1  │王小│ 100              │ 100       │ 台北市    │
│ 2  │李小│ 100              │ 200       │ 台中市    │
└────┴────┴──────────────┘      └───────────┴──────────┘
```

### 正規化 vs 反正規化

```
正規化優點：               正規化缺點：
─────────────              ─────────────
✓ 資料一致性              ✗ 查詢需要 JOIN
✓ 減少冗余                ✗ 效能損耗
✓ 更新簡單                ✗ 複雜查詢

何時可考慮反正規化：
- 讀取遠多於寫入
- 效能瓶頸在 JOIN
- 資料量大且查詢固定
```

## 索引設計

### 何時建立索引

```sql
-- 適合建立索引：
-- 1. WHERE 子句常使用的欄位
-- 2. JOIN 條件中的欄位
-- 3. ORDER BY / GROUP BY 中的欄位
-- 4. 唯一性約束的欄位

-- 不適合建立索引：
-- - 很少使用的欄位
-- - 很少返回少量資料的欄位
-- - 大量 NULL 值的欄位
-- - 頻繁更新的欄位
```

### 複合索引順序

```sql
-- 原則：選擇性高的欄位放前面
-- 但也要考慮查詢模式

-- 查詢：WHERE status = 'active' AND created_at > '2020-01-01'
-- 複合索引：(status, created_at)

-- 複合索引
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- 最左前綴原則
-- 以下查詢可以使用索引：
SELECT * FROM orders WHERE status = 'active';
SELECT * FROM orders WHERE status = 'active' AND created_at > '2020-01-01';

-- 以下查詢無法使用索引：
SELECT * FROM orders WHERE created_at > '2020-01-01';
```

### 索引維護

```sql
-- PostgreSQL
REINDEX INDEX idx_users_email;
VACUUM ANALYZE users;

-- MySQL
OPTIMIZE TABLE users;

-- 查看索引使用
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

## 視圖（Views）

### 基本視圖

```sql
-- 建立視圖
CREATE VIEW active_users AS
SELECT
    id,
    name,
    email,
    created_at
FROM users
WHERE created_at > datetime('now', '-30 days');

-- 使用視圖
SELECT * FROM active_users;
```

### 複雜視圖

```sql
CREATE VIEW order_summary AS
SELECT
    u.id AS user_id,
    u.name AS user_name,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(o.total), 0) AS total_spent,
    MAX(o.created_at) AS last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- 使用
SELECT * FROM order_summary WHERE total_spent > 10000;
```

### 可更新視圖

```sql
-- 簡單視圖可更新
CREATE VIEW simple_users AS
SELECT id, name, email FROM users;

INSERT INTO simple_users (name, email) VALUES ('王小明', 'wang@example.com');

-- 複雜視圖需要 INSTEAD OF 觸發器
CREATE VIEW user_orders AS
SELECT u.id, u.name, o.id AS order_id, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

CREATE TRIGGER user_orders_insert
INSTEAD OF INSERT ON user_orders
FOR EACH ROW
BEGIN
    INSERT INTO users (name) VALUES (NEW.name);
END;
```

## 預存程序（Stored Procedures）

### PostgreSQL

```sql
-- 函式
CREATE OR REPLACE FUNCTION get_user_stats(user_id INTEGER)
RETURNS TABLE (
    user_name TEXT,
    order_count BIGINT,
    total_spent NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        u.name,
        COUNT(o.id)::BIGINT,
        COALESCE(SUM(o.total), 0)
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.id = user_id
    GROUP BY u.name;
END;
$$ LANGUAGE plpgsql;

-- 呼叫
SELECT * FROM get_user_stats(1);
```

### MySQL

```sql
-- 預存程序
DELIMITER //

CREATE PROCEDURE get_user_orders(IN user_id INT)
BEGIN
    SELECT * FROM orders WHERE user_id = user_id;
END //

DELIMITER ;

-- 呼叫
CALL get_user_orders(1);

-- 條件判斷
CREATE PROCEDURE process_order(IN order_id INT)
BEGIN
    DECLARE order_total DECIMAL(10, 2);

    SELECT total INTO order_total FROM orders WHERE id = order_id;

    IF order_total > 1000 THEN
        UPDATE orders SET status = 'VIP' WHERE id = order_id;
    ELSE
        UPDATE orders SET status = 'NORMAL' WHERE id = order_id;
    END IF;
END //
```

## 觸發程序（Triggers）

### 基本語法

```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION log_user_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_logs (action, old_data, new_data, changed_at)
    VALUES (TG_OP, OLD, NEW, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_change_trigger
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_change();

-- MySQL
CREATE TRIGGER update_timestamp
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = NOW() WHERE id = NEW.id;
END;
```

## 結論

良好的資料庫設計需要平衡正規化和效能需求。適當使用索引可以大幅提升查詢效能，而視圖和預存程序則有助於封裝複雜邏輯和提升安全性。

---

## 延伸閱讀

- [資料庫正規化教學](https://www.google.com/search?q=database+normalization+tutorial)
- [SQL 索引設計](https://www.google.com/search?q=SQL+index+design+best+practices)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」歷史回顧系列之一。*