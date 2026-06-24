# 共識演算法：Paxos、Raft 與一致性

## 為什麼需要共識演算法？

### 分散式一致性的核心問題

在分散式系統中，多個節點需要對某個值達成一致：

```
拜占庭將軍問題：
────────────────────────────────

將軍 1 ────▶ 將軍 2 ────▶ 將軍 3
   │              │              │
   ◀──────────────┘              │
         │                       │
         ◀───────────────────────┘
              │
         叛徒可能發送矛盾的消息！

問題：如何讓忠誠的將軍達成一致的決定？
```

### 共識演算法的定義

```python
# 共識演算法的安全性要求

"""
1. Agreement（一致性）
   └── 所有正常節點決定相同的值
   
2. Validity（有效性）
   └── 決定的值必須是某個節點提議的
   
3. Termination（終止性）
   └── 所有正常節點最終都會做出決定
"""
```

## Paxos 演算法

### Paxos 的基本概念

Paxos 是 Leslie Lamport 於 1998 年提出的共識演算法：

```
Paxos 角色：
────────────────────────────────

Proposer（提議者）：
  - 提出值，等待批准
  
Acceptor（接受者）：
  - 投票決定是否接受提議
  
Learner（學習者）：
  - 學習被接受的值

多數派（Majority）：
  - 任何決定需要多數 acceptor 同意
  - N 個 acceptor 需要 floor(N/2)+1 票
```

### Paxos 兩階段

```python
# 簡化的 Paxos 演算法

# 第一階段：準備（Prepare）
class Proposer:
    def prepare(self, proposal_id):
        # 發送準備請求到所有 acceptor
        promises = []
        for acceptor in acceptors:
            promise = acceptor.receive_prepare(proposal_id)
            if promise.ack:
                promises.append(promise)
        
        # 收到多數派回應
        if len(promises) > len(acceptors) / 2:
            # 第二階段
            return self.propose(proposal_id, promises)

# 第二階段：提議（Propose）
class Proposer:
    def propose(self, proposal_id, promises):
        # 選擇最大 proposal_id 的值
        # 如果沒有，選擇自己的值
        value = max_promise_value(promises) or self.value
        
        # 發送 accept 請求
        for acceptor in acceptors:
            acceptor.receive_accept(proposal_id, value)
```

### Paxos 的問題

```
Paxos 的挑戰：
────────────────────────────────

1. 難以理解
   └── 論文以希臘故事開場，更加抽象
   
2. 難以實現
   └── 多 Paxos（Multi-Paxos）細節未明確定義
   
3. 效率問題
   └── 兩階段可能導致衝突
```

## Raft 共識演算法

### Raft 的設計目標

Raft 由 Diego Ongaro 和 John Ousterhout於 2014 年提出，旨在成為更容易理解的共識演算法：

```
Raft 設計原則：
────────────────────────────────

1. 分解問題
   └── 領導者選舉、日誌複製、的安全性分開處理

2. 減少狀態空間
   └── 簡化演算法狀態，降低不确定性

3. 強領導者（Strong Leader）
   └── 日誌條目只從領導者流向跟隨者
```

### Raft 領導者選舉

```python
# Raft 領導者選舉

class RaftNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.state = "follower"  # follower, candidate, leader
        
    def election_timeout(self):
        """等待隨機超時後開始選舉"""
        import random
        timeout = random.randint(150, 300)  # ms
        return timeout
    
    def start_election(self):
        self.state = "candidate"
        self.current_term += 1
        self.voted_for = self.node_id  # 投自己
        
        votes = 1
        for peer in peers:
            granted = peer.request_vote(
                term=self.current_term,
                candidate_id=self.node_id,
                last_log_index=len(self.log),
                last_log_term=self.log[-1].term if self.log else 0
            )
            if granted:
                votes += 1
        
        if votes > len(peers) / 2:
            self.become_leader()
```

### 日誌複製

```python
# Raft 日誌複製

class RaftNode:
    def handle_client_request(self, command):
        if self.state != "leader":
            return error
        
        # 添加到本地日誌
        self.log.append(LogEntry(term=self.current_term, command=command))
        
        # 並行發送給所有跟隨者
        for peer in peers:
            self.send_append_entries(peer)
        
        # 如果收到多數派確認，套用狀態機
        if self.replicated_to_majority(len(self.log) - 1):
            self.commit_index += 1
            self.apply_to_state_machine()
    
    def send_append_entries(self, peer, prev_log_index=0):
        entries = self.log[prev_log_index+1:]
        response = peer.append_entries(
            term=self.current_term,
            leader_id=self.node_id,
            prev_log_index=prev_log_index,
            prev_log_term=self.log[prev_log_index].term if prev_log_index > 0 else None,
            entries=entries,
            leader_commit=self.commit_index
        )
        # 處理響應...
```

## 一致性模型的實際應用

### etcd：K8s 的心臟

etcd 是一個高可用的鍵值儲存，使用 Raft 共識：

```
etcd 架構：
────────────────────────────────

用戶端 ────▶ etcd Leader ────▶ 寫入日誌
                  │
                  ▼
            複製到跟隨者
                  │
                  ▼
            客戶端讀取
                  │
         ┌────────┴────────┐
         ▼                 ▼
    Leader 讀         follower 讀
    （強一致性）     （最終一致性）
```

### ZooKeeper 的一致性模型

ZooKeeper 使用 Zab 協議（類似 Paxos）：

```python
# ZooKeeper 操作示例

from kazoo.client import KazooClient

zk = KazooClient('localhost:2181')
zk.start()

# 創建節點
zk.create("/myapp/data", b"value", make_stars=True)

# 讀取
data, stat = zk.get("/myapp/data")

# 更新
zk.set("/myapp/data", b"new_value")

# 監聽變化
@zk.DataWatch("/myapp/data")
def watch(data, stat):
    print(f"Data changed to: {data}")
```

## Raft vs Paxos

```
Raft vs Paxos：
────────────────────────────────

特性           │ Raft         │ Paxos
──────────────│──────────────│─────────
可理解性       │ ✓ 較好       │ ✗ 複雜
實現難度       │ ✓ 較易       │ ✗ 困難
社群採用       │ ✓ 廣泛       │ ⚠ 一般
效能           │ 相近         │ 相近
元資料開銷     │ 類似         │ 類似

實際採用：
- etcd、TiKV、CockroachDB 使用 Raft
- Google Chubby、Libcloud 使用 Paxos
```

## 延伸閱讀

- [Paxos 原始論文](https://www.google.com/search?q=Paxos+Lamport+1998+paper)
- [Raft 論文](https://www.google.com/search?q=Raft+Ongaro+Ousterhout+2014+paper)
- [Raft 視覺化](https://www.google.com/search?q=Raft+algorithm+visualization)
- [etcd 文檔](https://www.google.com/search?q=etcd+documentation+Rafty)
- [ZooKeeper 共識](https://www.google.com/search?q=ZooKeeper+Zab+consensus)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」歷史回顧系列之一。*