# RESTful API 路由設計

## 設計原則

RESTful API 路由設計的核心是資源導向。每個 URL 代表一個資源，HTTP 方法代表對該資源的操作。

## 資源路由模式

### 標準 CRUD 路由

```javascript
const express = require('express');
const router = express.Router();

// 集合操作
GET    /api/users          → 列表
POST   /api/users          → 建立

// 單一資源操作
GET    /api/users/:id      → 讀取
PUT    /api/users/:id      → 完整更新
PATCH  /api/users/:id      → 部分更新
DELETE /api/users/:id      → 刪除
```

### 巢狀資源

```javascript
// 一對多關係
GET    /api/users/:userId/posts
POST   /api/users/:userId/posts
GET    /api/users/:userId/posts/:postId
PUT    /api/users/:userId/posts/:postId
DELETE /api/users/:userId/posts/:postId

// 多對多關係
GET    /api/users/:userId/roles
POST   /api/users/:userId/roles/:roleId  // 建立關聯
DELETE /api/users/:userId/roles/:roleId  // 移除關聯
```

## Express Router 實作

```javascript
// routes/users.js
const express = require('express');
const router = express.Router({ mergeParams: true });

// GET /api/users
router.get('/', async (req, res) => {
  const { page = 1, limit = 10, sort = '-createdAt' } = req.query;

  const users = await User.find()
    .sort(sort)
    .skip((page - 1) * limit)
    .limit(Number(limit));

  const total = await User.countDocuments();

  res.json({
    data: users,
    meta: {
      page: Number(page),
      limit: Number(limit),
      total,
      pages: Math.ceil(total / limit)
    }
  });
});

// GET /api/users/:id
router.get('/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({ data: user });
});

// POST /api/users
router.post('/', async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json({ data: user });
});

// PUT /api/users/:id
router.put('/:id', async (req, res) => {
  const user = await User.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true, runValidators: true }
  );
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({ data: user });
});

// DELETE /api/users/:id
router.delete('/:id', async (req, res) => {
  const user = await User.findByIdAndDelete(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.status(204).end();
});

module.exports = router;
```

### 巢狀路由實作

```javascript
// routes/userPosts.js
const express = require('express');
const router = express.Router({ mergeParams: true });

// GET /api/users/:userId/posts
router.get('/', async (req, res) => {
  const posts = await Post.find({ user: req.params.userId });
  res.json({ data: posts });
});

// POST /api/users/:userId/posts
router.post('/', async (req, res) => {
  const post = await Post.create({
    ...req.body,
    user: req.params.userId
  });
  res.status(201).json({ data: post });
});

module.exports = router;
```

```javascript
// routes/index.js
const express = require('express');
const router = express.Router();

router.use('/users', require('./users'));
router.use('/users/:userId/posts', require('./userPosts'));

module.exports = router;
```

## 查詢過濾與排序

```javascript
// 進階查詢中介軟體
function advancedResults(model, populate) {
  return async (req, res, next) => {
    let query;

    // 複製 req.query
    const reqQuery = { ...req.query };

    // 排除的欄位
    const removeFields = ['select', 'sort', 'page', 'limit'];
    removeFields.forEach(param => delete reqQuery[param]);

    // 建立查詢字串
    let queryStr = JSON.stringify(reqQuery);

    // 轉換運算子
    queryStr = queryStr.replace(
      /\b(gt|gte|lt|lte|in)\b/g,
      match => `$${match}`
    );

    query = model.find(JSON.parse(queryStr));

    // 選擇欄位
    if (req.query.select) {
      const fields = req.query.select.split(',').join(' ');
      query = query.select(fields);
    }

    // 排序
    if (req.query.sort) {
      const sortBy = req.query.sort.split(',').join(' ');
      query = query.sort(sortBy);
    } else {
      query = query.sort('-createdAt');
    }

    // 分頁
    const page = parseInt(req.query.page, 10) || 1;
    const limit = parseInt(req.query.limit, 10) || 10;
    const startIndex = (page - 1) * limit;
    const total = await model.countDocuments(JSON.parse(queryStr));

    query = query.skip(startIndex).limit(limit);

    if (populate) {
      query = query.populate(populate);
    }

    const results = await query;

    res.pagination = {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    };

    res.results = results;
    next();
  };
}

// 使用
router.get(
  '/',
  advancedResults(User, 'posts'),
  (req, res) => {
    res.json({
      data: res.results,
      meta: res.pagination
    });
  }
);
```

## API 版本管理策略

```javascript
const express = require('express');
const app = express();

// 方式一：URL 版本
app.use('/api/v1/users', require('./routes/v1/users'));
app.use('/api/v2/users', require('./routes/v2/users'));

// 方式二：請求標頭版本（中介軟體）
app.use('/api/users', (req, res, next) => {
  const version = req.headers['accept-version'] || 'v1';

  if (version === 'v2') {
    req.version = 'v2';
  }

  next();
});
```

## 總結

良好的 RESTful API 路由設計應該遵循一致性原則：統一的命名慣例、恰當的 HTTP 方法使用、完整的狀態碼回應，以及合理的資源巢狀層次。

## 延伸閱讀

- [RESTful API 設計最佳實踐](https://www.google.com/search?q=RESTful+API+design+best+practices)
- [Express 路由指南](https://www.google.com/search?q=Express+routing+guide)
- [JSON API 規範](https://www.google.com/search?q=JSON+API+specification)
