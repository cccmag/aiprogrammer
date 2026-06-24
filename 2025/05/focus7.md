# API 設計最佳實踐

## 資源命名規範

一致的資源命名是良好 API 設計的基石。良好的命名讓 API 直覺、易於理解。

### 基本原則

```python
# 好的命名（複數名詞）
GET    /users              # 使用者列表
GET    /users/{id}         # 特定使用者
POST   /users              # 建立使用者
PUT    /users/{id}         # 更新使用者
DELETE /users/{id}         # 刪除使用者

# 不好的命名（動詞、單數、不一致）
GET    /getUser
POST   /create_user
PUT    /updateUser/1
DELETE /delete_user/1
```

### 巢狀資源

```python
GET    /users/{id}/orders            # 使用者的訂單
GET    /users/{id}/orders/{oid}      # 特定訂單
GET    /orders/{id}/items            # 訂單中的物品
```

### 搜尋與過濾

```python
# 使用查詢參數
GET    /products?category=electronics
GET    /products?q=search+term
GET    /products?min_price=100&max_price=500
GET    /products?sort=price&order=desc
```

## 分頁

```python
# 基於偏移的分頁
GET    /items?offset=0&limit=20

# 基於游標的分頁（推薦用於大型資料集）
GET    /items?cursor=abc123&limit=20
```

分頁回應格式：

```python
response = {
    "data": [...],
    "pagination": {
        "total": 100,
        "offset": 0,
        "limit": 20,
        "next": "/items?offset=20&limit=20",
        "prev": None
    }
}
```

## API 版本控制

```python
# URL 路徑版本（最常見）
GET    /v1/users
GET    /v2/users

# 請求頭版本
GET    /users
Accept: application/vnd.example.v2+json
```

在 FastAPI 中使用路徑版本：

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

@v1_router.get("/users")
def list_users_v1():
    return [{"id": 1, "name": "Alice"}]

@v2_router.get("/users")
def list_users_v2():
    return [{"id": 1, "name": "Alice", "email": "alice@example.com"}]

app.include_router(v1_router)
app.include_router(v2_router)
```

## 錯誤回應格式

統一的錯誤回應格式讓客戶端更容易處理錯誤：

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: dict = None

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "request_error",
            "message": exc.detail,
            "details": None
        }
    )

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(400, "ID 必須為正整數")
    return {"id": item_id}
```

建議的錯誤格式：

```json
{
    "error": "validation_error",
    "message": "輸入驗證失敗",
    "details": {
        "fields": {
            "email": "格式無效",
            "age": "必須大於 0"
        }
    },
    "request_id": "req-abc-123"
}
```

## 冪等性（Idempotency）

冪等性確保多次執行相同請求的效果與一次執行相同：

```python
# GET 是冪等的：多次查詢結果相同
GET /users/1

# PUT 是冪等的：多次更新的結果相同
PUT /users/1 {"name": "Alice"}

# POST 不是冪等的：每次建立新資源
POST /users {"name": "Alice"}

# DELETE 是冪等的：刪除後的狀態相同
DELETE /users/1
```

## 速率限制與節流

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import time

app = FastAPI()
limits = {}

def rate_limit(client_id: str, max_req: int = 100, window: int = 60):
    now = int(time.time())
    key = f"{client_id}:{now // window}"
    count = limits.get(key, 0)
    if count >= max_req:
        raise HTTPException(429, "請求過於頻繁")
    limits[key] = count + 1

@app.get("/api")
def api_endpoint():
    rate_limit("client-1")
    return {"message": "成功"}
```

## 回應中繼資料

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = "95"
    response.headers["X-Request-ID"] = "req-abc-123"
    return {"id": item_id}
```

## API 文件的重要性

使用 OpenAPI/Swagger 自動生成文件：

```python
from fastapi import FastAPI

app = FastAPI(
    title="商店 API",
    description="這是一個範例商店的 REST API",
    version="2.0.0",
    contact={"name": "支援團隊", "email": "support@example.com"},
    license_info={"name": "MIT"}
)
```

訪問 `http://localhost:8000/docs` 查看 Swagger UI。

---

## 延伸閱讀

- [Google API 設計指南](https://www.google.com/search?q=Google+API+design+guide)
- [Microsoft REST API 指南](https://www.google.com/search?q=Microsoft+REST+API+guidelines)
- [OpenAPI 規範](https://www.google.com/search?q=OpenAPI+specification)
