# 路徑參數與查詢參數

## 參數類型概覽

在 Web API 中，參數可以透過多種方式傳遞：路徑參數、查詢參數、請求主體、請求頭和 Cookie。路徑參數和查詢參數是最常用的兩種方式。

## 路徑參數（Path Parameters）

路徑參數是 URL 路徑的一部分，用於識別特定資源。例如，在 `/users/42` 中，`42` 就是路徑參數。

### FastAPI 中的路徑參數

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "message": f"查詢使用者 {user_id}"}
```

### 多個路徑參數

```python
@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {
        "user_id": user_id,
        "order_id": order_id,
        "message": f"查詢使用者 {user_id} 的訂單 {order_id}"
    }
```

### 路徑參數的型別驗證

FastAPI 會根據型別提示自動驗證路徑參數：

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):      # 自動驗證是否為整數
    return {"item_id": item_id}

@app.get("/files/{file_path:path}")
def get_file(file_path: str):    # :path 允許包含斜線的路徑
    return {"file_path": file_path}
```

請求 `/items/abc` 會回傳 422 驗證錯誤，因為 `abc` 無法轉換為整數。

### 路徑參數的預定義值（Enum）

```python
from enum import Enum
from fastapi import FastAPI

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"

app = FastAPI()

@app.get("/products/{category}")
def get_products(category: Category):
    return {
        "category": category,
        "message": f"瀏覽 {category.value} 類別"
    }
```

## 查詢參數（Query Parameters）

查詢參數是 URL 中 `?` 後面的鍵值對，用於過濾、排序和分頁。

### 基本查詢參數

```python
@app.get("/items/")
def list_items(
    skip: int = 0,          # 可選，預設 0
    limit: int = 10,        # 可選，預設 10
    search: str = None,     # 可選字串
):
    return {
        "skip": skip,
        "limit": limit,
        "search": search,
        "results": []
    }
```

訪問 `http://localhost:8000/items/?skip=0&limit=20&search=python`。

### 必填查詢參數

```python
@app.get("/search/")
def search(q: str):          # 無預設值 → 必填
    return {"query": q}
```

未提供 `q` 參數時回傳 422 錯誤。

### 布林值查詢參數

```python
@app.get("/products/")
def list_products(
    available: bool = True,
    on_sale: bool = False
):
    return {"available": available, "on_sale": on_sale}
```

訪問 `http://localhost:8000/products/?available=true&on_sale=false`。

### 列表查詢參數

```python
from typing import List

@app.get("/items/")
def filter_items(tags: List[str] = []):
    return {"tags": tags, "message": f"過濾標籤：{tags}"}
```

訪問 `http://localhost:8000/items/?tags=python&tags=api&tags=fastapi`。

## 路徑參數 vs 查詢參數

選擇原則：

```python
# 路徑參數：用於識別特定資源
GET /users/{user_id}           # 特定使用者
GET /users/{user_id}/orders    # 特定使用者的所有訂單

# 查詢參數：用於過濾、排序、分頁
GET /users?role=admin          # 過濾管理員
GET /users?page=2&limit=20    # 分頁
GET /users?sort=created_at     # 排序
```

## 參數驗證（Path 和 Query）

使用 FastAPI 的 `Path` 和 `Query` 進行更精細的驗證：

```python
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., title="物品 ID", ge=1, le=1000),
    q: str = Query(None, title="搜尋關鍵字", max_length=50),
    price: float = Query(0, ge=0, le=10000)
):
    return {
        "item_id": item_id,
        "q": q,
        "price": price
    }
```

### 別名查詢參數

```python
@app.get("/items/")
def list_items(
    page_number: int = Query(1, alias="page"),
    items_per_page: int = Query(10, alias="per_page")
):
    return {"page": page_number, "per_page": items_per_page}
```

客戶端使用 `?page=2&per_page=20` 而非 `?page_number=2&items_per_page=20`。

## 使用 requests 傳遞參數

```python
import requests

# 路徑參數
url = f"https://api.github.com/users/octocat"

# 查詢參數
params = {
    "q": "python",
    "sort": "stars",
    "order": "desc",
    "per_page": 5
}
response = requests.get("https://api.github.com/search/repositories",
    params=params)
print(response.url)  # 自動編碼參數
```

---

## 延伸閱讀

- [FastAPI Path 參數](https://www.google.com/search?q=FastAPI+path+parameters)
- [FastAPI Query 參數](https://www.google.com/search?q=FastAPI+query+parameters)
- [REST API URL 設計](https://www.google.com/search?q=REST+API+URL+design+best+practices)
