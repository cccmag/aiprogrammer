# 時序與向量時鐘：分散式系統的時間問題

## 分散式系統中的時間問題

### 為什麼時間是個問題？

在分散式系統中，沒有全域時鐘：

```
時鐘同步的困難：
────────────────────────────────

節點 A                           節點 B
│                               │
│  事件 1                       │
│───────────▶ (物理時間: 10:00) │
│                               │
│              ◀───────────────│
│              事件 2          │
│          (物理時間: 09:59:59)│  ⚠️ 時間不一致！

問題：
- 網路延遲不確定
- 實體時鐘會有偏移
- NTP 同步有延遲
```

## 邏輯時鐘

### Lamport 時鐘

Lamport 時鐘是一種記錄事件順序的機制：

```python
# Lamport 時鐘實現

class LamportClock:
    def __init__(self, node_id):
        self.node_id = node_id
        self.time = 0
    
    def local_event(self):
        """本地事件，時間遞增"""
        self.time += 1
        return self.time
    
    def send_event(self, message):
        """發送訊息，時間遞增"""
        self.time += 1
        message['lamport_time'] = self.time
        message['sender'] = self.node_id
        return message
    
    def receive_event(self, message):
        """接收訊息，與發送者時間取最大值"""
        self.time = max(self.time, message['lamport_time']) + 1
        return self.time

# 使用示例
clock = LamportClock("A")
clock.local_event()           # t=1
clock.local_event()           # t=2
msg = clock.send_event({})    # t=3, message contains {lamport_time: 3}
```

### Lamport 因果關係

```python
# 因果關係判斷

def happened_before(event1, event2):
    """
    如果 event1 在 event2 之前發生，
    返回 True
    """
    return event1.lamport_time < event2.lamport_time

# 問題：時間相同不代表無因果關係！
# Lamport 時鐘只能判斷「可能」或「確定不在」之前
```

## 向量時鐘

### 向量時鐘的原理

向量時鐘是對 Lamport 時鐘的增強，可以完整描述因果關係：

```python
# 向量時鐘實現

class VectorClock:
    def __init__(self, node_ids):
        self.node_ids = node_ids
        self.clock = {node_id: 0 for node_id in node_ids}
    
    def local_event(self, node_id):
        """本地事件"""
        self.clock[node_id] += 1
        return dict(self.clock)
    
    def send_event(self, node_id, message):
        """發送事件"""
        self.clock[node_id] += 1
        message['vector_clock'] = dict(self.clock)
        message['sender'] = node_id
        return message
    
    def receive_event(self, node_id, message):
        """接收事件"""
        vc = message['vector_clock']
        # 與發送者時間相加
        for n in self.node_ids:
            self.clock[n] = max(self.clock[n], vc.get(n, 0))
        self.clock[node_id] += 1
        return dict(self.clock)
```

### 向量時鐘比較

```python
# 向量時鐘比較

def compare_vc(vc1, vc2):
    """
    比較兩個向量時鐘的關係
    返回：
    - 'before': vc1 在 vc2 之前
    - 'after': vc1 在 vc2 之後
    - 'concurrent': 並發
    """
    before = all(vc1[n] <= vc2.get(n, 0) for n in vc1)
    after = all(vc1[n] >= vc2.get(n, 0) for n in vc1)
    
    if before and not after:
        return 'before'
    if after and not before:
        return 'after'
    return 'concurrent'

# 示例：判斷事件順序
clock_A = {'A': 1, 'B': 0, 'C': 0}
clock_B = {'A': 2, 'B': 0, 'C': 0}
clock_C = {'A': 1, 'B': 1, 'C': 0}

print(compare_vc(clock_A, clock_B))  # 'before' (A=1 <= 2)
print(compare_vc(clock_A, clock_C))  # 'before' (A=1 <= 1, B=0 <= 1)
print(compare_vc(clock_B, clock_C))  # 'concurrent' (A: 2 > 1, B: 0 < 1)
```

## 向量時鐘的應用

### 衝突偵測

```python
# 使用向量時鐘偵測更新衝突

class DVVMap:
    """基於向量時鐘的衝突偵測"""
    
    def __init__(self):
        self.values = {}  # key -> (value, vector_clock)
    
    def put(self, key, value, node_id):
        # 讀取當前時鐘
        current_vc = self.get_clock(key)
        
        # 更新時鐘
        for n in current_vc:
            current_vc[n] = max(current_vc[n], self.global_clock[n])
        current_vc[node_id] += 1
        
        # 檢查衝突
        if key in self.values:
            old_value, old_vc = self.values[key]
            relation = compare_vc(old_vc, current_vc)
            
            if relation == 'concurrent':
                # 發生衝突！
                return {'conflict': True, 'old': old_value, 'new': value}
        
        self.values[key] = (value, current_vc)
        return {'conflict': False}
    
    def get_clock(self, key):
        if key in self.values:
            return dict(self.values[key][1])
        return dict(self.global_clock)
```

### 實現最終一致性

```python
# CRDT（Conflict-free Replicated Data Type）

class GCounter:
    """最終一致的計數器"""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.counts = {node_id: 0}
    
    def increment(self):
        self.counts[self.node_id] += 1
    
    def merge(self, other_counts):
        for node, count in other_counts.items():
            self.counts[node] = max(self.counts.get(node, 0), count)
    
    def value(self):
        return sum(self.counts.values())
```

## TrueTime 與分散式事務

### Google Spanner 的 TrueTime

TrueTime 使用 GPS 和原子鐘實現高精確度時間：

```python
# TrueTime 概念

"""
TrueTime API：
- NOW() 返回區間 [earliest, latest]
- 事件時間戳在區間內不確定
- 事務提交需要等待時間不確定性過去

Spanner 使用時間戳保證：
- External Consistency（外部一致性）
- 類似於線性化
"""

class TrueTime:
    def now(self):
        import random
        # 類比 TrueTime 返回區間
        earliest = current_time()
        latest = earliest + 7  # ~7ms 不確定性
        return (earliest, latest)
    
    def wait_for_time(self, target_time):
        # 等待時間推進到目標時間
        while current_time() < target_time:
            sleep(0.001)
```

## 延伸閱讀

- [Lamport 時鐘](https://www.google.com/search?q=Lamport+logical+clock)
- [向量時鐘](https://www.google.com/search?q=vector+clock+distributed+systems)
- [分散式因果關係](https://www.google.com/search?q=causality+distributed+systems+vector+clock)
- [Google TrueTime](https://www.google.com/search?q=Google+TrueTime+Spanner)
- [CRDT 最終一致性](https://www.google.com/search?q=CRDT+conflict-free+replicated+data+type)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」歷史回顧系列之一。*