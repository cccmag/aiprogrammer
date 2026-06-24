# 本月新知

## 2026 年 5 月程式與 AI 技術動態

### 程式語言與框架

**Python 4.0 進入 Beta 測試**

Python 核心開發團隊於本月啟動 Python 4.0 Beta 測試，這是 Python 語言的第三個重大版本。Python 4.0 最大的變革是移除大量已棄用的舊語法，並引入了靜態型別系統的強化版本——「型別化 Python」（Typed Python）。新版支援了更嚴格的型別檢查模式，可選的記憶體安全保證，以及針對 Web 開發優化的標準函式庫改進。

**FastAPI 3.0 正式發布**

FastAPI 團隊於本月發布 3.0 版本，這是一個重大更新。新版本引入了基於 Pydantic V3 的增強驗證系統，原生支援 WebSocket 壓縮，以及全新的 Plugin API。最受關注的是 FastAPI 3.0 加入了「API 版本控制內建支援」，允許開發者在路由層級直接宣告版本策略。此外，自動化 OpenAPI 文件生成現在支援多種認證方案的同時展示。

**HTTP/4 協商啟動**

IETF HTTP 工作組於本月正式啟動 HTTP/4 的協商程序。HTTP/4 的目標是解決 HTTP/3 在超大規模部署中遇到的瓶頸，包括更高效的多路復用機制、改良的壅塞控制，以及對衛星網路等新型通訊鏈路的支援。業界預期 HTTP/4 草案將在 2027 年底前定案。

**curl 與 libcurl 重大安全更新**

curl 專案於本月發布了 8.20 版本，修復了多個高風險安全漏洞。更新重點包括：TLS 後量子密碼學支援正式穩定、新的 HTTP/3 連線管理機制，以及更好的 HTTP CONNECT 隧道支援。此版本也引入了實驗性的「HTTP Cookie 自動加密」功能。

### AI 與機器學習

**OpenAI 發布 GPT-5 企業版**

OpenAI 於本月推出了 GPT-5 Enterprise，這是在三月份 GPT-5 基礎上針對企業需求最佳化的版本。主要特色包括：更低的 API 呼叫成本（約為標準版 60%）、可自訂的微調能力、以及增強的隱私保護模式——所有資料在推理過程中保持在企業的 VPC 內。GPT-5 Enterprise 也支援了更多的函式呼叫並行度，適合複雜的 API 工作流程。

**AI API 閘道器市場爆發**

隨著越來越多企業將 AI 整合到產品中，API 閘道器市場迎來爆發。多家新創公司推出了專門針對 AI API 的代理和閘道器解決方案，提供速率限制、成本控制、A/B 測試和模型路由等功能。這些工具讓開發者可以在 OpenAI、Anthropic、Google 和開源模型之間靈活切換，同時統一管理 API 金鑰和用量監控。

**GitHub Copilot 支援 API 開發模式**

GitHub 宣布 Copilot 新增「API 開發模式」，專門針對 Web API 開發者設計。該模式可以根據 OpenAPI/Swagger 規範自動生成客戶端程式碼、API 測試案例，以及完整的 API 文件。Copilot 現在也能理解 RESTful 路由設計模式，在開發者設計 API 時給出符合業界最佳實踐的建議。

### 開發工具與雲端服務

**Postman 推出 AI 驅動的 API 測試**

Postman 於本月推出了 AI 驅動的 API 測試功能。開發者只需描述測試場景，AI 便自動生成測試案例、預期回應和邊界條件檢查。新功能還包含了 API 回應的智慧分析，能自動識別潛在的錯誤模式和效能瓶頸。

**Cloudflare API Gateway 全面升級**

Cloudflare 宣布其 API Gateway 服務全面升級，新增了 GraphQL 防護、API Schema 驗證，以及基於行為分析的異常檢測。Cloudflare 宣稱其 API 安全方案能阻止 OWASP API Security Top 10 中列出的所有攻擊類型。

### 業界動態

- **Google 開源 API 設計工具**：基於 AIP（API Improvement Proposals）的自動化 API 風格檢查工具
- **AWS 推出 API 優先的應用託管服務**：自動將資料庫結構映射為 REST/GraphQL 端點
- **Apple 增強 Swift OpenAPI Generator**：支援更多的認證方案和平台
- **Mozilla 發布 HTTP Observatory 2.0**：全新的 Web API 安全評分系統

### 標準與規範

- **OpenAPI 4.0 規範草案發布**：引入了 WebSocket 和 Server-Sent Events 的原生描述
- **JSON Schema 2026-05 版本發布**：新增了「依賴驗證」和「條件約束」功能
- **IETF 發布 OAuth 3.0 草案**：簡化了授權碼流程，支援更安全的裝置授權
