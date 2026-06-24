# 專題 4：Redis 快取與訊息佇列

## 高效能的記憶體資料結構儲存

Redis 是一個開源的記憶體資料結構儲存系統，可作為資料庫、快取層和訊息代理使用。其極低的延遲與豐富的資料結構使其成為現代應用架構中的關鍵元件。

### 核心資料結構

```javascript
// Redis 五種基本資料結構操作 (使用 ioredis)
import Redis from 'ioredis'
const redis = new Redis()

// 字串 (String)
await redis.set('user:1001', JSON.stringify({ name: 'Alice', visits: 42 }))
const user = JSON.parse(await redis.get('user:1001'))

// 串列 (List) - 可作為訊息佇列
await redis.lpush('queue:tasks', 'task1')
await redis.lpush('queue:tasks', 'task2')
const task = await redis.rpop('queue:tasks')

// 集合 (Set) - 支援交集/聯集操作
await redis.sadd('tags:javascript', 'oop', 'async', 'event-loop')
await redis.sadd('tags:nodejs', 'async', 'stream', 'event-loop')
const common = await redis.sinter('tags:javascript', 'tags:nodejs')

// 有序集合 (Sorted Set) - 排行榜應用
await redis.zadd('leaderboard', 100, 'Alice', 85, 'Bob', 92, 'Charlie')
const top3 = await redis.zrevrange('leaderboard', 0, 2, 'WITHSCORES')

// 雜湊 (Hash)
await redis.hset('session:abc123', 'userId', '1001', 'role', 'admin')
const session = await redis.hgetall('session:abc123')
```

### 快取策略

#### 快取穿透
當請求的資料不存在於資料庫與快取中時，大量請求直接打到資料庫。解決方案是使用空值快取或布隆過濾器。

```javascript
async function getUser(id) {
  let user = await redis.get(`user:${id}`)
  if (user !== null) return JSON.parse(user)
  user = await db.findUser(id)
  const ttl = user ? 3600 : 60 // 空值也快取但較短
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', ttl)
  return user
}
```

#### 快取雪崩
大規模快取同時失效導致資料庫壓力暴增。解決方案包括設定隨機 TTL 與使用本地備份快取。

```javascript
// 隨機 TTL 避免雪崩
const ttl = 3600 + Math.floor(Math.random() * 600) // 基礎 1 小時 + 隨機 10 分鐘
await redis.set(`cache:${key}`, value, 'EX', ttl)
```

### 發布/訂閱模式

Redis 的 Pub/Sub 功能適合實作即時訊息傳遞：

```javascript
// 發布者
await redis.publish('channel:notifications', JSON.stringify({
  type: 'user_login',
  userId: 1001,
  timestamp: Date.now()
}))

// 訂閱者
redis.subscribe('channel:notifications', (err, count) => {})
redis.on('message', (channel, message) => {
  console.log('收到訊息:', JSON.parse(message))
})
```

### 使用場景

- **快取層**：加速資料庫查詢，降低回應時間
- **工作佇列**：使用 List 實作先進先出佇列
- **即時計數器**：追蹤按讚數、瀏覽次數
- **排行榜**：使用 Sorted Set 實現動態排行榜
- **分散式鎖**：使用 SETNX 實現鎖機制

延伸閱讀：https://www.google.com/search?q=Redis+caching+strategies+guide
https://www.google.com/search?q=Redis+pub+sub+message+queue+tutorial
