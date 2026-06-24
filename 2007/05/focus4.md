# Web 服務安全：OAuth 先驅與 API 認證

## API 認證的重要性

2007 年，越來越多的網站開始提供 API。如何安全地認證 API 請求成為重要課題。

### 無認證的風險

```http
# 沒有認證的 API
GET /api/users/123/update-balance?amount=1000

# 攻擊者可以直接修改余額
```

## 早期的 API 認證方式

### 1. API Key

```http
# API Key 認證
GET /api/data?api_key=abc123xyz

# Header 方式
X-API-Key: abc123xyz
```

```python
# 伺服器端驗證
def verify_api_key(api_key):
    return api_key in valid_keys

@app.route('/api/data')
def get_data():
    api_key = request.headers.get('X-API-Key')
    if not verify_api_key(api_key):
        return jsonify({'error': 'Invalid API key'}), 401
    return jsonify({'data': 'secret'})
```

### 2. HTTP Basic Auth

```http
# Basic Auth
Authorization: Basic dXNlcjpwYXNz

# 解碼後：user:pass
```

```python
# Flask Basic Auth
from functools import wraps
from flask import request, jsonify
import base64

def basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not verify_user(auth.username, auth.password):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/protected')
@basic_auth
def protected():
    return jsonify({'secret': 'data'})
```

## OAuth 先驅

2007 年，OAuth 1.0 協議正在制定中。在 OAuth 之前，已有多種「OAuth 先驅」方案：

### Google AuthSub

```python
# Google AuthSub 流程
# 1. 使用者訪問應用，應用請求 AuthSub URL
auth_url = "https://www.google.com/accounts/AuthSubRequest"
next_url = "http://myapp.com/callback"
scope = "http://www.google.com/calendar/feeds/"

# 建構 AuthSub URL
auth_link = f"{auth_url}?next={next_url}&scope={scope}"

# 2. 使用者授權後，Google 返回 token
# 3. 應用使用 token 訪問 Google 服務
headers = {'Authorization': 'AuthSub token=' + token}
response = requests.get(calendar_url, headers=headers)
```

### Yahoo BBAuth

```python
# Yahoo BBAuth
# 使用者訪問應用，應用重定向到 Yahoo
# Yahoo 認證後，返回 auth token
# 應用使用 token 獲取使用者資訊
```

### 這些方案的共同問題

```
早期第三方認證方案的問題：
─────────────────────────
1. 每個服務提供商有自己的實現
2. 沒有統一標準
3. 安全性參差不齊
4. 使用者需要向第三方應用透露密碼
```

## OAuth 1.0 的解決方案

2007 年 11 月，OAuth Core 1.0 草案發布。OAuth 的核心思想是：

### 不向第三方應用透露密碼

```
OAuth 流程（簡化）：
─────────────────────
1. 應用向服務商請求 Request Token
2. 使用者被重定向到服務商，授權
3. 應用獲得 Access Token
4. 應用使用 Access Token 訪問 API
5. 使用者可以撤回對某應用的授權
```

### OAuth 1.0 的簽名機制

```python
# OAuth 1.0 簽名（簡化）
import hashlib
import hmac
import base64
import time
import random

def oauth_sign_base_string(method, url, params, consumer_secret, token_secret=''):
    # 1. 參數排序
    sorted_params = sorted(params.items())

    # 2. 組成字串
    param_str = '&'.join(f'{k}={v}' for k, v in sorted_params)
    base_string = f'{method.upper()}&{quote(url)}&{quote(param_str)}'

    # 3. 簽名
    signing_key = f'{quote(consumer_secret)}&{quote(token_secret)}'
    signature = hmac.new(
        signing_key.encode(),
        base_string.encode(),
        hashlib.sha1
    ).digest()

    return base64.b64encode(signature).decode()
```

### 完整的 OAuth 1.0 流程

```python
# OAuth 1.0 客戶端實作（簡化）
class OAuthClient:
    def __init__(self, consumer_key, consumer_secret, request_token_url,
                 authorize_url, access_token_url, api_base_url):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.request_token_url = request_token_url
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.api_base_url = api_base_url
        self.token = None
        self.token_secret = None

    def get_request_token(self):
        params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': str(random.randint(0, 2**32)),
            'oauth_version': '1.0',
            'oauth_callback': 'oob'  # out-of-band
        }

        # 簽名並發送請求
        # ...

        # 返回 token
        return {'oauth_token': 'token', 'oauth_token_secret': 'secret'}

    def get_authorize_url(self, token):
        return f'{self.authorize_url}?oauth_token={token}'

    def get_access_token(self, verifier):
        # 使用 verifier 換取 access token
        # ...

        self.token = access_token
        self.token_secret = access_token_secret
        return {'oauth_token': access_token}

    def api_call(self, method, path, **kwargs):
        # 使用 access token 調用 API
        # ...
```

## 其他安全考量

### HTTPS 的必要性

```http
# HTTP（不安全）
GET /api/users/123 HTTP/1.1

# 可能被中間人攻擊截獲
```

```http
# HTTPS（安全）
GET /api/users/123 HTTP/1.1
Host: api.example.com

# 傳輸加密，無法被截獲
```

### 輸入驗證

```python
# 驗證 API 輸入
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id < 0:
        return jsonify({'error': 'Invalid user ID'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user)
```

## 結語

2007 年的 API 安全處於過渡期——傳統的 API Key 和 Basic Auth 仍然普遍，但 OAuth 1.0 的出現預示著未來的方向。

OAuth 的核心價值：
1. **不使用戶密碼洩漏**
2. **提供標準化授權流程**
3. **允許使用者撤回授權**
4. **保護使用者隱私**

---

## 延伸閱讀

- [OAuth+1.0+2007+specification](https://www.google.com/search?q=OAuth+1.0+2007+specification)
- [Google+AuthSub+API](https://www.google.com/search?q=Google+AuthSub+API)
- [API+authentication+methods+comparison](https://www.google.com/search?q=API+authentication+methods+comparison)

---

*本篇文章為「AI 程式人雜誌 2007 年 5 月號」本期焦點系列之一。*