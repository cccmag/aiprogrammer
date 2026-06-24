# 本期焦點

## API 設計與後端架構

### 引言

API（Application Programming Interface）是現代軟體開發的核心基礎。從微服務通訊到前端後端互動，從第三方整合到開放平台，API 的設計品質直接決定了系統的可維護性、可擴展性和開發者體驗。

本期雜誌將全面探討 API 設計與後端架構的各個面向，從 RESTful 原則到 GraphQL，從認證授權到速率限制，從文件工具到測試自動化。

### 大綱

* [程式：api_design.js — Express 風格 API 路由與中介軟體](focus_code.md)
  - Router 實作
  - Auth 中介軟體
  - Rate Limiter
  - JSON 驗證

1. [API 設計原則：RESTful](focus1.md)
   - 資源導向設計
   - 統一介面約束

2. [請求與回應格式](focus2.md)
   - JSON 結構設計
   - 錯誤回應規範

3. [API 版本管理](focus3.md)
   - URI 版本 vs Header 版本
   - 平滑遷移策略

4. [認證與授權策略](focus4.md)
   - JWT、OAuth 2.0、API Key
   - RBAC 與權限控制

5. [API 文件與測試](focus5.md)
   - OpenAPI / Swagger
   - Postman / Newman

6. [速率限制與安全性](focus6.md)
   - Token Bucket、Leaky Bucket
   - CORS、CSRF、SQL Injection

7. [GraphQL 入門](focus7.md)
   - Schema、Query、Mutation
   - 與 REST 的比較

### API 設計層次

```
用戶端（Web / Mobile / CLI）
  ┊ HTTP/TLS
API 閘道（Gateway / Reverse Proxy）
  ┊ 路由、限流、認證
服務層（微服務 / 單體）
  ┊ 商業邏輯
資料層（資料庫 / 快取 / 佇列）
```

### 濃縮回顧

#### REST 的六大約束

Fielding 在博士論文中定義了 REST 架構風格的六個約束：客戶端-伺服器、無狀態、快取、統一介面、分層系統、隨需程式碼。其中「統一介面」是 REST 的核心，包含資源識別、透過表徵操作資源、自描述訊息、超媒體作為應用狀態引擎（HATEOAS）。

#### API 設計的黃金法則

1. **一致性**：命名慣例、錯誤格式、分頁方式保持一致
2. **向後相容**：新增欄位而非修改既有欄位
3. **明確的錯誤**：提供可讀懂的錯誤訊息與錯誤碼
4. **安全性優先**：從第一天就考慮認證、授權、限流
5. **文件即規範**：先定義 OpenAPI 規格，再實作程式碼

#### API 技術比較

| 特性 | REST | GraphQL | gRPC |
|------|------|---------|------|
| 傳輸格式 | JSON/XML | JSON | Protobuf |
| 查詢彈性 | 固定欄位 | 客戶端自訂 | 固定欄位 |
| 版本管理 | URI/Header | Schema 演進 | 套件版本 |
| 快取 | HTTP 快取 | 需額外設定 | 無 |
| 學習曲線 | 低 | 中 | 高 |

---

**下一步**：[程式實作](focus_code.md) → [RESTful 原則](focus1.md)

## 延伸閱讀

- [RESTful API Design](https://www.google.com/search?q=RESTful+API+design+best+practices)
- [Microsoft API Design Guide](https://www.google.com/search?q=Microsoft+API+design+guide)
- [Google API Design Guide](https://www.google.com/search?q=Google+API+design+guide)
