# JWT 身份驗證

## JWT 結構

JWT（JSON Web Token）由三部分組成，用句點分隔：

```
header.payload.signature
```

**Header**：包含 token 類型與使用的雜湊演算法

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**：包含 claims（聲明），如使用者 ID、過期時間等

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature**：對 header 與 payload 的數位簽章

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

## 使用 JWT

```python
# 安裝 PyJWT
# pip install PyJWT

import jwt
import datetime

# 產生 JWT
def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, 'secret_key', algorithm='HS256')

# 驗證 JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 過期
    except jwt.InvalidTokenError:
        return None  # 無效 Token
```

## JWT vs Session

| 特性 | JWT | Session |
|------|-----|---------|
| 儲存位置 | 客戶端 | 伺服器端 |
| 可擴展性 | 較好，無需集中儲存 | 需要 Redis 等集中儲存 |
| 撤銷困難 | 需要額外機制 | 可直接刪除 session |
| 傳輸開銷 | 每次請求都攜帶 | 只傳遞 session ID |
| 適用場景 | API、無狀態 | 傳統 Web 應用 |

## 常見 JWT 攻擊與防護

### 攻擊 1：演算法置換（Algorithm Confusion）

攻擊者將 header 中的 `HS256` 改為 `none`，然後用空密碼簽章。

**防護**：指定允許的演算法，不依賴 client 指定的演算法

```python
# 不安全的做法
payload = jwt.decode(token, options={"verify_signature": False})

# 安全的做法：只允許特定演算法
payload = jwt.decode(token, 'secret', algorithms=['HS256'])
```

### 攻擊 2：使用公鑰驗證時的混淆

當使用 RS256（非對稱）時，攻擊者可能誘使伺服器使用公鑰作為密碼。

**防護**：嚴格驗證公鑰指紋，不要信任 client 提供的密鑰。

### 攻擊 3：Token 過期沒有清理

洩露的 Token 在過期前都可以使用。

**防護**：
- 設定合理的過期時間（不要設太長）
- 提供 Token 撤銷機制
- 使用 Refresh Token

## 安全的 JWT 實作

```python
import jwt
import datetime
import hashlib

# 使用足夠長的密鑰
SECRET_KEY = hashlib.sha256(b"your-app-secret-key").digest()

# 只在 JWT 中存放必要的資訊
def create_token(user_id, email, role):
    payload = {
        'sub': str(user_id),
        'email': email,
        'role': role,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# 驗證並解析 Token
def get_user_from_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=['HS256'],
            options={
                'require': ['exp', 'iat', 'sub']
            }
        )
        return {
            'user_id': int(payload['sub']),
            'email': payload['email'],
            'role': payload['role']
        }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

## Refresh Token 機制

Access Token 過期時間短，Refresh Token 過期時間長：

```python
def refresh_tokens(refresh_token):
    # 驗證 refresh token
    payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=['HS256'])

    # 產生新的 access token
    new_access = create_access_token(payload['user_id'])

    # 可選：產生新的 refresh token（token rotation）
    new_refresh = create_refresh_token(payload['user_id'])

    return {
        'access_token': new_access,
        'refresh_token': new_refresh
    }
```

## 安全檢查清單

1. 使用強密鑰（建議 256 位元）
2. 指定安全的演算法（HS256）
3. 總是檢查過期時間
4. 不要在 JWT 中存放敏感資訊
5. 使用 HTTPS 傳輸
6. 提供 Token 撤銷機制
7. 設定合理的過期時間

## 參考資源

- https://www.google.com/search?q=JWT+JSON+Web+Token+身份驗證+原理+結構+2016
- https://www.google.com/search?q=JWT+安全+攻擊+演算法置換+防護+Best+Practices
- https://www.google.com/search?q=JWT+vs+Session+比較+何時使用+優缺點