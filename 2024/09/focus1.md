# API 設計原則：RESTful

## REST 的六大約束

REST（Representational State Transfer）是 Roy Fielding 在 2000 年的博士論文中提出的架構風格。它不是一個協定或標準，而是一組設計約束。理解這六個約束是掌握 RESTful API 設計的基礎。

### 1. 客戶端-伺服器（Client-Server）

分離關注點：客戶端負責使用者介面，伺服器負責資料儲存與商業邏輯。客戶端不需要知道伺服器的內部實作，伺服器也不需要關心客戶端的使用者介面。

### 2. 無狀態（Stateless）

伺服器不儲存客戶端的上下文資訊。每個請求都包含處理該請求所需的所有資訊。這帶來了可擴展性——任何伺服器都可以處理任何請求，無需共享 session 狀態。

```javascript
// ❌ 有狀態的設計
app.post('/api/checkout', (req, res) => {
  req.session.cart.items; // 依賴 session
});

// ✅ 無狀態的設計
app.post('/api/checkout', (req, res) => {
  const { items, shippingAddress } = req.body;
  // 所有資訊都在請求中
});
```

### 3. 可快取（Cacheable）

伺服器需要明確標示回應是否可快取以及快取的時效。HTTP 協定提供了 `Cache-Control`、`ETag`、`Last-Modified` 等機制。適當的快取可以大幅減輕伺服器負擔。

### 4. 統一介面（Uniform Interface）

這是 REST 的核心約束，包含四個子約束：

- **資源識別**：每個資源用 URI 唯一識別，例如 `/api/users/42`
- **資源操作**：透過表徵（Representation）來操作資源，客戶端擁有的只是資源的表述
- **自描述訊息**：每個回應包含足夠的元資料（Content-Type、Link 等）讓客戶端知道如何處理
- **HATEOAS**：回應中包含超媒體連結，引導客戶端發現後續操作

### 5. 分層系統（Layered System）

客戶端不知道它直接與哪個服務器通訊。中間可以存在負載均衡器、快取層、API 閘道等。這是系統可擴展性的關鍵。

### 6. 隨需程式碼（Code on Demand）

這是唯一可選的約束。伺服器可以傳送可執行程式碼（如 JavaScript 小程式）給客戶端擴展功能。

## 資源導向設計

RESTful API 的核心是以「資源」為中心，而非以「動作」為中心。

```javascript
// ❌ 動作導向（RPC 風格）
POST /api/createUser
POST /api/getUser
POST /api/deleteUser

// ✅ 資源導向（RESTful 風格）
POST   /api/users        // 建立
GET    /api/users        // 列表
GET    /api/users/:id    // 單筆
PATCH  /api/users/:id    // 部分更新
DELETE /api/users/:id    // 刪除
```

### 資源命名最佳實踐

- 使用名詞複數：`/api/users`、`/api/orders`
- 巢狀資源表示關聯：`/api/users/:id/orders`
- 使用連字號而非底線：`/api/shipping-addresses`
- 查詢參數用於過濾排序：`/api/users?role=admin&sort=createdAt`

```javascript
// 巢狀資源範例
GET    /api/users/42/orders
POST   /api/users/42/orders
GET    /api/users/42/orders/5
PATCH  /api/users/42/orders/5
```

## 操作與資源的對應

有些操作不符合標準的 CRUD：

```javascript
// 非 CRUD 操作：使用子資源
POST /api/users/42/activate     // ✅ 啟用使用者
POST /api/users/42/deactivate   // ✅ 停用使用者
POST /api/orders/5/cancel       // ✅ 取消訂單
POST /api/orders/5/ship         // ✅ 出貨

// 或者使用查詢參數
POST /api/orders/5?action=cancel // ⚠️ 較不直覺
```

## 小結

RESTful 設計的目標不是為了嚴格遵循規範，而是為了獲得一致性、可預測性和可維護性。當開發者熟悉了你的 API 模式後，他們不需要查文件就能推斷出新資源的使用方式——這才是 RESTful 設計的真正價值。

---

**下一步**：[請求與回應格式](focus2.md)

## 延伸閱讀

- [REST Architectural Constraints](https://www.google.com/search?q=REST+architectural+constraints+Fielding)
- [RESTful API 命名慣例](https://www.google.com/search?q=RESTful+API+naming+conventions)
- [Richardson Maturity Model](https://www.google.com/search?q=Richardson+maturity+model+REST)
