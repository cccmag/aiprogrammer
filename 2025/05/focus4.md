# FastAPI 建立 REST API

## FastAPI 簡介

FastAPI 是由 Sebastián Ramírez 於 2018 年建立的現代 Python Web 框架。它以高效能（與 Node.js 和 Go 相當）、自動 API 文件生成（OpenAPI + Swagger）和基於 Python 型別提示的資料驗證聞名。FastAPI 基於 Starlette（Web 層）和 Pydantic（資料層）構建。

## 安裝與第一個應用

```bash
pip install fastapi uvicorn
```

```python
from fastapi import FastAPI

app = FastAPI(title="我的 API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

```bash
uvicorn main:app --reload
```

執行後訪問 `http://localhost:8000/docs` 即可看到 Swagger UI 文件。

## 路徑參數

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "message": f"查詢物品 {item_id}"}

@app.get("/users/{username}")
def read_user(username: str):
    return {"username": username}
```

FastAPI 會自動根據型別提示進行參數驗證：`item_id` 必須是整數，否則回傳 422 驗證錯誤。

## 查詢參數

```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10, category: str = None):
    return {"skip": skip, "limit": limit, "category": category}
```

訪問 `http://localhost:8000/items/?skip=0&limit=5&category=book`。

查詢參數可選的秘訣：給予預設值或型別註記為 `Optional`。

## 請求主體（Pydantic 模型）

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

Pydantic 會自動驗證請求主體：`name` 必須是字串、`price` 必須是浮點數。

### 巢狀模型

```python
from pydantic import BaseModel
from typing import List

class Tag(BaseModel):
    name: str
    color: str = "blue"

class Article(BaseModel):
    title: str
    content: str
    tags: List[Tag] = []

@app.post("/articles/")
def create_article(article: Article):
    return article
```

## 回應模型

```python
from pydantic import BaseModel
from typing import Optional

class ItemOut(BaseModel):
    id: int
    name: str
    price: float

@app.post("/items/", response_model=ItemOut)
def create_item(name: str, price: float):
    # 實際應用中這裡會存入資料庫
    item = {"id": 123, "name": name, "price": price}
    return item  # FastAPI 會自動過濾欄位
```

回應模型確保 API 只回傳客戶端需要的欄位，不會洩漏內部資料。

## 路徑操作與 HTTP 方法

```python
ITEMS = []

@app.get("/items/")
def list_items():
    return ITEMS

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    return {"error": "not found"}

@app.post("/items/")
def create_item(item: Item):
    new_item = item.dict()
    new_item["id"] = len(ITEMS) + 1
    ITEMS.append(new_item)
    return new_item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    for i, existing in enumerate(ITEMS):
        if existing["id"] == item_id:
            ITEMS[i] = {"id": item_id, **item.dict()}
            return ITEMS[i]
    return {"error": "not found"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, existing in enumerate(ITEMS):
        if existing["id"] == item_id:
            ITEMS.pop(i)
            return {"message": "deleted"}
    return {"error": "not found"}
```

## 錯誤處理

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="ID 必須大於 0")
    item = find_item(item_id)  # 假設的函式
    if item is None:
        raise HTTPException(status_code=404, detail="物品不存在")
    return item
```

## 完整的 CRUD 範例

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False

class TaskOut(Task):
    id: int

tasks = []
counter = 1

@app.post("/tasks/", response_model=TaskOut)
def create_task(task: Task):
    global counter
    new = {"id": counter, **task.dict()}
    tasks.append(new)
    counter += 1
    return new

@app.get("/tasks/", response_model=List[TaskOut])
def list_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(404, "任務不存在")

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks[i] = {"id": task_id, **task.dict()}
            return tasks[i]
    raise HTTPException(404, "任務不存在")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return {"message": "已刪除"}
    raise HTTPException(404, "任務不存在")
```

---

## 延伸閱讀

- [FastAPI 官方文件](https://www.google.com/search?q=FastAPI+official+documentation)
- [Pydantic 官方文件](https://www.google.com/search?q=Pydantic+official+documentation)
- [Starlette 官方文件](https://www.google.com/search?q=Starlette+framework)
