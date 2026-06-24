# 測試驅動的 API 設計

## 前言

TDD 不只用於功能實作，也可用於 API 設計。先寫測試，明確定義 API 的預期行為，再進行實作。

## API TDD 流程

```
1. 撰寫 API 規格（測試案例）
2. 執行測試（預期失敗）
3. 實作 API
4. 重構與驗證
```

## Flask API 實作

### 第一步：寫測試

```python
# test_api.py
import pytest
from flask import json

@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post('/api/users', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['email'] == 'test@example.com'
    assert 'id' in data
    assert 'password' not in data  # 安全檢查

def test_create_user_invalid_email(client):
    response = client.post('/api/users', json={
        'email': 'invalid-email',
        'name': 'Test'
    })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_user(client):
    # 先建立
    create_resp = client.post('/api/users', json={
        'email': 'user@example.com',
        'name': 'User'
    })
    user_id = json.loads(create_resp.data)['id']
    
    # 再取得
    response = client.get(f'/api/users/{user_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'user@example.com'

def test_get_user_not_found(client):
    response = client.get('/api/users/9999')
    assert response.status_code == 404
```

### 第二步：實作 API

```python
# app.py
from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

users_db = {}

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data.get('email') or not validate_email(data['email']):
        return jsonify({'error': 'Invalid email'}), 400
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    user_id = str(uuid.uuid4())[:8]
    user = {
        'id': user_id,
        'email': data['email'],
        'name': data['name'],
        'created_at': datetime.now().isoformat()
    }
    users_db[user_id] = user
    
    return jsonify(user), 201

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/api/users', methods=['GET'])
def list_users():
    return jsonify(list(users_db.values()))

def create_app():
    return app
```

## RESTful 設計原則

| 方法 | 路徑 | 說明 | 測試案例 |
|------|------|------|----------|
| GET | /users | 列出所有使用者 | 200, 陣列 |
| GET | /users/:id | 取得特定使用者 | 200, 404 |
| POST | /users | 建立新使用者 | 201, 400 |
| PUT | /users/:id | 更新使用者 | 200, 404 |
| DELETE | /users/:id | 刪除使用者 | 204, 404 |

## API 版本管理

```python
@app.route('/api/v1/users', methods=['GET'])
def list_users_v1():
    return jsonify({'version': 'v1', 'users': []})

@app.route('/api/v2/users', methods=['GET'])
def list_users_v2():
    return jsonify({'version': 'v2', 'data': []})
```

## 測試輔助函式

```python
# test_helpers.py
import functools

def with_auth(func):
    @functools.wraps(func)
    def wrapper(client, *args, **kwargs):
        # 登入取得 token
        login_resp = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = json.loads(login_resp.data)['token']
        
        # 在 header 中附加 token
        headers = {'Authorization': f'Bearer {token}'}
        return func(client, headers=headers, *args, **kwargs)
    return wrapper

def test_protected_endpoint(client, headers):
    response = client.get('/api/protected', headers=headers)
    assert response.status_code == 200
```

## 延伸閱讀

- [Flask RESTful API 教學](https://www.google.com/search?q=flask+rest+api+tutorial+2016)
- [API TDD 實踐](https://www.google.com/search?q=test+driven+api+development+2016)
- [RESTful API 設計指南](https://www.google.com/search?q=restful+api+design+guidelines+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*