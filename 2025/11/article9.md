# 可擴展性設計模式

## 六大經典模式讓你的系統輕鬆擴展

## 為什麼需要可擴展性？

可擴展性（Scalability）是指系統在增加資源後，能夠相應地提升處理能力的能力。沒有好的可擴展性設計，即使增加再多的伺服器，效能也可能無法線性提升。

```
理想情況：
  2 倍資源 → 2 倍吞吐量
  4 倍資源 → 4 倍吞吐量

現實情況（沒有好的設計）：
  2 倍資源 → 1.5 倍吞吐量
  4 倍資源 → 2 倍吞吐量（邊際效益遞減）
```

---

## 模式一：水平擴展（Horizontal Scaling）

### 概念

增加更多機器來分擔工作負載。

```
垂直擴展（Scale Up）：
  單台 64 核心伺服器 → $10,000/月

水平擴展（Scale Out）：
  8 台 8 核心伺服器 → $1,000/月 × 8 = $8,000/月（更便宜）
```

### 實現要點

- **無狀態設計**：伺服器不儲存用戶狀態
- **共用儲存**：所有伺服器存取同一資料來源
- **負載平衡**：均勻分發請求

---

## 模式二：快取（Caching）

將昂貴計算或頻繁存取的資料暫存在高速儲存中。

```python
# 未使用快取
def get_user_orders(user_id):
    return db.query(Order).filter(Order.user_id == user_id).all()
    # 每次查詢 ~50ms

# 使用快取
def get_user_orders(user_id):
    cache_key = f"orders:{user_id}"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)  # ~1ms
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    redis.setex(cache_key, 300, json.dumps(orders))
    return orders
```

### 快取層次

```
瀏覽器快取（最快，容量最小）
  → CDN 快取（次快，分佈全球）
    → 應用快取（Redis/Memcached）
      → 資料庫快取（InnoDB Buffer Pool）
        → 磁碟（最慢，容量最大）
```

---

## 模式三：非同步處理（Asynchronous Processing）

將耗時操作移到背景執行，避免阻塞請求。

### 同步 vs 非同步

```
同步處理（用戶等待）：
  請求 → 驗證 → 寫入資料庫 → 發送 Email → 回傳回應
  總時間：100ms + 2000ms（Email）= 2100ms

非同步處理（即時回應）：
  請求 → 驗證 → 寫入資料庫 → 將 Email 任務放入佇列 → 回傳回應
  總時間：100ms + 5ms（入隊）= 105ms
  → Email 在背景發送（+2000ms，不影響用戶）
```

### 消息佇列實現

```python
# 同步版（不好）
def create_order(user_id, items):
    order = create_order_in_db(user_id, items)
    send_email(user_id, "訂單已建立")  # 可能花 2 秒
    update_recommendation(user_id, items)  # 可能花 5 秒
    return order

# 非同步版（好）
def create_order(user_id, items):
    order = create_order_in_db(user_id, items)
    queue.publish("email", {"user_id": user_id, "type": "order_created"})
    queue.publish("recommendation", {"user_id": user_id, "items": items})
    return order
```

---

## 模式四：資料庫分片（Sharding）

將大型資料庫拆分為多個較小的資料庫。

### 分片鍵選擇

```python
# 好的分片鍵：user_id（均勻分佈且不可變）
shard_id = hash(user_id) % 8

# 不好的分片鍵：created_at（可能產生熱點）
# 所有新資料都集中在最近的分片
```

### 分片實現

```python
class ShardedDB:
    def __init__(self, shards):
        self.shards = shards

    def _get_shard(self, shard_key):
        return self.shards[hash(shard_key) % len(self.shards)]

    def save_user(self, user):
        shard = self._get_shard(user.id)
        shard.execute("INSERT INTO users ...", user)

    def get_user(self, user_id):
        shard = self._get_shard(user_id)
        return shard.query("SELECT * FROM users WHERE id = ?", user_id)
```

---

## 模式五：讀寫分離（Read Replicas）

主庫處理寫入，從庫處理讀取，分散資料庫負載。

```
寫入路徑：應用程式 → 主資料庫
讀取路徑：應用程式 → 從資料庫（x N 個）
```

```python
class ReadWriteRouter:
    def execute_write(self, query):
        return master.execute(query)

    def execute_read(self, query):
        slave = random.choice(self.slaves)
        return slave.execute(query)
```

---

## 模式六：服務拆分（Decomposition）

將單體應用拆分為更小的服務。

```
拆分策略：
  按功能：使用者服務、訂單服務、商品服務
  按流量：熱門功能獨立部署、冷門功能合併
  按團隊：每個團隊擁有自己的服務
```

### 拆分原則

```python
# 好的拆分：職責清晰
class OrderService:
    def create_order(self, user_id, items):
        return db.save(Order(user_id=user_id, items=items))

class InventoryService:
    def deduct(self, product_id, quantity):
        return db.update(Product, id=product_id, quantity=quantity - 1)

# 不好的拆分：過度碎片化
class OrderCreator: ...      # 只負責建立訂單
class OrderValidator: ...     # 只負責驗證
class OrderPricer: ...        # 只負責計算價格
```

---

## 可擴展性檢查清單

- [ ] 應用是無狀態的嗎？
- [ ] 資料庫讀取操作是否經過快取？
- [ ] 耗時操作是否非同步處理？
- [ ] 資料庫是否需要分片？
- [ ] 是否需要讀寫分離？
- [ ] 服務是否按業務領域拆分？
- [ ] 是否有水平擴展的機制？
- [ ] 監控系統能否識別瓶頸？

---

## 實際案例：電商平台可擴展性方案

```
瓶頸識別：
  1. 商品詳情頁（大量讀取）→ CDN + Redis 快取
  2. 下單流程（大量寫入）→ 訊息佇列非同步處理
  3. 訂單查詢（資料量大）→ 資料庫分片 + 讀寫分離
  4. 搜尋功能（複雜查詢）→ Elasticsearch 獨立服務

改造前：單體應用，最大支撐 1000 QPS
改造後：微服務架構，最大支撐 100000 QPS
```

---

## 延伸閱讀

- [Scalability Patterns](https://www.google.com/search?q=scalability+patterns+distributed+systems)
- [Designing Data-Intensive Applications](https://www.google.com/search?q=Designing+Data-Intensive+Applications+book)
- [Scalable Web Architecture](https://www.google.com/search?q=scalable+web+architecture+patterns)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之九。*
