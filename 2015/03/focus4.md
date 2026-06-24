# MySQL 與 MariaDB：架構、儲存引擎、複製

## 前言

MySQL 是世界上最流行的開源資料庫，MariaDB 是其社群分支。兩者都有廣泛的使用者群體。

## MySQL 架構

```
MySQL 架構：
───────────────────────────────

┌─────────────────────────────────────┐
│           客戶端連線                │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         連線池 / 執行緒池             │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         SQL 介面 / 剖析器             │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         查詢快取 / 最佳化器           │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         儲存引擎層                   │
│  ┌─────────┬─────────┬──────────┐   │
│  │ InnoDB  │ MyISAM  │ Memory   │   │
│  └─────────┴─────────┴──────────┘   │
└─────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────┐
│           檔案系統                   │
└─────────────────────────────────────┘
```

## 儲存引擎

### InnoDB（預設）

```sql
-- 建立 InnoDB 表格（預設）
CREATE TABLE users_innodb (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
) ENGINE=InnoDB;

-- 特色
-- - 支援交易（ACID）
-- - 支援外鍵
-- - 支援資料列鎖定
-- - 支援 MVCC
-- - 自動崩潰復原
-- - 叢集索引
```

### MyISAM

```sql
-- 建立 MyISAM 表格
CREATE TABLE users_myisam (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
) ENGINE=MyISAM;

-- 特色
-- - 不支援交易
-- - 不支援外鍵
-- - 支援全文搜尋
-- - 較小的儲存空間
-- - 較快的讀取速度
```

### MEMORY

```sql
-- 建立記憶體表格
CREATE TABLE cache_table (
    key_col VARCHAR(50) PRIMARY KEY,
    value_col TEXT
) ENGINE=MEMORY;

-- 特色
-- - 資料存在記憶體中
-- - 極快的存取速度
-- - 系統當機資料流失
-- - 適合做為快取
```

## InnoDB 特性

### 交易支援

```sql
START TRANSACTION;

INSERT INTO accounts (user_id, balance) VALUES (1, 1000);
UPDATE accounts SET balance = balance - 500 WHERE user_id = 1;
UPDATE accounts SET balance = balance + 500 WHERE user_id = 2;

COMMIT;
-- 或 ROLLBACK;
```

### 外鍵約束

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

### 鎖定與並發

```sql
-- 讀取不阻塞讀取
SET SESSION tx_isolation = 'READ-COMMITTED';

-- 明確鎖定資料列
SELECT * FROM users WHERE id = 1 FOR UPDATE;

-- 鎖定讀取（不加鎖）
SELECT * FROM users WHERE id = 1 LOCK IN SHARE MODE;
```

## MariaDB 特有功能

### 分割（Partitions）

```sql
-- RANGE 分割
CREATE TABLE sales (
    id INT,
    sale_date DATE,
    amount DECIMAL(10, 2)
)
PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2014 VALUES LESS THAN (2015),
    PARTITION p2015 VALUES LESS THAN (2016),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);

-- 查詢分割
SELECT * FROM sales WHERE sale_date BETWEEN '2015-01-01' AND '2015-12-31';
```

### 序列（Sequences）

```sql
-- MariaDB 序列
SELECT SEQ_USER_ID.NEXTVAL;
SELECT SEQ_USER_ID.CURRVAL;

-- 建立序列
CREATE SEQUENCE seq_user_id START WITH 1 INCREMENT BY 1;
```

### 虛擬欄位

```sql
CREATE TABLE products (
    price DECIMAL(10, 2),
    quantity INT,
    total DECIMAL(10, 2) GENERATED ALWAYS AS (price * quantity) STORED
);
```

## 複製（Replication）

### 主從複製

```sql
-- 主庫設定（my.cnf）
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-do-db = myapp

-- 從庫設定
CHANGE MASTER TO
    MASTER_HOST = 'master-host',
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'password',
    MASTER_LOG_FILE = 'mysql-bin.000001',
    MASTER_LOG_POS = 123;

START SLAVE;
```

```
主從複製架構：
─────────────────

┌─────────┐         複製          ┌─────────┐
│ Master  │ ─────────────────────►│ Slave 1 │
│ (寫入)  │                        │ (讀取)  │
└─────────┘                        └─────────┘
     │                                  │
     │ 複製                              │ 讀取
     ▼                                  ▼
┌─────────┐                        ┌─────────┐
│ 客戶端  │                        │ 客戶端   │
└─────────┘                        └─────────┘
```

### GTID 複製（MySQL 5.6+）

```sql
-- 啟用 GTID
[mysqld]
gtid_mode = ON
enforce_gtid_consistency = ON

-- 自動定位
CHANGE MASTER TO
    MASTER_AUTO_POSITION = 1;
```

## 效能優化

### 查詢優化

```sql
-- 使用 EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 分析表格
ANALYZE TABLE users;
CHECK TABLE users;

-- 優化表格
OPTIMIZE TABLE users;
```

### 索引優化

```sql
-- 建立索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- 複合索引順序
-- 考慮性：等於 > 範圍 > 多欄位

-- 前綴索引
CREATE INDEX idx_users_name ON users(name(10));
```

### 設定優化（my.cnf）

```ini
[mysqld]
# 緩衝區大小
innodb_buffer_pool_size = 4G
key_buffer_size = 256M

# 連線數
max_connections = 500

# 查詢快取（MySQL 5.7 已棄用）
# query_cache_size = 128M

# 日誌
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
```

## 結論

MySQL 和 MariaDB 是成熟且廣泛使用的資料庫。InnoDB 提供了交易支援和外鍵約束，而多元的儲存引擎讓你可以根據需求選擇最適合的方案。

---

## 延伸閱讀

- [MySQL 官方文檔](https://www.google.com/search?q=MySQL+documentation)
- [MariaDB vs MySQL](https://www.google.com/search?q=MariaDB+vs+MySQL+comparison)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」歷史回顧系列之一。*