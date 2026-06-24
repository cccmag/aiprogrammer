# 分散式資料庫的一致性挑戰

## 一致性問題的由來

在分散式資料庫中，資料被儲存在多個節點上。當網路分割發生時，如何保證資料的一致性成為核心挑戰。CAP 定理告訴我們，在網路分割時，必須在一致性和可用性之間做出選擇。

## 一致性的層次

### 線性一致性（Linearizability）

最強的一致性保證。所有操作看起來像是瞬時在單一節點上執行的。

```python
# 線性一致性的簡化示意
def linearizable_write(node, key, value):
    # 向所有節點發送寫入
    responses = broadcast_to_all_nodes({
        'type': 'write',
        'key': key,
        'value': value,
        'timestamp': time.time()
    })

    # 等待大多數節點確認
    if count_acks(responses) > len(nodes) // 2:
        return True
    return False
```

### 順序一致性（Sequential Consistency）

只保證所有節點看到相同的操作順序，不要求操作是瞬時的。

### 因果一致性（Causal Consistency）

保證有因果關係的操作順序一致。

## 一致性實現機制

### 向量時鐘

向量時鐘是一種追蹤事件因果關係的機制：

```python
class VectorClock:
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = {node_id: 0}

    def increment(self):
        """遞增本地時鐘"""
        self.clock[self.node_id] += 1
        return self.clock.copy()

    def update(self, remote_clock):
        """合併遠端時鐘"""
        for node, time in remote_clock.items():
            if node not in self.clock:
                self.clock[node] = 0
            self.clock[node] = max(self.clock[node], time)

    def happens_before(self, other):
        """判斷是否在其他時鐘之前"""
        for node in self.clock:
            if self.clock[node] > other.get(node, 0):
                return False
        return True

    def concurrent(self, other):
        """判斷是否並發"""
        return not self.happens_before(other) and not other.happens_before(self)
```

### Paxos 共識演算法

Paxos 是實現強一致性的經典共識演算法：

```python
class PaxosProposer:
    def __init__(self, node_id, acceptors):
        self.node_id = node_id
        self.acceptors = acceptors
        self.proposal_number = 0

    def prepare(self):
        """發送 prepare 請求"""
        self.proposal_number += 1
        request = {
            'type': 'prepare',
            'proposal_id': (self.proposal_number, self.node_id),
            'node_id': self.node_id
        }

        # 等待多數派回應
        promises = []
        for acceptor in self.acceptors:
            response = acceptor.handle_prepare(request)
            if response.get('promise'):
                promises.append(response)

        return len(promises) > len(self.acceptors) // 2

    def accept(self, value):
        """發送 accept 請求"""
        request = {
            'type': 'accept',
            'proposal_id': (self.proposal_number, self.node_id),
            'value': value
        }

        accepted = []
        for acceptor in self.acceptors:
            response = acceptor.handle_accept(request)
            if response.get('accepted'):
                accepted.append(response)

        return len(accepted) > len(self.acceptors) // 2
```

### Raft 共識演算法

Raft 是更容易理解的共識演算法：

```python
class RaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = 'follower'
        self.current_term = 0
        self.voted_for = None
        self.log = []

    def election_timeout(self):
        """開始選舉"""
        self.state = 'candidate'
        self.current_term += 1
        self.voted_for = self.node_id

        votes = 1  # 自己的一票

        for peer in self.peers:
            # 發送 RequestVote
            response = peer.request_vote({
                'term': self.current_term,
                'candidate_id': self.node_id,
                'last_log_index': len(self.log),
                'last_log_term': self.log[-1]['term'] if self.log else 0
            })

            if response['term'] > self.current_term:
                # 發現更新的任期
                self.state = 'follower'
                return

            if response['vote_granted']:
                votes += 1

        if votes > len(self.peers) // 2:
            self.state = 'leader'
            self.send_heartbeat()
```

## NoSQL 中的實現

### Cassandra 的最終一致性

```python
# Cassandra 的一致性等級
# ONE：任一台節點確認即可
# QUORUM：大多數節點確認
# ALL：所有節點確認

from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('myapp')

# 強一致性寫入
session.execute(
    "INSERT INTO users (id, name) VALUES (%s, %s)",
    ['user1', 'John'],
    consistency_level=ConsistencyLevel.QUORUM
)

# 最終一致性寫入（快速）
session.execute(
    "INSERT INTO users (id, name) VALUES (%s, %s)",
    ['user1', 'John'],
    consistency_level=ConsistencyLevel.ONE
)
```

### MongoDB 的寫入確認

```python
from pymongo import WriteConcern

# 單一節點確認（快）
collection = db.get_collection('users', write_concern=WriteConcern(w=1))

# 大多數節點確認（強一致）
collection = db.get_collection('users', write_concern=WriteConcern(w='majority'))

# 多數據中心確認
collection = db.get_collection('users',
    write_concern=WriteConcern(w='majority', wtimeout=5000))
```

## 處理分割場景

### 自動故障轉移

```python
class ClusterManager:
    def __init__(self, nodes):
        self.nodes = nodes

    def detect_node_failure(self, node):
        """偵測節點失敗"""
        for other in self.nodes:
            if other != node:
                if not other.is_reachable(node):
                    self.mark_node_down(node)
                    return True
        return False

    def mark_node_down(self, node):
        """標記節點為失敗，觸發故障轉移"""
        # 通知所有節點
        for other in self.nodes:
            if other != node:
                other.notify_node_down(node)

        # 提升從節點
        if node.is_primary:
            new_primary = self.promote_replica(node)
            self.update_cluster_config(new_primary)
```

## 設計建議

### 選擇正確的一致性等級

1. **金融交易**：使用強一致性
2. **社交動態**：可以使用最終一致性
3. **物聯網資料**：通常可以使用最終一致性

### 監控一致性延遲

```python
def monitor_replication_lag(primary, replica):
    """監控複製延遲"""
    lag = primary.last_write_time - replica.applied_time
    if lag > threshold:
        alert(f"複製延遲過高: {lag}ms")
    return lag
```

## 結論

一致性是分散式系統中的核心挑戰。理解不同的一致性模型和實現機制，是設計可靠分散式系統的基礎。