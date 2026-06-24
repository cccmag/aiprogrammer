# 請求與回應格式

## 請求結構設計

API 的請求格式直接影響開發者體驗。一致的請求結構可以大幅降低整合成本。

### URL 路徑與查詢參數

```javascript
// 路徑參數：用於識別特定資源
GET /api/users/42
GET /api/orders/2024-09-001

// 查詢參數：用於過濾、排序、分頁
GET /api/users?role=admin&status=active
GET /api/users?page=2&limit=20&sort=-createdAt
```

### 請求主體（Request Body）

POST 和 PATCH 請求的主體應使用 JSON 格式。以下是設計原則：

```javascript
// POST：建立資源（不包含 ID）
POST /api/users
Content-Type: application/json

{
  "name": "Alice Chen",
  "email": "alice@example.com",
  "role": "developer"
}

// PATCH：部分更新（只傳送要修改的欄位）
PATCH /api/users/42
Content-Type: application/json

{
  "email": "alice@new-company.com"
}
```

### 統一回應格式

設計一個通用的回應包裝結構讓客戶端可以一致地處理結果：

```javascript
// 成功回應
{
  "success": true,
  "data": { ... },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2024-09-01T12:00:00Z"
  }
}

// 列表回應
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 142,
    "totalPages": 8
  }
}

// 錯誤回應
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email 格式不正確",
    "details": [
      { "field": "email", "message": "必須是有效的 Email 地址" }
    ]
  },
  "meta": {
    "requestId": "req_def456"
  }
}
```

## HTTP 狀態碼使用指南

正確使用 HTTP 狀態碼可以讓客戶端在不解析回應主體的情況下了解請求結果：

```javascript
// 2xx：成功
200 OK          // GET 請求成功
201 Created     // POST 建立資源成功
204 No Content  // DELETE 成功

// 3xx：重新導向
301 Moved Permanently  // 資源已永久移動
304 Not Modified       // 資源未修改（快取）

// 4xx：客戶端錯誤
400 Bad Request        // 請求格式錯誤
401 Unauthorized       // 未認證
403 Forbidden          // 無權限
404 Not Found          // 資源不存在
409 Conflict           // 資源衝突（如重複建立）
422 Unprocessable      // 驗證失敗
429 Too Many Requests  // 速率限制

// 5xx：伺服器錯誤
500 Internal Server Error    // 伺服器內部錯誤
502 Bad Gateway              // 上游服務錯誤
503 Service Unavailable      // 服務暫時不可用
```

## 錯誤回應設計準則

好的錯誤回應應該讓客戶端知道「出了什麼問題」以及「如何解決」：

```javascript
// ❌ 不明確的錯誤
{ "error": "Something went wrong" }

// ✅ 具體且有幫助的錯誤
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "無效的請求資料",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email 格式不正確，請輸入有效的電子郵件地址"
      }
    ]
  }
}
```

## 最佳實踐總結

1. **使用 JSON：** 這是現代 API 的通用語言
2. **一致的包裝結構：** 成功和錯誤使用相同的頂層結構
3. **狀態碼正確：** 每個情境使用最精確的 HTTP 狀態碼
4. **有用的錯誤訊息：** 告訴客戶端問題所在和解決方式
5. **分頁標準化：** 統一分頁請求與回應格式
6. **無狀態：** 每個請求獨立，不依賴上下文
7. **內容協商：** 使用 Content-Type 和 Accept header

---

**下一步**：[API 版本管理](focus3.md)

## 延伸閱讀

- [HTTP Status Codes 規範](https://www.google.com/search?q=HTTP+status+codes+specification)
- [JSON API 規範](https://www.google.com/search?q=JSON+API+specification)
- [Problem Details for HTTP APIs (RFC 9457)](https://www.google.com/search?q=RFC+9457+problem+details)
