# Replica Set 與分片：MongoDB 的擴展

## 副本集（Replica Set）

### 副本集概念

```markdown
副本集是 MongoDB 的高可用性解決方案：

               Primary
              ┌─────┐
              │  W  │
              └──┬──┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌───────┐   ┌───────┐   ┌───────┐
│Sec. 1 │   │Sec. 2 │   │Arbiter│
│  R    │   │  R    │   │       │
└───────┘   └───────┘   └───────┘

特點：
- 1 個 Primary（主節點）
- 2+ 個 Secondary（從節點）
- 自動故障轉移
- 讀寫分離可選
```

### 配置副本集

```python
# 初始化副本集
# 在 MongoDB Shell 中
config = {
    "_id": "myapp",
    "members": [
        {"_id": 0, "host": "mongo1:27017"},
        {"_id": 1, "host": "mongo2:27017"},
        {"_id": 2, "host": "mongo3:27017"}
    ]
}

rs.initiate(config)
rs.status()
```

### 複製原理

```python
# MongoDB 複製使用 oplog（操作日誌）

# 寫入 Primary
db.users.insert({"name": "張三", "age": 30})

# MongoDB 將操作寫入 oplog
# {
#   "ts": Timestamp(...),
#   "op": "i",
#   "ns": "myapp.users",
#   "o": {"_id": ObjectId(...), "name": "張三", "age": 30}
# }

# Secondary 讀取 oplog 並應用
# 這個過程是非同步的
```

### 故障轉移

```python
# 自動故障轉移

# 當 Primary 不可用時：
# 1. 自動選擇新的 Primary
# 2. 所有寫入轉向新的 Primary
# 3. 舊 Primary 恢復後成為 Secondary

# 應用層無需任何改變
# MongoDB 驅動程式自動處理
```

## 分片（Sharding）

### 分片概念

```markdown
分片是 MongoDB 的水平擴展解決方案：

┌─────────────────────────────────────────────────────────────┐
│                         路由器                               │
│                    （mongos 路由）                           │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌────────┐
│Shard 1 │  │Shard 2 │  │Shard 3 │
│  Chunk │  │  Chunk │  │  Chunk │
│  A-F   │  │  G-L   │  │  M-R   │
└────────┘  └────────┘  └────────┘

特點：
- 自動資料分散
- 負載均衡
- 對應用透明
```

### 分片鍵

```python
# 選擇分片鍵

# 基於使用者 ID 分片
db.users.ensure_index({"user_id": "hashed"})

# 開啟分片
sh.enableSharding("myapp")
sh.shardCollection("myapp.users", {"user_id": "hashed"})

# 查詢路由
# mongos 根據分片鍵將查詢路由到正確的分片
db.users.find({"user_id": "user123"})
# 只查詢包含 user123 的分片
```

### 分片策略

```python
# 1. 範圍分片
sh.shardCollection("myapp.orders", {"order_id": 1})

# 數據會根據 order_id 範圍分割
# chunk1: order_id < 1000
# chunk2: 1000 <= order_id < 2000

# 2. 雜湊分片
sh.shardCollection("myapp.users", {"user_id": "hashed"})

# 數據均勻分散
# 但範圍查詢效率較低
```

## 集群配置

### 生產環境配置

```python
# 生產環境 MongoDB 集群

# 配置伺服器（Config Server）
# 儲存集群元數據
# 通常 3 個

# 路由伺服器（mongos）
# 路由查詢
# 通常 2+ 個

# 分片伺服器（Shard）
# 實際資料儲存
# 通常 3+ 個

# 最小配置：
# - 3 個 config server
# - 2 個 mongos
# - 3 個 shard（每個 3 副本）
```

### 監控和管理

```python
# MongoDB 管理命令

# 查看分片狀態
sh.status()

# 查看副本集狀態
rs.status()

# 查看集合分片情況
db.printShardingStatus()

# 移動 chunk
sh.moveChunk("myapp.users", {"user_id": "user123"}, "shard2")
```

## 擴展考量

### 何時需要分片

```markdown
分片時機：

1. 單機磁碟不足
   - 磁碟使用量接近硬體限制

2. 寫入效能下降
   - 寫入量超過單機處理能力

3. 記憶體不足
   - 資料量超過記憶體容量

4. 延遲增加
   - 查詢延遲超過可接受範圍
```

### 分片限制

```python
# 分片的限制

# 1. 分片鍵選擇不當
# - 熱點分片（某個分片負擔過重）
# - 無法滿足特定查詢

# 2. 分散不均
# - chunk 遷移不及時
# - 某些分片過大

# 3. 查詢路由限制
# - 需要分片鍵的查詢才能路由
# - 全集合查詢需要掃描所有分片
```

## 結語

MongoDB 的副本集和分片機制提供了企業級的高可用性和水平擴展能力。2009 年的 MongoDB 1.0 雖然功能相對簡單，但已經奠定了這些基礎。

下一篇文章將討論 NoSQL 的未來發展趨勢。

---

## 延伸閱讀

- [MongoDB Replica Set](https://www.google.com/search?q=MongoDB+replica+set+2009)
- [MongoDB Sharding](https://www.google.com/search?q=MongoDB+sharding+explained)
- [分散式資料庫擴展](https://www.google.com/search?q=database+horizontal+scaling)

---

*本篇文章為「AI 程式人雜誌 2009 年 9 月號」焦點系列之一。*