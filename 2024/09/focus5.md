# API 文件與測試

## 為何需要 API 文件

好的 API 文件不僅僅是參考手冊，它是開發者體驗的核心部分。當開發者可以快速理解如何使用 API 時，整合時間從數週縮短到數小時。

## OpenAPI / Swagger

OpenAPI 規格（原名 Swagger）是 API 文件的事實標準。它是一個與語言無關的描述格式，可以用 YAML 或 JSON 撰寫。

```yaml
openapi: 3.1.0
info:
  title: User Management API
  version: 1.0.0
  description: 使用者管理 API

paths:
  /api/users:
    get:
      summary: 取得使用者列表
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 20 }
      responses:
        200:
          description: 成功回傳使用者列表
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: 建立新使用者
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        201:
          description: 使用者建立成功

components:
  schemas:
    User:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        email: { type: string, format: email }
      required: [id, name, email]
    CreateUser:
      type: object
      properties:
        name: { type: string }
        email: { type: string, format: email }
      required: [name, email]
```

### 文件即規範（Design-First）

在寫程式碼之前先定義 OpenAPI 規格，帶來以下好處：
- 客戶端和伺服器可以並行開發
- 規格作為團隊間的溝通合約
- 可以自動產生 mock server 和測試

```javascript
// 從 OpenAPI 規格自動產生驗證邏輯
const OpenApiValidator = require('express-openapi-validator');

app.use(OpenApiValidator.middleware({
  apiSpec: './openapi.yaml',
  validateRequests: true,
  validateResponses: true
}));
```

## API 測試策略

### 單元測試：測試路由處理器邏輯

```javascript
describe('GET /api/users/:id', () => {
  it('應回傳指定使用者', async () => {
    const ctx = await router.dispatch({
      method: 'GET',
      path: '/api/users/42',
      headers: { authorization: 'Bearer valid-token-123' }
    });
    expect(ctx.status).toBe(200);
    expect(ctx.body.user.id).toBe(42);
  });

  it('使用者不存在時回傳 404', async () => {
    const ctx = await router.dispatch({
      method: 'GET',
      path: '/api/users/999',
      headers: { authorization: 'Bearer valid-token-123' }
    });
    expect(ctx.status).toBe(404);
  });
});
```

### 整合測試：測試 API 閘道流程

```javascript
describe('POST /api/users 整合測試', () => {
  it('應通過驗證、限流、認證和資料驗證', async () => {
    const req = {
      method: 'POST',
      path: '/api/users',
      headers: { authorization: 'Bearer valid-token-123' },
      bodyStream: [JSON.stringify({
        name: 'Test User',
        email: 'test@example.com'
      })]
    };
    const ctx = await router.dispatch(req);
    expect(ctx.status).toBe(201);
  });
});
```

### 契約測試（Contract Testing）

確保 API 提供者和消費者之間的一致性。Pact 和 Spring Cloud Contract 是常見工具。

## 自動化測試流程

```
commit → 單元測試 → 整合測試 → 契約測試 → 部署
         ├── 快速回饋 ──┤ ├── 完整驗證 ──┤
```

## 測試替換率 vs 測試品質

更重要的是測試的品質而非數量：每個測試應該測試一個明確的行為，並涵蓋邊界情況（空列表、大數值、特殊字元、未認證請求等）。

---

**下一步**：[速率限制與安全性](focus6.md)

## 延伸閱讀

- [OpenAPI Specification](https://www.google.com/search?q=OpenAPI+specification+3.1)
- [Swagger Editor](https://www.google.com/search?q=Swagger+editor+online)
- [API Testing Best Practices](https://www.google.com/search?q=API+testing+best+practices)
