# Postman 測試與自動化

## Postman 的基本概念

Postman 是 API 開發和測試的最熱門工具之一。它從一個簡單的 HTTP 用戶端發展為完整的 API 生命週期管理平台。

## 環境與變數管理

```javascript
// Postman 環境變數
// 開發環境
{
  "baseUrl": "http://localhost:3000",
  "apiKey": "dev-test-key-123"
}

// 正式環境
{
  "baseUrl": "https://api.example.com",
  "apiKey": "{{productionApiKey}}"
}

// 在請求中使用
// {{baseUrl}}/api/users
// Authorization: Bearer {{accessToken}}
```

## Pre-request Script（請求前腳本）

```javascript
// 在請求發送前自動取得 Token
pm.sendRequest({
  url: pm.environment.get('baseUrl') + '/auth/login',
  method: 'POST',
  header: { 'Content-Type': 'application/json' },
  body: {
    mode: 'raw',
    raw: JSON.stringify({
      username: pm.environment.get('username'),
      password: pm.environment.get('password')
    })
  }
}, (err, response) => {
  if (!err) {
    const data = response.json();
    pm.environment.set('accessToken', data.token);
    pm.environment.set('refreshToken', data.refreshToken);
  }
});
```

## Tests Script（測試腳本）

```javascript
// 狀態碼驗證
pm.test('狀態碼為 200', () => {
  pm.response.to.have.status(200);
});

// 回應結構驗證
pm.test('回應包含資料和 meta', () => {
  const body = pm.response.json();
  pm.expect(body).to.have.property('data');
  pm.expect(body).to.have.property('meta');
  pm.expect(body.meta).to.have.property('requestId');
});

// 資料內容驗證
pm.test('使用者資料格式正確', () => {
  const user = pm.response.json().data;
  pm.expect(user).to.be.an('object');
  pm.expect(user).to.have.all.keys(['id', 'name', 'email', 'createdAt']);
  pm.expect(user.id).to.be.a('number');
  pm.expect(user.email).to.match(/^[\w.-]+@[\w.-]+\.\w+$/);
});

// 回應時間驗證
pm.test('回應時間小於 500ms', () => {
  pm.expect(pm.response.responseTime).to.be.below(500);
});

// Header 驗證
pm.test('Content-Type 為 JSON', () => {
  pm.response.to.have.header('Content-Type', 'application/json; charset=utf-8');
});

// 設定環境變數供後續請求使用
pm.test('儲存使用者 ID', () => {
  const userId = pm.response.json().data.id;
  pm.environment.set('userId', userId);
});
```

## Collection Runner

```bash
# 使用 Newman 在命令列執行 Postman Collection

# 安裝 Newman
npm install -g newman

# 執行 Collection
newman run user-api.postman_collection.json \
  --environment production.postman_environment.json \
  --reporters cli,json,junit \
  --reporter-junit-export results/junit-report.xml \
  --reporter-json-export results/json-report.json \
  --delay-request 100 \
  --timeout-request 10000
```

## CI/CD 整合

```yaml
# GitHub Actions 範例
name: API Test

on:
  push:
    branches: [main]

jobs:
  api-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Start server
        run: npm start &
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost/test

      - name: Wait for server
        run: sleep 5

      - name: Run Postman tests
        run: |
          npx newman run tests/postman/collection.json \
            --environment tests/postman/ci.json \
            --reporters cli,junit \
            --reporter-junit-export results/api-test-results.xml

      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: api-test-results
          path: results/
```

## 測試集合組織

```
api-tests/
├── collections/
│   ├── user-api.postman_collection.json
│   └── order-api.postman_collection.json
├── environments/
│   ├── development.postman_environment.json
│   ├── staging.postman_environment.json
│   └── production.postman_environment.json
├── data/
│   ├── users.csv          # 資料驅動測試
│   └── orders.json
└── results/
    └── api-test-results.xml
```

## 資料驅動測試

```csv
name,email,expectedStatus
Alice,alice@test.com,201
Bob,bob@test.com,201
,missing-email,422
invalid-email,not-an-email,422
@invalid,invalid@,422
```

```bash
newman run collection.json \
  --iteration-data data/users.csv \
  --reporters cli
```

## 小結

Postman 加上 Newman 提供了從開發、測試到 CI/CD 整合的完整 API 測試方案。關鍵是建立可重複的測試集合，包含正面案例、邊界案例和錯誤案例，並在每次部署時自動執行。

---

## 延伸閱讀

- [Postman 官方教學](https://www.google.com/search?q=Postman+learning+center)
- [Newman Documentation](https://www.google.com/search?q=Newman+CLI+documentation)
- [API Testing with Postman](https://www.google.com/search?q=API+testing+Postman+guide)
