# RESTful API 設計：資源路由、HTTP 方法、狀態碼

## 前言

REST（Representational State Transfer）是一種 API 設計架構风格，基於 HTTP 協定，讓 API 直覺且易於理解。

## REST 核心原則

```
REST 六原則：
─────────────
1. 用戶端-伺服器分離
2. 無狀態
3. 可快取
4. 分層系統
5. 統一介面
6. 按需代碼（可選）
```

## 資源導向路由

### 基本模式

```
傳統路由：              REST 路由：
─────────────          ──────────────
GET /getUsers        → GET    /users
GET /getUser?id=1    → GET    /users/1
POST /createUser     → POST   /users
POST /updateUser     → PUT    /users/1
POST /deleteUser     → DELETE /users/1
```

### 巢狀資源

```javascript
// 使用者擁有的文章
GET    /users/1/posts           // 使用者 1 的所有文章
GET    /users/1/posts/2         // 使用者 1 的文章 2
POST   /users/1/posts           // 在使用者 1 下建立文章
PUT    /users/1/posts/2         // 更新使用者 1 的文章 2
DELETE /users/1/posts/2         // 刪除使用者 1 的文章 2
```

### 集合與單一資源

```javascript
GET /users          // 集合：所有使用者
GET /users/1        // 單一：ID 為 1 的使用者

POST /users         // 在集合中建立
PUT  /users/1       // 更新單一資源
DELETE /users/1     // 刪除單一資源
```

## HTTP 方法語義

### 方法對照

```
方法      語義         安全   冪等
─────────────────────────────────
GET       讀取         ✓      ✓
POST      建立         ✗      ✗
PUT       完全更新     ✗      ✓
PATCH     部分更新     ✗      ✓
DELETE    刪除         ✗      ✓
HEAD      僅標頭       ✓      ✓
OPTIONS   支援的方法    ✓      ✓
```

### 實作範例

```javascript
const express = require('express');
const app = express();
app.use(express.json());

let users = [
  { id: 1, name: '王小明', email: 'wang@example.com' },
  { id: 2, name: '李小華', email: 'lee@example.com' }
];

// GET /users - 取得所有使用者
app.get('/users', (req, res) => {
  const { name, limit = 10 } = req.query;
  let result = users;

  if (name) {
    result = result.filter(u => u.name.includes(name));
  }

  result = result.slice(0, parseInt(limit));
  res.json({ users: result, count: result.length });
});

// GET /users/:id - 取得單一使用者
app.get('/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({ user });
});

// POST /users - 建立使用者
app.post('/users', (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }

  const newUser = {
    id: users.length + 1,
    name,
    email
  };
  users.push(newUser);

  res.status(201).json({ created: true, user: newUser });
});

// PUT /users/:id - 完全更新
app.put('/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = users.findIndex(u => u.id === id);

  if (index === -1) {
    return res.status(404).json({ error: 'User not found' });
  }

  const { name, email } = req.body;
  users[index] = { id, name: name || users[index].name, email: email || users[index].email };

  res.json({ updated: true, user: users[index] });
});

// PATCH /users/:id - 部分更新
app.patch('/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const user = users.find(u => u.id === id);

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  const { name, email } = req.body;
  if (name) user.name = name;
  if (email) user.email = email;

  res.json({ updated: true, user });
});

// DELETE /users/:id - 刪除
app.delete('/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = users.findIndex(u => u.id === id);

  if (index === -1) {
    return res.status(404).json({ error: 'User not found' });
  }

  users.splice(index, 1);
  res.json({ deleted: true, id });
});
```

## HTTP 狀態碼

### 類別

```
2xx: 成功
3xx: 重定向
4xx: 用戶端錯誤
5xx: 伺服器錯誤
```

### 常見狀態碼

```javascript
// 成功
res.status(200).json({ ok: true });           // OK
res.status(201).json({ created: true });      // Created
res.status(204).end();                        // No Content

// 用戶端錯誤
res.status(400).json({ error: 'Bad Request' });           // 語法錯誤
res.status(401).json({ error: 'Unauthorized' });          // 未認證
res.status(403).json({ error: 'Forbidden' });              // 無權限
res.status(404).json({ error: 'Not Found' });             // 找不到
res.status(409).json({ error: 'Conflict' });              // 衝突
res.status(422).json({ error: 'Unprocessable Entity' });  // 語意錯誤

// 伺服器錯誤
res.status(500).json({ error: 'Internal Server Error' });
res.status(503).json({ error: 'Service Unavailable' });
```

## 錯誤處理

### 統一錯誤格式

```javascript
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);

  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';

  res.status(status).json({
    error: {
      message,
      status,
      timestamp: new Date().toISOString()
    }
  });
};

// 自訂錯誤
class NotFoundError extends Error {
  constructor(message) {
    super(message);
    this.status = 404;
  }
}

app.get('/users/:id', (req, res, next) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return next(new NotFoundError('User not found'));
  }
  res.json({ user });
});

app.use(errorHandler);
```

## API 版本控制

```javascript
// URL 路径
app.use('/api/v1', require('./routes/v1'));
app.use('/api/v2', require('./routes/v2'));

// Header
app.get('/users', (req, res) => {
  const version = req.headers['accept-version'];
  if (version === '2') {
    // v2 回應格式
  } else {
    // v1 回應格式
  }
});
```

## 分頁與過濾

```javascript
app.get('/users', (req, res) => {
  const {
    page = 1,
    limit = 10,
    sort = 'name',
    order = 'asc'
  } = req.query;

  const offset = (page - 1) * limit;

  let result = users;

  // 排序
  result.sort((a, b) => {
    const aVal = a[sort];
    const bVal = b[sort];
    if (order === 'asc') return aVal > bVal ? 1 : -1;
    return aVal < bVal ? 1 : -1;
  });

  // 分頁
  result = result.slice(offset, offset + parseInt(limit));

  res.json({
    data: result,
    pagination: {
      page: parseInt(page),
      limit: parseInt(limit),
      total: users.length,
      pages: Math.ceil(users.length / limit)
    }
  });
});
```

## 結論

RESTful API 設計讓 Web 服務更加直覺和標準化。遵循 HTTP 方法語義、使用適當的狀態碼、提供清晰的錯誤訊息，都是好的 API 設計的關鍵。

---

## 延伸閱讀

- [REST API 設計指南](https://www.google.com/search?q=REST+API+design+best+practices)
- [HTTP 狀態碼參考](https://www.google.com/search?q=HTTP+status+codes+reference)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」歷史回顧系列之一。*