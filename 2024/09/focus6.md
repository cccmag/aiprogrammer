# 速率限制與安全性

## 速率限制的重要性

速率限制（Rate Limiting）是 API 安全的第一道防線。它可以防止暴力破解、DDoS 攻擊、資源濫用，以及確保公平使用。

### 常見的速率限制演算法

#### Token Bucket（權杖桶）

權杖以固定速率放入桶中，每個請求消耗一個權杖。桶滿時多餘的權杖被丟棄。

```javascript
class TokenBucket {
  constructor(capacity, fillRate) {
    this.capacity = capacity;      // 桶的最大容量
    this.tokens = capacity;        // 當前權杖數
    this.fillRate = fillRate;      // 每秒補充速率
    this.lastRefill = Date.now();
  }

  allow() {
    this._refill();
    if (this.tokens > 0) {
      this.tokens--;
      return true;
    }
    return false;
  }

  _refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(
      this.capacity,
      this.tokens + elapsed * this.fillRate
    );
    this.lastRefill = now;
  }
}
```

#### Leaky Bucket（漏水桶）

請求以可變速率進入桶子，但以固定速率「漏出」處理。桶滿時新請求被拒絕。

```javascript
class LeakyBucket {
  constructor(capacity, leakRate) {
    this.capacity = capacity;
    this.water = 0;
    this.leakRate = leakRate;
    this.lastLeak = Date.now();
  }

  allow() {
    this._leak();
    if (this.water < this.capacity) {
      this.water++;
      return true;
    }
    return false;
  }

  _leak() {
    const now = Date.now();
    const elapsed = (now - this.lastLeak) / 1000;
    this.water = Math.max(0, this.water - elapsed * this.leakRate);
    this.lastLeak = now;
  }
}
```

#### 滑動視窗（Sliding Window）

記錄每個時間視窗內的請求次數，視窗隨著時間滑動。

### 分散式速率限制

在分散式系統中，需要共享計數器。常見方案：

```javascript
// 使用 Redis 實作分散式速率限制
const redis = require('redis');
const client = redis.createClient();

async function slidingWindowRateLimit(userId, maxReqs, windowSec) {
  const key = `ratelimit:${userId}`;
  const now = Date.now();
  const windowStart = now - windowSec * 1000;

  // 移除視窗外的舊記錄
  await client.zRemRangeByScore(key, 0, windowStart);
  // 加入當前請求
  await client.zAdd(key, { score: now, value: `${now}` });
  // 設定 TTL 避免記憶體洩漏
  await client.expire(key, windowSec * 2);
  // 計算視窗內請求數
  const count = await client.zCard(key);

  return count <= maxReqs;
}
```

## API 安全頭盔（Security Headers）

```javascript
// 安全 Header 中介軟體
function securityHeaders(req, res, next) {
  res.set({
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
  });
  next();
}
```

### CORS 處理

```javascript
function corsMiddleware(origins) {
  return (req, res, next) => {
    const origin = req.headers['origin'];
    if (origins.includes('*') || origins.includes(origin)) {
      res.set('Access-Control-Allow-Origin', origin || '*');
      res.set('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE');
      res.set('Access-Control-Allow-Headers', 'Content-Type,Authorization');
    }
    if (req.method === 'OPTIONS') {
      return res.status(204).end();
    }
    next();
  };
}
```

## 輸入驗證與注入防護

### SQL Injection 防護

```javascript
// ❌ 危險：字串拼接
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;

// ✅ 安全：使用參數化查詢
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [req.params.id]);
```

### NoSQL Injection 防護

```javascript
// ❌ 危險：直接傳入查詢物件
db.collection('users').find(req.query);

// ✅ 安全：明確過濾允許的欄位
const allowedFields = ['name', 'email', 'role'];
const filter = {};
for (const key of allowedFields) {
  if (req.query[key]) filter[key] = req.query[key];
}
db.collection('users').find(filter);
```

## 小結

速率限制和安全性是 API 設計中不可妥協的部分。身處 API-first 的世界，安全必須是設計的內建屬性，而非事後補救。

---

**下一步**：[GraphQL 入門](focus7.md)

## 延伸閱讀

- [OWASP REST Security Cheat Sheet](https://www.google.com/search?q=OWASP+REST+security+cheat+sheet)
- [Rate Limiting Patterns](https://www.google.com/search?q=rate+limiting+patterns+API)
- [HTTP Security Headers](https://www.google.com/search?q=HTTP+security+headers+guide)
