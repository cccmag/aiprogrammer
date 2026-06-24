# API 程式設計

## REST API 基礎

REST（Representational State Transfer）是現代 Web API 的主流架構風格。

### HTTP 方法對應 CRUD

| 方法 | 操作 | 範例 |
|------|------|------|
| GET | 讀取資源 | GET /users/1 |
| POST | 創建資源 | POST /users |
| PUT | 更新資源 | PUT /users/1 |
| DELETE | 刪除資源 | DELETE /users/1 |

### 狀態碼

| 狀態碼 | 意義 |
|--------|------|
| 200 | 成功 |
| 201 | 已創建 |
| 400 | 請求錯誤 |
| 401 | 未授權 |
| 404 | 找不到 |
| 500 | 伺服器錯誤 |

## Python requests 庫

```python
import requests

# GET
response = requests.get("https://api.example.com/users")
print(response.json())

# 带 header
headers = {"Authorization": "Bearer token123"}
response = requests.get("https://api.example.com/protected", headers=headers)

# POST 带 JSON
data = {"name": "Alice", "email": "alice@example.com"}
response = requests.post("https://api.example.com/users", json=data)
print(response.status_code)
```

## Flask 快速建立 API

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# 模擬資料庫
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_id = max(u["id"] for u in users) + 1
    user = {"id": new_id, "name": data["name"], "email": data["email"]}
    users.append(user)
    return jsonify(user), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user.update(data)
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return "", 204

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

## 測試 API

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# 測試 GET
response = requests.get(f"{BASE_URL}/users")
print(response.json())

# 測試 POST
new_user = {"name": "Charlie", "email": "charlie@example.com"}
response = requests.post(f"{BASE_URL}/users", json=new_user)
print(response.status_code, response.json())

# 測試 PUT
updated = {"name": "Charles"}
response = requests.put(f"{BASE_URL}/users/3", json=updated)
print(response.json())
```

## 錯誤處理

```python
import requests

def safe_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 錯誤: {e}")
    except requests.exceptions.ConnectionError:
        print("連線錯誤")
    except requests.exceptions.Timeout:
        print("請求超時")
    except requests.exceptions.RequestException as e:
        print(f"請求失敗: {e}")
    return None

result = safe_request("GET", "https://api.example.com/data")
```

## API 認證

### Basic Auth

```python
from requests.auth import HTTPBasicAuth

response = requests.get(
    "https://api.example.com/protected",
    auth=HTTPBasicAuth("username", "password")
)
```

### Token Auth

```python
headers = {"Authorization": "Bearer your_token_here"}
response = requests.get("https://api.example.com/user", headers=headers)
```

## 速率限制處理

```python
import time

def rate_limited_request(get_url, max_retries=3):
    for i in range(max_retries):
        response = requests.get(url)

        if response.status_code == 429:
            # 速率限制，等待後重試
            retry_after = int(response.headers.get("Retry-After", 60))
            print(f"速率限制，等待 {retry_after} 秒")
            time.sleep(retry_after)
        else:
            return response

    return None
```

## 總結

REST API 是前後端分離的基礎。Flask 是快速建立 Python API 的好工具。實際應用需注意錯誤處理、認證、速率限制等問題。