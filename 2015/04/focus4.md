# 主題四：Redis 3.0 叢集功能

## Redis 3.0 概述

Redis 3.0 在 2015 年 4 月正式發布，這是 Redis 發展史上最重要的版本之一。最大的亮點是原生支援 Redis Cluster，實現了多年來社群期待的分散式功能。

在此之前，Redis 的分散式部署需要依賴第三方工具如 Twemproxy 或 Redis Sentinel，現在有了官方標準解決方案。

## Redis Cluster 架構

### 分散式哈希槽

Redis Cluster 將所有資料分為 16384 個哈希槽（Hash Slot）。每個節點負責維護一部分槽，資料根據鍵的哈希值自動分發到相應的節點。

```
槽分佈範例（6 節點叢集）：
- 節點 1：槽 0-2730
- 節點 2：槽 2731-5460
- 節點 3：槽 5461-8190
- 節點 4：槽 8191-10920
- 節點 5：槽 10921-13650
- 節點 6：槽 13651-16383
```

這種設計的優點：
- 新增節點時只需重新分配部分槽
- 客戶端可以直接聯繫目標節點
- 無需代理層，延遲更低

### 自動分片

Redis Cluster 自動將資料分片到多個節點。客戶端可以連接任何一個節點，節點會返回正確的目標節點資訊，客戶端直接存取目標節點。

```python
# Redis Cluster 客戶端範例
import redis

# 連接到叢集中的任一節點
cluster = redis.RedisCluster(
    host='localhost',
    port=7000,
    skip_full_coverage_check=True
)

# 客戶端自動處理分片
cluster.set('key1', 'value1')
cluster.set('key2', 'value2')
value = cluster.get('key1')
```

### 失敗偵測與自動轉移

Redis Cluster 使用 Gossip 協定進行節點間的通訊和失敗偵測。當主節點失敗時，從節點會自動投票選舉，失敗的主節點會被從節點取代。

失敗轉移的流程：
1. 節點定期發送 Ping/Pong 訊息
2. 當一個節點超過閾值時間沒有回應，標記為疑似失敗
3. 其他節點投票確認失敗
4. 從節點發起選舉，獲得大多數票的成為新主節點

## 客戶端支援

Redis 3.0 發布時，已有多种語言的客戶端支援 Cluster：

- **Python**：redis-py 3.0+ 支援 Cluster
- **Java**：Jedis 3.0+ 支援 Cluster
- **Node.js**：ioredis 支援 Cluster
- **Ruby**：ruby-pICluster 支援

使用 Cluster 時，客戶端需要支援 MOVED 和 ASK 指令來處理資料重導向。

## 叢集限制

Redis Cluster 有一些設計上的限制：

### 操作的原子性

多鍵操作（如交集、聯集）只能在同一個節點內執行。跨節點的 Lua 腳本也只有在所有鍵都在同一個節點時才能保證原子性。

### 插槽過期

Redis Cluster 不支援在不同插槽之間搬遷單一鍵。雖然可以使用 `CLUSTER SETSLOT` 命令手動遷移插槽，但過程比較複雜。

### 必要的節點數量

Redis Cluster 至少需要 3 個主節點才能正常運作（為了確保大多數投票）。

## 部署架構建議

### 最小生產部署

生產環境建議至少使用 6 節點（3 主 3 從）：

```
主節點：
- 7000 (master) -> 7003 (slave)
- 7001 (master) -> 7004 (slave)
- 7002 (master) -> 7005 (slave)
```

### 跨機架部署

為提高可用性，建議將節點分散到不同的機架或可用區域。

```bash
# 啟動 Redis Cluster 節點
redis-server --port 7000 --cluster-enabled yes --cluster-config-file nodes.conf
redis-server --port 7001 --cluster-enabled yes --cluster-config-file nodes.conf
# ... 更多節點

# 建立叢集
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
    127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 --cluster-replicas 1
```

## 與哨兵模式的比較

Redis Sentinel 仍然是高可用性的有效方案，適合不需要分片的場景。Cluster 和 Sentinel 的選擇：

| 特性 | Sentinel | Cluster |
|------|----------|---------|
| 資料分片 | 不支援 | 支援（16384 槽） |
| 寫入可用性 | 取決於配置 | 主節點可寫入 |
| 最小節點 | 1 主 + 至少 1 從 | 至少 3 主 |
| 故障轉移 | 哨兵投票決定 | 叢集內投票 |
| 應用場景 | 讀寫分離 | 水平擴展 |

Redis 3.0 Cluster 的發布，讓 Redis 從一個記憶體快取進化為完整的分散式資料庫解決方案。