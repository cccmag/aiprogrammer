# Node.js 後端開發完整實作

## 前言

本篇文章對應的完整程式碼位於 `_code/node_server.js`。這個單一腳本檔案涵蓋了本期焦點中的核心概念：檔案系統操作、HTTP 伺服器模擬、JWT 認證實作，以及 Express-like 的路由和中介軟體架構。

---

## 原始碼

完整的 Node.js 實作請參考：[_code/node_server.js](_code/node_server.js)

```javascript
#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 簡易 JWT 實作
function createToken(payload, secret) {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = crypto.createHmac('sha256', secret).update(`${header}.${body}`).digest('base64url');
  return `${header}.${body}.${signature}`;
}

function verifyToken(token, secret) {
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [header, body, signature] = parts;
  const expected = crypto.createHmac('sha256', secret).update(`${header}.${body}`).digest('base64url');
  if (signature !== expected) return null;
  return JSON.parse(Buffer.from(body, 'base64url').toString());
}

// 簡易路由模擬 (Express-like)
class App {
  constructor() {
    this.routes = { GET: {}, POST: {}, PUT: {}, DELETE: {} };
    this.middlewares = [];
  }

  use(fn) { this.middlewares.push(fn); return this; }

  get(path, handler) { this.routes.GET[path] = handler; return this; }
  post(path, handler) { this.routes.POST[path] = handler; return this; }
  put(path, handler) { this.routes.PUT[path] = handler; return this; }
  delete(path, handler) { this.routes.DELETE[path] = handler; return this; }

  handle(req, res) {
    const run = (i) => {
      if (i < this.middlewares.length) {
        this.middlewares[i](req, res, () => run(i + 1));
      } else {
        const route = this.routes[req.method]?.[req.url];
        if (route) route(req, res);
        else { res.statusCode = 404; res.end('Not Found'); }
      }
    };
    run(0);
  }
}
```

---

## 執行結果

```
=== Node.js 後端開發示範 ===

1. 檔案系統操作
   寫入/讀取: Hello, Node.js!
   暫存檔案已清理

2. HTTP 伺服器模擬
   [2024-02-15T12:00:00.000Z] GET /api/hello
   GET 回應: {"message":"Hello World"}

3. JWT 認證示範
   產生的 Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   驗證結果: { userId: 123, role: 'admin' }

=== 示範完成 ===
```

---

## 功能說明

### 1. 檔案系統操作

使用 `fs` 和 `path` 模組建立暫存目錄、寫入檔案、讀取檔案、刪除檔案：

```
mkdir → writeFile → readFile → unlink → rmdir
```

展示了 Node.js 同步 API 的基本使用方式。

### 2. HTTP 伺服器模擬

實作了一個 Express 風格的 `App` 類別，支援：

- **中介軟體鏈**：透過 `.use()` 註冊中介軟體函式，形成處理鏈
- **路由註冊**：`.get()`、`.post()`、`.put()`、`.delete()` 方法
- **請求處理**：`handle()` 方法依序執行中介軟體，最後匹配路由

### 3. JWT 認證示範

實作了完整的 JWT 建立與驗證流程：

- `createToken()`：將 payload 編碼為 Header.Body.Signature 格式
- `verifyToken()`：解析並驗證簽章，回傳解碼後的 payload
- **路由守衛**：中介軟體檢查 Authorization 標頭，保護敏感路由

### 4. 完整的中介軟體鏈

```
請求進入
  ↓
日誌中介軟體 (記錄時間戳和請求方法/URL)
  ↓
認證中介軟體 (檢查受保護路由的 JWT Token)
  ↓
路由處理器 (回傳資料)
```

## 結論

這個範例程式展示了 Node.js 後端開發的核心概念，從底層的 `http`、`fs`、`path` 內建模組，到高層的路由抽象和 JWT 認證機制。透過這個簡化的實作，讀者可以更清楚地理解 Express 框架的設計原理。

## 延伸閱讀

- [Node.js 執行期與事件循環](focus1.md)
- [Express 框架入門](focus3.md)
- [REST API 設計](focus5.md)
- [認證與授權：JWT](focus7.md)
- [範例程式碼](_code/)
