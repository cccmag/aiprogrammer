# REST API 設計

## RESTful 原則

REST（Representational State Transfer）是 Roy Fielding 在 2000 年提出的架構風格。遵循 RESTful 原則設計的 API 具有統一介面、無狀態、可快取等特性。

### 六大約束

1. **客戶端-伺服器分離**：關注點分離，客戶端不關心資料儲存
2. **無狀態**：每個請求包含所有必要資訊，伺服器不儲存會話狀態
3. **可快取**：回應應明確標示是否可快取
4. **統一介面**：資源通過 URI 識別，使用標準 HTTP 方法
5. **分層系統**：客戶端無法直接得知是否與終端伺服器通訊
6. **隨需程式碼（可選）**：伺服器可傳送可執行代碼

## 資源設計

REST API 的核心是資源（Resource）。每個資源通過 URI 識別：

```
GET    /users          # 取得使用者列表
POST   /users          # 建立使用者
GET    /users/:id      # 取得特定使用者
PUT    /users/:id      # 更新使用者（完整更新）
PATCH  /users/:id      # 部分更新使用者
DELETE /users/:id      # 刪除使用者
```

### 資源命名規範

```javascript
// 好的命名
GET    /api/articles
GET    /api/articles/:id
GET    /api/articles/:id/comments
POST   /api/articles/:id/comments

// 不好的命名
GET    /api/getArticles       // 不應在 URI 中包含動詞
POST   /api/createArticle      // HTTP 方法已表達動作
GET    /api/article_list       // 請用連字號或駝峰式
```

### 關聯資源

```javascript
// 巢狀資源
GET    /api/users/:userId/orders
GET    /api/users/:userId/orders/:orderId

// 扁平化設計（有時更好）
GET    /api/orders?userId=123
```

## 使用 Express 實作 CRUD

```javascript
const express = require('express');
const router = express.Router();

let users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
];
let nextId = 3;

// GET /api/users
router.get('/', (req, res) => {
  const { page = 1, limit = 10 } = req.query;
  const start = (page - 1) * limit;
  const result = users.slice(start, start + Number(limit));
  res.json({ data: result, total: users.length, page: Number(page) });
});

// GET /api/users/:id
router.get('/:id', (req, res) => {
  const user = users.find(u => u.id === Number(req.params.id));
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json({ data: user });
});

// POST /api/users
router.post('/', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required' });
  }
  const user = { id: nextId++, name, email };
  users.push(user);
  res.status(201).json({ data: user });
});

// PUT /api/users/:id
router.put('/:id', (req, res) => {
  const idx = users.findIndex(u => u.id === Number(req.params.id));
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  users[idx] = { id: users[idx].id, ...req.body };
  res.json({ data: users[idx] });
});

// DELETE /api/users/:id
router.delete('/:id', (req, res) => {
  const idx = users.findIndex(u => u.id === Number(req.params.id));
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  users.splice(idx, 1);
  res.status(204).send();
});

module.exports = router;
```

## 狀態碼使用指南

```javascript
// 2xx 成功
res.status(200).json({ data: item });     // OK
res.status(201).json({ data: item });     // Created
res.status(204).send();                    // No Content

// 3xx 重新導向
res.status(301).redirect('/new-location'); // Moved Permanently

// 4xx 客戶端錯誤
res.status(400).json({ error: 'Bad request' });     // Bad Request
res.status(401).json({ error: 'Unauthorized' });    // Unauthorized
res.status(403).json({ error: 'Forbidden' });       // Forbidden
res.status(404).json({ error: 'Not found' });       // Not Found
res.status(409).json({ error: 'Conflict' });        // Conflict
res.status(422).json({ error: 'Validation failed' }); // Unprocessable

// 5xx 伺服器錯誤
res.status(500).json({ error: 'Internal server error' });
```

## API 版本管理

```javascript
// 方式一：URI 路徑版本
app.use('/api/v1/users', userRoutesV1);
app.use('/api/v2/users', userRoutesV2);

// 方式二：請求標頭版本
app.use('/api/users', (req, res, next) => {
  const version = req.headers['accept-version'];
  req.apiVersion = version || 'v1';
  next();
});
```

## 回應格式規範

建議使用統一的回應格式：

```javascript
// 成功回應
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100
  }
}

// 錯誤回應
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [...]
  }
}
```

## 總結

良好的 REST API 設計不僅關乎路由組織，更關乎使用者體驗。統一的命名慣例、恰當的狀態碼、完整的錯誤資訊，以及前後一致的資料格式，都是高品質 API 的必要條件。

## 延伸閱讀

- [RESTful API 設計指南](https://www.google.com/search?q=RESTful+API+design+guidelines)
- [HTTP 狀態碼完整列表](https://www.google.com/search?q=HTTP+status+codes+list)
- [JSON API 規範](https://www.google.com/search?q=JSON+API+specification)
