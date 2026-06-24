# Redis 3.0 叢集架構指南

## 前言

Redis 3.0 最重要的新功能是原生支援 Redis Cluster，使得 Redis 終於有了官方的分散式解決方案。本文將詳細介紹如何規劃、部署和管理 Redis Cluster。

## Redis Cluster 核心概念

### 插槽分發

Redis Cluster 將整個鍵空間分為 16384 個槽。當你執行 `SET key value` 時，Redis 會計算 `CRC16(key) mod 16384` 來決定將鍵放到哪個槽。

```
鍵到槽的映射：
key = "user:1000"
slot = CRC16("user:1000") mod 16384 = 12539
槽 12539 位於某個特定的節點上
```

### 客戶端重導向

客戶端連接到任意節點，如果該節點不是目標鍵所在的槽，會回應 `MOVED` 錯誤告知客戶端正確的節點。

```
GET user:1000
-> REDIRECT 12539 127.0.0.1:7002
```

先進的客戶端會快取這些映射，自動找到正確的節點。

## 部署規劃

### 最小架構

生產環境建議最少 6 個節點（3 主 3 從）：

```bash
# 每個節點的設定（redis.conf）
port 7000
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 15000
appendonly yes

# 資料目錄
dir /data/redis
```

### 網路拓撲建議

```
客戶端
   |
   v
[Redis Cluster]
   |
   +-- 7000 (master) -> 7003 (slave)
   +-- 7001 (master) -> 7004 (slave)
   +-- 7002 (master) -> 7005 (slave)
```

## 叢集建立與管理

### 建立叢集

```bash
# 使用 redis-cli 建立叢集
redis-cli --cluster create \
    127.0.0.1:7000 \
    127.0.0.1:7001 \
    127.0.0.1:7002 \
    127.0.0.1:7003 \
    127.0.0.1:7004 \
    127.0.0.1:7005 \
    --cluster-replicas 1

# 輸出範例：
# >>> Creating cluster
# [OK] All 16384 slots covered
```

### 驗證叢集狀態

```bash
# 檢視叢集資訊
redis-cli -p 7000 cluster info

# 檢視節點列表
redis-cli -p 7000 cluster nodes

# 測試連接
redis-cli -p 7000 cluster slots
```

### 新增節點

```bash
# 1. 啟動新節點
redis-server --port 7006 --cluster-enabled yes

# 2. 新增為主節點
redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000

# 3. 重新分發槽（可選）
redis-cli --cluster reshard 127.0.0.1:7000
```

## Python 客戶端實作

```python
import redis

class RedisClusterClient:
    def __init__(self, nodes):
        self.nodes = nodes
        self.clients = {
            f"node_{i}": redis.Redis(
                host=node['host'],
                port=node['port'],
                decode_responses=True
            ) for i, node in enumerate(nodes)
        }

    def set(self, key, value):
        """自動分發到正確的節點"""
        slot = self._get_slot(key)
        node = self._get_node_for_slot(slot)
        return self.clients[node].set(key, value)

    def get(self, key):
        """從正確的節點讀取"""
        slot = self._get_slot(key)
        node = self._get_node_for_slot(slot)
        return self.clients[node].get(key)

    def _get_slot(self, key):
        """計算 CRC16 並取模"""
        # 簡化版本，實際應使用完整的 CRC16 演算法
        return hash(key) % 16384

    def _get_node_for_slot(self, slot):
        """根據槽決定節點"""
        node_index = slot % len(self.clients)
        return f"node_{node_index}"


# 使用範例
cluster = RedisClusterClient([
    {'host': 'localhost', 'port': 7000},
    {'host': 'localhost', 'port': 7001},
    {'host': 'localhost', 'port': 7002}
])

cluster.set('name', 'Redis Cluster')
print(cluster.get('name'))
```

## 故障處理

### 自動失敗轉移

當主節點失敗時，對應的從節點會自動選舉為新的主節點：

```bash
# 模擬主節點失敗
redis-cli -p 7000 debug segfault

# 檢查叢集狀態
sleep 10
redis-cli -p 7003 cluster nodes  # 7003 應該已成為主節點
```

### 手動故障轉移

可用於預定維護升級：

```bash
# 在從節點上執行
redis-cli -p 7003 cluster failover
```

## 監控與維護

### 重要監控指標

- **叢集健康**：所有槽都有對應的主節點
- **節點狀態**：所有節點都應該是 `fail` 狀態以外
- **複製延遲**：從節點的複製是否跟得上主節點
- **記憶體使用**：確保沒有節點記憶體不足

### 常見問題處理

```bash
# 節點無法加入：檢查網路和防火牆
# 槽分配不均：使用 redis-cli --cluster rebalance
# 客戶端連線過多：調整 maxclients
```

## 結論

Redis Cluster 為 Redis 提供了原生的分散式能力。雖然有一些限制（如多鍵操作的約束），但對於大多數使用場景，這是一個穩定可靠的解決方案。