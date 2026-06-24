# Express 專案結構

## 為什麼專案結構很重要？

當 Express 應用從簡單的 prototype 成長為正式的產品時，良好的專案結構決定了程式碼的可維護性和團隊協作效率。本文將介紹多種經過實戰驗證的專案結構方案。

## 基礎結構

對於小型專案，最簡單的結構：

```
my-app/
├── app.js              # Express 應用設定
├── server.js           # 伺服器啟動
├── routes/
│   └── index.js        # 路由定義
├── package.json
└── node_modules/
```

```javascript
// app.js
const express = require('express');
const app = express();

app.use(express.json());

const routes = require('./routes');
app.use('/api', routes);

module.exports = app;
```

```javascript
// server.js
const app = require('./app');
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## 中型專案結構

當專案增長時，建議按功能（Feature）組織：

```
src/
├── app.js
├── server.js
├── config/
│   ├── index.js          # 統一設定
│   ├── database.js       # 資料庫設定
│   └── env.js            # 環境變數
├── routes/
│   ├── index.js          # 路由匯總
│   ├── users.js
│   └── products.js
├── controllers/
│   ├── userController.js
│   └── productController.js
├── models/
│   ├── User.js
│   └── Product.js
├── middleware/
│   ├── auth.js
│   ├── validate.js
│   └── errorHandler.js
├── services/
│   ├── userService.js
│   └── emailService.js
├── utils/
│   ├── logger.js
│   └── helpers.js
└── validators/
    ├── userValidator.js
    └── productValidator.js
```

## 分層架構

### Controller 層

```javascript
// controllers/userController.js
const userService = require('../services/userService');

exports.getUsers = async (req, res, next) => {
  try {
    const users = await userService.findAll(req.query);
    res.json({ data: users });
  } catch (err) {
    next(err);
  }
};

exports.getUser = async (req, res, next) => {
  try {
    const user = await userService.findById(req.params.id);
    if (!user) return res.status(404).json({ error: 'Not found' });
    res.json({ data: user });
  } catch (err) {
    next(err);
  }
};
```

### Service 層

```javascript
// services/userService.js
const User = require('../models/User');

exports.findAll = async (query = {}) => {
  const { page = 1, limit = 10 } = query;
  return User.find()
    .skip((page - 1) * limit)
    .limit(limit);
};

exports.findById = async (id) => {
  return User.findById(id);
};
```

### Route 層

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const auth = require('../middleware/auth');
const validate = require('../middleware/validate');

router.get('/', userController.getUsers);
router.get('/:id', userController.getUser);
router.post('/', validate('createUser'), userController.createUser);
router.put('/:id', auth, userController.updateUser);
router.delete('/:id', auth, userController.deleteUser);

module.exports = router;
```

## 大型專案結構（Monorepo）

```javascript
// 使用 npm workspaces
// package.json
{
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "dev": "npm run dev --workspace=packages/server"
  }
}
```

```
monorepo/
├── packages/
│   ├── server/           # Express 伺服器
│   │   ├── src/
│   │   └── package.json
│   ├── shared/           # 共用程式碼
│   │   ├── src/
│   │   └── package.json
│   └── client/           # 前端應用
│       └── package.json
├── package.json
└── .github/
```

## 環境變數管理

```javascript
// config/index.js
require('dotenv').config();

module.exports = {
  port: process.env.PORT || 3000,
  db: {
    uri: process.env.MONGODB_URI,
    options: { maxPoolSize: 10 }
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '1h'
  },
  env: process.env.NODE_ENV || 'development'
};
```

```javascript
// .env（不使用版本控制）
PORT=3000
MONGODB_URI=mongodb://localhost:27017/myapp
JWT_SECRET=your-secret-key
NODE_ENV=development
```

## 錯誤處理結構

```javascript
// middleware/errorHandler.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

const errorHandler = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.isOperational
    ? err.message
    : 'Internal server error';

  console.error(err);

  res.status(statusCode).json({
    success: false,
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
};

module.exports = { AppError, errorHandler };
```

## 總結

沒有放諸四海皆準的專案結構。關鍵原則是：關注點分離、低耦合高內聚、易於測試。隨著專案成長，定期重構結構是維持程式碼品質的必要工作。

## 延伸閱讀

- [Express 專案結構最佳實踐](https://www.google.com/search?q=Express+project+structure+best+practices)
- [Node.js 分層架構](https://www.google.com/search?q=Node.js+layered+architecture)
- [Monorepo with npm workspaces](https://www.google.com/search?q=npm+workspaces+monorepo)
