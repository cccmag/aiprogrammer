# 分散式系統概述：分散式運算的基礎概念

## 什麼是分散式系統？

### 分散式系統的定義

分散式系統是由多個獨立的計算節點組成的系統，這些節點通過網路進行通訊和協調，共同完成任務：

```
分散式系統示意圖：
────────────────────────────────

    ┌─────────┐     ┌─────────┐
    │ Node 1  │────▶│ Node 2  │
    └────┬────┘     └────┬────┘
         │                │
    ┌────┴────────────────┴────┐
    │         網路              │
    └────┬────────────────┬────┘
         │                │
    ┌────┴────┐     ┌────┴────┐
    │ Node 3  │────▶│ Node 4  │
    └─────────┘     └─────────┘

特點：
- 每個節點都是獨立的計算機
- 節點間通過訊息傳遞進行溝通
- 節點故障不應導致整個系統崩潰
- 對使用者呈現為單一系統
```

### 為什麼需要分散式系統？

```
分散式系統的驅動因素：
────────────────────────────────

1. 橫向擴展（Scale Out）
   └── 新增節點即可擴展容量
   
2. 高可用性
   └── 單一節點故障不影響整體服務
   
3. 地理分散
   └── 將資料和服務放在接近使用者的位置
   
4. 效能
   └── 平行處理加速大規模計算
```

## CAP 定理

### CAP 的三選二

Eric Brewer 提出的 CAP 定理指出，分散式系統無法同時滿足以下三個特性：

```
CAP 定理：
────────────────────────────────

      Consistency（一致性）
           /\
          /  \
         /    \
        /  ✕  \
       /        \
      /──────────\
 Consistency     Availability
（一致性）         （可用性）
       ↘         ↙
         Partition
         Tolerance
        （分割容錯）

結論：當發生網路分割時，必須在一致性和可用性之間選擇
```

### 在實際應用中的選擇

不同系統根據業務需求做出不同的選擇：

| 系統 | C/A/P 選擇 | 典型應用 |
|------|------------|----------|
| 強一致性系統 | C + P | 銀行業務、分散式資料庫 |
| 高可用系統 | A + P | 網頁暫存、CDN |
| 最終一致系統 | A + C | NoSQL、Cassandra |

## 一致性模型

### 強一致性

所有節點在同一時刻看到相同的資料：

```python
# 強一致性範例
def transfer_strong(src, dst, amount):
    # 鎖定帳戶
    lock(src)
    lock(dst)
    
    src.balance -= amount
    dst.balance += amount
    
    unlock(src)
    unlock(dst)
    # 全域同步完成後才返回
```

### 最終一致性

允許暫時的不一致，但最終會達成一致：

```python
# 最終一致性範例（採用事件溯源）
def transfer_eventual(src, dst, amount):
    event = TransferEvent(src, dst, amount)
    # 寫入本地日誌，立即返回
    append_to_log(event)
    
    # 背景同步到其他節點
    background_sync()
    # 最終所有節點都會看到相同結果
```

### 不同的一致性級別

```
一致性級別光譜：
────────────────────────────────

強一致性  ───►  最終一致性

│         │         │         │         │
Sync      Sequential  Causal   Eventual  Weak
Weak      Serializability  Eventual   Any
一致性

範例：
- 強一致性：線性化所有操作
- 順序一致性：每個客戶端看到操作順序一致
- 因果一致性：因果相關的操作順序一致
- 最終一致性：只要沒有新更新，最終會一致
- 弱一致性：只有確定性保證
```

## 失敗模型

### 失敗類型

分散式系統中的節點可能以多種方式失敗：

```
失敗模型分級：
────────────────────────────────

1. 停頓失敗（Fail-Stop）
   └── 節點停止工作，容易偵測
   
2. 崩潰失敗（Crash Failure）
   └── 節點停止回應，但無法區分停頓和崩潰
   
3. 遺漏失敗（Omission Failure）
   └── 節點無法成功發送或接收訊息
   
4. 任意失敗（Byzantine Failure）
   └── 節點可能發送任意錯誤的訊息
   └── 最難處理的失敗類型
```

### 容錯策略

```python
# 冗餘和備份
class ReplicatedService:
    def __init__(self, replicas):
        self.replicas = replicas  # 多個副本
    
    def write(self, value):
        # 寫入所有副本
        for replica in self.replicas:
            replica.write(value)
    
    def read(self):
        # 讀取多數副本
        results = [r.read() for r in self.replicas]
        # 多數決
        return majority(results)
```

## 時鐘和順序

### 分散式系統中的時間問題

在分散式系統中，確定事件的全局順序是一個根本挑戰：

```
實體時鐘的問題：
────────────────────────────────

節點 A                              節點 B
│                                  │
│  事件 1 (T=10:00:00.100)         │
│─────────────────────▶            │
│                                  │
│          ◀─────────────────      │
│          事件 2 (T=10:00:00.050) │  ⚠️ T2 < T1 但 B 收到較早
│                                  │
問題：A 和 B 的時鐘可能不同步！
```

### 邏輯時鐘

```python
# Lamport 時鐘
class LamportClock:
    def __init__(self):
        self.time = 0
    
    def tick(self):
        self.time += 1
        return self.time
    
    def update(self, received_time):
        self.time = max(self.time, received_time) + 1
        return self.time

# 事件比較
def happened_before(event1, event2):
    return event1.lamport_time < event2.lamport_time
```

## 延伸閱讀

- [分散式系統經典教材](https://www.google.com/search?q=distributed+systems+textbook+安德魯)
- [CAP 定理解釋](https://www.google.com/search?q=CAP+theorem+Brewer+explained)
- [一致性模型比較](https://www.google.com/search?q=consistency+models+distributed+systems)
- [分散式時鐘](https://www.google.com/search?q=lamport+logical+clock+distributed+systems)
- [故障容錯機制](https://www.google.com/search?q=fault+tolerance+distributed+systems)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」歷史回顧系列之一。*