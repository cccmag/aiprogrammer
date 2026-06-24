# 實作 REST 伺服器與客戶端

## 前言

本篇將實作一個簡單的 REST API 伺服器，使用 Python Flask 框架，並搭配瀏覽器端的 AJAX 客戶端展示呼叫方式。

---

## 原始碼

完整的 Python 實作：[_code/rest_server.py](_code/rest_server.py)

```python
#!/usr/bin/env python3
"""REST API 伺服器 - Flask 實作"""

from flask import Flask, jsonify, request, abort
from functools import wraps
import time
import hashlib

app = Flask(__name__)

users_db = {
    '1': {'id': '1', 'name': 'John', 'email': 'john@example.com'},
    '2': {'id': '2', 'name': 'Mary', 'email': 'mary@example.com'},
    '3': {'id': '3', 'name': 'Bob', 'email': 'bob@example.com'},
}

posts_db = {
    '1': {'id': '1', 'author_id': '1', 'title': 'Hello World', 'content': 'First post'},
    '2': {'id': '2', 'author_id': '2', 'title': 'REST API', 'content': 'About REST'},
}

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            abort(401, description='Missing authentication')
        # 簡化的認證（實際應用請使用 OAuth 或 JWT）
        if not verify_credentials(auth.username, auth.password):
            abort(401, description='Invalid credentials')
        return f(*args, **kwargs)
    return decorated

def verify_credentials(username, password):
    return username == 'admin' and password == 'secret'

def json_response(data, status=200):
    return jsonify(data), status

@app.route('/api/users', methods=['GET'])
def list_users():
    return json_response({'users': list(users_db.values())})

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if not user:
        abort(404, description='User not found')
    return json_response(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data:
        abort(400, description='Name is required')

    user_id = str(int(max(users_db.keys(), default='0')) + 1)
    user = {
        'id': user_id,
        'name': data['name'],
        'email': data.get('email', '')
    }
    users_db[user_id] = user
    return json_response(user, 201)

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = users_db.get(user_id)
    if not user:
        abort(404, description='User not found')

    data = request.json
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    return json_response(user)

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users_db:
        abort(404, description='User not found')
    del users_db[user_id]
    return '', 204

@app.route('/api/posts', methods=['GET'])
def list_posts():
    return json_response({'posts': list(posts_db.values())})

@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = posts_db.get(post_id)
    if not post:
        abort(404, description='Post not found')
    return json_response(post)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    if not data or 'title' not in data:
        abort(400, description='Title is required')

    post_id = str(int(max(posts_db.keys(), default='0')) + 1)
    post = {
        'id': post_id,
        'author_id': data.get('author_id', '1'),
        'title': data['title'],
        'content': data.get('content', '')
    }
    posts_db[post_id] = post
    return json_response(post, 201)

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': str(e.description)}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': str(e.description)}), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify({'error': str(e.description)}), 401

def demo():
    print('REST API 伺服器範例')
    print('=' * 40)
    print()
    print('可用端點：')
    print('  GET    /api/users          - 列出所有用戶')
    print('  GET    /api/users/<id>    - 取得指定用戶')
    print('  POST   /api/users         - 建立新用戶')
    print('  PUT    /api/users/<id>    - 更新用戶')
    print('  DELETE /api/users/<id>    - 刪除用戶')
    print('  GET    /api/posts         - 列出所有文章')
    print('  GET    /api/posts/<id>    - 取得指定文章')
    print('  POST   /api/posts         - 建立新文章')
    print()
    print('測試客戶端範例：')
    print()
    print('1. 列出所有用戶：')
    print('   curl http://localhost:5000/api/users')
    print()
    print('2. 取得用戶 #1：')
    print('   curl http://localhost:5000/api/users/1')
    print()
    print('3. 建立新用戶：')
    print("   curl -X POST http://localhost:5000/api/users \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"name\": \"Alice\", \"email\": \"alice@example.com\"}'")
    print()
    print('4. 使用認證：')
    print('   curl -u admin:secret http://localhost:5000/api/users')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo()
    else:
        print('啟動伺服器在 http://localhost:5000')
        app.run(debug=True, port=5000)
```

---

## REST 客戶端範例

```python
#!/usr/bin/env python3
"""REST API 客戶端 - 使用 urllib"""

import json
import urllib.request
import base64

BASE_URL = 'http://localhost:5000/api'

def make_request(method, path, data=None, auth=None):
    url = BASE_URL + path

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    if auth:
        credentials = base64.b64encode(f'{auth[0]}:{auth[1]}'.encode()).decode()
        headers['Authorization'] = f'Basic {credentials}'

    if data:
        data = json.dumps(data).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode()
            return json.loads(result) if result else None
    except urllib.error.HTTPError as e:
        error = json.loads(e.read().decode())
        print(f'Error: {error.get("error", str(e))}')
        return None

def demo():
    print('REST 客戶端測試')
    print('=' * 40)

    print('\n1. 列出所有用戶：')
    users = make_request('GET', '/users')
    print(f'   {users}')

    print('\n2. 取得用戶 #1：')
    user = make_request('GET', '/users/1')
    print(f'   {user}')

    print('\n3. 建立新用戶：')
    new_user = make_request('POST', '/users', {'name': 'Alice', 'email': 'alice@test.com'})
    print(f'   {new_user}')

    print('\n4. 使用認證：')
    users = make_request('GET', '/users', auth=('admin', 'secret'))
    print(f'   {users}')

if __name__ == '__main__':
    demo()
```

---

## 測試方式

```bash
# 啟動伺服器
python3 rest_server.py

# 另一個終端執行客戶端測試
python3 rest_client.py
```

### curl 測試

```bash
# 列出所有用戶
curl http://localhost:5000/api/users

# 取得單一用戶
curl http://localhost:5000/api/users/1

# 建立用戶
curl -X POST http://localhost:5000/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Test", "email": "test@example.com"}'

# 更新用戶
curl -X PUT http://localhost:5000/api/users/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated"}'

# 刪除用戶
curl -X DELETE http://localhost:5000/api/users/3

# 使用認證
curl -u admin:secret http://localhost:5000/api/users
```

---

## 設計要點

### REST API 設計原則

1. **資源導向 URL**：`/users` 而非 `/getUsers`
2. **使用 HTTP 方法**：`GET`, `POST`, `PUT`, `DELETE`
3. **正確的狀態碼**：`200 OK`, `201 Created`, `204 No Content`, `404 Not Found`
4. **JSON 格式**：現代 API 的主流選擇

### 錯誤處理

```python
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Invalid request'}), 400
```

---

## 延伸練習

有興趣的讀者可以嘗試以下改進：

1. **加入分頁**：`/users?page=1&limit=10`
2. **加入過濾**：`/users?role=admin`
3. **加入排序**：`/users?sort=name&order=asc`
4. **加入 JWT 認證**
5. **加入速率限制**

---

## 結語

這個簡單的 REST API 展示了 REST 設計的核心原則：
- 資源導向的 URL
- 標準 HTTP 方法
- 無狀態設計
- JSON 格式

實際生產環境需要加入更多功能，但這些基礎原則是不變的。

---

*本篇文章為「AI 程式人雜誌 2007 年 5 月號」程式實作系列之一。*