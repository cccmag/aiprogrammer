# 錯誤處理最佳實踐

## 為什麼錯誤處理很重要？

在 Node.js 應用中，未妥善處理的錯誤可能導致伺服器崩潰、資料遺失或安全漏洞。一個好的錯誤處理策略不僅能提升應用穩定性，還能提供更好的開發體驗和使用者體驗。

## 同步錯誤處理

```javascript
const express = require('express');
const app = express();

// Express 5.0 之前，同步錯誤會自動被 catch
app.get('/sync-error', (req, res) => {
  throw new Error('This will be caught by Express');
});

// 但在非同步回呼中不會
app.get('/async-error', (req, res) => {
  setTimeout(() => {
    throw new Error('This will crash the server!');
  }, 100);
});
```

## 非同步錯誤處理

```javascript
// Express 4.x 需要手動處理非同步錯誤
const asyncHandler = (fn) => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// 使用
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({ data: user });
}));
```

## 自訂錯誤類別

```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;  // 可預期的操作錯誤
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(errors) {
    super('Validation failed', 422);
    this.errors = errors;
  }
}

class NotFoundError extends AppError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401);
  }
}
```

## 集中式錯誤中介軟體

```javascript
// middleware/errorHandler.js
const errorHandler = (err, req, res, next) => {
  let statusCode = err.statusCode || 500;
  let message = err.message || 'Internal server error';

  // MongoDB 錯誤處理
  if (err.name === 'CastError') {
    statusCode = 400;
    message = 'Invalid ID format';
  }

  if (err.code === 11000) {
    statusCode = 409;
    const field = Object.keys(err.keyValue)[0];
    message = `Duplicate value for ${field}`;
  }

  if (err.name === 'ValidationError') {
    statusCode = 422;
    message = Object.values(err.errors)
      .map(e => e.message)
      .join(', ');
  }

  // JWT 錯誤
  if (err.name === 'JsonWebTokenError') {
    statusCode = 401;
    message = 'Invalid token';
  }

  if (err.name === 'TokenExpiredError') {
    statusCode = 401;
    message = 'Token expired';
  }

  // 開發環境回傳詳細資訊
  const response = {
    success: false,
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && {
        stack: err.stack,
        details: err.errors
      })
    }
  };

  console.error(`${statusCode} - ${message}`);
  if (process.env.NODE_ENV === 'development') {
    console.error(err.stack);
  }

  res.status(statusCode).json(response);
};

module.exports = errorHandler;
```

## 全域未捕捉錯誤

```javascript
// 捕捉未處理的 Promise 拒絕
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // 優雅關閉伺服器
  server.close(() => process.exit(1));
});

// 捕捉未捕捉的例外
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  process.exit(1);
});
```

## 實戰：完整的錯誤處理設置

```javascript
// app.js
const express = require('express');
const errorHandler = require('./middleware/errorHandler');
const { AppError, NotFoundError } = require('./utils/errors');

const app = express();

// 全域非同步處理包裝器
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// 路由範例
app.get('/api/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) throw new NotFoundError('User');

  res.json({ data: user });
}));

app.post('/api/users', asyncHandler(async (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    throw new ValidationError([
      { field: 'name', message: 'Name is required' },
      { field: 'email', message: 'Email is required' }
    ]);
  }

  const user = await User.create({ name, email });
  res.status(201).json({ data: user });
}));

// 404 處理（必須在所有路由之後）
app.use('*', (req, res) => {
  throw new NotFoundError(`Route ${req.originalUrl}`);
});

// 錯誤處理中介軟體（必須最後註冊）
app.use(errorHandler);

module.exports = app;
```

## 日誌與監控

```javascript
// utils/logger.js
const fs = require('fs');
const path = require('path');

class Logger {
  constructor() {
    this.logDir = path.join(__dirname, '../logs');
    if (!fs.existsSync(this.logDir)) {
      fs.mkdirSync(this.logDir);
    }
  }

  error(message, meta = {}) {
    const entry = {
      timestamp: new Date().toISOString(),
      level: 'error',
      message,
      meta
    };

    fs.appendFileSync(
      path.join(this.logDir, 'error.log'),
      JSON.stringify(entry) + '\n'
    );

    console.error(message, meta);
  }

  warn(message, meta = {}) {
    const entry = {
      timestamp: new Date().toISOString(),
      level: 'warn',
      message,
      meta
    };

    fs.appendFileSync(
      path.join(this.logDir, 'app.log'),
      JSON.stringify(entry) + '\n'
    );
  }
}

module.exports = new Logger();
```

## 總結

錯誤處理不應該是最後才想到的事。透過建立分層的錯誤處理機制──從自訂錯誤類別、中介軟體處理，到全域的未捕捉錯誤管理，才能確保應用在各種異常情況下都能優雅回應。

## 延伸閱讀

- [Express 錯誤處理官方指南](https://www.google.com/search?q=Express+error+handling+guide)
- [Node.js 錯誤處理最佳實踐](https://www.google.com/search?q=Node.js+error+handling+best+practices)
- [JavaScript Promise 錯誤處理](https://www.google.com/search?q=JavaScript+Promise+error+handling)
