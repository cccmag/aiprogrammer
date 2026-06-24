# 中介軟體實戰

## 中介軟體的概念

中介軟體（Middleware）是 Express 的核心設計模式。它是一串在請求被路由處理器處理之前或之後執行的函式。每個中介軟體都有機會修改請求物件、回應物件，或終止請求處理。

## 常見中介軟體實作

### 日誌記錄

```javascript
const express = require('express');
const app = express();

app.use((req, res, next) => {
  const start = Date.now();
  const { method, url } = req;

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(
      `[${new Date().toISOString()}] ${method} ${url} ${res.statusCode} ${duration}ms`
    );
  });

  next();
});
```

### 請求速率限制

```javascript
const rateLimit = {};

app.use((req, res, next) => {
  const ip = req.ip;
  const now = Date.now();

  if (!rateLimit[ip]) {
    rateLimit[ip] = [];
  }

  // 過濾掉 60 秒前的紀錄
  rateLimit[ip] = rateLimit[ip].filter(t => now - t < 60000);

  if (rateLimit[ip].length >= 100) {
    return res.status(429).json({
      error: 'Too many requests, please try again later'
    });
  }

  rateLimit[ip].push(now);
  next();
});
```

### CORS 中介軟體

```javascript
app.use((req, res, next) => {
  const allowedOrigins = ['http://localhost:3000', 'https://myapp.com'];
  const origin = req.headers.origin;

  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }

  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Max-Age', '86400');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  next();
});
```

### 請求驗證中介軟體

```javascript
function validate(schema) {
  return (req, res, next) => {
    const errors = [];

    for (const [field, rules] of Object.entries(schema)) {
      const value = req.body[field];

      if (rules.required && !value) {
        errors.push(`${field} is required`);
        continue;
      }

      if (value) {
        if (rules.type === 'string' && typeof value !== 'string') {
          errors.push(`${field} must be a string`);
        }
        if (rules.minLength && value.length < rules.minLength) {
          errors.push(`${field} must be at least ${rules.minLength} characters`);
        }
        if (rules.pattern && !rules.pattern.test(value)) {
          errors.push(`${field} format is invalid`);
        }
      }
    }

    if (errors.length > 0) {
      return res.status(422).json({ errors });
    }

    next();
  };
}

// 使用
app.post('/users', validate({
  name: { required: true, type: 'string', minLength: 2 },
  email: { required: true, type: 'string', pattern: /^[^\s@]+@[^\s@]+$/ },
  age: { type: 'number', min: 0 }
}), (req, res) => {
  res.json({ success: true });
});
```

## 錯誤處理中介軟體

```javascript
// 非同步錯誤包裝器
function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// 使用
app.get('/api/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    throw new AppError('User not found', 404);
  }
  res.json({ data: user });
}));

// 404 處理
app.use((req, res, next) => {
  res.status(404).json({
    error: 'Not found',
    path: req.originalUrl
  });
});

// 通用錯誤處理（四個參數）
app.use((err, req, res, next) => {
  console.error('Error:', err);

  if (err.name === 'ValidationError') {
    return res.status(422).json({
      error: 'Validation failed',
      details: Object.values(err.errors).map(e => e.message)
    });
  }

  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({ error: 'Invalid token' });
  }

  res.status(err.statusCode || 500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message
  });
});
```

## 第三方中介軟體整合

```javascript
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');

const app = express();

// 安全
app.use(helmet());
app.use(cors());

// 效能
app.use(compression());

// 日誌
app.use(morgan('combined'));

// 速率限制
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 分鐘
  max: 100,
  message: 'Too many requests'
});
app.use('/api', limiter);

// 解析
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
```

## 中介軟體執行順序

```javascript
// 執行順序由註冊順序決定

// 1. 全域中介軟體
app.use(helmet());
app.use(cors());
app.use(express.json());

// 2. 路徑特定中介軟體
app.use('/api', apiLogger);

// 3. 路由中介軟體
app.get('/profile', authenticate, getUserProfile);

// 4. 錯誤處理中介軟體（最後註冊）
app.use(errorHandler);
```

## 總結

中介軟體是 Express 最強大的功能之一。透過組合和自訂中介軟體，開發者可以建構靈活、可重用且易於維護的後端應用。從日誌記錄到認證授權，從請求驗證到錯誤處理，中介軟體貫穿了請求解際週期的每一個環節。

## 延伸閱讀

- [Express 中介軟體官方文件](https://www.google.com/search?q=Express+middleware+documentation)
- [撰寫自訂 Express 中介軟體](https://www.google.com/search?q=writing+custom+Express+middleware)
- [熱門 Express 中介軟體](https://www.google.com/search?q=popular+Express+middleware+packages)
