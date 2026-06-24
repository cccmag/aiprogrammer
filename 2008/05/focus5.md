# Cassandra 列式資料庫

## Cassandra 概述

Cassandra 由 Facebook 開發，結合了 BigTable 的列式儲存和 Dynamo 的分散式設計。2008 年貢獻給 Apache 基金會。

### 特點

- **分散式**：無單點故障
- **高可用**：持續可用
- **線性擴展**：新增節點即可
- **靈活Schema**：列可動態新增

## 安裝與設定

### 安裝 Cassandra

```bash
wget http://archive.apache.org/dist/cassandra/0.4.0/apache-cassandra-0.4.0-bin.tar.gz
tar -xzf apache-cassandra-0.4.0-bin.tar.gz
export CASSANDRA_HOME=/path/to/cassandra
```

### 設定 cassandra.yaml

```yaml
cluster_name: 'MyCluster'
initial_token: 0
seed_provider:
  - seeds: "127.0.0.1"
listen_address: 127.0.0.1
rpc_address: 0.0.0.0
```

### 啟動服務

```bash
# 啟動
$CASSANDRA_HOME/bin/cassandra -f

# 連接客戶端
$CASSANDRA_HOME/bin/cassandra-cli
```

## CQL 語法

### 建立 Keyspace

```sql
CREATE KEYSPACE myapp
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};
```

### 建立表格

```sql
CREATE TABLE users (
    user_id uuid PRIMARY KEY,
    name text,
    email text,
    age int
);
```

### CRUD 操作

```sql
-- 插入
INSERT INTO users (user_id, name, email, age)
VALUES (uuid(), 'John', 'john@example.com', 30);

-- 查詢
SELECT * FROM users;
SELECT * FROM users WHERE user_id = ?;

-- 更新
UPDATE users SET age = 31 WHERE user_id = ?;

-- 刪除
DELETE FROM users WHERE user_id = ?;
```

## Python API

### 使用 pycassa

```python
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
import uuid

# 連接到叢集
pool = ConnectionPool('myapp', ['localhost:9160'])

# 選擇 ColumnFamily
users = ColumnFamily(pool, 'users')

# 插入
user_id = uuid.uuid1()
users.insert(user_id, {
    'name': 'John',
    'email': 'john@example.com',
    'age': 30
})

# 查詢
user = users.get(user_id)
print(user)

# 讀取多行
for key, columns in users.get_range(start='', finish=''):
    print(key, columns)
```

## 資料模型

### Column Family

```python
# 類似表格但更靈活
users = {
    'user1': {
        'name': 'John',
        'email': 'john@example.com'
    },
    'user2': {
        'name': 'Mary',
        'email': 'mary@example.com'
    }
}
```

### 寬欄表

```sql
-- 時序資料
CREATE TABLE events (
    user_id uuid,
    event_time timestamp,
    event_type text,
    data map<text, text>,
    PRIMARY KEY (user_id, event_time)
);

-- 查詢特定使用者的所有事件
SELECT * FROM events WHERE user_id = ?;
```

### 超級欄

```sql
-- 超級欄（已棄用）
CREATE TABLE timeline (
    user_id text,
    timeline_key text,
    event_id timeuuid,
    content text,
    PRIMARY KEY (user_id, timeline_key, event_id)
);
```

## 分散式架構

### 一致性雜湊

```
環：
    0
    │
    ├── Node1 (0-85)
    ├── Node2 (85-170)
    └── Node3 (170-255)
```

### 副本策略

```python
# SimpleStrategy（單一資料中心）
# NetworkTopologyStrategy（多資料中心）
```

### 一致性層級

```python
# 讀取一致性
ONE  # 一個節點確認即可
QUORUM  # 過半數節點
ALL  # 所有節點確認

# 寫入一致性
ANY  # 任何節點（包含 hinted handoff）
QUORUM  # 過半數
```

## 結論

Cassandra 的分散式設計和水平擴展能力使其成為處理大規模時序資料的理想選擇。其 CQL 語法也降低了學習曲線。

---

**延伸閱讀**

- [BigTable 列式儲存](focus1.md)
- [Dynamo 分散式設計](focus2.md)
- [Cassandra+documentation](https://www.google.com/search?q=Cassandra+documentation)