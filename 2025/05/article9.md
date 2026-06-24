# 錯誤處理與狀態碼

## 錯誤處理的重要性

良好的錯誤處理是優秀 API 與平庸 API 的分水嶺。適當的錯誤回應讓客戶端開發者能夠快速理解問題所在，並採取正確的應對措施。

## HTTP 狀態碼的正確使用

### 常見錯誤狀態碼場景

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    # 400：請求格式錯誤
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="ID 必須為正整數")

    # 401：未認證
    # 由認證中介軟體處理

    # 403：無權限
    # 由授權中介軟體處理

    # 404：資源不存在
    if item_id > 100:
        raise HTTPException(status_code=404, detail="物品不存在")

    # 409：資源衝突
    # 例如建立重複的資源

    # 422：驗證錯誤
    # FastAPI 自動處理型別驗證錯誤

    # 429：請求過於頻繁
    # 由速率限制中介軟體處理

    # 500：伺服器錯誤（不應主動拋出，讓例外處理器處理）
    return {"id": item_id, "name": f"物品 {item_id}"}
```

## 統一的錯誤回應格式

定義一致的錯誤回應結構：

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict] = None
    request_id: Optional[str] = None

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=f"ERR_{exc.status_code}",
            message=exc.detail,
            request_id=request.headers.get("X-Request-ID")
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="ERR_500",
            message="伺服器內部錯誤",
            request_id=request.headers.get("X-Request-ID")
        ).model_dump()
    )
```

## 輸入驗證錯誤

```python
from pydantic import BaseModel, Field, field_validator

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str
    age: int = Field(ge=0, le=150)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email 格式無效')
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('使用者名稱只能包含字母和數字')
        return v

@app.post("/users/")
def create_user(user: UserCreate):
    return {"message": "使用者建立成功", "user": user}
```

## 自訂例外類別

```python
class NotFoundError(Exception):
    def __init__(self, resource: str, resource_id):
        self.resource = resource
        self.resource_id = resource_id
        self.message = f"{resource}（ID: {resource_id}）不存在"
        super().__init__(self.message)

class BusinessError(Exception):
    def __init__(self, message: str, code: str = "BUSINESS_ERROR"):
        self.code = code
        self.message = message
        super().__init__(self.message)

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error_code="NOT_FOUND",
            message=exc.message,
        ).model_dump()
    )

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error_code=exc.code,
            message=exc.message,
        ).model_dump()
    )
```

## 客戶端錯誤處理

```python
import requests

def safe_api_call(url: str, **kwargs):
    try:
        response = requests.get(url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "REQUEST_TIMEOUT", "message": "請求逾時"}
    except requests.exceptions.ConnectionError:
        return {"error": "CONNECTION_ERROR", "message": "無法連線"}
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 404:
            return {"error": "NOT_FOUND", "message": "資源不存在"}
        elif status == 429:
            return {"error": "RATE_LIMITED", "message": "請求過於頻繁"}
        elif status == 500:
            return {"error": "SERVER_ERROR", "message": "伺服器錯誤"}
        return {"error": f"HTTP_{status}", "message": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": "UNKNOWN", "message": str(e)}
```

## 驗證錯誤的詳細回應

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "輸入驗證失敗",
            "details": errors
        }
    )
```

## requests 的錯誤重試

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

def create_retry_session(retries: int = 3):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

session = create_retry_session()
try:
    resp = session.get("https://api.example.com/unstable", timeout=10)
    resp.raise_for_status()
except requests.exceptions.RetryError:
    print("重試次數已用完，請求仍然失敗")
```

---

## 延伸閱讀

- [HTTP 狀態碼 RFC 7231](https://www.google.com/search?q=HTTP+status+codes+RFC+7231)
- [FastAPI 錯誤處理](https://www.google.com/search?q=FastAPI+error+handling)
- [REST API 錯誤回應規範](https://www.google.com/search?q=REST+API+error+response+best+practices)
