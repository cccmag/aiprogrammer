# 5. 身份驗證與授權

## 身份驗證 vs 授權

這是兩個容易混淆的概念：

**身份驗證（Authentication）**：確認「你是誰」，通常透過密碼、憑證、指紋等方式。

**授權（Authorization）**：確認「你能做什麼」，在驗證之後決定存取權限。

## 密碼認證

密碼是最常見的身份驗證方式，但也是最脆弱的一環。

### 密碼儲存

**千萬不要儲存明文密碼！** 正確的做法是使用雜湊函數：

```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

### 密碼強度

使用雜湊的同時，應該強制密碼強度：

```python
import re

def check_password_strength(password):
    errors = []
    if len(password) < 8:
        errors.append("密碼至少需要 8 個字元")
    if not re.search(r"[A-Z]", password):
        errors.append("密碼需要包含大寫字母")
    if not re.search(r"[a-z]", password):
        errors.append("密碼需要包含小寫字母")
    if not re.search(r"\d", password):
        errors.append("密碼需要包含數字")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("密碼需要包含特殊字元")
    return errors
```

### 多因素認證（MFA）

增加驗證層次，即使密碼被竊也更難被入侵：

**知道的東西（Something you know）**：密碼、PIN

**擁有的東西（Something you have）**：手機、硬體 Token

**是誰（Something you are）**：指紋、虹膜、臉部辨識

```python
# 驗證 OTP（一次性密碼）
import pyotp

def verify_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
```

## Session 管理

### Session ID 生成

Session ID 必須是密碼學上安全的隨機值：

```python
import secrets

def generate_session_id():
    return secrets.token_urlsafe(32)
```

### Session 儲存

不要在 Cookie 中儲存敏感資料。Session ID 只是索引，實際資料應存在伺服器端：

```python
import redis
import secrets

session_store = redis.Redis()

def create_session(user_id):
    session_id = secrets.token_urlsafe(32)
    session_store.setex(f"session:{session_id}", 3600, user_id)
    return session_id

def get_session(session_id):
    return session_store.get(f"session:{session_id}")
```

### Session 固定攻擊

攻擊者試圖讓受害者使用已知的 Session ID。

**防護**：登入成功後更換 Session ID

```python
def login(user_id):
    # 刪除舊 session
    if current_session:
        session_store.delete(f"session:{current_session}")
    # 建立新 session
    return create_session(user_id)
```

## 授權模型

### RBAC（Role-Based Access Control）

根據角色分配權限：

```python
ROLES = {
    "admin": ["read", "write", "delete", "manage_users"],
    "editor": ["read", "write"],
    "viewer": ["read"]
}

def has_permission(role, action):
    return action in ROLES.get(role, [])
```

### 最小權限原則

每個使用者、每個系統元件都應該只擁有完成任務所需的最小權限。

## 速率限制

防止暴力破解攻擊：

```python
from functools import wraps
import redis

login_attempts = redis.Redis()

def rate_limit(max_attempts=5, window=300):
    def decorator(f):
        @wraps(f)
        def wrapper(username, *args, **kwargs):
            key = f"login_attempt:{username}"
            attempts = login_attempts.get(key)
            if attempts and int(attempts) >= max_attempts:
                raise ValueError("Too many login attempts")
            
            result = f(username, *args, **kwargs)
            
            pipe = login_attempts.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            pipe.execute()
            return result
        return wrapper
    return decorator
```

## 參考資源

- https://www.google.com/search?q=身份驗證+授權+MFA+Session+管理+安全+2016
- https://www.google.com/search?q=密碼+bcrypt+雜湊+儲存+安全+最佳實踐+強度+驗證
- https://www.google.com/search?q=CSRF+防護+Token+Session+固定攻擊+速率限制