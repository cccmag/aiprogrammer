# REST API 設計指南

## 從零設計使用者管理 API

本文將從零開始設計一個 RESTful 使用者管理 API，展示本文前面各主題的實際應用。

## 資源識別與 URI 設計

```javascript
// 使用者資源
GET    /api/v1/users          // 列表
POST   /api/v1/users          // 建立
GET    /api/v1/users/:id      // 單筆
PATCH  /api/v1/users/:id      // 部分更新
DELETE /api/v1/users/:id      // 刪除

// 巢狀資源：使用者的訂單
GET    /api/v1/users/:id/orders
POST   /api/v1/users/:id/orders
GET    /api/v1/users/:id/orders/:orderId
```

### 資源命名規則

- 使用名詞複數：`/users`、`/orders`、`/products`
- 巢狀關係不超過兩層：`/users/:id/orders` 正確，`/users/:id/orders/:oid/items` 不建議
- 查詢參數用於過濾而非路徑：`/users?status=active` 而非 `/users/active`

## 請求與回應結構

```javascript
// 列表請求：支援分頁、過濾、排序
// GET /api/v1/users?page=1&limit=20&role=admin&sort=-createdAt

// 統一回應格式
function successResponse(data, meta = {}) {
  return {
    success: true,
    data,
    meta: {
      requestId: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      ...meta
    }
  };
}

function errorResponse(code, message, details = []) {
  return {
    success: false,
    error: { code, message, details },
    meta: {
      requestId: crypto.randomUUID(),
      timestamp: new Date().toISOString()
    }
  };
}
```

## 完整 CRUD 實作

```javascript
const express = require('express');
const router = express.Router();

// GET /api/v1/users — 列表
router.get('/users', async (req, res) => {
  const { page = 1, limit = 20, sort = '-createdAt' } = req.query;
  const offset = (page - 1) * limit;

  const [users, total] = await Promise.all([
    db.users.findAll({ limit, offset, order: [[sort.replace('-', ''), sort.startsWith('-') ? 'DESC' : 'ASC']] }),
    db.users.count()
  ]);

  res.json(successResponse(users, {
    pagination: {
      page: Number(page),
      limit: Number(limit),
      total,
      totalPages: Math.ceil(total / limit)
    }
  }));
});

// GET /api/v1/users/:id — 單筆
router.get('/users/:id', async (req, res) => {
  const user = await db.users.findByPk(req.params.id);
  if (!user) {
    return res.status(404).json(errorResponse('NOT_FOUND', '使用者不存在'));
  }
  res.json(successResponse(user));
});

// POST /api/v1/users — 建立
router.post('/users', async (req, res) => {
  const { name, email } = req.body;
  // 驗證邏輯
  if (!name || !email) {
    return res.status(422).json(errorResponse('VALIDATION_ERROR', '缺少必要欄位', [
      { field: 'name', message: '姓名為必填' },
      { field: 'email', message: 'Email 為必填' }
    ]));
  }

  const existing = await db.users.findOne({ where: { email } });
  if (existing) {
    return res.status(409).json(errorResponse('CONFLICT', 'Email 已被使用'));
  }

  const user = await db.users.create({ name, email });
  res.status(201).json(successResponse(user));
});

// PATCH /api/v1/users/:id — 部分更新
router.patch('/users/:id', async (req, res) => {
  const user = await db.users.findByPk(req.params.id);
  if (!user) {
    return res.status(404).json(errorResponse('NOT_FOUND', '使用者不存在'));
  }

  const allowedFields = ['name', 'email'];
  const updates = {};
  for (const field of allowedFields) {
    if (req.body[field] !== undefined) updates[field] = req.body[field];
  }

  await user.update(updates);
  res.json(successResponse(user));
});

// DELETE /api/v1/users/:id — 刪除
router.delete('/users/:id', async (req, res) => {
  const user = await db.users.findByPk(req.params.id);
  if (!user) {
    return res.status(404).json(errorResponse('NOT_FOUND', '使用者不存在'));
  }
  await user.destroy();
  res.status(204).end();
});
```

## 內聚的錯誤處理

```javascript
// 全域錯誤處理中介軟體
function errorHandler(err, req, res, next) {
  console.error(`[${req.id}] ${err.message}`, err.stack);

  if (err.name === 'ValidationError') {
    return res.status(422).json(errorResponse('VALIDATION_ERROR', '資料驗證失敗', err.details));
  }
  if (err.name === 'UnauthorizedError') {
    return res.status(401).json(errorResponse('UNAUTHORIZED', '認證失敗'));
  }
  if (err.status) {
    return res.status(err.status).json(errorResponse(err.code || 'ERROR', err.message));
  }

  res.status(500).json(errorResponse('INTERNAL_ERROR', '伺服器內部錯誤'));
}
```

## 分頁設計

```javascript
// 基於偏移的分頁（Offset-based）
GET /api/v1/users?page=2&limit=20
// 回應包含 pagination 資訊

// 基於游標的分頁（Cursor-based）
GET /api/v1/users?cursor=eyJpZCI6NDJ9&limit=20
// 適用於即時資料，避免插入新資料導致分頁偏移

function cursorEncode(value) {
  return Buffer.from(JSON.stringify(value)).toString('base64');
}

function cursorDecode(cursor) {
  return JSON.parse(Buffer.from(cursor, 'base64').toString());
}
```

## 設計檢查清單

- [ ] 資源使用名詞複數
- [ ] HTTP 方法正確對應 CRUD 操作
- [ ] 狀態碼正確使用
- [ ] 統一回應格式
- [ ] 錯誤訊息有助於除錯
- [ ] 分頁支援
- [ ] 過濾與排序支援
- [ ] 認證與授權
- [ ] 速率限制
- [ ] 版本管理策略

---

## 延伸閱讀

- [RESTful API Design by Microsoft](https://www.google.com/search?q=Microsoft+RESTful+API+design)
- [JSON API Specification](https://www.google.com/search?q=JSON+API+specification)
