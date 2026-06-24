# 認證與授權：JWT

## 什麼是 JWT？

JWT（JSON Web Token）是一種開放標準（RFC 7519），定義了一種緊湊且自包含的方式，用於在各方之間以 JSON 物件形式安全地傳遞資訊。JWT 廣泛應用於分布式系統的認證和授權。

### JWT 的結構

一個 JWT Token 由三個部分組成，以點號分隔：

```
header.payload.signature
```

**Header**：包含 Token 類型和簽名演算法

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**：包含要傳遞的聲明（Claims）

```json
{
  "sub": "1234567890",
  "name": "Alice",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature**：用於驗證 Token 未被篡改

```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

## 在 Node.js 中使用 JWT

### 安裝與基本使用

```bash
npm install jsonwebtoken
```

```javascript
const jwt = require('jsonwebtoken');
const SECRET = 'your-secret-key';

// 簽發 Token
const token = jwt.sign(
  { userId: 123, role: 'admin' },
  SECRET,
  { expiresIn: '1h' }
);
console.log(token);

// 驗證 Token
try {
  const decoded = jwt.verify(token, SECRET);
  console.log('Decoded:', decoded);
} catch (err) {
  console.error('Invalid token:', err.message);
}
```

### 自製簡易 JWT（無第三方套件）

參考 `_code/node_server.js` 中的實作：

```javascript
const crypto = require('crypto');

function createToken(payload, secret) {
  const header = Buffer.from(
    JSON.stringify({ alg: 'HS256', typ: 'JWT' })
  ).toString('base64url');

  const body = Buffer.from(
    JSON.stringify(payload)
  ).toString('base64url');

  const signature = crypto
    .createHmac('sha256', secret)
    .update(`${header}.${body}`)
    .digest('base64url');

  return `${header}.${body}.${signature}`;
}
```

## Express 整合

### 登入路由

```javascript
const express = require('express');
const jwt = require('jsonwebtoken');
const app = express();

app.use(express.json());

const SECRET = 'your-secret-key';
const users = [
  { id: 1, username: 'alice', password: 'password123' },
];

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username);

  if (!user || user.password !== password) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = jwt.sign(
    { userId: user.id, username: user.username },
    SECRET,
    { expiresIn: '24h' }
  );

  res.json({ token });
});
```

### 驗證中介軟體

```javascript
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(403).json({ error: 'Invalid or expired token' });
  }
}

// 保護需要認證的路由
app.get('/api/profile', authenticate, (req, res) => {
  res.json({ user: req.user });
});

app.get('/api/admin', authenticate, (req, res) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Insufficient permissions' });
  }
  res.json({ message: 'Admin access granted' });
});
```

### 角色授權

```javascript
function authorize(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user || !allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// 使用方式
app.get('/api/admin/users',
  authenticate,
  authorize('admin'),
  (req, res) => {
    res.json({ users: [...] });
  }
);
```

## Token 管理最佳實踐

### 存取 Token 與刷新 Token

```javascript
// 短期存取 Token + 長期刷新 Token
const accessToken = jwt.sign(
  { userId: user.id },
  SECRET,
  { expiresIn: '15m' }
);

const refreshToken = jwt.sign(
  { userId: user.id, type: 'refresh' },
  REFRESH_SECRET,
  { expiresIn: '7d' }
);

// 刷新端點
app.post('/api/refresh', (req, res) => {
  const { refreshToken } = req.body;
  try {
    const decoded = jwt.verify(refreshToken, REFRESH_SECRET);
    const newAccessToken = jwt.sign(
      { userId: decoded.userId },
      SECRET,
      { expiresIn: '15m' }
    );
    res.json({ accessToken: newAccessToken });
  } catch (err) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});
```

### 安全注意事項

```javascript
// 1. 使用強密鑰（至少 256 bits）
const SECRET = crypto.randomBytes(32).toString('hex');

// 2. 設定合理的過期時間
jwt.sign(payload, SECRET, { expiresIn: '15m' });

// 3. 避免在 payload 中存放敏感資訊
// 不要這樣做
jwt.sign({ password: user.password }, SECRET);

// 4. 使用 HTTPS 傳輸 Token
// 5. 將 Token 存放在 httpOnly Cookie 而非 localStorage
```

## 總結

JWT 是現代 Web 應用中最常用的認證方案之一。它無狀態的特性使其特別適合分布式系統和微服務架構。掌握 JWT 的原理和實作方式，是 Node.js 後端開發者的必備技能。

## 延伸閱讀

- [JWT 官方網站](https://www.google.com/search?q=JSON+Web+Token+official)
- [RFC 7519](https://www.google.com/search?q=RFC+7519+JWT)
- [jsonwebtoken npm](https://www.google.com/search?q=jsonwebtoken+npm+package)
