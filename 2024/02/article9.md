# JWT 認證實作

## 認證流程設計

一個完整的 JWT 認證系統包含三個主要部分：註冊/登入、Token 發放、Token 驗證。

```
客戶端                   伺服器
  │                       │
  │── POST /api/login ──→ │  提供帳號密碼
  │                       │  驗證身份
  │←── { token } ───────│  回傳 JWT
  │                       │
  │── GET /api/profile ──→│  附帶 Bearer Token
  │   Authorization:      │  驗證 Token
  │   Bearer <token>      │
  │←── { user data } ───│  回傳受保護資源
  │                       │
```

## 完整實作

### 使用者模型與資料庫

```javascript
// models/User.js (Mongoose)
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true, minlength: 6, select: false },
  role: { type: String, enum: ['user', 'admin'], default: 'user' }
}, { timestamps: true });

// 密碼加密
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// 驗證密碼
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

### 認證服務

```javascript
// services/authService.js
const jwt = require('jsonwebtoken');
const User = require('../models/User');

const SECRET = process.env.JWT_SECRET;
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;

class AuthService {
  generateTokens(user) {
    const payload = { userId: user._id, role: user.role };

    const accessToken = jwt.sign(payload, SECRET, { expiresIn: '15m' });
    const refreshToken = jwt.sign(payload, REFRESH_SECRET, { expiresIn: '7d' });

    return { accessToken, refreshToken };
  }

  async register({ name, email, password }) {
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      throw new AppError('Email already in use', 409);
    }

    const user = await User.create({ name, email, password });
    const tokens = this.generateTokens(user);

    return {
      user: { id: user._id, name: user.name, email: user.email },
      ...tokens
    };
  }

  async login({ email, password }) {
    const user = await User.findOne({ email }).select('+password');
    if (!user) {
      throw new AppError('Invalid credentials', 401);
    }

    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      throw new AppError('Invalid credentials', 401);
    }

    const tokens = this.generateTokens(user);

    return {
      user: { id: user._id, name: user.name, email: user.email },
      ...tokens
    };
  }

  refreshToken(token) {
    try {
      const decoded = jwt.verify(token, REFRESH_SECRET);
      const user = { _id: decoded.userId, role: decoded.role };
      return this.generateTokens(user);
    } catch (err) {
      throw new AppError('Invalid refresh token', 401);
    }
  }
}

module.exports = new AuthService();
```

### 認證中介軟體

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Access denied. No token provided.' });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired', code: 'TOKEN_EXPIRED' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
};

const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};

module.exports = { authenticate, authorize };
```

### 認證路由

```javascript
// routes/auth.js
const express = require('express');
const router = express.Router();
const authService = require('../services/authService');
const { authenticate } = require('../middleware/auth');

// POST /api/auth/register
router.post('/register', async (req, res, next) => {
  try {
    const result = await authService.register(req.body);
    res.status(201).json(result);
  } catch (err) {
    next(err);
  }
});

// POST /api/auth/login
router.post('/login', async (req, res, next) => {
  try {
    const result = await authService.login(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
});

// POST /api/auth/refresh
router.post('/refresh', async (req, res, next) => {
  try {
    const { refreshToken } = req.body;
    if (!refreshToken) {
      return res.status(400).json({ error: 'Refresh token required' });
    }
    const tokens = authService.refreshToken(refreshToken);
    res.json(tokens);
  } catch (err) {
    next(err);
  }
});

// GET /api/auth/me
router.get('/me', authenticate, (req, res) => {
  res.json({ user: req.user });
});

module.exports = router;
```

### 保護路由

```javascript
// 使用範例
const { authenticate, authorize } = require('./middleware/auth');

// 任何已登入使用者
app.get('/api/profile', authenticate, (req, res) => {
  res.json({ userId: req.user.userId });
});

// 僅管理員
app.get('/api/admin/users',
  authenticate,
  authorize('admin'),
  (req, res) => {
    res.json({ users: [...] });
  }
);
```

## 安全性考量

```javascript
// 1. 使用 httpOnly Cookie（更安全）
res.cookie('token', token, {
  httpOnly: true,    // 禁止 JavaScript 存取
  secure: true,      // 僅 HTTPS
  sameSite: 'strict', // 防止 CSRF
  maxAge: 15 * 60 * 1000 // 15 分鐘
});

// 2. Token 黑名單（登出用）
const blacklist = new Set();
app.post('/api/auth/logout', authenticate, (req, res) => {
  const token = req.headers.authorization.split(' ')[1];
  blacklist.add(token);
  res.json({ message: 'Logged out' });
});

// 在黑名單中介軟體中檢查
app.use((req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (token && blacklist.has(token)) {
    return res.status(401).json({ error: 'Token revoked' });
  }
  next();
});
```

## 總結

JWT 認證實作涉及多個層面的設計：使用者管理、Token 生命週期、安全性考量。透過合理的架構設計（Service 層、Middleware 層、Route 層分離），可以建構一個安全且可維護的認證系統。

## 延伸閱讀

- [JWT 官方網站](https://www.google.com/search?q=JSON+Web+Token+introduction)
- [jsonwebtoken npm 套件](https://www.google.com/search?q=jsonwebtoken+npm)
- [Node.js 認證安全指南](https://www.google.com/search?q=Node.js+authentication+security+best+practices)
