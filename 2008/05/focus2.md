# Amazon Dynamo 的分散式設計

## Dynamo 概述

Amazon 在 2007 年發表 Dynamo 論文，介紹了為亞馬遜電子商務設計的高可用鍵值儲存系統。

### 設計背景

Amazon 的購物車服務需要：
- 99.9% 可用性
- 低延遲
- 持續可用（即使部分節點故障）

### 設計目標

- **可擴展**：線性擴展能力
- **高可用**：即使在網路分割時也要可用
- **高效能**：毫秒級延遲
- **簡單**：易於部署和運維

## 一致性雜湊

### 傳統雜湊的問題

```python
# 傳統雜湊
node = nodes[hash(key) % len(nodes)]

# 問題：節點增減時幾乎所有 key 都需要重新分配
```

### 一致性雜湊解決方案

```python
# 將節點和資料key映射到同一個環上
# 資料儲存在順時針方向最近的第一個節點

# 虛擬節點
# 每個物理節點有多個虛擬節點在環上
node1: [vnode1, vnode4, vnode7]
node2: [vnode2, vnode5, vnode8]
node3: [vnode3, vnode6, vnode9]
```

### 優點

- 新增/移除節點時只需移動部分資料
- 負載均衡更均勻

## 資料管理

### 資料分割

```python
def get_node(key):
    hash_value = hash(key)
    for i in range(N):
        node = ring[(hash_value + i) % len(ring)]
        if is_alive(node):
            return node
    return None
```

### 副本策略

預設 3 副本，分散在不同的節點：

```python
# N=3, R=2, W=2
# N: 副本數
# R: 讀取需要的最少節點數
# W: 寫入需要的最少節點數
```

## 一致性與衝突處理

### 最終一致性

Dynamo 採用最終一致性模型：

```
寫入 → 儲存到本地 → 异步複製到其他節點
                ↓
        許久後所有副本一致
```

### 向量時鐘

解決衝突的機制：

```python
# 向量時鐘範例
# 節點 A 更新：{A: 1}
# 節點 B 更新：{A: 1, B: 1}
# 節點 A 再次更新：{A: 2, B: 1}

# 衝突：
# {A: 2} vs {A: 1, B: 1}
# 無法判斷誰更新
```

### 衝突解決策略

| 策略 | 說明 |
|------|------|
| Last Write Wins (LWW) | 時間戳記決定 |
| Vector Clock | 保留所有版本 |
| Application-specific | 應用自訂邏輯 |

## 容錯機制

### 節點故障檢測

```python
# 透過gossip協議檢測節點故障
def detect_failures():
    for node in alive_nodes:
        if node not in heartbeat_received:
            # 節點可能故障
            mark_suspect(node)
```

### Hint Handoff

當某節點故障時，其他節點暫時儲存該節點的資料：

```python
# 節點 B 故障
# 節點 A 收到寫入 B 的請求
# A 標記並儲存為 "Hints: B"
# B 恢復後，A 將資料傳給 B
```

### Merkle Tree

快速同步資料：

```python
# 每個節點維護 Merkle Tree
# 比較根節點即可快速發現差異
```

## Amazon DynamoDB

DynamoDB 是 AWS 提供的託管服務：

```python
import boto

dynamodb = boto.connect_dynamodb()
table = dynamodb.create_table(
    'users',
    schema=[{'KeyType': 'HASH', 'AttributeName': 'user_id'}],
    throughput={'read': 100, 'write': 50}
)

# 儲存
table.put_item({'user_id': '123', 'name': 'John'})

# 讀取
item = table.get_item('123')
```

## 結論

Dynamo 的設計體現了「可用性優先」的理念。向量時鐘、Hint Handoff 等機制為分散式系統提供了新的解決思路。

---

**延伸閱讀**

- [BigTable 列式儲存](focus1.md)
- [Cassandra 列式資料庫](focus5.md)
- [Dynamo+paper](https://www.google.com/search?q=Amazon+Dynamo+paper)