# API 版本管理

## 為什麼需要版本管理

API 一旦發布，就會有客戶端依賴它。當 API 需要升級時，若直接修改既有端點的行為，會導致現有客戶端崩潰。版本管理讓 API 提供者可以在引入破壞性變更的同時，維護對舊版客戶端的支援。

## 版本策略比較

### 1. URI 路徑版本（最常見）

```javascript
// 版本寫在 URL 路徑中
GET /api/v1/users
GET /api/v2/users

// 實作方式
router.get('/api/v1/users', handlerV1);
router.get('/api/v2/users', handlerV2);

// 或用前綴分組
const v1 = new Router();
const v2 = new Router();

v1.get('/users', handlerV1);
v2.get('/users', handlerV2);
```

**優點：** 簡單直覺、容易快取、瀏覽器可直接存取
**缺點：** URI 混亂、語意上資源版本而非 API 版本

### 2. Header 版本（自訂 Header）

```javascript
// 客戶端透過 Header 指定版本
GET /api/users
Accept-Version: v1
// 或
X-API-Version: 2

// 實作方式
function versionMiddleware(versionMap) {
  return (req, res, next) => {
    const version = req.headers['accept-version'] || 'v1';
    req.apiVersion = version;
    next();
  };
}

router.get('/api/users', versionMiddleware({
  v1: handlerV1,
  v2: handlerV2
}));
```

**優點：** URI 乾淨、符合 REST 理念
**缺點：** 快取複雜、客戶端實作較麻煩

### 3. 查詢參數版本

```javascript
GET /api/users?version=1
GET /api/users?version=2

// 實作方式
router.get('/api/users', (req, res) => {
  const version = req.query.version || '1';
  switch(version) {
    case '1': return handlerV1(req, res);
    case '2': return handlerV2(req, res);
  }
});
```

**優點：** 實作簡單、預設值靈活
**缺點：** 容易遺漏、URL 參數污染、違反 REST 原則

### 4. Content-Type 版本（媒體類型）

```javascript
// 客戶端指定媒體類型版本
GET /api/users
Accept: application/vnd.myapp.v2+json

// 回應
Content-Type: application/vnd.myapp.v2+json
```

**優點：** 最符合 REST 的內容協商精神
**缺點：** 複雜度高、工具支援有限

## 版本遷移策略

### 向後相容的關鍵原則

```javascript
// ✅ 安全的新增（向後相容）
// 回應中加入新欄位（客戶端忽略未知欄位）
// 原本：{ "id": 1, "name": "Alice" }
// 新增：{ "id": 1, "name": "Alice", "email": "alice@test.com" }

// ❌ 破壞性變更（需要新版本）
// 移除欄位
// 修改欄位型別
// 修改端點 URL
// 修改錯誤格式
// 修改認證方式
```

### 平滑遷移策略

```javascript
// 並行運行（Parallel Run）
// v1 和 v2 同時運行，逐步將流量從 v1 轉移到 v2

// 棄用期（Deprecation Period）
router.get('/api/v1/users', (req, res) => {
  res.set('Sunset', 'Sat, 01 Mar 2025 00:00:00 GMT');
  res.set('Deprecation', 'true');
  // 回傳 v1 的資料，但加上棄用通知
  res.json({
    data: getUsersV1(),
    deprecation: {
      sunset: '2025-03-01',
      migration: '/docs/migration-v2'
    }
  });
});
```

### 版本生命週期管理

```
發布 v1 → 發布 v2（同時支援 v1）→ v1 棄用通知 → v1 下線
├─────────────── 並行支援期 ───────────────┤
                ├───── 棄用通知期 ────┤
```

## 實戰建議

1. **並非所有變更需要新版本：** 新增欄位、新增端點通常不需要新版本
2. **內部 API vs 公開 API：** 內部 API 可以更頻繁地版本更迭，公開 API 需要更長的並行支援期
3. **文件同步更新：** 每個版本的 API 文件必須獨立維護
4. **預設最新版本：** 未指定版本的請求預設使用最新穩定版本

---

**下一步**：[認證與授權策略](focus4.md)

## 延伸閱讀

- [API Versioning Best Practices](https://www.google.com/search?q=API+versioning+best+practices)
- [REST API Versioning Strategies](https://www.google.com/search?q=REST+API+versioning+strategies)
- [Microsoft REST API Versioning](https://www.google.com/search?q=Microsoft+REST+API+versioning)
