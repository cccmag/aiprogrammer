# 文章 6：Redis 快取策略

## 打造高效能的快取層

Redis 作為記憶體快取層，能顯著提升應用程式的回應速度。然而，不當的快取策略可能導致資料不一致或效能瓶頸。本文探討常見的快取策略與最佳實踐。

### 快取模式

#### Cache-Aside (延遲載入)

應用程式先檢查快取，找不到再查資料庫並寫入快取：

```javascript
import Redis from 'ioredis'
const redis = new Redis()

async function getUser(id) {
  const cacheKey = `user:${id}`

  // 1. 嘗試從快取讀取
  let user = await redis.get(cacheKey)
  if (user) return JSON.parse(user)

  // 2. 快取未命中，查詢資料庫
  user = await db.findUser(id)
  if (!user) return null

  // 3. 寫入快取，設定 TTL
  const ttl = 3600
  await redis.set(cacheKey, JSON.stringify(user), 'EX', ttl)

  return user
}
```

#### Write-Through (同步寫入)

每次寫入資料庫時同時更新快取：

```javascript
async function updateUser(id, data) {
  const cacheKey = `user:${id}`

  // 同時更新資料庫與快取
  const [user] = await Promise.all([
    db.updateUser(id, data),
    redis.set(cacheKey, JSON.stringify(data), 'EX', 3600)
  ])
  return user
}
```

#### Write-Behind (非同步寫入)

先寫入快取，非同步寫入資料庫：

```javascript
class WriteBehindCache {
  constructor(redis, db) {
    this.redis = redis
    this.db = db
    this.queue = []
    setInterval(() => this.flush(), 5000)
  }

  async set(key, value) {
    await this.redis.set(key, JSON.stringify(value), 'EX', 3600)
    this.queue.push({ key, value })
  }

  async flush() {
    while (this.queue.length > 0) {
      const batch = this.queue.splice(0, 100)
      await Promise.all(batch.map(item =>
        this.db.update(item.key, item.value)
      ))
    }
  }
}
```

### 常見問題與解決方案

#### 快取穿透

當大量請求查詢不存在的資料，繞過快取直接打到資料庫。

```javascript
async function safeGetUser(id) {
  const cacheKey = `user:${id}`

  let cached = await redis.get(cacheKey)
  if (cached !== null) {
    return cached === 'NULL' ? null : JSON.parse(cached)
  }

  const user = await db.findUser(id)
  // 空值也快取，但 TTL 較短
  const ttl = user ? 3600 : 60
  await redis.set(cacheKey, user ? JSON.stringify(user) : 'NULL', 'EX', ttl)
  return user
}
```

#### 快取雪崩

大量快取同時過期導致資料庫壓力暴增：

```javascript
// 使用隨機 TTL 分散過期時間
function getRandomTtl(base) {
  return base + Math.floor(Math.random() * base * 0.2)
}

// 使用本地備用快取 (多層快取)
class MultiLevelCache {
  constructor() {
    this.local = new Map()
  }

  async get(key) {
    // L1: 本地記憶體快取
    const local = this.local.get(key)
    if (local && local.expires > Date.now()) return local.value

    // L2: Redis 快取
    const redis = await redis.get(key)
    if (redis) {
      this.local.set(key, { value: JSON.parse(redis), expires: Date.now() + 10000 })
      return JSON.parse(redis)
    }

    return null
  }
}
```

### 快取失效策略

```javascript
// 主動失效
async function invalidateUser(id) {
  await redis.del(`user:${id}`)
  await redis.publish('cache:invalidate', `user:${id}`)
}

// 版本號快取
async function getVersionedData(key, version) {
  const cacheKey = `v${version}:${key}`
  let data = await redis.get(cacheKey)
  if (!data) {
    data = await db.fetchData(key)
    await redis.set(cacheKey, JSON.stringify(data), 'EX', 3600)
  }
  return JSON.parse(data)
}
```

### 監控與調校

```javascript
// 快取命中率監控
const stats = {
  hits: 0,
  misses: 0
}

async function monitoredGet(key) {
  const result = await redis.get(key)
  if (result !== null) {
    stats.hits++
    return JSON.parse(result)
  }
  stats.misses++
  return null
}

// 定期輸出命中率
setInterval(() => {
  const total = stats.hits + stats.misses
  const hitRate = total > 0 ? (stats.hits / total * 100).toFixed(2) : 0
  console.log(`快取命中率: ${hitRate}%`)
}, 60000)
```

延伸閱讀：https://www.google.com/search?q=Redis+caching+patterns+and+strategies
https://www.google.com/search?q=cache+penetration+breakdown+solutions+redis
