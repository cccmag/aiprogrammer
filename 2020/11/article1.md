# 分散式資料庫：Cassandra 與 DynamoDB

## 前言

隨著資料量的爆發性增長，傳統的單機關聯式資料庫已經無法滿足需求。分散式 NoSQL 資料庫應運而生，其中 Cassandra 和 DynamoDB 是兩個最具代表性的系統。

## 一致性雜湊

### 傳統雜湊的問題

```python
# 傳統雜湊的問題
def traditional_hash(key, num_nodes):
    return hash(key) % num_nodes

# 當新增或移除節點時幾乎所有資料都需要移動
nodes = ["node1", "node2", "node3"]
key = "user123"

# 原本：key 映射到 node1
print(hash(key) % 3)  # 假設得到 1

# 新增 node4：需要重新映射幾乎所有 key
nodes = ["node1", "node2", "node3", "node4"]
print(hash(key) % 4)  # 假設得到 2
```

### 一致性雜湊環

```python
import hashlib

class ConsistentHash:
    def __init__(self, nodes=None, virtual_nodes=100):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)
    
    def add_node(self, node):
        for i in range(self.virtual_nodes):
            vnode = f"{node}#{i}"
            key = self._hash(vnode)
            self.ring[key] = node
        
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key):
        hash_key = self._hash(key)
        
        # 二分搜尋找到第一個 >= hash_key 的位置
        for node_key in self.sorted_keys:
            if node_key >= hash_key:
                return self.ring[node_key]
        
        # 迴繞到第一個節點
        return self.ring[self.sorted_keys[0]]

# 使用範例
ch = ConsistentHash(["node1", "node2", "node3"], virtual_nodes=100)
print(ch.get_node("user123"))  # 一致性映射
ch.add_node("node4")            # 只移動受影響的 key
print(ch.get_node("user123"))  # 大部分 key 保持不變
```

## Cassandra 架構

### 分散式架構

```
Cassandra 架構：
────────────────────────────────

Client
  │
  ▼
┌──────────────────────────────┐
│     Coordinator Node         │
│  (協調節點，客戶端連接的節點) │
└──────────────┬───────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐
│Node 1 │  │Node 2 │  │Node 3 │
│ ring  │  │ ring  │  │ ring  │
└───┬───┘  └───┬───┘  └───┬───┘
    │          │          │
    └──────────┼──────────┘
               │
         Data Center
```

### 資料複製策略

```python
# Cassandra 複製因子 (Replication Factor)

"""
RF = 3 表示每筆資料會有 3 份副本

複製策略：
- SimpleStrategy：用於單一資料中心
- NetworkTopologyStrategy：用於多資料中心

一致性等級：
- ONE：任何一個副本回應即可
- QUORUM：大多數副本確認
- ALL：所有副本確認
- LOCAL_ONE：本地資料中心的一個副本
"""
```

### CQL 基本操作

```sql
-- 建立 keyspace
CREATE KEYSPACE myapp
WITH REPLICATION = {
    'class': 'NetworkTopologyStrategy',
    'dc1': 3
};

-- 建立表格
CREATE TABLE myapp.users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP
);

-- 插入資料
INSERT INTO myapp.users (user_id, name, email, created_at)
VALUES (uuid(), 'Alice', 'alice@example.com', toTimestamp(now()));

-- 查詢
SELECT * FROM myapp.users WHERE user_id = ?;

-- 更新
UPDATE myapp.users SET name = 'Bob' WHERE user_id = ?;

-- 刪除
DELETE FROM myapp.users WHERE user_id = ?;
```

## DynamoDB

### Amazon 的分散式 key-value 儲存

```
DynamoDB 特性：
────────────────────────────────

- 完全托管：無需管理伺服器
- 自動擴展：根據流量自動擴展
- 單一延遲：毫秒級回應
- 99.99% 可用性 SLA
- 主鍵設計影響效能
```

### 分區和讀寫容量

```python
# DynamoDB 的吞吐量和分區

"""
DynamoDB 根據項目大小和讀寫吞吐量自動分區

每個分區：
- 最多 3000 RCU (讀取容量單位)
- 最多 1000 WCU (寫入容量單位)
- 約 10GB 資料

設計良好的主鍵：
- 避免熱點（所有請求集中在一個分區）
- 考虑訪問模式
"""

import boto3

dynamodb = boto3.resource('dynamodb')

# 全域表格
table = dynamodb.Table('myapp_users')

# 寫入
table.put_item(
    Item={
        'user_id': '123',
        'name': 'Alice',
        'email': 'alice@example.com'
    }
)

# 讀取
response = table.get_item(
    Key={'user_id': '123'}
)
```

### DynamoDB 的特點

```
DynamoDB 與 Cassandra 比較：
────────────────────────────────

DynamoDB：
  ✓ 完全托管
  ✓ 自動擴展
  ✓ 簡單定價（按請求量）
  ✗ 有限的自定義選項
  ✗ 主鍵設計約束

Cassandra：
  ✓ 完全可自訂
  ✓ 可以部署在任何環境
  ✓ 靈活的資料模型
  ✗ 需要自己管理
  ✗ 運維複雜
```

## 一致性模型

### 可調整一致性

```python
# Cassandra 的一致性級別

"""
可以為每個查詢指定一致性級別

讀取：
- ONE：最快的讀取，可能讀到過時資料
- QUORUM：讀取大多數副本，更一致
- ALL：讀取所有副本，最一致但最慢

寫入：
- ONE：寫入一個副本
- QUORUM：寫入大多數副本
- ALL：寫入所有副本

可以同時指定讀寫的一致性：
- quorum + quorum：讀寫都達到 QUORUM
"""
```

## 延伸閱讀

- [Cassandra 官方網站](https://www.google.com/search?q=Apache+Cassandra+official)
- [DynamoDB 文件](https://www.google.com/search?q=Amazon+DynamoDB+documentation)
- [一致性雜湊](https://www.google.com/search?q=consistent+hashing+algorithm)
- [分散式資料庫比較](https://www.google.com/search?q=distributed+database+NoSQL+comparison)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*