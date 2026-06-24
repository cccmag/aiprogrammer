# 資料庫讀寫分離

## 實戰搭建主從複寫與自動故障轉移

## 為什麼需要讀寫分離？

當資料庫的讀取壓力成為瓶頸時，最直接的解決方案就是讀寫分離。

```
典型場景：
  電商網站：商品瀏覽（讀取）遠多於下單（寫入）
  社群媒體：刷動態（讀取）遠多於發文（寫入）
  內容平台：查看文章（讀取）遠多於發布（寫入）

讀寫比例通常為 10:1 到 100:1
```

### 讀寫分離的收益

- **讀取擴展**：增加從庫數量即可提升讀取吞吐量
- **故障隔離**：從庫故障不影響寫入操作
- **報表查詢隔離**：將慢查詢導向從庫，不阻塞主庫

---

## MySQL 主從複寫設定

### 主庫設定

```ini
# my.cnf (master)
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = ecommerce
```

```sql
-- 在 Master 建立複寫用戶
CREATE USER 'replica'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';
FLUSH PRIVILEGES;

-- 查看主庫狀態
SHOW MASTER STATUS;
-- File: mysql-bin.000001, Position: 154
```

### 從庫設定

```ini
# my.cnf (slave)
[mysqld]
server-id = 2
relay_log = /var/log/mysql/mysql-relay-bin.log
read_only = 1
```

```sql
-- 在 Slave 設定複寫
CHANGE MASTER TO
  MASTER_HOST='master-host',
  MASTER_USER='replica',
  MASTER_PASSWORD='password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=154;

START SLAVE;

-- 檢查複寫狀態
SHOW SLAVE STATUS\G
-- Slave_IO_Running: Yes
-- Slave_SQL_Running: Yes
```

---

## Python 讀寫分離路由

### 基礎實現

```python
import mysql.connector
import random

class DatabaseRouter:
    def __init__(self, master_config, slave_configs):
        self.master = mysql.connector.connect(**master_config)
        self.slaves = [
            mysql.connector.connect(**cfg)
            for cfg in slave_configs
        ]

    def execute_write(self, query, params=None):
        cursor = self.master.cursor()
        cursor.execute(query, params or ())
        self.master.commit()
        return cursor

    def execute_read(self, query, params=None):
        slave = random.choice(self.slaves)
        cursor = slave.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()

# 使用
router = DatabaseRouter(
    master_config={"host": "master-db", "user": "app", "password": "..."},
    slave_configs=[
        {"host": "slave1-db", "user": "app", "password": "..."},
        {"host": "slave2-db", "user": "app", "password": "..."},
    ]
)

# 寫入 → 主庫
router.execute_write(
    "INSERT INTO orders (user_id, total) VALUES (%s, %s)",
    (1, 99.99)
)

# 讀取 → 從庫
orders = router.execute_read(
    "SELECT * FROM orders WHERE user_id = %s",
    (1,)
)
```

---

## 自動故障轉移

### 健康檢查

```python
import time

class HealthChecker:
    def __init__(self, router, check_interval=5):
        self.router = router
        self.check_interval = check_interval
        self.master_healthy = True
        self.slave_healthy = [True] * len(router.slaves)

    def check_master(self):
        try:
            cursor = self.router.master.cursor()
            cursor.execute("SELECT 1")
            self.master_healthy = True
        except Exception:
            self.master_healthy = False

    def check_slaves(self):
        for i, slave in enumerate(self.router.slaves):
            try:
                cursor = slave.cursor()
                cursor.execute("SELECT 1")
                self.slave_healthy[i] = True
            except Exception:
                self.slave_healthy[i] = False
                print(f"Slave {i} is down")
```

### 自動提昇

```python
class FailoverManager:
    def __init__(self, router, configs):
        self.router = router
        self.configs = configs

    def promote_slave(self, slave_index):
        """將從庫提昇為主庫"""
        slave_host = self.configs["slaves"][slave_index]["host"]
        print(f"Promoting {slave_host} to master")

        # 在從庫執行
        # STOP SLAVE;
        # RESET SLAVE ALL;
        # 更新應用配置

        new_master_config = self.configs["slaves"][slave_index]
        self.router.master = mysql.connector.connect(**new_master_config)
        print("Failover completed")

    def auto_failover(self):
        """偵測主庫故障後自動提昇"""
        while True:
            if not self.router.master_healthy():
                # 選取資料最新的從庫
                best_slave = self._find_best_slave()
                self.promote_slave(best_slave)
            time.sleep(5)
```

---

## 常見問題與解決方案

### 複寫延遲

從庫的資料更新落後於主庫。

```
主庫寫入 t0 → 從庫接收到 t0 + Δt
問題：用戶寫入後立即讀取，可能讀到舊資料
```

**解決方案**：

```python
class SmartRouter:
    def read_after_write(self, user_id, query, params):
        # 寫入後的讀取強制走主庫
        if self._is_recent_write(user_id):
            return self.execute_on_master(query, params)
        return self.execute_read(query, params)
```

### 從庫故障

```python
class ResilientRouter:
    def execute_read(self, query, params=None):
        for i, slave in enumerate(self.slaves):
            if self.health[i]:  # 跳過不健康的從庫
                try:
                    cursor = slave.cursor()
                    cursor.execute(query, params or ())
                    return cursor.fetchall()
                except Exception:
                    self.health[i] = False
                    print(f"Slave {i} failed, trying next")
        # 全部從庫都故障，降級到主庫讀取
        return self.execute_on_master(query, params)
```

---

## 監控指標

```sql
-- 複寫延遲（秒）
SHOW SLAVE STATUS;
-- Seconds_Behind_Master: 0

-- 從庫讀取量
SHOW GLOBAL STATUS LIKE 'Com_select';

-- 主庫寫入量
SHOW GLOBAL STATUS LIKE 'Com_insert';
SHOW GLOBAL STATUS LIKE 'Com_update';
```

推薦的監控工具：
- **Prometheus + mysqld_exporter**：即時監控
- **Orchestrator**：自動故障轉移管理
- **ProxySQL**：智慧代理，自動路由讀寫

---

## 延伸閱讀

- [MySQL Replication Official Docs](https://www.google.com/search?q=MySQL+replication+configuration+guide)
- [Read-Write Split Pattern](https://www.google.com/search?q=database+read+write+splitting+pattern)
- [MySQL High Availability](https://www.google.com/search?q=MySQL+high+availability+failover)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之五。*
