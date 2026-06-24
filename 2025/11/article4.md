# Redis 快取實戰

## 從基礎配置到進階策略

## Redis 基礎

Redis 是一個記憶體中鍵值資料庫，以極高的讀寫速度（每秒數十萬次操作）而聞名。

### 安裝與啟動

```bash
# macOS
brew install redis
brew services start redis

# Docker
docker run --name redis -p 6379:6379 -d redis:7

# 連線測試
redis-cli ping
# PONG
```

### Python 連線

```python
import redis

r = redis.Redis(host="localhost", port=6379, db=0)

# 基本操作
r.set("key", "value")
print(r.get("key"))  # b'value'
```

---

## 資料型態與使用場景

### String（字串）

最基本的型態，適合快取序列化物件。

```python
import json

user = {"id": 1, "name": "Alice", "email": "alice@example.com"}
r.setex(f"user:{user['id']}", 3600, json.dumps(user))
# 1 小時後自動過期

cached = r.get("user:1")
if cached:
    user = json.loads(cached)
```

### List（列表）

適合實作訊息佇列、時間線。

```python
# 生產者
r.lpush("queue:orders", "order-001")
r.lpush("queue:orders", "order-002")

# 消費者
while True:
    order = r.brpop("queue:orders", timeout=5)
    if order:
        print(f"Processing {order}")
```

### Set（集合）

適合標籤、去重、共同好友。

```python
# 用戶關注
r.sadd("user:1:follows", "user:2", "user:3")
r.sadd("user:2:follows", "user:1", "user:3")

# 共同關注
common = r.sinter("user:1:follows", "user:2:follows")
print(common)  # {b'user:3'}
```

### Sorted Set（有序集合）

適合排行榜、延遲佇列。

```python
# 遊戲排行榜
r.zadd("leaderboard", {"player1": 1000, "player2": 2000, "player3": 1500})

# 前十名
top10 = r.zrevrange("leaderboard", 0, 9, withscores=True)
print(top10)  # [(b'player2', 2000.0), (b'player3', 1500.0), ...]
```

### Hash（哈希）

適合物件儲存，可以單獨存取欄位。

```python
r.hset("user:1", mapping={"name": "Alice", "email": "a@example.com"})
print(r.hget("user:1", "name"))     # b'Alice'
print(r.hgetall("user:1"))          # 所有欄位
```

---

## 快取策略實作

### Cache-Aside 模式

```python
class ProductService:
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db

    def get_product(self, product_id):
        cache_key = f"product:{product_id}"
        # 1. 先查快取
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        # 2. 未命中，查資料庫
        product = self.db.query(Product).get(product_id)
        if product:
            # 3. 寫入快取
            self.redis.setex(cache_key, 1800, json.dumps(product.to_dict()))
        return product

    def update_product(self, product_id, data):
        # 4. 更新資料庫
        self.db.query(Product).filter_by(id=product_id).update(data)
        # 5. 使快取失效
        self.redis.delete(f"product:{product_id}")
```

### 快取穿透防護

使用布隆過濾器（Bloom Filter）：

```python
class BloomFilter:
    def __init__(self, redis, key, size=1000000, hash_count=7):
        self.redis = redis
        self.key = key
        self.size = size
        self.hash_count = hash_count

    def add(self, item):
        for i in range(self.hash_count):
            pos = hash(f"{i}:{item}") % self.size
            self.redis.setbit(self.key, pos, 1)

    def contains(self, item):
        for i in range(self.hash_count):
            pos = hash(f"{i}:{item}") % self.size
            if not self.redis.getbit(self.key, pos):
                return False
        return True

bloom = BloomFilter(redis_client, "bloom:users")
bloom.add("user:1001")
print(bloom.contains("user:1001"))  # True
print(bloom.contains("user:9999"))  # False（一定不存在）
```

### 熱點 Key 保護

```python
import time
import threading

class HotKeyProtection:
    def __init__(self, redis):
        self.redis = redis
        self.local_cache = {}
        self.lock = threading.Lock()

    def get_hot_data(self, key, db_func, ttl=60):
        # 1. 檢查本地快取
        with self.lock:
            if key in self.local_cache:
                data, exp = self.local_cache[key]
                if time.time() < exp:
                    return data

        # 2. 檢查 Redis
        data = self.redis.get(key)
        if data:
            with self.lock:
                self.local_cache[key] = (data, time.time() + ttl // 2)
            return data

        # 3. 查資料庫（分散式鎖保護）
        lock_key = f"lock:{key}"
        if self.redis.setnx(lock_key, "1"):
            self.redis.expire(lock_key, 5)
            data = db_func()
            self.redis.setex(key, ttl, data)
            self.redis.delete(lock_key)
            return data

        # 4. 未取得鎖，等快取更新
        time.sleep(0.05)
        return self.get_hot_data(key, db_func, ttl)
```

---

## 記憶體管理

### 最大記憶體與淘汰策略

```bash
# redis.conf 配置
maxmemory 4gb
maxmemory-policy allkeys-lru
```

**淘汰策略**：
- `noeviction`：寫入時回傳錯誤
- `allkeys-lru`：淘汰最近最少使用的 key
- `allkeys-lfu`：淘汰最不常用的 key
- `volatile-ttl`：淘汰 TTL 最短的 key

### 節省記憶體

```python
# 使用壓縮
r.set("large_key", compressed_data)

# 使用 hash 儲存多個欄位（比多個 string 省記憶體）
r.hset("user:1", "name", "Alice")
r.hset("user:1", "email", "a@example.com")
```

---

## 高可用配置

### 主從複寫

```bash
# slave 設定
replicaof 192.168.1.10 6379
```

### Sentinel 高可用

```python
from redis.sentinel import Sentinel

sentinel = Sentinel([("localhost", 26379)], socket_timeout=0.1)
master = sentinel.master_for("mymaster")
slave = sentinel.slave_for("mymaster")
```

### Redis Cluster

```python
from redis.cluster import RedisCluster

rc = RedisCluster(host="127.0.0.1", port=7000)
rc.set("key", "value")
print(rc.get("key"))
```

---

## 效能監控

```bash
# 監控命令
redis-cli info      # 伺服器資訊
redis-cli monitor   # 即時命令監控
redis-cli slowlog   # 慢查詢
redis-cli --stat    # 統計資訊
```

---

## 延伸閱讀

- [Redis Official Documentation](https://www.google.com/search?q=Redis+official+documentation)
- [Redis Caching Patterns](https://www.google.com/search?q=Redis+caching+patterns+best+practices)
- [Redis Performance Tuning](https://www.google.com/search?q=Redis+performance+tuning+optimization)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之四。*
