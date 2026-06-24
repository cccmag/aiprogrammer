# 速率限制實作

## 為什麼需要速率限制

速率限制（Rate Limiting）保護 API 免於資源濫用。沒有速率限制的 API 就像沒有鎖的門——任何人都可以無限次進出。

## 演算法實作

### Token Bucket（權杖桶）

權杖桶是最流行的限流演算法，允許突發流量：

```javascript
class TokenBucket {
  constructor(capacity, fillPerSecond) {
    this.capacity = capacity;          // 最大突發容量
    this.tokens = capacity;            // 目前權杖數
    this.fillPerSecond = fillPerSecond; // 補充速率
    this.lastRefill = Date.now();
  }

  tryConsume(count = 1) {
    this.refill();
    if (this.tokens >= count) {
      this.tokens -= count;
      return true;
    }
    return false;
  }

  refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(
      this.capacity,
      this.tokens + elapsed * this.fillPerSecond
    );
    this.lastRefill = now;
  }
}

// 使用範例：每分鐘 100 個請求，突發上限 20
const limiter = new TokenBucket(20, 100 / 60);
```

### Leaky Bucket（漏水桶）

漏水桶平滑輸出速率，適合需要穩定流量的場景：

```javascript
class LeakyBucket {
  constructor(capacity, leakRate) {
    this.capacity = capacity;     // 佇列容量
    this.water = 0;               // 當前水量
    this.leakRate = leakRate;     // 漏水速率（請求/秒）
    this.lastLeak = Date.now();
  }

  tryConsume() {
    this.leak();
    if (this.water < this.capacity) {
      this.water++;
      return true;
    }
    return false;
  }

  leak() {
    const now = Date.now();
    const elapsed = (now - this.lastLeak) / 1000;
    this.water = Math.max(0, this.water - elapsed * this.leakRate);
    this.lastLeak = now;
  }
}
```

### Fixed Window（固定視窗）

最簡單的實作，但邊界問題可能導致雙倍流量：

```javascript
class FixedWindow {
  constructor(windowMs, maxRequests) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
    this.windows = new Map();
  }

  tryConsume(key) {
    const now = Date.now();
    const windowStart = Math.floor(now / this.windowMs);

    if (!this.windows.has(key)) {
      this.windows.set(key, new Map());
    }

    const userWindows = this.windows.get(key);
    const count = userWindows.get(windowStart) || 0;

    if (count >= this.maxRequests) {
      return false;
    }

    userWindows.set(windowStart, count + 1);
    return true;
  }
}
```

### Sliding Window Log（滑動視窗日誌）

使用有序集合記錄每個請求的時間戳：

```javascript
class SlidingWindowLog {
  constructor(windowMs, maxRequests) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
    this.logs = new Map();
  }

  tryConsume(key) {
    const now = Date.now();
    const windowStart = now - this.windowMs;

    if (!this.logs.has(key)) {
      this.logs.set(key, []);
    }

    const timestamps = this.logs.get(key);
    // 移除視窗外的記錄
    while (timestamps.length > 0 && timestamps[0] < windowStart) {
      timestamps.shift();
    }

    if (timestamps.length >= this.maxRequests) {
      return false;
    }

    timestamps.push(now);
    return true;
  }
}
```

## 分散式速率限制（Redis）

```javascript
const redis = require('redis');
const client = redis.createClient();

class RedisSlidingWindow {
  constructor(windowMs, maxRequests) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
  }

  async tryConsume(key) {
    const now = Date.now();
    const windowKey = `ratelimit:${key}`;
    const windowStart = now - this.windowMs;

    const multi = client.multi();
    multi.zRemRangeByScore(windowKey, 0, windowStart);
    multi.zCard(windowKey);
    multi.zAdd(windowKey, { score: now, value: `${now}` });
    multi.expire(windowKey, Math.ceil(this.windowMs / 1000) * 2);

    const results = await multi.exec();
    const count = results[1][1]; // zCard 結果

    if (count >= this.maxRequests) {
      return { allowed: false, remaining: 0 };
    }

    return {
      allowed: true,
      remaining: this.maxRequests - count - 1
    };
  }
}
```

## 速率限制 Header

標準的速率限制資訊透過回應 Header 傳遞：

```javascript
function rateLimitMiddleware(limiter) {
  return async (req, res, next) => {
    const key = req.ip || req.user?.id || 'anonymous';
    const result = await limiter.tryConsume(key);

    res.set({
      'X-RateLimit-Limit': limiter.maxRequests,
      'X-RateLimit-Remaining': result.remaining,
      'X-RateLimit-Reset': Math.ceil((Date.now() + limiter.windowMs) / 1000)
    });

    if (!result.allowed) {
      res.set('Retry-After', Math.ceil(limiter.windowMs / 1000));
      return res.status(429).json({
        error: 'RATE_LIMIT_EXCEEDED',
        message: '請求次數過多，請稍後再試',
        retryAfter: Math.ceil(limiter.windowMs / 1000)
      });
    }

    next();
  };
}
```

## 分層限流策略

```
全球層：所有請求總和（防止 DDoS）
  ┊  每 IP 每秒 1000 請求
服務層：每個服務的總流量
  ┊  每服務每秒 5000 請求
使用者層：每個使用者的限制
  ┊  每使用者每秒 100 請求
端點層：每個端點的細粒度限制
  ┊  POST /api/login 每分鐘 5 次
```

## 小結

選擇速率限制演算法時要考慮：是否需要突發流量、是否需要嚴格的速率平滑、是否為分散式系統。Token Bucket 是最通用的選擇，Redis 方案適合分散式部署。

---

## 延伸閱讀

- [Rate Limiting Strategies](https://www.google.com/search?q=API+rate+limiting+strategies+comparison)
- [Redis Rate Limiting Patterns](https://www.google.com/search?q=Redis+rate+limiting+patterns)
- [NGINX Rate Limiting](https://www.google.com/search?q=NGINX+rate+limiting+module)
