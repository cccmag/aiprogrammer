# 主題一：MySQL 5.0 到 5.1

## 開源資料庫的進化

MySQL 是世界上最流行的開源關聯式資料庫，從 5.0 到 5.1 的演化，展現了開源資料庫持續進化的決心。

## MySQL 5.0 的重要功能

### 預存程序

```sql
-- MySQL 5.0 預存程序
DELIMITER //

CREATE PROCEDURE get_user_orders(IN user_id INT)
BEGIN
    SELECT orders.*, products.name, products.price
    FROM orders
    JOIN products ON orders.product_id = products.id
    WHERE orders.user_id = user_id;
END //

DELIMITER ;

-- 呼叫預存程序
CALL get_user_orders(1);
```

### 觸發器

```sql
-- 建立觸發器
CREATE TRIGGER after_insert_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE products
    SET stock = stock - NEW.quantity
    WHERE id = NEW.product_id;
END//
```

### 視圖

```sql
-- 建立視圖
CREATE VIEW user_orders_view AS
SELECT
    u.name AS user_name,
    o.order_date,
    o.total,
    p.name AS product_name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id;
```

## MySQL 5.1 的新功能

### 表格劃分 (Table Partitioning)

```sql
-- RANGE 劃分
CREATE TABLE sales (
    id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2006 VALUES LESS THAN (2007),
    PARTITION p2007 VALUES LESS THAN (2008),
    PARTITION p2008 VALUES LESS THAN (2009),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);

-- LIST 劃分
CREATE TABLE customers (
    id INT,
    region VARCHAR(50),
    name VARCHAR(100)
)
PARTITION BY LIST (region) (
    PARTITION north VALUES IN ('NY', 'MA', 'CT'),
    PARTITION south VALUES IN ('FL', 'GA', 'TX'),
    PARTITION west VALUES IN ('CA', 'OR', 'WA')
);

-- HASH 劃分
CREATE TABLE logs (
    id INT,
    log_date DATE,
    message TEXT
)
PARTITION BY HASH (id)
PARTITIONS 4;
```

### 事件排程器

```sql
-- 啟用事件排程器
SET GLOBAL event_scheduler = ON;

-- 建立事件
CREATE EVENT daily_cleanup
ON SCHEDULE EVERY 1 DAY
DO
    DELETE FROM logs
    WHERE log_date < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- 檢視事件
SHOW EVENTS;
SELECT * FROM mysql.event;
```

### 視圖增強

```sql
-- 可更新的視圖
CREATE OR REPLACE VIEW active_users AS
SELECT id, name, email
FROM users
WHERE status = 'active';

-- 透過視圖更新
UPDATE active_users SET email = 'new@example.com' WHERE id = 1;
```

## MySQL 5.1 的效能改進

### 查询缓存增强

```ini
# my.cnf 設定
query_cache_type = 1
query_cache_size = 64M
query_cache_limit = 2M
```

### InnoDB 改進

```ini
# InnoDB 效能調校
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
innodb_thread_concurrency = 8
```

## 結語

MySQL 5.0 到 5.1 的進化，展現了開源資料庫持續改進和功能豐富的努力。劃分表和事件排程器等功能，使 MySQL 更適合企業級應用。

---

*延伸閱讀：*
- [MySQL 官方網站](https://developers.google.com/search/?q=mysql+official)
- [MySQL 5.1 文件](https://developers.google.com/search/?q=mysql+5.1+documentation)*