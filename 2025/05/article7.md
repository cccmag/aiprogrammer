# API 文件自動生成

## 為什麼需要 API 文件？

API 文件是開發者使用 API 的說明書。良好的 API 文件能大幅降低整合成本。傳統的手寫文件容易過時且難以維護，因此自動生成文件成為最佳實踐。

## OpenAPI 規範

OpenAPI（原名 Swagger）是一種用於描述 RESTful API 的規範。它定義了一個語言無關的介面描述格式，允許人類和電腦理解 API 的功能。

FastAPI 會根據程式碼自動產生 OpenAPI 規範：

```python
from fastapi import FastAPI

app = FastAPI(
    title="任務管理 API",
    description="一個用於管理待辦事項的 RESTful API",
    version="1.0.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "API 支援",
        "url": "https://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)
```

## Swagger UI

FastAPI 自動提供 Swagger UI，訪問 `/docs` 即可查看：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/")
def list_users():
    """取得所有使用者列表（此說明會出現在 Swagger UI 中）"""
    return [{"id": 1, "name": "Alice"}]

@app.post("/users/")
def create_user(name: str, email: str):
    """建立新使用者
    
    - **name**: 使用者名稱（必填）
    - **email**: 電子郵件地址（必填）
    """
    return {"id": 2, "name": name, "email": email}
```

### 自訂 Swagger UI

```python
app = FastAPI(
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "list",
        "syntaxHighlight": {"theme": "monokai"},
    }
)
```

## ReDoc 替代方案

FastAPI 也支援 ReDoc──另一個美觀的 API 文件介面：

```python
from fastapi.openapi.docs import get_redoc_html

@app.get("/redoc", include_in_schema=False)
async def redoc():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
    )
```

預設訪問 `/redoc` 即可使用。

## 請求與回應範例

OpenAPI 支援在 Pydantic 模型中定義範例：

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Alice")
    email: str = Field(..., example="alice@example.com")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Alice",
                    "email": "alice@example.com"
                }
            ]
        }
    }

@app.post("/users/", response_model=User)
def create_user(user: User):
    return user
```

## 標籤分組

使用標籤（Tags）將 API 分組：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/", tags=["使用者"])
def list_users():
    return []

@app.get("/orders/", tags=["訂單"])
def list_orders():
    return []

@app.post("/orders/", tags=["訂單"])
def create_order():
    return {}
```

## 棄用端點

```python
@app.get("/old-endpoint/", deprecated=True)
def old_endpoint():
    """這個端點已棄用，請使用新版 API"""
    return {"message": "This endpoint is deprecated"}
```

## 匯出 OpenAPI JSON/Schema

```python
import requests

# 取得 OpenAPI 規範
resp = requests.get("http://localhost:8000/openapi.json")
openapi_spec = resp.json()
print(openapi_spec["info"]["title"])
print(openapi_spec["paths"].keys())
```

## 自動生成客戶端程式碼

有了 OpenAPI 規範，可以自動生成各種語言的客戶端程式碼：

```python
# 使用 openapi-generator CLI
# 生成 Python 客戶端
# openapi-generator generate -i openapi.json -g python -o ./client
```

## 文件中的安全性說明

```python
from fastapi import FastAPI
from fastapi.security import HTTPBearer

app = FastAPI()

security = HTTPBearer()

@app.get("/secure-data/")
def secure_data(token: str = Depends(security)):
    """此端點需要 Bearer Token 認證"""
    return {"data": "這是受保護的資料"}
```

Swagger UI 會自動顯示「Authorize」按鈕，讓使用者輸入 Token。

## 完整的文件化 API 範例

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="書籍管理 API",
    description="用於管理書籍收藏的 RESTful API",
    version="2.0.0",
)

class Book(BaseModel):
    title: str
    author: str
    year: int
    isbn: str
    tags: List[str] = []

class BookResponse(Book):
    id: int

books_db = []

@app.get("/books/", response_model=List[BookResponse], tags=["書籍"])
def list_books(
    author: Optional[str] = Query(None, description="依作者過濾"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """取得所有書籍，支援過濾和分頁"""
    result = books_db
    if author:
        result = [b for b in result if b["author"] == author]
    return result[skip:skip + limit]

@app.post("/books/", response_model=BookResponse,
    status_code=201, tags=["書籍"])
def create_book(book: Book):
    """新增一本書到收藏"""
    new = {"id": len(books_db) + 1, **book.model_dump()}
    books_db.append(new)
    return new
```

---

## 延伸閱讀

- [OpenAPI 官方規範](https://www.google.com/search?q=OpenAPI+specification+3.1)
- [Swagger UI 官方文件](https://www.google.com/search?q=Swagger+UI+documentation)
- [FastAPI OpenAPI 整合](https://www.google.com/search?q=FastAPI+OpenAPI+integration)
