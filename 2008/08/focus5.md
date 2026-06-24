# 資料庫查詢優化

## 索引

### 建立索引

```sql
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_order_date ON orders(created_at);
CREATE INDEX idx_order_user ON orders(user_id, created_at);
```

### 複合索引

```sql
-- 複合索引順序很重要
CREATE INDEX idx_user_status ON users(status, created_at);

-- 查詢時要考慮索引順序
SELECT * FROM users WHERE status = 'active';  -- 使用索引
SELECT * FROM users WHERE created_at > '2020-01-01';  -- 不使用索引
```

## 查詢分析

### EXPLAIN

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

### 慢查詢日誌

```python
# MySQL 慢查詢配置
slow_query_log = 1
slow_query_log_file = '/var/log/mysql/slow.log'
long_query_time = 2
```

## 連接池

### Python 範例

```python
import MySQLdb.pool

pool = MySQLdb.pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host='localhost',
    user='root',
    password='',
    database='mydb'
)

# 使用連接
conn = pool.connection()
cursor = conn.cursor()
cursor.execute('SELECT * FROM users')
conn.close()
```

## 快取

### 查詢快取

```sql
-- MySQL 查詢快取
SET GLOBAL query_cache_type = 1;
SET GLOBAL query_cache_size = 67108864;  -- 64MB
```

## 結論

資料庫效能優化需要綜合考慮索引、查詢分析和連接管理。

---

**延伸閱讀**

- [Database+query+optimization](https://www.google.com/search?q=database+query+optimization)