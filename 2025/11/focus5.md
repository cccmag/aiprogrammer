# 資料庫分片與複寫

## 水平擴展的關鍵

當單一資料庫無法支撐業務成長時，有兩種主要的擴展手段：複寫（Replication）和分片（Sharding）。複寫側重於讀取擴展和高可用性，分片則針對寫入擴展和資料量限制。

---

## 主從複寫

### 基本架構

```
         ┌───────────┐
         │   Master   │（可讀可寫）
         └─────┬─────┘
               │ 非同步/同步複製
      ┌────────┼────────┐
      │        │        │
  ┌───▼──┐ ┌───▼──┐ ┌───▼──┐
  │Slave1 │ │Slave2 │ │Slave3 │
  │唯讀   │ │唯讀   │ │唯讀   │
  └──────┘ └──────┘ └──────┘
```

### 複寫模式

**非同步複寫**：Master 寫入後立即回覆客戶端，後續非同步同步到 Slave。

```
寫入時間：10ms（僅寫入 Master）
資料風險：Master 當機時，未同步的資料可能丟失
適用場景：對資料安全性要求不高的讀多寫少場景
```

**同步複寫**：所有 Slave 都確認寫入後，Master 才回覆客戶端。

```
寫入時間：50ms（等待所有 Slave 確認）
資料風險：零（所有節點一致）
適用場景：需要強一致性的場景
```

**半同步複寫**：至少一個 Slave 確認後回覆。

```
折衷方案：效能和一致性的平衡點
```

### 讀寫分離

```python
class DatabaseRouter:
    def __init__(self):
        self.master = "master-db:3306"
        self.slaves = ["slave1-db:3306", "slave2-db:3306"]

    def write(self, query, params):
        return execute(self.master, query, params)

    def read(self, query, params):
        slave = random.choice(self.slaves)
        return execute(slave, query, params)
```

---

## 資料庫分片

將資料水平拆分到多個資料庫節點上。

### 分片策略

**基於 Key 的分片（Hash Sharding）**

```
shard_id = hash(user_id) % 4

user_id = 1001 → hash % 4 = 1 → Shard 1
user_id = 1002 → hash % 4 = 2 → Shard 2
user_id = 1003 → hash % 4 = 3 → Shard 3
user_id = 1004 → hash % 4 = 0 → Shard 0
```

**優點**：資料均勻分佈
**缺點**：增加節點時需要重新分片（Resharding）

**基於範圍的分片（Range Sharding）**

```
Shard 0: user_id 1 ~ 1,000,000
Shard 1: user_id 1,000,001 ~ 2,000,000
Shard 2: user_id 2,000,001 ~ 3,000,000
```

**優點**：範圍查詢效率高、新增節點容易
**缺點**：資料可能不均勻（熱點問題）

**基於目錄的分片（Directory Sharding）**

```
查詢目錄服務 → 獲得資料所在的分片

lookup_table = {
    "user:1001": "Shard 1",
    "user:1002": "Shard 2",
}
```

**優點**：靈活性最高
**缺點**：目錄服務可能成為瓶頸和單點故障

---

## 一致性挑戰

### 分散式事務

跨分片的寫入操作需要保證原子性。

**兩階段提交（2PC）**
```
Phase 1: Prepare — 所有節點準備好
Phase 2: Commit — 所有節點提交
```

**Saga 模式**
```
Step 1: 扣庫存（成功）
  Step 2: 建立訂單（成功）
    Step 3: 扣款（失敗）
      → 補償：恢復庫存
      → 補償：取消訂單
```

---

## 路由策略

### 應用層路由

應用程式根據分片鍵直接選擇資料庫。

```python
def get_shard(user_id):
    shard_id = hash(user_id) % 4
    return shards[shard_id]
```

### 中間層路由

使用 Proxy 自動路由，如 ProxySQL、Vitess。

```
應用程式 → Proxy（自動路由） → 資料庫分片
```

### 分片鍵的選擇

好的分片鍵需要滿足：
1. **均勻分佈**：避免某些分片過熱
2. **查詢友好**：大部分查詢包含分片鍵
3. **不可變**：用戶 ID 比用戶名好（用戶名可能改變）

---

## 實際案例：用戶系統分片

```python
class UserService:
    SHARD_COUNT = 8

    def get_shard_id(self, user_id):
        return user_id % self.SHARD_COUNT

    def get_shard_connection(self, shard_id):
        return connections[shard_id]

    def create_user(self, name, email):
        user_id = self.next_id()  # 全域唯一 ID
        shard_id = self.get_shard_id(user_id)
        conn = self.get_shard_connection(shard_id)
        conn.execute(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            user_id, name, email
        )
        return user_id

    def get_user(self, user_id):
        shard_id = self.get_shard_id(user_id)
        conn = self.get_shard_connection(shard_id)
        return conn.query(
            "SELECT * FROM users WHERE id = ?",
            user_id
        )
```

---

## 常見陷阱

1. **跨分片 Join**：避免在應用層做跨分片的關聯查詢
2. **分片鍵變更**：一旦分片，分片鍵不應變更
3. **熱點問題**：部分用戶資料量特別大時需要二次分片
4. **備份與恢復**：分片環境的備份比單機複雜得多

---

## 延伸閱讀

- [Database Sharding Explained](https://www.google.com/search?q=database+sharding+patterns+and+strategies)
- [Master-Slave Replication](https://www.google.com/search?q=master+slave+database+replication+patterns)
- [Consistent Hashing](https://www.google.com/search?q=consistent+hashing+distributed+systems)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」系統設計系列之五。*
