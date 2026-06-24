# RESTful API 設計原則：資源、URI、HTTP 動詞

## REST 的核心概念

REST（Representational State Transfer）的核心是「資源」（Resource）。在 REST 的世界中，所有東西都是資源——文件、資料、使用者、訂單、照片等。

### 資源的表示

資源是概念上的實體，而「表示」（Representation）是資源的具體呈現：

```
資源 vs 表示：
──────────────
資源：          「使用者 #123」
表示（JSON）：   {"id": 123, "name": "John", "email": "john@example.com"}
表示（XML）：    <user><id>123</id><name>John</name></user>
表示（HTML）：   <div>...</div>
```

## URI 設計

### 基本原則

URI 應該清晰地表達資源：

```http
# 好的 URI 設計
GET /users              # 使用者列表
GET /users/123          # 使用者 #123
GET /users/123/orders   # 使用者 #123 的訂單
POST /users             # 建立新使用者
PUT /users/123          # 更新使用者 #123
DELETE /users/123       # 刪除使用者 #123

# 不好的 URI 設計
GET /getUsers
GET /getUser?id=123
POST /createUser
POST /updateUser?id=123
```

### URI 命名慣例

```http
# 使用名詞，非動詞
GET /products           # 而非 GET /getProducts
GET /orders             # 而非 GET /listOrders

# 使用複數名詞
GET /users              # 而非 GET /user
GET /orders             # 而非 GET /order

# 使用小寫與連字符
GET /user-profiles      # 而非 GET /userProfiles
GET /order-items        # 而非 GET /orderItems

# 使用 ID 而非名稱查詢
GET /users/123          # 而非 GET /users?name=john
```

### 巢狀資源

```http
# 巢狀結構
GET /users/123/orders              # 使用者 #123 的訂單
GET /users/123/orders/456          # 使用者 #123 的訂單 #456
GET /users/123/orders/456/items     # 訂單 #456 的項目

# 過度巢狀是不好的
# 不推薦：GET /orgs/1/depts/2/teams/3/members/4

# 更好的方式
GET /members/4                     # 成員 ID 本身是唯一的
GET /teams/3/members               # 查詢團隊成員
```

## HTTP 動詞

RESTful API 使用標準的 HTTP 動詞：

```http
GET     # 讀取資源（安全、冪等）
POST    # 建立新資源
PUT     # 完全更新資源（冪等）
PATCH   # 部分更新資源
DELETE  # 刪除資源（冪等）
HEAD    # 獲取資源 metadata
OPTIONS # 獲取資源支援的操作
```

### 動詞與資源操作的對應

```
HTTP 動詞與 CRUD 操作：
────────────────────────
動詞      操作         說明                    範例
─────────────────────────────────────────────────────
GET       Read        讀取資源（安全）        GET /users
POST      Create      建立新資源              POST /users
PUT       Update      完全更新資源（冪等）    PUT /users/123
PATCH     Update      部分更新資源            PATCH /users/123
DELETE    Delete      刪除資源（冪等）        DELETE /users/123
```

### 實際範例

```http
# 建立資源
POST /users HTTP/1.1
Content-Type: application/json

{
  "name": "John",
  "email": "john@example.com"
}

---

HTTP/1.1 201 Created
Location: /users/456
Content-Type: application/json

{
  "id": 456,
  "name": "John",
  "email": "john@example.com",
  "created_at": "2007-05-15T10:30:00Z"
}


# 讀取資源
GET /users/456 HTTP/1.1
Accept: application/json

---

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 456,
  "name": "John",
  "email": "john@example.com"
}


# 完全更新資源
PUT /users/456 HTTP/1.1
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}

---

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 456,
  "name": "John Doe",
  "email": "john@example.com",
  "updated_at": "2007-05-15T11:00:00Z"
}


# 部分更新資源
PATCH /users/456 HTTP/1.1
Content-Type: application/json

{
  "email": "newemail@example.com"
}

---

HTTP/1.1 200 OK


# 刪除資源
DELETE /users/456 HTTP/1.1

---

HTTP/1.1 204 No Content
```

## Stateless 設計

REST 要求無狀態（Stateless）——伺服器不應該依賴會話狀態：

```python
# 好的設計：每個請求都包含所有必要資訊
def get_user(request):
    user_id = request.headers.get('X-User-Id')
    auth_token = request.headers.get('Authorization')
    # 不依賴伺服器端 session

# 不好的設計：依賴伺服器 session
def get_user(request):
    user_id = request.session.get('user_id')  # 不好！
```

## HTTP 狀態碼

RESTful API 應該使用適當的 HTTP 狀態碼：

```
常用 HTTP 狀態碼：
─────────────────
2xx 成功
  200 OK            請求成功
  201 Created       資源已建立
  204 No Content    請求成功但無回傳內容

4xx 客戶端錯誤
  400 Bad Request   請求格式錯誤
  401 Unauthorized   需要認證
  403 Forbidden      無權限
  404 Not Found      資源不存在
  409 Conflict       資源衝突
  422 Unprocessable  驗證失敗

5xx 伺服器錯誤
  500 Internal Error 伺服器錯誤
  503 Service Unavailable 服務不可用
```

## 結語

RESTful API 設計的核心原則是**簡單、一致、面向資源**。好的 REST API 應該是：

1. **直觀**：URI 就能表達資源
2. **一致**：相同的模式適用於所有資源
3. **無狀態**：每個請求都是獨立的
4. **使用標準 HTTP**：動詞、狀態碼、標頭

---

## 延伸閱讀

- [RESTful+API+design+principles](https://www.google.com/search?q=RESTful+API+design+principles)
- [HTTP+methods+REST+best+practices](https://www.google.com/search?q=HTTP+methods+REST+best+practices)
- [Roy+Fielding+REST+constraints](https://www.google.com/search?q=Roy+Fielding+REST+constraints)

---

*本篇文章為「AI 程式人雜誌 2007 年 5 月號」本期焦點系列之一。*