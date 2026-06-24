# api_design.js：Express 風格 API 路由與中介軟體實作

## 概述

`api_design.js` 是一個從零實作的 Express 風格 API 框架，展示了現代後端架構的核心元件：路由、中介軟體鏈、認證、速率限制和 JSON 驗證。總共約 150 行 JavaScript 程式碼，完整呈現了 API 設計的關鍵模式。

## 核心概念

### 1. Router 類別：路徑匹配與參數萃取

```javascript
class Router {
  constructor() {
    this.routes = [];
    this.middleware = [];
  }
  match(method, path) {
    const segments = path.split('/').filter(Boolean);
    for (const route of this.routes) {
      if (route.method !== method) continue;
      const routeSegs = route.path.split('/').filter(Boolean);
      if (routeSegs.length !== segments.length) continue;
      const params = {};
      // 逐一比對區段，:id 視為參數
    }
  }
}
```

路由匹配採用區段比對法：將路徑按 `/` 分割後逐一比較，遇到 `:param` 格式的區段則萃取為參數。這種實作與 Express 的核心邏輯相同。

### 2. 中介軟體鏈

```javascript
const run = async (i) => {
  if (i < this.middleware.length && nextCalled) {
    nextCalled = false;
    await this.middleware[i](ctx, () => { nextCalled = true; run(i + 1); });
  }
};
await run(0);
```

中介軟體鏈採用遞迴方式執行：每個中介軟體接收 `(ctx, next)`，呼叫 `next()` 時觸發下一個中介軟體。若中介軟體不呼叫 `next()`，鏈條終止，路由處理器也不會被執行——這就是認證失敗時回傳 401 的機制。

### 3. 認證中介軟體

```javascript
function authMiddleware(validTokens) {
  return async (ctx, next) => {
    const auth = ctx.req.headers?.['authorization'] || '';
    const token = auth.replace('Bearer ', '');
    if (!validTokens.includes(token)) {
      ctx.status = 401;
      ctx.body = { error: 'Unauthorized' };
      return; // 不呼叫 next，鏈條中斷
    }
    await next();
  };
}
```

Bearer Token 驗證：從 Authorization header 萃取 token，比對白名單。失敗時中斷鏈條並回傳 401。

### 4. 速率限制器

```javascript
function rateLimiter(maxReqs, windowMs) {
  const hits = new Map();
  setInterval(() => hits.clear(), windowMs);
  return async (ctx, next) => {
    const ip = ctx.req.ip || 'unknown';
    const count = (hits.get(ip) || 0) + 1;
    hits.set(ip, count);
    if (count > maxReqs) {
      ctx.status = 429;
      ctx.body = { error: 'Too Many Requests', retryAfterMs: windowMs };
      return;
    }
    await next();
  };
}
```

基於記憶體的滑動視窗實作：以 IP 為鍵記錄請求次數，超過閾值時回傳 429。`setInterval` 定期清空計數器。

### 5. JSON Schema 驗證

```javascript
function validateJson(schema) {
  return async (ctx, next) => {
    const body = ctx.req.body;
    for (const [key, type] of Object.entries(schema)) {
      if (body[key] === undefined) {
        ctx.status = 400;
        ctx.body = { error: `Missing field: ${key}` };
        return;
      }
      if (typeof body[key] !== type) {
        ctx.status = 400;
        ctx.body = { error: `Field ${key} must be ${type}` };
        return;
      }
    }
    await next();
  };
}
```

簡單的欄位型別驗證：檢查必要欄位是否存在以及型別是否正確。這相當於 JSON Schema 的最小可行實作。

## 執行結果

```
GET /api/users -> 200 {"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]}
GET /api/users/42 -> 200 {"user":{"id":42,"name":"User42"}}
POST /api/users -> 201 {"created":{"id":3,"name":"Charlie","email":"charlie@test.com"}}
POST /api/users -> 400 {"error":"Missing field: email"}
GET /api/users -> 401 {"error":"Unauthorized"}
GET /api/unknown -> 404 {"error":"Not Found"}
```

各測試案例分別對應：正常列表、參數綁定、新增成功、驗證失敗、認證失敗、路由未匹配。六種情境涵蓋了 API 設計中最常見的回應路徑。

## api_design.js 教會我們的事

### 1. 中介軟體是 API 架構的核心模式

一個請求從接收到回應，經過的每個中介軟體各自負責一個關注點：解析 body、檢查速率、驗證 token、校驗資料。這種「職責鏈」模式讓 API 的每個層面都可以獨立測試和替換。

### 2. 優雅的錯誤處理

每個中介軟體在發現錯誤時立即回傳對應的狀態碼和結構化錯誤訊息，而不是拋出例外。這保證了 API 的回應永遠是結構化的 JSON。

### 3. 可組合性

認證、限流、驗證——這些功能以函數工廠的形式提供，可以靈活組合在不同路由上。這種設計來自 Express/Koa 的中介軟體生態。

---

## 延伸閱讀

- [完整程式碼](_code/api_design.js)
- [Express.js 中介軟體](https://www.google.com/search?q=Express.js+middleware)
- [Node.js 路由設計模式](https://www.google.com/search?q=Node.js+routing+patterns)
