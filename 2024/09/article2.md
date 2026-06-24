# HTTP 方法與狀態碼複習

## HTTP 協定基礎

HTTP（Hypertext Transfer Protocol）是 API 的底層通訊協定。理解 HTTP 的語意是設計好 API 的前提。

## HTTP 請求方法

### 核心方法（RESTful API 常用）

```javascript
// GET：取得資源（安全、冪等）
GET /api/users
GET /api/users/42

// POST：建立資源（不安全、非冪等）
POST /api/users
// 每次 POST 可能建立不同資源

// PUT：完整取代資源（不安全、冪等）
PUT /api/users/42
// 必須傳送完整資源，缺少的欄位視為清空

// PATCH：部分更新資源（不安全、非冪等）
PATCH /api/users/42
// 只傳送要修改的欄位

// DELETE：刪除資源（不安全、冪等）
DELETE /api/users/42
// 刪除後再次 DELETE 仍回傳 204 或 404
```

### 冪等性（Idempotency）

冪等性是指「多次執行同一操作」與「執行一次」的結果相同。這對網路重試機制非常重要：

```javascript
// GET：安全且冪等
// 多次請求不會改變伺服器狀態

// PUT：冪等
PUT /api/users/42
// 不管執行幾次，最終結果都是更新為指定資料

// DELETE：冪等
DELETE /api/users/42
// 第一次回傳 204，之後可能回傳 404
// 但最終狀態都是「該資源不存在」

// POST：非冪等
POST /api/users
// 每次執行都會建立新資源
```

## HTTP 狀態碼

### 2xx 成功

```javascript
// 200 OK：請求成功（GET、PATCH）
res.status(200).json({ data: user });

// 201 Created：資源建立成功（POST）
res.status(201).json({ data: newUser });

// 202 Accepted：請求已接受但未完成（非同步）
res.status(202).json({ status: 'processing', jobId: 'job_123' });

// 204 No Content：請求成功但無回應主體（DELETE）
res.status(204).end();
```

### 3xx 重新導向

```javascript
// 301 Moved Permanently：資源已永久移動
res.status(301).set('Location', '/api/v2/users');

// 304 Not Modified：資源未修改（條件式請求）
res.status(304).end();
```

### 4xx 客戶端錯誤

```javascript
// 400 Bad Request：請求格式錯誤
res.status(400).json({ error: '無效的 JSON 格式' });

// 401 Unauthorized：未認證
res.status(401).json({ error: '請提供有效的 Token' });

// 403 Forbidden：無權限
res.status(403).json({ error: '您沒有執行此操作的權限' });

// 404 Not Found：資源不存在
res.status(404).json({ error: '找不到使用者' });

// 405 Method Not Allowed：不允許的方法
res.status(405).set('Allow', 'GET, POST').end();

// 409 Conflict：資源衝突
res.status(409).json({ error: 'Email 已被其他使用者使用' });

// 422 Unprocessable Entity：驗證失敗
res.status(422).json({
  error: '資料驗證失敗',
  details: [{ field: 'email', message: 'Email 格式不正確' }]
});

// 429 Too Many Requests：速率限制
res.status(429)
  .set('Retry-After', '60')
  .json({ error: '請求次數過多，請稍後再試' });
```

### 5xx 伺服器錯誤

```javascript
// 500 Internal Server Error：伺服器內部錯誤（不應暴露細節）
res.status(500).json({ error: '伺服器內部錯誤' });

// 502 Bad Gateway：上游服務回應無效
res.status(502).json({ error: '資料庫服務暫時無回應' });

// 503 Service Unavailable：服務暫時不可用
res.status(503)
  .set('Retry-After', '120')
  .json({ error: '系統維護中，請稍後再試' });
```

## HTTP 標頭（Headers）

### 請求標頭

```javascript
// Content-Type：請求主體的格式
Content-Type: application/json
Content-Type: multipart/form-data

// Authorization：認證資訊
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Authorization: Basic base64(username:password)

// Accept：客戶端期望的回應格式
Accept: application/json
Accept: application/vnd.myapp.v2+json

// Cache-Control：快取策略
Cache-Control: no-cache
```

### 回應標頭

```javascript
// Content-Type：回應主體的格式
Content-Type: application/json; charset=utf-8

// Cache-Control：快取指示
Cache-Control: public, max-age=3600

// ETag：資源版本標記（用於條件式請求）
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"

// Location：新資源的位置（201 Created 時）
Location: /api/users/42
```

## HTTP/2 與 HTTP/3

HTTP/2 引入了多工（Multiplexing）、伺服器推送（Server Push）和 Header 壓縮（HPACK）。HTTP/3 使用 QUIC（基於 UDP）取代 TCP，減少了連線建立的延遲。

對於 API 設計者來說，這些底層協定的改變不需要修改應用層程式碼，但可以顯著提升 API 的傳輸效能。

---

## 延伸閱讀

- [HTTP Status Codes 完整列表](https://www.google.com/search?q=HTTP+status+codes+list)
- [MDN HTTP 方法](https://www.google.com/search?q=MDN+HTTP+request+methods)
- [RFC 7231 HTTP Semantics](https://www.google.com/search?q=RFC+7231+HTTP+semantics)
