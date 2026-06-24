# RESTful API 設計原則

## 前言

REST（Representational State Transfer）是最流行的 Web API 設計風格。

---

## REST 基礎

### 資源導向

REST 是資源導向的，每個資源有一個 URI。

```
/users          # 使用者集合
/users/123      # ID 為 123 的使用者
/posts          # 文章集合
/posts/456      # ID 為 456 的文章
```

### HTTP 方法

| 方法 | 用途 | 範例 |
|------|------|------|
| GET | 取得資源 | GET /users |
| POST | 建立資源 | POST /users |
| PUT | 更新資源 | PUT /users/123 |
| DELETE | 刪除資源 | DELETE /users/123 |
| PATCH | 部分更新 | PATCH /users/123 |

---

## API 設計原則

### 1. 使用名詞，而非動詞

```bash
# 錯誤
GET /getUsers
POST /createUser

# 正確
GET /users
POST /users
```

### 2. 使用複數名詞

```bash
# 標準
GET /users
GET /users/123
```

### 3. 巢狀資源

```bash
# 使用者的文章
GET /users/123/posts

# 文章的評論
GET /posts/456/comments
```

### 4. 版本控制

```bash
# URL 版本
GET /api/v1/users

# Header 版本
Accept: application/vnd.api+json;version=1
```

---

## HTTP 狀態碼

| 範圍 | 意義 | 常用狀態碼 |
|------|------|------------|
| 1xx | 資訊 | 100 Continue |
| 2xx | 成功 | 200 OK, 201 Created, 204 No Content |
| 3xx | 重新導向 | 301 Moved, 304 Not Modified |
| 4xx | 用戶端錯誤 | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx | 伺服器錯誤 | 500 Internal Error, 503 Service Unavailable |

### 常見狀態碼使用

```http
# 成功
200 OK              # GET 成功
201 Created         # POST 成功建立
204 No Content      # DELETE 成功

# 用戶端錯誤
400 Bad Request     # 請求格式錯誤
401 Unauthorized     # 未認證
403 Forbidden        # 無權限
404 Not Found        # 資源不存在
422 Unprocessable    # 驗證失敗

# 伺服器錯誤
500 Internal Error   # 伺服器錯誤
503 Unavailable      # 服務不可用
```

---

## 請求與回應格式

### JSON 格式

```json
// GET /users/123
{
  "id": 123,
  "name": "John",
  "email": "john@example.com",
  "created_at": "2025-01-01T00:00:00Z"
}
```

### 建立資源

```http
POST /users HTTP/1.1
Content-Type: application/json

{
  "name": "John",
  "email": "john@example.com"
}
```

回應：

```http
HTTP/1.1 201 Created
Location: /users/124
Content-Type: application/json

{
  "id": 124,
  "name": "John",
  "email": "john@example.com",
  "created_at": "2025-01-01T12:00:00Z"
}
```

### 錯誤回應

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

---

## 設計範例

### 電子商務 API

```
GET    /products              # 列出商品
GET    /products/:id          # 取得商品
POST   /products              # 新增商品
PUT    /products/:id          # 更新商品
DELETE /products/:id          # 刪除商品

GET    /orders                # 列出訂單
GET    /orders/:id            # 取得訂單
POST   /orders                # 建立訂單
PUT    /orders/:id/status     # 更新訂單狀態

GET    /users/:id/cart        # 取得使用者購物車
POST   /users/:id/cart/items  # 新增商品到購物車
DELETE /users/:id/cart/items/:itemId  # 移除商品
```

---

## 分頁與過濾

### 分頁

```http
GET /users?page=2&per_page=20
```

回應：

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### 過濾

```bash
GET /users?role=admin&active=true
GET /posts?author_id=123&published=true
GET /products?category=electronics&price_min=100&price_max=500
```

### 排序

```bash
GET /users?sort=created_at&order=desc
GET /posts?sort=title&order=asc
```

[搜尋 REST API design best practices](https://www.google.com/search?q=REST+API+design+best+practices)

---

## 小結

良好的 RESTful API 設計應該是直覺的、一致的和可預測的。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [REST API 設計指南](https://www.google.com/search?q=REST+API+design+guide)
- [HTTP 狀態碼完整列表](https://www.google.com/search?q=HTTP+status+codes+complete)