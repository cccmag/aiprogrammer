# 自動化測試整合

## 1. 引言

自動化測試是 CI/CD 管線的品質守門員。沒有完善的測試，自動化部署就失去了信心基礎。本文將探討如何在 DevOps 管線中整合各層級的自動化測試。

## 2. 測試金字塔

現代軟體測試按照範圍和速度分為三個層級：

```
    ╱╲
   ╱ E2E ╲
  ╱────────╲
 ╱ 整合測試  ╲
╱──────────────╲
╱   單元測試    ╲
╱────────────────╲
```

**單元測試**：測試單一函式或模組，速度快，覆蓋率高
**整合測試**：測試多個模組的互動，驗證 API 正確性
**E2E 測試**：測試完整的使用者流程，最接近真實場景

## 3. 在 CI 中整合測試

```yaml
# workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      
      # 單元測試
      - run: npm run test:unit
      
      # 整合測試（需要資料庫）
      - name: Start services
        run: docker compose up -d db redis
      - run: npm run test:integration
      
      # E2E 測試
      - name: Start application
        run: docker compose up -d
      - run: npm run test:e2e
      
      # 測試覆蓋率
      - run: npm run coverage
      - uses: codecov/codecov-action@v3
```

## 4. 測試覆蓋率閘道

設定測試覆蓋率的最低門檻：

```javascript
// jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

在 CI 中檢查覆蓋率，不達標則中斷管線：

```bash
npx jest --coverage --coverageThreshold='{"global":{"lines":80}}'
```

## 5. 整合測試實戰

```javascript
// tests/integration/api.test.js
const request = require('supertest');
const app = require('../src/app');

describe('API Integration Tests', () => {
  let server;

  beforeAll(async () => {
    // 啟動應用（假設資料庫已由 docker compose 啟動）
    server = app.listen(4000);
  });

  afterAll(async () => {
    await server.close();
  });

  test('GET /api/users 返回用戶列表', async () => {
    const res = await request(app)
      .get('/api/users')
      .expect(200);
    
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBeGreaterThan(0);
  });

  test('POST /api/users 建立新用戶', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@test.com' })
      .expect(201);
    
    expect(res.body).toHaveProperty('id');
    expect(res.body.name).toBe('Alice');
  });
});
```

## 6. 程式碼品質檢查

除了功能測試，CI 管線還應包含程式碼品質檢查：

```bash
# Lint 檢查
npm run lint

# 格式化檢查
npx prettier --check .

# 類型檢查（TypeScript）
npx tsc --noEmit

# 安全掃描
npx audit fix --dry-run

# 依賴檢查
npx dependency-check
```

## 7. 平行化測試執行

大規模測試需要平行化以節省時間：

```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npx jest --shard=${{ matrix.shard }}/4
```

## 8. 結語

自動化測試是 CI/CD 管線的靈魂。沒有測試的自動化部署只是自動化災難。透過分層測試、覆蓋率閘道和品質檢查，你可以確保每次部署的都是高品質的軟體。
