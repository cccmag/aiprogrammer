# 文章集錦

## API 設計與後端架構專輯

### 程式相關（10 篇）

#### 1. [REST API 設計指南](article1.md)

深入探討 RESTful API 的資源命名、HTTP 方法對應、狀態碼選擇和回應結構設計。包含從零設計一個使用者管理 API 的完整案例，涵蓋 CRUD 操作、巢狀資源、過濾排序和分頁實作。適合初學者和想系統化複習 REST 的開發者。

#### 2. [HTTP 方法與狀態碼複習](article2.md)

HTTP 協定是 API 的底層基礎。本文系統性回顧 HTTP/1.1 到 HTTP/3 的核心概念：請求方法（GET、POST、PUT、PATCH、DELETE）、狀態碼分類（1xx-5xx）、Header 的語意、內容協商機制。包含各方法的冪等性分析與快取策略。

#### 3. [JSON Schema 驗證](article3.md)

JSON Schema 是 API 資料驗證的標準工具。從基本型別驗證到複雜的條件約束（if-then-else、oneOf、allOf），再到整合到 Express 中介軟體中的實戰範例。也探討 JSON Schema 2020-12 的新特性與效能優化技巧。

#### 4. [API 版本策略](article4.md)

版本管理是 API 演進的必經之路。比較 URI 版本、Header 版本、查詢參數版本和 Content-Type 版本四種策略的優缺點。包含實際的版本遷移案例、棄用策略和向後相容檢查工具的使用方法。

#### 5. [OAuth 2.0 流程](article5.md)

OAuth 2.1（2024 年標準）的完整流程解析。從授權碼流程（Authorization Code + PKCE）到用戶端憑證流程（Client Credentials），每種流程都有 Node.js 實作範例。包含 JWT 整合、Token 刷新和撤銷實作。

#### 6. [OpenAPI / Swagger 文件](article6.md)

OpenAPI 3.1 的完整教學。從 YAML 基礎語法到複雜的元件引用，從自動產生程式碼到整合 Swagger UI。包含如何使用 `express-openapi-validator` 在執行期驗證請求和回應，實現「文件即規範」的開發流程。

#### 7. [Postman 測試與自動化](article7.md)

Postman 從手動測試到自動化的完整工作流程。環境變數管理、Pre-request Script、Tests Script、Collection Runner、Newman CLI 整合 CI/CD。包含一個完整的 API 測試集合案例，涵蓋認證、資料驗證和錯誤情境。

#### 8. [速率限制實作](article8.md)

從 Token Bucket、Leaky Bucket 到滑動視窗的演算法實作。包含單機記憶體方案和分散式 Redis 方案。探討 Rate Limiting Header 的標準格式（X-RateLimit-Limit、X-RateLimit-Remaining、Retry-After）以及如何設計分層限流策略。

#### 9. [GraphQL 查詢語言](article9.md)

GraphQL 查詢語言的完整教學。從 Schema 定義、Query、Mutation、Subscription 到變數、片段（Fragment）和指令（Directive）。包含 DataLoader 解決 N+1 問題、查詢複雜度分析和 Apollo Server 的生產部署配置。

#### 10. [API 閘道模式](article10.md)

API 閘道（Gateway）作為系統的統一入口：路由轉發、認證聚合、協議轉換、限流快取。比較 Kong、NGINX、Express Gateway、Envoy 和雲端方案（AWS API Gateway、Azure API Management）。包含自訂 API 閘道的 Node.js 實作。
