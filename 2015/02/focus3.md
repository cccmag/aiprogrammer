# Express 框架：路由、中介層、模板引擎

## 前言

Express 是 Node.js 最流行的 Web 框架，簡潔而彈性，適合建立 API 和 Web 應用。

## 基本設定

```javascript
const express = require('express');
const app = express();

// 靜態檔案
app.use(express.static('public'));

// JSON 解析
app.use(express.json());

// URL 編碼解析
app.use(express.urlencoded({ extended: true }));

// 路由
app.get('/', (req, res) => {
  res.send('Hello World');
});

app.listen(3000);
```

## 路由系統

### 基本路由

```javascript
app.get('/users', (req, res) => {
  res.json({ users: [] });
});

app.post('/users', (req, res) => {
  const user = req.body;
  res.status(201).json({ created: true, user });
});

app.put('/users/:id', (req, res) => {
  const { id } = req.params;
  const user = req.body;
  res.json({ updated: true, id, user });
});

app.delete('/users/:id', (req, res) => {
  const { id } = req.params;
  res.json({ deleted: true, id });
});
```

### 路由參數

```javascript
// 路由參數
app.get('/users/:id', (req, res) => {
  const { id } = req.params;
  res.json({ userId: id });
});

// 多個參數
app.get('/users/:userId/posts/:postId', (req, res) => {
  const { userId, postId } = req.params;
  res.json({ userId, postId });
});

// 可選參數
app.get('/users/:id?', (req, res) => {
  if (req.params.id) {
    res.json({ userId: req.params.id });
  } else {
    res.json({ users: [] });
  }
});
```

### 查詢字串

```javascript
app.get('/search', (req, res) => {
  const { q, page = 1, limit = 10 } = req.query;
  res.json({
    query: q,
    page: parseInt(page),
    limit: parseInt(limit)
  });
});

// URL: /search?q=node&page=2&limit=20
```

### 路由組織

```javascript
// 使用 Router
const usersRouter = express.Router();

usersRouter.get('/', (req, res) => {
  res.json({ users: [] });
});

usersRouter.get('/:id', (req, res) => {
  res.json({ userId: req.params.id });
});

usersRouter.post('/', (req, res) => {
  res.status(201).json({ created: true });
});

app.use('/users', usersRouter);
```

## 中介層

### 概念

```
請求流程：
──────────

用戶端 → [中介層1] → [中介層2] → [路由處理]
                    ↑                    ↓
                    └── 下一個中介層 ←───┘
```

### 內建中介層

```javascript
// 靜態檔案
app.use(express.static('public'));

// JSON 解析
app.use(express.json());

// 記錄請求
app.use((req, res, next) => {
  console.log(`${new Date()} ${req.method} ${req.url}`);
  next();
});

// CORS
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});
```

### 自訂中介層

```javascript
// 驗證中介層
const authenticate = (req, res, next) => {
  const token = req.headers.authorization;
  if (token === 'valid-token') {
    next();
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

// 錯誤處理中介層（4 個參數）
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
};

app.use(authenticate);
app.use(errorHandler);
```

### 第三方中介層

```javascript
// 安裝
npm install morgan compression helmet cookie-parser

// 使用
const morgan = require('morgan');      // HTTP 記錄
const compression = require('compression'); // 壓縮
const helmet = require('helmet');      // 安全標頭
const cookieParser = require('cookie-parser'); // Cookie 解析

app.use(morgan('dev'));               // 開發模式記錄
app.use(compression());                // gzip 壓縮
app.use(helmet());                     // 安全標頭
app.use(cookieParser());               // Cookie
```

## 請求處理

### req 物件

```javascript
app.get('/demo', (req, res) => {
  // URL 參數
  req.params        // { id: '123' }

  // 查詢字串
  req.query         // { name: 'John' }

  // Body（需先 app.use(express.json())）
  req.body          // { name: 'John' }

  // Headers
  req.headers       // { authorization: 'Bearer token' }

  // 路徑
  req.path          // '/demo'
  req.originalUrl   // '/demo?name=John'

  // 主機
  req.hostname      // 'example.com'
  req.ip            // '192.168.1.1'

  // 協定
  req.protocol      // 'http' 或 'https'
  req.secure        // true 或 false
});
```

### res 物件

```javascript
app.get('/demo', (req, res) => {
  // 傳送回應
  res.send('Hello');                    // 文字
  res.send({ user: { name: 'John' } }); // JSON
  res.send(Buffer.from('test'));       // 二進位

  // JSON
  res.json({ name: 'John' });
  res.jsonp({ name: 'John' });         // JSONP

  // 狀態碼
  res.status(404).send('Not Found');
  res.status(201).json({ created: true });

  // 標頭
  res.setHeader('Content-Type', 'application/json');
  res.set('X-Custom-Header', 'value');

  // Cookie
  res.cookie('name', 'value', {
    maxAge: 900000,
    httpOnly: true
  });
  res.clearCookie('name');

  // 下載檔案
  res.download('./file.pdf');

  // 重定向
  res.redirect('/new-url');
});
```

## 模板引擎

### EJS

```bash
npm install ejs
```

```javascript
// 設定視圖引擎
app.set('view engine', 'ejs');
app.set('views', './views');

// 渲染
app.get('/', (req, res) => {
  res.render('index', {
    title: '首頁',
    user: { name: 'John', age: 30 }
  });
});
```

```ejs
<!-- views/index.ejs -->
<!DOCTYPE html>
<html>
<head>
  <title><%= title %></title>
</head>
<body>
  <h1>Hello, <%= user.name %>!</h1>
  <p>年齡: <%= user.age %></p>

  <% if (user.age >= 18) { %>
    <p>已成年</p>
  <% } else { %>
    <p>未成年</p>
  <% } %>

  <% users.forEach(function(u) { %>
    <li><%= u.name %></li>
  <% }); %>
</body>
</html>
```

### 靜態檔案

```javascript
// 靜態檔案目錄
app.use(express.static('public'));
app.use('/static', express.static('public'));

// 多個靜態目錄
app.use(express.static('public'));
app.use(express.static('uploads'));
```

## 結論

Express 的簡潔設計讓 Web 開發變得愉悅。路由系統直覺、中介層彈性、模板引擎支援完善，使得 Express 成為 Node.js 開發的首選框架。

---

## 延伸閱讀

- [Express 官方網站](https://www.google.com/search?q=Express.js+framework+tutorial)
- [Express 4.x 文檔](https://www.google.com/search?q=Express+4+middleware+tutorial)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」歷史回顧系列之一。*