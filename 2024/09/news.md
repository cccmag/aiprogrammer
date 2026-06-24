# 本月新知

## 2024 年 9 月程式與 API 技術動態

### API 設計與標準

**OpenAPI 4.0 進入草案階段**

OpenAPI Initiative 於本月初發布了 OpenAPI 4.0 的首個公開草案。新版本引入了 JSON Schema 2020-12 完整支援、增強的安全性方案描述（支援 OAuth 2.1 和 FAPI）、以及更精確的 Webhook 定義。向後相容性維持到 OpenAPI 3.1。

**GraphQL 2024 年度調查發布**

GraphQL 基金會公布了 2024 年度生態調查結果。GraphQL 的生產部署較去年增長 35%，最受歡迎的用戶端仍是 Apollo Client，後端框架以 Yoga GraphQL 和 Hasura 增長最快。安全性與快取策略被列為 GraphQL 使用者的首要挑戰。

**JSON Schema 2020-12 成為 IETF 標準**

JSON Schema 2020-12 正式被 IETF 採納為 RFC 標準（RFC 9427-9430）。這套規範將資料驗證標準化，從 API 請求校驗到設定檔管理都有廣泛應用。新的 `unevaluatedProperties` 和 `prefixItems` 關鍵字大幅提升了表達能力。

### 後端框架與工具

**Fastify v5 發布**

Node.js 後端框架 Fastify 發布 v5 版本。主要更新包括：完整的 TypeScript 類型推斷支援、基於 Pino v9 的日誌系統重構、以及新的 `@fastify/type-provider` 模組讓序列化效能再提升 20%。

**Express v5 進入 LTS**

Express.js v5 終於進入 LTS 階段。這是 Express 十年來最大的更新，移除了廢棄的 API、支援非同步錯誤處理、並引入了 `req.params` 的新型別系統。社群期待已久的現代化終於到來。

**Hono 崛起：邊緣運算的 API 框架**

Hono 框架（適用於 Cloudflare Workers、Deno、Bun）的採用率在 2024 年快速成長。Hono 以極小的 bundle size（<14KB）和優秀的效能著稱，特別適合邊緣運算場景。其路由速度經過基準測試，在大多數場景下超越 Express 和 Fastify。

### 認證與安全

**OAuth 2.1 最終發布**

IETF 正式發布 OAuth 2.1（RFC 9568-9571）。OAuth 2.1 整合了過去十年的最佳實踐，廢棄了隱含授予流程（Implicit Grant）和 Resource Owner Password Credentials 授予流程，並強制使用 PKCE 和狀態參數，顯著提升了授權碼流程的安全性。

**API 安全事件：Accel 資料洩漏**

知名 API 管理平台 Accel 因 API 速率限制配置不當，導致未認證的攻擊者可在短時間內爬取大量使用者資料。此事件凸顯了速率限制與 API 安全性的重要性——即使有認證機制，缺乏限流仍可能導致資料外洩。

**WebAuthn Passkey 採用率突破 20%**

無密碼驗證技術 WebAuthn（Passkey）的採用率在主要科技平台突破 20%。Google、Apple、Microsoft 的全平台支援使得 Passkey 的用戶體驗大幅改善，越來越多的 API 開始支援 Passkey 作為第二因素或無密碼登入。

### AI 與 API

**AI 輔助 API 文件生成工具**

多家公司推出基於大型語言模型的 API 文件生成工具。這些工具能夠從程式碼和測試中自動推斷 API 的行為，生成包含請求範例、回應結構和錯誤碼的 OpenAPI 規格文件。

**LLM 作為 API 用戶端**

隨著 AI 代理（Agent）的普及，越來越多的 API 流量來自 LLM 而非人類使用者。這對 API 設計提出了新的要求：更一致的錯誤回應、更結構化的輸出、以及支援「工具呼叫」（Tool Calling）模式的端點設計。

### 微服務與架構

- **eBPF 用於 API 閘道監控**：eBPF 技術開始被應用在 API 閘道層，提供無侵入的請求監控和安全過濾
- **WebAssembly 在 API 閘道的應用**：Wasm 外掛讓 API 閘道可以安全地執行自訂邏輯，Envoy 和 Kong 都已支援
- **AsyncAPI 用於事件驅動架構**：AsyncAPI 規範的生態系持續成長，成為事件驅動 API 的事實標準
