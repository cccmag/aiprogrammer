# API 認證與安全性

## 為什麼需要 API 認證？

Web API 暴露在網際網路上，如果沒有適當的認證機制，任何人都可以存取你的 API。認證（Authentication）確認使用者是誰，授權（Authorization）確認使用者能做什麼。

## API Key 認證

API Key 是最簡單的認證方式。伺服器為每個客戶端產生唯一的金鑰，客戶端在每次請求中帶入該金鑰。

```python
import requests

API_KEY = "your-api-key-here"
headers = {"X-API-Key": API_KEY}
response = requests.get("https://api.example.com/data", headers=headers)
```

### FastAPI 實作 API Key

```python
from fastapi import FastAPI, HTTPException, Header

VALID_KEYS = {"key1", "key2", "key3"}

app = FastAPI()

@app.get("/data")
def get_data(x_api_key: str = Header(...)):
    if x_api_key not in VALID_KEYS:
        raise HTTPException(status_code=403, detail="無效的 API Key")
    return {"data": "這是受保護的資料"}
```

## JWT（JSON Web Token）

JWT 是一種基於 JSON 的開放標準（RFC 7519），用於在各方之間安全地傳遞聲明。JWT 由三部分組成：Header、Payload、Signature。

```python
import jwt
from datetime import datetime, timedelta

# 建立 JWT
def create_token(user_id: int, secret: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, secret, algorithm="HS256")

# 驗證 JWT
def verify_token(token: str, secret: str):
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

secret = "my-secret-key"
token = create_token(42, secret)
print(f"Token: {token}")
payload = verify_token(token, secret)
print(f"Payload: {payload}")
```

### FastAPI 整合 JWT

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

app = FastAPI()
security = HTTPBearer()
SECRET = "my-secret-key"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="無效的 Token")

@app.get("/profile")
def get_profile(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id, "message": "這是個人資料"}
```

## OAuth2 授權框架

OAuth2 是一種授權框架，允許第三方應用程式在不用戶提供密碼的情況下，獲得有限的資源存取權限。常見的 OAuth2 流程：授權碼流程（Authorization Code Flow）是安全度最高的方式。

FastAPI 內建 OAuth2 支援：

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(username: str, password: str):
    # 驗證使用者身份
    if username == "admin" and password == "secret":
        token = create_token(1, SECRET)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(400, "帳號或密碼錯誤")

@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "你已通過驗證", "token": token}
```

## HTTPS 與 TLS

HTTPS（HTTP Secure）是 HTTP 的安全版本，透過 TLS（Transport Layer Security）加密通訊內容。

```python
# 使用 HTTPS 發起請求
response = requests.get("https://api.github.com/users/octocat")
print(response.url)  # https://...
```

在 FastAPI 中啟用 HTTPS：

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=443, ssl_keyfile="key.pem",
        ssl_certfile="cert.pem")
```

## 速率限制（Rate Limiting）

防止 API 被過度使用：

```python
from fastapi import FastAPI, HTTPException
from collections import defaultdict
import time

app = FastAPI()
rate_limits = defaultdict(list)
LIMIT = 100  # 每分鐘最多 100 個請求

@app.get("/api")
def api_endpoint(client_id: str = "anonymous"):
    now = time.time()
    requests = rate_limits[client_id]
    requests[:] = [t for t in requests if now - t < 60]
    if len(requests) >= LIMIT:
        raise HTTPException(429, "請求過於頻繁，請稍後再試")
    requests.append(now)
    return {"message": "成功"}
```

## 安全最佳實踐

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
import hashlib
import hmac

app = FastAPI()
security = HTTPBearer()

def verify_signature(payload: bytes, signature: str, secret: str):
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/webhook")
def webhook_handler(payload: dict, x_signature: str = Header(...)):
    if not verify_signature(str(payload).encode(), x_signature, "webhook-secret"):
        raise HTTPException(400, "簽名驗證失敗")
    return {"status": "received"}
```

### 安全檢查清單

1. 使用 HTTPS（絕不使用 HTTP）
2. 驗證所有輸入資料（型別、格式、範圍）
3. 使用強認證機制（JWT 或 OAuth2）
4. 實作速率限制
5. 記錄所有 API 存取日誌
6. 使用安全的密碼雜湊（bcrypt）
7. 避免在 URL 中傳遞敏感資訊
8. 最小權限原則

---

## 延伸閱讀

- [JWT 官方網站](https://www.google.com/search?q=JSON+Web+Token)
- [OAuth2 授權框架](https://www.google.com/search?q=OAuth2+authorization+framework)
- [OWASP API 安全](https://www.google.com/search?q=OWASP+API+security+top+10)
