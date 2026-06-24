# 主題六：資料庫 Replication

## 資料庫複寫與擴展

Replication（複寫）是建立高可用性和可擴展資料庫系統的關鍵技術。2007 年，各種資料庫都提供了成熟的 Replication 解決方案。

## Replication 的目的

```python
"""
為什麼需要 Replication？
"""

def replication_purposes():
    purposes = {
        "高可用性": "主庫當機時從庫可以接手",
        "讀取擴展": "將讀取請求分散到多個從庫",
        "異地備援": "在不同地點建立副本",
        "資料安全": "提供即時備份",
        "負載平衡": "分散查詢壓力",
    }

    print("Replication 的目的：")
    for purpose, desc in purposes.items():
        print(f"  {purpose}: {desc}")

replication_purposes()
```

## MySQL Replication

### 主從Replication

```ini
# 主庫設定 (my.cnf)
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-do-db = myapp
```

```sql
-- 從庫設定
CHANGE MASTER TO
    MASTER_HOST = 'master.example.com',
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'password',
    MASTER_LOG_FILE = 'mysql-bin.000001',
    MASTER_LOG_POS = 12345;

START SLAVE;
```

### Replication 運作原理

```markdown
# 主從Replication流程

1. 主庫記錄所有變更到 Binary Log
2. 從庫連接主庫，請求新的日誌事件
3. 主庫傳送日誌事件到從庫
4. 從庫執行這些事件，更新本地資料庫

# 同步方式

- 同步 Replication（Synch）：事務在所有節點提交後才返回
- 异步 Replication（Async）：主庫提交後立即返回
- 半同步 Replication（Semi-sync）：至少一個從庫確認後返回
```

### 常見拓撲

```markdown
# 常見 Replication 拓撲

1. 主從（Master-Slave）
   - 一個主庫，多個從庫
   - 寫入主庫，讀取分散到從庫

2. 主主（Master-Master）
   - 兩個主庫，互相複寫
   - 可雙向寫入

3. 鏈式（Master -> Slave -> Slave）
   - 減少主庫負載
   - 延長複製延遲
```

## PostgreSQL Replication

### Streaming Replication

```ini
# postgresql.conf (主庫)
wal_level = hot_standby
max_wal_senders = 3
wal_keep_segments = 32
```

```ini
# postgresql.conf (從庫)
hot_standby = on
```

```bash
# 建立基礎備份
pg_basebackup -h master -D /var/lib/postgresql/standby
```

### 設定檔

```ini
# recovery.conf (從庫)
standby_mode = 'on'
primary_conninfo = 'host=master port=5432 user=repl'
trigger_file = '/tmp/postgresql.trigger'
```

## 故障轉移

### 手動故障轉移

```sql
-- MySQL
STOP SLAVE;
CHANGE MASTER TO MASTER_HOST='';
RESET SLAVE;

-- 提升從庫為新的主庫
RESET MASTER;
```

### 自動故障轉移

```bash
# DRBD (分散式副本區塊設備)
drbdadm primary all
# 將 DRBD 設備掛載為 MySQL 資料目錄

# Heartbeat + DRBD
# 提供自動故障轉移
```

### 故障轉移工具

```markdown
# 常見故障轉移方案

1. MMM (MySQL Master-Master Replication Manager)
   - 虛擬 IP 管理
   - 自動故障轉移
   - 節點監控

2. Heartbeat + DRBD
   - 區塊層級複寫
   - 作業系統級故障轉移

3. Linux HA
   - 整合多種資源
   - 企業級可靠性
```

## Replication 監控

### MySQL 監控

```sql
-- 檢視 Replication 狀態
SHOW SLAVE STATUS\G

-- 重要欄位
-- Slave_IO_Running: I/O 執行緒狀態
-- Slave_SQL_Running: SQL 執行緒狀態
-- Seconds_Behind_Master: 延遲秒數
-- Last_Error: 最後的錯誤
```

### 常見問題處理

```sql
-- 跳過錯誤
SET GLOBAL sql_slave_skip_counter = 1;
STOP SLAVE; START SLAVE;

-- 重新同步從庫
STOP SLAVE;
RESET SLAVE;
CHANGE MASTER TO ...
START SLAVE;
```

## 結語

Replication 是建立可靠資料庫系統的核心技術。透過主從複寫，可以實現高可用性和讀取擴展；透過故障轉移機制，可以確保系統的持續運行。選擇合適的 Replication 方案，需要根據應用的可用性需求和成本考量來決定。

---

*延伸閱讀：*
- [MySQL Replication](https://developers.google.com/search/?q=mysql+replication)
- [PostgreSQL Streaming Replication](https://developers.google.com/search/?q=postgresql+streaming+replication)*