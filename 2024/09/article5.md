# OAuth 2.0 流程

## OAuth 2.0 的角色

OAuth 2.0 定義了四個角色：

- **資源擁有者（Resource Owner）：** 使用者，擁有資料
- **客戶端（Client）：** 應用程式，想存取使用者的資料
- **授權伺服器（Authorization Server）：** 負責認證和發放 Token
- **資源伺服器（Resource Server）：** 儲存資料，驗證 Token 後提供資料

## 授權碼流程（Authorization Code + PKCE）

這是 OAuth 2.1 唯一推薦的流程，適用於前端和後端應用。

```javascript
// 1. 前端重新導向到授權伺服器
const authUrl = new URL('https://accounts.example.com/oauth/authorize');
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('client_id', 'YOUR_CLIENT_ID');
authUrl.searchParams.set('redirect_uri', 'https://yourapp.com/callback');
authUrl.searchParams.set('scope', 'profile email');

// PKCE: 產生 code_verifier 和 code_challenge
const crypto = require('crypto');

function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto.createHash('sha256')
    .update(verifier)
    .digest('base64url');
  return { verifier, challenge };
}

const { verifier, challenge } = generatePKCE();
authUrl.searchParams.set('code_challenge', challenge);
authUrl.searchParams.set('code_challenge_method', 'S256');

// 儲存 verifier 在 session 中供後續使用
session.pkceVerifier = verifier;

// 2. 使用者同意後，授權伺服器重新導向回 callback
// GET /callback?code=AUTH_CODE_XYZ

// 3. 後端用授權碼 + PKCE verifier 換取 Token
app.get('/callback', async (req, res) => {
  const { code } = req.query;

  const tokenResponse = await fetch('https://accounts.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'authorization_code',
      code,
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      redirect_uri: 'https://yourapp.com/callback',
      code_verifier: session.pkceVerifier  // PKCE 驗證
    })
  });

  const tokens = await tokenResponse.json();
  // tokens: { access_token, refresh_token, expires_in, token_type }

  // 4. 使用 Access Token 存取資源伺服器
  const userResponse = await fetch('https://api.example.com/user', {
    headers: {
      'Authorization': `Bearer ${tokens.access_token}`
    }
  });
  const userData = await userResponse.json();

  // 5. 登入成功
  req.session.user = userData;
  res.redirect('/dashboard');
});
```

## 用戶端憑證流程（Client Credentials）

適用於伺服器對伺服器的通訊，沒有使用者參與：

```javascript
// 機器對機器通訊
async function getMachineToken() {
  const response = await fetch('https://accounts.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'client_credentials',
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      scope: 'read:orders write:orders'
    })
  });

  const data = await response.json();
  return data.access_token;
}

// 使用 Token 呼叫 API
async function callApi(endpoint) {
  const token = await getMachineToken();
  return fetch(`https://api.example.com/${endpoint}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
}
```

## 重新整理 Token（Refresh Token）

Access Token 通常有較短的有效期（如 1 小時），Refresh Token 用於取得新的 Access Token：

```javascript
async function refreshAccessToken(refreshToken) {
  const response = await fetch('https://accounts.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET
    })
  });

  const data = await response.json();
  return {
    accessToken: data.access_token,
    expiresIn: data.expires_in,
    refreshToken: data.refresh_token || refreshToken  // 可能輪換
  };
}

// 自動重新整理的 Axios 攔截器
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      const { accessToken } = await refreshAccessToken(storedRefreshToken);
      error.config.headers['Authorization'] = `Bearer ${accessToken}`;
      return axios(error.config);
    }
    return Promise.reject(error);
  }
);
```

## Token 撤銷

```javascript
async function revokeToken(token, tokenTypeHint = 'access_token') {
  await fetch('https://accounts.example.com/oauth/revoke', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      token,
      token_type_hint: tokenTypeHint,
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET
    })
  });
}
```

## 安全最佳實踐

1. **永遠使用 PKCE：** 即使是後端應用也應該使用，防禦授權碼攔截攻擊
2. **短效 Access Token：** 建議 15-60 分鐘
3. **Refresh Token 輪換：** 每次使用 Refresh Token 時同時更新它
4. **使用 HTTPS：** 所有 Token 傳輸必須加密
5. **驗證 redirect_uri：** 防止開放重新導向攻擊
6. **最小權限範圍：** 只要求需要的 Scope
7. **認證伺服器日誌：** 監控異常的授權活動

---

## 延伸閱讀

- [OAuth 2.0 官方文件](https://www.google.com/search?q=OAuth+2.0+official+documentation)
- [OAuth 2.1 RFC](https://www.google.com/search?q=OAuth+2.1+RFC+9568)
- [OAuth Security Best Practices](https://www.google.com/search?q=OAuth+security+best+practices)
