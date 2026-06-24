# 訊息佇列與事件驅動

## 非同步解耦的核心

## 為什麼需要訊息佇列？

在同步請求-回應模型中，服務之間的耦合度很高。如果訂單服務在下單時需要同步呼叫庫存服務、支付服務、通知服務，那麼任何一個服務的延遲或故障都會阻塞整個請求。

```
同步呼叫（耦合度高）：
  下單請求 → 訂單服務 → 庫存服務（等待）
                       → 支付服務（等待）
                       → 通知服務（等待）
              總延遲 = 三者之合

非同步（解耦）：
  下單請求 → 訂單服務 → 發送「訂單已建立」事件
               ↓ 立即回應
    事件驅動：
      庫存服務 ← 消費事件 → 扣庫存
      支付服務 ← 消費事件 → 處理支付
      通知服務 ← 消費事件 → 發送通知
```

---

## 訊息佇列模型

### 點對點（Point-to-Point）

```
生產者 ──→ [佇列] ──→ 消費者（唯一）
```

每個訊息只被一個消費者處理。適合任務分配場景。

```
訂單處理：多個 worker 競爭消費
  [訂單佇列] ← Worker 1（處理 order-001）
             ← Worker 2（處理 order-002）
             ← Worker 3（處理 order-003）
```

### 發布-訂閱（Pub-Sub）

```
生產者 ──→ [Topic/Exchange] ──→ 消費者 A
                               ──→ 消費者 B
                               ──→ 消費者 C
```

每個訊息可以被多個消費者接收。適合事件廣播。

```
「用戶註冊」事件
  → 通知服務發送歡迎郵件
  → 分析服務記錄註冊事件
  → 推薦服務初始化用戶偏好
```

---

## 事件驅動架構

### 事件通知

服務在狀態變更時發布事件，不關心誰會消費。

```python
class OrderService:
    def create_order(self, user_id, items):
        order = Order(user_id=user_id, items=items)
        db.save(order)
        # 發布事件
        event_bus.publish("order.created", {
            "order_id": order.id,
            "user_id": user_id,
            "total": order.total
        })
        return order
```

### 事件攜帶狀態遷移

事件包含完整的狀態變更資訊，消費者可以據此更新自己的狀態。

```
order.created:
  { order_id, user_id, items, total, timestamp }
  
inventory.service 消費者：
  扣減庫存並記錄
  
notification.service 消費者：
  發送訂單確認通知
```

### CQRS（命令查詢責任分離）

將寫入操作（Command）和讀取操作（Query）分離，透過事件同步資料。

```
寫入端（Command Side）：
  寫入資料庫 → 發布事件
  
讀取端（Query Side）：
  監聽事件 → 更新讀取模型
  
查詢請求 → 讀取模型（快，已預先聚合）
```

---

## 最終一致性

### 什麼是最終一致性？

在分散式系統中，不同的資料副本不會立即一致，但經過足夠時間後最終會達成一致。

```
時間線：
  t0: 訂單服務建立訂單（狀態：paid）
  t1: 事件發布到佇列
  t2: 庫存服務消費事件（尚未更新）
  t3: 用戶查詢訂單（訂單狀態 paid ✅）
  t4: 庫存服務完成更新（庫存 -1）
  t5: 庫存查詢正確（✅）
  
  在 t2～t4 期間，庫存資料是「不一致」的
```

### 實現最終一致性的關鍵

**冪等性（Idempotency）**：同一事件處理多次，結果相同。

```python
def handle_order_created(event):
    # 使用事件 ID 去重
    if redis.sismember("processed_events", event.id):
        return  # 已經處理過
    deduct_inventory(event.items)
    redis.sadd("processed_events", event.id)
```

**重試機制**：處理失敗時自動重試。

```
第一次：處理失敗（資料庫超時）
第二次：處理成功
```

**補償事務**：失敗時執行逆向操作。

```
扣庫存成功 → 建立訂單失敗（信用卡問題）
→ 補償：恢復庫存（發送 compensate 事件）
```

---

## 訊息序保證

### 同一個 Partition/Queue 內有序

Kafka 保證同一個 Partition 內的訊息順序。

```
Partition 0: [msg1(訂單A), msg2(訂單A), msg3(訂單B)]
  → msg1 先於 msg2 被消費
  → msg3 可能在 msg2 前後（不同訂單，無所謂）
```

### 全局有序的代價

全局有序會限制效能，因為所有訊息必須經過單一節點。

```
全局有序（效能差）：
  所有訂單 → 單一 Partition → 單一消費者
  
按訂單 ID 分區（效能好）：
  訂單 A → Partition 0 → Consumer A
  訂單 B → Partition 1 → Consumer B
```

---

## 實際案例：電商事件流

```
用戶下單
  │
  ▼
訂單服務 → 發布 order.created
  │
  ├──→ 庫存服務：扣減庫存
  │     └──→ 庫存不足時發布 inventory.shortage
  │
  ├──→ 支付服務：處理付款
  │     └──→ 成功發布 payment.completed
  │     └──→ 失敗發布 payment.failed
  │
  ├──→ 通知服務：發送訂單確認
  │
  └──→ 分析服務：記錄事件用於後續分析
```

---

## 常見的訊息佇列系統

| 系統 | 模型 | 持久化 | 順序保證 | 典型場景 |
|------|------|--------|---------|---------|
| RabbitMQ | Queue/Exchange | 支援 | 單一 Queue | 任務分配 |
| Apache Kafka | Topic/Partition | 支援 | 單一 Partition | 事件串流 |
| AWS SQS | Queue | 支援 | 不保證 | 微服務解耦 |
| Redis Stream | Stream | 可選 | 有序 | 輕量級場景 |

---

## 延伸閱讀

- [Event-Driven Architecture](https://www.google.com/search?q=event+driven+architecture+patterns)
- [Message Queue Comparison](https://www.google.com/search?q=RabbitMQ+Kafka+comparison+message+queue)
- [CQRS Pattern](https://www.google.com/search?q=CQRS+command+query+responsibility+segregation)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」系統設計系列之六。*
