# API 閘道模式

## 什麼是 API 閘道

API 閘道（API Gateway）位於客戶端和後端服務之間，作為所有 API 請求的統一入口。它負責請求路由、認證、速率限制、日誌記錄、協議轉換等橫切關注點（Cross-cutting Concerns）。

## API 閘道的核心功能

### 路由與負載平衡

```javascript
const http = require('http');
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer({});

const routes = {
  '/api/users': 'http://user-service:3001',
  '/api/orders': 'http://order-service:3002',
  '/api/products': 'http://product-service:3003'
};

const server = http.createServer((req, res) => {
  const target = Object.keys(routes).find(prefix =>
    req.url.startsWith(prefix)
  );

  if (target) {
    proxy.web(req, res, { target: routes[target] });
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});
```

### 認證聚合

```javascript
// 閘道層統一認證，後端服務不需要各自實作
async function gatewayAuth(req, res, next) {
  const token = req.headers['authorization']?.replace('Bearer ', '');

  try {
    const user = await authService.verifyToken(token);
    // 將使用者資訊轉發到後端服務
    req.headers['x-user-id'] = user.id;
    req.headers['x-user-role'] = user.role;
    next();
  } catch {
    res.status(401).json({ error: 'Unauthorized' });
  }
}
```

### 速率限制

```javascript
// 閘道層統一限流
const rateLimiter = new RedisSlidingWindow(60000, 100);

app.use(async (req, res, next) => {
  const key = req.headers['x-api-key'] || req.ip;
  const result = await rateLimiter.tryConsume(key);

  res.set({
    'X-RateLimit-Limit': '100',
    'X-RateLimit-Remaining': result.remaining
  });

  if (!result.allowed) {
    return res.status(429).json({ error: 'Too Many Requests' });
  }
  next();
});
```

### 協議轉換

```javascript
// 將 REST 請求轉換為 gRPC
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDef = protoLoader.loadSync('user.proto');
const grpcObj = grpc.loadPackageDefinition(packageDef);
const userClient = new grpcObj.UserService('user-service:50051', grpc.credentials.createInsecure());

app.get('/api/users/:id', async (req, res) => {
  userClient.GetUser({ id: req.params.id }, (err, response) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(response);
  });
});
```

## 實際的 Node.js API 閘道實作

```javascript
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// 全域中介軟體
app.use(express.json());
app.use(require('morgan')('combined'));

// 認證中介軟體
app.use('/api', async (req, res, next) => {
  const publicPaths = ['/api/login', '/api/register', '/api/health'];
  if (publicPaths.some(p => req.path.startsWith(p))) {
    return next();
  }
  return gatewayAuth(req, res, next);
});

// 速率限制
app.use('/api', rateLimitMiddleware);

// 路由到微服務
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  changeOrigin: true,
  onProxyReq: (proxyReq, req) => {
    proxyReq.setHeader('x-request-id', req.id);
  }
}));

app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  changeOrigin: true
}));

app.use('/api/products', createProxyMiddleware({
  target: 'http://product-service:3003',
  changeOrigin: true
}));

// 統一回應包裝
app.use('/api', (err, req, res, next) => {
  console.error(`[Gateway Error] ${req.id}:`, err.message);
  res.status(err.status || 500).json({
    success: false,
    error: {
      code: 'GATEWAY_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'Internal error' : err.message
    },
    meta: { requestId: req.id }
  });
});
```

## 閘道模式的優勢

```
客戶端 → API 閘道 → 微服務

✅ 單一入口：客戶端只需知道閘道位址
✅ 關注點分離：認證、限流、日誌統一在閘道處理
✅ 協議轉換：後端服務可以選擇最適合的協議
✅ 服務抽象：後端服務重構時不影響客戶端
✅ 安全防護：閘道是第一道防線
```

## 常見 API 閘道方案比較

| 方案 | 類型 | 語言 | 擴充性 | 學習曲線 | 生態系 |
|------|------|------|--------|---------|--------|
| Kong | 獨立 | Lua/Go | 外掛豐富 | 中 | 大 |
| NGINX | 獨立 | C | 高度自訂 | 高 | 極大 |
| Express Gateway | Node.js | JS | 外掛系統 | 低 | 中 |
| Envoy | 獨立 | C++ | L7 代理 | 高 | 大 |
| AWS API Gateway | 雲端 | 託管 | 無伺服器 | 低 | AWS 生態 |
| Azure API Management | 雲端 | 託管 | 政策驅動 | 中 | Azure 生態 |

## 閘道模式的挑戰

1. **單點故障：** 閘道是關鍵路徑，必須高可用部署
2. **延遲增加：** 每個請求多一層網路跳躍
3. **閘道膨脹：** 避免將商業邏輯放進閘道
4. **除錯困難：** 分佈式追蹤（如 Jaeger、Zipkin）是必備工具

## 小結

API 閘道是微服務架構中的關鍵元件。它不是一個可選項——在服務數量超過 3-5 個時，閘道帶來的統一管理收益遠超過其引入的複雜度。

---

## 延伸閱讀

- [API Gateway Pattern](https://www.google.com/search?q=API+gateway+pattern+microservices)
- [Kong API Gateway](https://www.google.com/search?q=Kong+API+gateway)
- [NGINX as API Gateway](https://www.google.com/search?q=NGINX+as+API+gateway)
