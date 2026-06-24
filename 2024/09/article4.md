# API 版本策略

## 版本管理的必要性

當 API 從 v1 演進到 v2 時，需要同時維護舊版本以支援既有客戶端。版本管理不是技術問題，而是產品和商業決策——如何在創新的同時不破壞現有整合。

## 四種版本策略深入分析

### 1. URI 版本（Path-based）

```javascript
// 實作：Express Router 分組
const v1 = express.Router();
const v2 = express.Router();

v1.get('/users', (req, res) => {
  res.json({ version: 'v1', users: data_v1 });
});

v2.get('/users', (req, res) => {
  res.json({ version: 'v2', users: data_v2 });
});

app.use('/api/v1', v1);
app.use('/api/v2', v2);
```

**優點：** 最直覺，適合公開 API
**缺點：** URI 不再是資源的唯一識別，版本是 API 維度而非資源維度

### 2. Header 版本（Header-based）

```javascript
function versionResolver(req, res, next) {
  const version = req.headers['x-api-version'] || '1';
  req.apiVersion = version;
  next();
}

app.get('/api/users', versionResolver, (req, res) => {
  switch (req.apiVersion) {
    case '1':
      return res.json({ data: getUsersV1() });
    case '2':
      return res.json({ data: getUsersV2(), meta: { version: '2' } });
    default:
      return res.status(400).json({ error: 'Unsupported version' });
  }
});
```

**優點：** URI 保持乾淨，版本是通訊協定的一部分
**缺點：** 瀏覽器無法直接測試，快取不直觀

### 3. 查詢參數版本（Query-based）

```javascript
app.get('/api/users', (req, res) => {
  const version = req.query.version || '1';
  const handler = versionHandlers[version];
  if (!handler) {
    return res.status(400).json({ error: `Unsupported version: ${version}` });
  }
  handler(req, res);
});
```

**優點：** 實作簡單，瀏覽器可直接測試
**缺點：** URI 不一致，違反 RESTful 原則

### 4. 媒體類型版本（Media Type）

```javascript
app.get('/api/users', (req, res) => {
  const accept = req.headers['accept'] || '';
  if (accept.includes('vnd.myapp.v2+json')) {
    return res.json({ version: 'v2', data: getUsersV2() });
  }
  return res.json({ version: 'v1', data: getUsersV1() });
});
```

**優點：** 最符合 HTTP 內容協商精神
**缺點：** 實作複雜，工具支援有限

## 版本策略選擇矩陣

```
               URI    Header   Query   MediaType
簡單性         ★★★    ★★      ★★★★    ★
可快取性       ★★★★   ★★       ★★★    ★
RESTful 純粹度  ★★     ★★★      ★      ★★★★
瀏覽器可測試    ★★★★   ★        ★★★★    ★
工具支援       ★★★★   ★★       ★★★    ★
內部 API       ★★     ★★★      ★★★    ★★★★
公開 API       ★★★★   ★★★      ★★     ★★
```

## 向後相容性檢查

檢查變更是否向後相容的自動化工具：

```javascript
// 使用 openapi-diff 比較兩個版本的規格
// npm install openapi-diff

const OpenAPIDiff = require('openapi-diff');

const result = OpenAPIDiff.compareSpecs({
  sourceSpec: v1Spec,
  destinationSpec: v2Spec
});

if (result.breakingDifferences.length > 0) {
  console.error('⚠️  發現破壞性變更：');
  result.breakingDifferences.forEach(diff => {
    console.error(`  - ${diff.message}`);
  });
  process.exit(1);
}
```

## 版本生命週期管理

```javascript
// 棄用通知中介軟體
function deprecationMiddleware(sunsetDate, migrationUrl) {
  return (req, res, next) => {
    res.set('Sunset', new Date(sunsetDate).toUTCString());
    res.set('Deprecation', 'true');
    res.set('Link', `<${migrationUrl}>; rel="migration"`);
    next();
  };
}

// 使用
app.use('/api/v1', deprecationMiddleware('2025-06-01', '/docs/migration-v2'), v1Router);
```

## 實戰建議：何時該開新版本

**需要新版本：**
- 移除或重新命名欄位
- 修改欄位型別（如 string → number）
- 修改端點 URL
- 修改請求或回應格式
- 修改認證方式
- 修改錯誤格式

**不需要新版本：**
- 新增欄位（客戶端忽略未知欄位）
- 新增端點
- 新增可選的查詢參數
- 擴充錯誤訊息
- 效能改善

## 小結

版本管理的目標不是「永遠不改」，而是「有節制地改」。選擇版本策略時要考慮團隊習慣、客戶端類型、API 生命週期和生態系統支援。

---

## 延伸閱讀

- [API Versioning: Why and How](https://www.google.com/search?q=API+versioning+why+and+how)
- [Semantic Versioning for APIs](https://www.google.com/search?q=semantic+versioning+for+APIs)
- [Stripe API Versioning](https://www.google.com/search?q=Stripe+API+versioning+strategy)
