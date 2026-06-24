# FastAPI 快速入門

## FastAPI 的優勢

FastAPI 是 Python 生態系中最受歡迎的新一代 Web 框架。與 Flask 和 Django 相比，FastAPI 具有以下優勢：

1. **高效能**：基於 ASGI，效能可與 Node.js 和 Go 媲美
2. **自動文件**：內建 OpenAPI 和 Swagger UI
3. **型別安全**：基於 Python 型別提示的資料驗證
4. **非同步支援**：原生支援 async/await
5. **現代化**：支援 WebSocket、GraphQL、背景任務等

## 環境準備

```bash
pip install fastapi uvicorn
```

## Hello World API

```python
from fastapi import FastAPI

app = FastAPI(title="我的第一個 API")

@app.get("/")
def hello():
    return {"message": "Hello, FastAPI!"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"greeting": f"你好，{name}！"}
```

## 啟動伺服器

```bash
uvicorn main:app --reload
```

參數說明：
- `main:app`：檔案名稱 `main.py`，變數名稱 `app`
- `--reload`：開發模式，修改程式碼後自動重啟
- `--port 8000`：指定通訊埠
- `--host 0.0.0.0`：允許外部連線

## Pydantic 模型與資料驗證

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(ge=0, le=150, default=0)
    is_active: bool = True
    tags: list[str] = []

@app.post("/users/")
def create_user(user: User):
    return {
        "message": f"使用者 {user.name} 建立成功",
        "user": user
    }
```

## 多個端點的組織

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items_db = []

@app.get("/")
def root():
    return {"service": "商店 API", "version": "1.0"}

@app.get("/items/")
def list_items():
    return {"items": items_db, "total": len(items_db)}

@app.post("/items/")
def create_item(item: Item):
    new = {"id": len(items_db) + 1, **item.model_dump()}
    items_db.append(new)
    return new

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "not found"}
```

## 型別提示與自動驗證

FastAPI 的最大特色是利用 Python 型別提示進行自動驗證：

```python
@app.get("/search/")
def search_items(
    q: str,                    # 必填字串
    page: int = 1,             # 可選整數，預設值 1
    limit: int = 10,           # 可選整數，預設值 10
    sort: str = "name",        # 可選字串，預設值 "name"
    desc: bool = False,        # 可選布林值
):
    return {
        "query": q,
        "page": page,
        "limit": limit,
        "sort": sort,
        "descending": desc
    }
```

訪問 `http://localhost:8000/search/?q=python&page=2&limit=20&desc=true`，FastAPI 會自動將參數轉換為正確的型別。

## 請求頭與 Cookie

```python
from fastapi import FastAPI, Header, Cookie

app = FastAPI()

@app.get("/headers/")
def read_headers(
    user_agent: str = Header(None),
    accept: str = Header(None),
    x_token: str = Header(None, alias="X-Token")
):
    return {
        "User-Agent": user_agent,
        "Accept": accept,
        "X-Token": x_token
    }

@app.get("/cookies/")
def read_cookies(session_id: str = Cookie(None)):
    return {"session_id": session_id}
```

## 回應狀態碼

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(name: str, price: float):
    return {"name": name, "price": price}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None
```

## 靜態檔案服務

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
```

將 HTML、CSS、JS 檔案放在 `static/` 目錄下，即可透過 `/static/filename` 存取。

## 背景任務

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str, message: str):
    # 模擬發送郵件
    print(f"發送郵件到 {email}：{message}")

@app.post("/notify/")
def notify(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "歡迎使用！")
    return {"message": "通知已排入佇列"}
```

---

## 延伸閱讀

- [FastAPI 官方教學](https://www.google.com/search?q=FastAPI+tutorial)
- [Pydantic V2 文件](https://www.google.com/search?q=Pydantic+v2+documentation)
- [Uvicorn 部署指南](https://www.google.com/search?q=Uvicorn+deployment)
