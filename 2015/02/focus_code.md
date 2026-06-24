# Express 框架實務：REST API 開發範例

## 概述

本期實作將展示如何使用 Express 4.0 建立一個完整的 RESTful API，包含路由設計、中介層應用和錯誤處理。

## 基本 Express 伺服器

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to API' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

## 完整 REST API 實作

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// 模擬資料庫
let users = [
  { id: 1, name: '王小明', email: 'wang@example.com' },
  { id: 2, name: '李小華', email: 'lee@example.com' },
  { id: 3, name: '陳大同', email: 'chen@example.com' }
];

// CORS 中介層
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
});

// 日誌中介層
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  next();
});

// 路由
app.get('/api/users', (req, res) => {
  res.json({ users, count: users.length });
});

app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({ user });
});

app.post('/api/users', (req, res) => {
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

app.put('/api/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = users.findIndex(u => u.id === id);

  if (index === -1) {
    return res.status(404).json({ error: 'User not found' });
  }

  const { name, email } = req.body;
  users[index] = {
    ...users[index],
    name: name || users[index].name,
    email: email || users[index].email
  };

  res.json({ updated: true, user: users[index] });
});

app.delete('/api/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = users.findIndex(u => u.id === id);

  if (index === -1) {
    return res.status(404).json({ error: 'User not found' });
  }

  users.splice(index, 1);
  res.json({ deleted: true, id });
});

// 錯誤處理中介層
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(3000, () => {
  console.log('REST API running on http://localhost:3000');
});
```

## REST API 測試

```bash
# 取得所有使用者
curl http://localhost:3000/api/users

# 取得單一使用者
curl http://localhost:3000/api/users/1

# 建立使用者
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "張小美", "email": "zhang@example.com"}'

# 更新使用者
curl -X PUT http://localhost:3000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "王小明 Jr."}'

# 刪除使用者
curl -X DELETE http://localhost:3000/api/users/1
```

## 程式碼展示

本期的程式碼位於 `_code/` 目錄：

- `server.js` - REST API 伺服器
- `client.js` - API 用戶端測試

執行方式：

```bash
node server.js &
node client.js
```

---

*本期程式實作到此結束。*