# 認證與授權策略

## 認證 vs 授權

- **認證（Authentication）：** 確認你是誰（Who are you?）
- **授權（Authorization）：** 確認你能做什麼（What can you do?）

## API Key 認證

最簡單的認證方式，適合服務對服務的通訊：

```javascript
// API Key 放在 Header 中
const API_KEYS = ['sk-prod-abc123', 'sk-prod-def456'];

function apiKeyMiddleware(req, res, next) {
  const key = req.headers['x-api-key'];
  if (!key || !API_KEYS.includes(key)) {
    return res.status(401).json({ error: 'Invalid API Key' });
  }
  req.apiKey = key;
  next();
}
```

**適用場景：** 內部服務通訊、公開 API 的金鑰管理
**安全考量：** API Key 應視為密碼，定期輪換

## JWT（JSON Web Token）認證

JWT 是現代 API 最廣泛使用的認證方式。它由三部分組成：Header、Payload、Signature。

```javascript
const jwt = require('jsonwebtoken');

// 登入後產生 JWT
function loginHandler(req, res) {
  const { username, password } = req.body;
  const user = authenticate(username, password);
  const token = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
  res.json({ token, expiresIn: 3600 });
}

// JWT 驗證中介軟體
function jwtMiddleware(req, res, next) {
  const auth = req.headers['authorization'];
  if (!auth || !auth.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }
  try {
    const token = auth.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}
```

### JWT 最佳實踐

- 使用短有效期（15-60 分鐘）搭配 Refresh Token
- 不在 Payload 中存放敏感資訊（Payload 只做 Base64 編碼，非加密）
- 使用 HTTPS 傳輸
- Token 撤銷透過黑名單或短有效期實作

## OAuth 2.0 授權框架

OAuth 2.0 是授權的業界標準，讓應用程式可以代表使用者存取資源：

```javascript
// 授權碼流程（Authorization Code Flow）
// 這是 OAuth 2.1 推薦的唯一流程

// 1. 使用者點擊「以 Google 登入」
// 2. 重新導向到 Google 授權頁面
const authUrl = 'https://accounts.google.com/o/oauth2/auth?' +
  'client_id=YOUR_CLIENT_ID' +
  '&redirect_uri=https://yourapp.com/callback' +
  '&response_type=code' +
  '&scope=profile email';

// 3. 使用者同意後，Google 重新導向回 callback
// 4. 後端用授權碼換取 Access Token
app.get('/callback', async (req, res) => {
  const { code } = req.query;
  const response = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code,
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      redirect_uri: 'https://yourapp.com/callback',
      grant_type: 'authorization_code'
    })
  });
  const tokens = await response.json();
  // tokens.access_token, tokens.refresh_token
});
```

## RBAC（Role-Based Access Control）

基於角色的權限控制是最常見的授權模式：

```javascript
const ROLES = {
  admin: ['read', 'write', 'delete', 'manage'],
  editor: ['read', 'write'],
  viewer: ['read']
};

function authorize(...allowedRoles) {
  return (req, res, next) => {
    const userRole = req.user?.role;
    if (!userRole || !allowedRoles.includes(userRole)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

// 使用方式
router.get('/api/users', jwtMiddleware, authorize('admin', 'editor', 'viewer'), getUsers);
router.delete('/api/users/:id', jwtMiddleware, authorize('admin'), deleteUser);
```

## 安全最佳實踐總結

1. **永遠使用 HTTPS：** 所有 API 通訊必須加密
2. **Token 有效期短：** 減少 Token 洩漏的損害範圍
3. **Rate Limiting：** 防止暴力破解和 DDoS 攻擊
4. **最小權限原則：** 只給應用程式和最少的必要權限
5. **日誌記錄：** 記錄所有認證事件，便於稽核
6. **安全 Header：** 使用 CSP、CORS、X-Frame-Options 等

---

**下一步**：[API 文件與測試](focus5.md)

## 延伸閱讀

- [JWT.io](https://www.google.com/search?q=JWT+JSON+Web+Token)
- [OAuth 2.0 Simplified](https://www.google.com/search?q=OAuth+2.0+simplified+guide)
- [OWASP API Security](https://www.google.com/search?q=OWASP+API+security+top+10)
