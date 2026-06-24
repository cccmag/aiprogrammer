# API 安全設計

## API 安全的挑戰

API 面臨著與傳統 Web 應用不同的安全挑戰：
- 無狀態設計更需要依赖身份驗證
- 更廣的攻击面（多種客戶端）
- 需要同時保護效能與安全

## 速率限制（Rate Limiting）

防止 API 滥用和暴力破解：

```python
from flask import Flask, request, jsonify, g
import redis
import time

app = Flask(__name__)
redis_client = redis.Redis()

@app.before_request
def check_rate_limit():
    # 根據 IP 或 API Key 限制
    key = f"rate_limit:{request.api_key or request.remote_addr}"

    current = redis_client.get(key)
    if current is None:
        redis_client.setex(key, 60, 1)
        g.remaining = 59
    else:
        if int(current) >= 100:  # 每分鐘 100 次
            return jsonify(error="Rate limit exceeded"), 429
        redis_client.incr(key)
        g.remaining = 100 - int(current)
```

### 響應 Header

```python
@app.after_request
def add_rate_headers(response):
    response.headers['X-RateLimit-Limit'] = '100'
    response.headers['X-RateLimit-Remaining'] = str(g.get('remaining', 0))
    return response
```

## OAuth 2.0

OAuth 2.0 是授權的行业標準，適用於第三方應用存取：

### 授權碼流程（Authorization Code Flow）

```
1. 使用者訪問客戶端，客戶端導向授權伺服器
2. 使用者同意授權
3. 授權伺服器返回授權碼
4. 客戶端用授權碼換取 Access Token
5. 客戶端用 Access Token 存取資源
```

### 實作

```python
# 授權端點
@app.route('/oauth/authorize')
def authorize():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    response_type = request.args.get('response_type')
    scope = request.args.get('scope')

    # 驗證 client_id 和 redirect_uri
    client = get_client(client_id)
    if not client or client.redirect_uri != redirect_uri:
        return jsonify(error="invalid_request"), 400

    if response_type != 'code':
        return jsonify(error="unsupported_response_type"), 400

    # 檢查使用者是否已登入，顯示授權頁面
    if not current_user:
        return redirect(url_for('login', next=request.url))

    # 產生授權碼
    code = generate_auth_code()
    save_auth_code(code, client_id, current_user.id, scope)

    return redirect(f"{redirect_uri}?code={code}")
```

## API Key 管理

對於機器對機器（M2M）通訊，API Key 是常見的方案：

### 產生安全的 API Key

```python
import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)
```

### 驗證 API Key

```python
@app.before_request
def verify_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return jsonify(error="API key required"), 401

    user = validate_api_key(api_key)
    if not user:
        return jsonify(error="Invalid API key"), 401

    g.current_user = user
```

### API Key 的安全性

1. 只在傳輸層加密（TLS）下傳輸
2. 儲存時使用 bcrypt 雜湊
3. 支援 multiple keys 讓更換方便
4. 提供過期時間

## JWT 在 API 的使用

```python
@app.route('/api/data')
def get_data():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return jsonify(error="Token required"), 401

    token = auth[7:]
    payload = verify_jwt(token)
    if not payload:
        return jsonify(error="Invalid token"), 401

    return jsonify(data=get_user_data(payload['user_id']))
```

## CORS（跨域資源共享）

正確設定 CORS 防止不需要的跨域存取：

```python
@app.after_request
def add_cors_headers(response):
    allowed_origins = ['https://example.com']
    origin = request.headers.get('Origin')

    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '3600'

    return response
```

## 輸入驗證

```python
from marshmallow import Schema, validate, ValidationError

class UserSchema(Schema):
    name = validate.Length(min=1, max=100)
    email = validate.Email()
    age = validate.Range(min=0, max=150)

@app.route('/api/users', methods=['POST'])
def create_user():
    schema = UserSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(errors=err.messages), 400

    return jsonify(create_user(data)), 201
```

## 錯誤處理

不要在錯誤回應中透露系統資訊：

```python
@app.errorhandler(Exception)
def handle_error(e):
    if app.debug:
        return jsonify(error=str(e)), 500

    logger.error(f"Error: {e}")
    return jsonify(error="An error occurred"), 500
```

## 參考資源

- https://www.google.com/search?q=API+安全+設計+OAuth2+JWT+速率限制+2016
- https://www.google.com/search?q=RESTful+API+安全+Best+Practices+驗證+授權+CORS
- https://www.google.com/search?q=API+Key+vs+JWT+vs+OAuth+比較+選擇+建議