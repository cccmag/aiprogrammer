# API 金鑰與 JWT 認證

## API 金鑰認證

API 金鑰（API Key）是最簡單的 API 認證方式。伺服器為每個客戶端產生唯一的金鑰，客戶端在請求時帶入該金鑰進行身份識別。

### 產生與管理 API 金鑰

```python
import secrets
import hashlib

def generate_api_key():
    """產生安全的 API 金鑰"""
    return secrets.token_urlsafe(32)

def hash_api_key(api_key: str):
    """對 API 金鑰進行雜湊（儲存雜湊值而非原始金鑰）"""
    return hashlib.sha256(api_key.encode()).hexdigest()

# 使用範例
raw_key = generate_api_key()
hashed = hash_api_key(raw_key)
print(f"原始金鑰：{raw_key}")
print(f"雜湊值：{hashed}")
```

### FastAPI API Key 認證

```python
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

VALID_KEYS = {"key1-hashed", "key2-hashed"}

def validate_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key not in VALID_KEYS:
        raise HTTPException(status_code=403, detail="無效的 API 金鑰")
    return api_key

@app.get("/protected/")
def protected_route(api_key: str = Security(validate_api_key)):
    return {"message": "通過 API Key 驗證", "key": api_key}
```

## JWT（JSON Web Token）

JWT 是一種緊湊的、URL 安全的權杖格式，用於在各方之間傳遞聲明。JWT 由三部分組成，以句點分隔：

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.abc123...
\_______________/\_______________/\_______________/
     Header           Payload          Signature
```

### JWT 產生與驗證

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_access_token(user_id: int, expires_delta: timedelta = timedelta(hours=1)):
    payload = {
        "sub": str(user_id),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### FastAPI JWT 認證

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer

app = FastAPI()
security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="無效或過期的 Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(payload["sub"])

@app.post("/login")
def login(username: str, password: str):
    # 驗證使用者（實際應用應查詢資料庫）
    if username == "admin" and password == "secret":
        token = create_access_token(user_id=1)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="帳號或密碼錯誤")

@app.get("/profile")
def get_profile(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id, "message": "個人資料"}
```

### 使用 requests 進行 JWT 認證

```python
import requests

# 登入取得 Token
login_resp = requests.post("http://localhost:8000/login",
    data={"username": "admin", "password": "secret"})
token = login_resp.json()["access_token"]

# 使用 Token 存取受保護的端點
headers = {"Authorization": f"Bearer {token}"}
profile_resp = requests.get("http://localhost:8000/profile",
    headers=headers)
print(profile_resp.json())
```

## OAuth2 密碼流程

FastAPI 內建 OAuth2 Password Flow：

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username != "admin" or password != "secret":
        raise HTTPException(401, "帳號或密碼錯誤")
    token = create_access_token(user_id=1)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(401, "無效的 Token")
    return {"user_id": payload["sub"]}
```

## Refresh Token 實作

```python
from pydantic import BaseModel

REFRESH_SECRET = "refresh-secret-key"

def create_refresh_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=30),
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm=ALGORITHM)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@app.post("/refresh")
def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET,
            algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(401, "無效的 Refresh Token")
        user_id = int(payload["sub"])
        new_token = create_access_token(user_id)
        return {"access_token": new_token, "token_type": "bearer"}
    except jwt.InvalidTokenError:
        raise HTTPException(401, "無效或過期的 Refresh Token")
```

## 安全最佳實踐總結

```python
import bcrypt  # 用於密碼雜湊

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

1. 永遠使用 HTTPS
2. Token 設定過期時間（Access Token 短，Refresh Token 長）
3. 使用安全的隨機數產生器生成 API Key
4. 儲存雜湊值而非原始金鑰或密碼
5. 支援 Token 撤銷機制

---

## 延伸閱讀

- [JWT 官方網站](https://www.google.com/search?q=JSON+Web+Token+official)
- [OAuth2 授權流程](https://www.google.com/search?q=OAuth2+authorization+flow)
- [FastAPI 安全性指南](https://www.google.com/search?q=FastAPI+security+guide)
