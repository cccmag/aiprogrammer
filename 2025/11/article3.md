# 負載平衡演算法

## 深入解析與程式碼實現

## 輪詢（Round-Robin）

最直觀的演算法，將請求依序分配給每台伺服器。

### 實作

```python
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.index = 0

    def next(self):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server

# 測試
lb = RoundRobin(["srv-a", "srv-b", "srv-c"])
for i in range(6):
    print(f"req-{i} → {lb.next()}")
# req-0 → srv-a
# req-1 → srv-b
# req-2 → srv-c
# req-3 → srv-a
# req-4 → srv-b
# req-5 → srv-c
```

### 加權輪詢（Weighted Round-Robin）

為不同效能的伺服器設定權重。

```python
class WeightedRoundRobin:
    def __init__(self, servers, weights):
        self.servers = servers
        self.weights = weights
        self.current = 0
        self.gcd = self._gcd_all(weights)

    def _gcd_all(self, nums):
        import math
        return math.gcd(*nums)

    def next(self):
        while True:
            for i, server in enumerate(self.servers):
                if self.weights[i] >= self.current:
                    self.current += 1
                    if self.current > max(self.weights):
                        self.current = 1
                    return server
            self.current += 1

# 測試：srv-a 權重 3，srv-b 權重 2，srv-c 權重 1
lb = WeightedRoundRobin(["srv-a", "srv-b", "srv-c"], [3, 2, 1])
# 每 6 個請求的分配：a, a, a, b, b, c
```

---

## 最少連接（Least Connections）

將請求分配給當前活躍連接數最少的伺服器。

```python
class LeastConnections:
    def __init__(self, servers):
        self.connections = {s: 0 for s in servers}

    def next(self):
        server = min(self.connections, key=self.connections.get)
        self.connections[server] += 1
        return server

    def release(self, server):
        self.connections[server] = max(0, self.connections[server] - 1)

# 模擬：長連接場景
lb = LeastConnections(["srv-a", "srv-b", "srv-c"])
# 假設 srv-a 已有 5 個連接，srv-b 有 3 個，srv-c 有 0 個
lb.connections = {"srv-a": 5, "srv-b": 3, "srv-c": 0}
print(lb.next())  # srv-c（最少連接）
print(lb.next())  # srv-c（還是最少，因為剛分配一個）
```

### 何時使用最少連接？

- 請求處理時間差異大（部分請求複雜、部分簡單）
- 保持連線模式（WebSocket、資料庫連接池）
- HTTP/2 多路複用場景

---

## IP Hash

根據客戶端 IP 的 Hash 值決定伺服器，保證同一客戶端總是發送到同一伺服器。

```python
class IPHash:
    def __init__(self, servers):
        self.servers = servers

    def next(self, client_ip):
        hash_val = hash(client_ip) % len(self.servers)
        return self.servers[hash_val]

lb = IPHash(["srv-a", "srv-b", "srv-c"])
print(lb.next("192.168.1.1"))  # 總是 → srv-b
print(lb.next("192.168.1.1"))  # 總是 → srv-b
print(lb.next("192.168.1.2"))  # 總是 → srv-c
```

### 一致性 Hash（Consistent Hashing）

解決 IP Hash 在伺服器增減時大量重新分配的問題。

```python
import hashlib

class ConsistentHash:
    def __init__(self, servers, virtual_nodes=10):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        for server in servers:
            self._add_server(server)

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def _add_server(self, server):
        for i in range(self.virtual_nodes):
            node_key = f"{server}:{i}"
            pos = self._hash(node_key)
            self.ring[pos] = server

    def get_server(self, key):
        if not self.ring:
            return None
        pos = self._hash(key)
        sorted_keys = sorted(self.ring.keys())
        for k in sorted_keys:
            if pos <= k:
                return self.ring[k]
        return self.ring[sorted_keys[0]]
```

一致性 Hash 確保：
- 移除一台伺服器時，只有該伺服器負責的請求被重新分配
- 新增一台伺服器時，只有部分請求需要重新分配
- 虛擬節點（Virtual Nodes）解決資料傾斜問題

---

## 隨機（Random）

隨機選取一台伺服器。

```python
import random

class RandomLB:
    def __init__(self, servers):
        self.servers = servers

    def next(self):
        return random.choice(self.servers)
```

當請求數量足夠大時，隨機分配的效果接近均勻分佈。適合所有伺服器配置相同的情況。

---

## 地理感知（Geo-aware）

根據用戶的地理位置分配最近的伺服器。

```
用戶在東京 ──→ 東京資料中心（延遲 5ms）
用戶在紐約 ──→ 紐約資料中心（延遲 5ms）
用戶在倫敦 ──→ 法蘭克福資料中心（延遲 10ms）
```

**實作方式**：
- DNS Geo-Routing：根據來源 IP 解析不同的 DNS 結果
- Anycast：多個節點共享同一 IP，路由協議自動選擇最近的

---

## 演算法比較

| 演算法 | 均勻性 | 狀態需求 | 伺服器變動影響 | 適用場景 |
|--------|--------|---------|--------------|---------|
| Round-Robin | 高 | 無 | 小 | 伺服器配置相同 |
| Weighted Round-Robin | 依權重 | 無 | 小 | 伺服器配置不同 |
| Least Connections | 動態 | 有 | 小 | 長連接、處理時間不等 |
| IP Hash | 依 Hash | 無 | 大 | Session 黏性 |
| Consistent Hash | 依 Hash | 無 | 小 | 分散式快取 |
| Random | 漸進 | 無 | 小 | 簡單場景 |

---

## 實戰建議

### 多層負載平衡

```text
Global LB（DNS/Anycast）
  └──→ Regional LB（Nginx/HAProxy）
        └──→ Service Mesh（Envoy/Istio）
              └──→ 應用例項
```

### 健康檢查整合

負載平衡演算法必須與健康檢查配合，將不健康的伺服器從候選清單中移除。

```python
class HealthCheck:
    def __init__(self, servers, check_interval=10):
        self.servers = {s: True for s in servers}
        self.check_interval = check_interval

    def mark_down(self, server):
        self.servers[server] = False

    def get_healthy_servers(self):
        return [s for s, alive in self.servers.items() if alive]
```

---

## 延伸閱讀

- [Load Balancing Algorithms](https://www.google.com/search?q=load+balancing+algorithms+comparison)
- [Consistent Hashing Explained](https://www.google.com/search?q=consistent+hashing+algorithm+explained)
- [NGINX Load Balancing](https://www.google.com/search?q=nginx+load+balancing+algorithms+configuration)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之三。*
