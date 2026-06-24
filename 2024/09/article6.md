# OpenAPI / Swagger 文件

## OpenAPI 是什麼

OpenAPI 規格（原名 Swagger）提供了一個標準格式來描述 RESTful API。它是語言無關的，可以用 YAML 或 JSON 撰寫。有了 OpenAPI 規格，就可以自動產生文件、模擬伺服器、用戶端程式碼和測試。

## 從規格到文件

### 安裝與設定

```javascript
// 使用 swagger-jsdoc 從 JSDoc 註解產生規格
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {
  definition: {
    openapi: '3.1.0',
    info: {
      title: 'User Management API',
      version: '1.0.0',
      description: '使用者管理 API 文件'
    },
    servers: [
      { url: 'http://localhost:3000', description: '開發環境' },
      { url: 'https://api.example.com', description: '正式環境' }
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT'
        }
      }
    },
    security: [{ bearerAuth: [] }]
  },
  apis: ['./routes/*.js'] // 掃描路由檔案
};

const spec = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(spec));
```

### 在程式碼中撰寫文件註解

```javascript
/**
 * @openapi
 * /api/users:
 *   get:
 *     summary: 取得使用者列表
 *     description: 回傳所有使用者，支援分頁和過濾
 *     tags: [Users]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *         description: 頁碼
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *         description: 每頁筆數
 *       - in: query
 *         name: role
 *         schema:
 *           type: string
 *           enum: [admin, editor, viewer]
 *         description: 角色過濾
 *     responses:
 *       200:
 *         description: 成功回傳使用者列表
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/User'
 *                 pagination:
 *                   $ref: '#/components/schemas/Pagination'
 */
router.get('/users', async (req, res) => {
  // 實作...
});
```

## 定義可複用的 Schema 元件

```javascript
/**
 * @openapi
 * components:
 *   schemas:
 *     User:
 *       type: object
 *       properties:
 *         id:
 *           type: integer
 *           description: 使用者 ID
 *         name:
 *           type: string
 *           description: 使用者姓名
 *         email:
 *           type: string
 *           format: email
 *           description: 電子郵件
 *         role:
 *           type: string
 *           enum: [admin, editor, viewer]
 *         createdAt:
 *           type: string
 *           format: date-time
 *       required:
 *         - id
 *         - name
 *         - email
 *
 *     CreateUserRequest:
 *       type: object
 *       properties:
 *         name:
 *           type: string
 *         email:
 *           type: string
 *           format: email
 *       required:
 *         - name
 *         - email
 *
 *     ErrorResponse:
 *       type: object
 *       properties:
 *         success:
 *           type: boolean
 *           example: false
 *         error:
 *           type: object
 *           properties:
 *             code:
 *               type: string
 *             message:
 *               type: string
 *             details:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   field:
 *                     type: string
 *                   message:
 *                     type: string
 *
 *     Pagination:
 *       type: object
 *       properties:
 *         page:
 *           type: integer
 *         limit:
 *           type: integer
 *         total:
 *           type: integer
 *         totalPages:
 *           type: integer
 */
```

## 執行期驗證（文件即規範）

```javascript
const OpenApiValidator = require('express-openapi-validator');

app.use(OpenApiValidator.middleware({
  apiSpec: './openapi.yaml',
  validateRequests: true,   // 自動驗證請求
  validateResponses: true,  // 自動驗證回應
  operationHandlers: false
}));

// 如果有欄位不符合 Schema，自動回傳 400
// 不需要手動撰寫驗證邏輯
```

## 從 OpenAPI 產生用戶端程式碼

```bash
# 使用 openapi-generator 產生各種語言的用戶端
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g javascript \
  -o ./client/javascript

npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./client/typescript

npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./client/python
```

## 文件品質檢查清單

- [ ] 每個端點都有準確的 HTTP 方法和路徑
- [ ] 每個端點都有參數說明（路徑、查詢、請求主體）
- [ ] 所有回應狀態碼都有定義（包括 4xx 和 5xx）
- [ ] Schema 定義完整，使用 `$ref` 避免重複
- [ ] 有認證方式說明（API Key / Bearer / OAuth）
- [ ] 有標籤（Tags）分類端點
- [ ] 有範例值（Example）
- [ ] 錯誤回應有明確的格式

## 小結

OpenAPI 不僅僅是文件工具。它是一個完整的生態系——從設計、開發、測試到部署，OpenAPI 規格貫穿整個 API 生命週期。採用「文件即規範」的工作流程可以顯著減少溝通成本和整合問題。

---

## 延伸閱讀

- [Swagger UI Demo](https://www.google.com/search?q=Swagger+UI+demo)
- [OpenAPI Generator](https://www.google.com/search?q=OpenAPI+Generator)
- [Design-First API Development](https://www.google.com/search?q=design+first+API+development+OpenAPI)
