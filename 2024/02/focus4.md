# 路由與中介軟體

## 路由深入

Express 的路由系統比初看起來更加靈活。除了基本的 HTTP 方法匹配，還支援模式匹配和參數驗證。

### 路由參數

```javascript
const express = require('express');
const app = express();

// 具名參數
app.get('/users/:userId/books/:bookId', (req, res) => {
  res.json(req.params);
  // { "userId": "42", "bookId": "5" }
});

// 可選參數
app.get('/articles/:year/:month?', (req, res) => {
  // month 可能不存在
  res.json(req.params);
});

// 萬用參數
app.get('/files/*', (req, res) => {
  // 匹配 /files/anything/here
  res.json({ path: req.params[0] });
});
```

### 正規表達式路由

```javascript
// 匹配 /user/123，不匹配 /user/abc
app.get(/^\/user\/(\d+)$/, (req, res) => {
  res.send(`User ID: ${req.params[0]}`);
});
```

### 路由分組與前綴

```javascript
const express = require('express');
const app = express();

// 使用 Router
const adminRouter = express.Router();

adminRouter.use((req, res, next) => {
  console.log('Admin middleware:', req.ip);
  next();
});

adminRouter.get('/dashboard', (req, res) => {
  res.send('Admin Dashboard');
});

adminRouter.get('/users', (req, res) => {
  res.send('Admin Users');
});

// 掛載到 /admin 路徑
app.use('/admin', adminRouter);
```

## 中介軟體深入

中介軟體是 Express 最重要的概念之一。每個中介軟體函式都可以決定終止請求處理或將控制權傳遞給下一個中介軟體。

### 中介軟體的類型

```javascript
const express = require('express');
const app = express();

// 1. 應用層中介軟體
app.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

// 2. 路由層中介軟體
app.use('/api', (req, res, next) => {
  console.log('API request');
  next();
});

// 3. 錯誤處理中介軟體（四個參數）
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

### 中介軟體的執行順序

```javascript
app.use((req, res, next) => {
  console.log('1');
  next();
  console.log('5'); // 在回應送出後執行
});

app.use((req, res, next) => {
  console.log('2');
  next();
  console.log('4');
});

app.get('/', (req, res) => {
  console.log('3');
  res.send('Hello');
});
```

輸出順序：1 → 2 → 3 → 4 → 5

### 實用中介軟體範例

```javascript
// 請求計時中介軟體
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.url} - ${duration}ms`);
  });
  next();
});

// IP 白名單中介軟體
const whitelist = ['127.0.0.1', '::1'];
app.use((req, res, next) => {
  if (!whitelist.includes(req.ip)) {
    return res.status(403).send('Access denied');
  }
  next();
});

// 條件式中介軟體
app.use('/api', (req, res, next) => {
  if (req.headers['x-api-key'] !== 'secret') {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  next();
});
```

## 鏈式處理

同一個路徑可以綁定多個中介軟體，形成處理鏈：

```javascript
const validateUser = (req, res, next) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Missing fields' });
  }
  next();
};

const checkEmail = (req, res, next) => {
  if (!req.body.email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  next();
};

const createUser = (req, res) => {
  // 建立使用者
  res.status(201).json({ success: true });
};

app.post('/users', validateUser, checkEmail, createUser);
```

## 第三方中介軟體

```javascript
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const app = express();

app.use(helmet());          // 安全相關標頭
app.use(cors());            // 跨域請求
app.use(morgan('combined')); // 請求日誌
app.use(express.json());    // 解析 JSON 主體
app.use(express.static('public'));
```

## 總結

路由與中介軟體是 Express 框架的兩大支柱。靈活的路由系統讓 URL 設計變得直觀，而中介軟體機制則提供了強大且可擴充的功能組合方式。掌握這兩個概念，就能充分發揮 Express 的潛力。

## 延伸閱讀

- [Express 路由指南](https://www.google.com/search?q=Express+routing+guide)
- [Express 中介軟體使用](https://www.google.com/search?q=Express+middleware+usage)
- [撰寫自訂中介軟體](https://www.google.com/search?q=writing+custom+Express+middleware)
