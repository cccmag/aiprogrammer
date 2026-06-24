# 本月新知

## 2024 年 3 月程式與 AI 技術動態

### 程式語言與框架

**React 19 正式發布**

React 19 於本月正式發布，這是自 React 18 以來最大幅度的更新。新版本引入了 React Server Components 的穩定支援，允許開發者在伺服器端渲染元件，大幅減少客戶端 JavaScript 體積。此外，Actions API 簡化了表單處理流程，useOptimistic hook 讓樂觀更新變得直覺。

**Vite 5.1 推出**

Vite 團隊發布 5.1 版本，帶來更快的冷啟動速度和更佳的 HMR 體驗。新版本支援 Rolldown——一個基於 Rust 的打包器，建置速度比 Rollup 提升 10 倍。Vite 已成為前端開發者最喜愛的建置工具。

**Node.js 22 進入 LTS**

Node.js 22 於本月進入長期支援階段，帶來原生 ESM 支援的全面強化。新版本改進了 WebSocket 支援、提升了 require() 與 import 的互通性，並加入了內建的測試執行器增強功能。這些改進使 Node.js 成為更完善的伺服器端 JavaScript 執行環境。

**TypeScript 5.4 發布**

微軟發布 TypeScript 5.4，強化了型別縮小（Narrowing）能力，支援在閉包中更精確地追蹤型別。新版還加入了 NoInfer 工具型別，讓開發者能控制泛型型別的推斷行為。

**Sass 1.71 更新**

Sass 發布 1.71 版本，繼續推進棄用 @import 規則的計畫。新版鼓勵開發者全面遷移至 @use 與 @forward 模組系統，並支援更靈活的內建函式。

### AI 與機器學習

**Claude 3 問世**

Anthropic 於本月發布 Claude 3 系列模型，包含 Haiku、Sonnet 和 Opus 三個版本。Claude 3 Opus 在複雜推理任務上超越 GPT-4，並支援 200K token 上下文視窗。其視覺分析能力使得開發者可以直接上傳圖像進行分析。

**GPT-4 Turbo 正式上線**

OpenAI 發布 GPT-4 Turbo 的正式版本，支援 128K token 上下文，並大幅降低了 API 呼叫成本。新的 JSON 模式確保了結構化輸出，讓開發者更容易將 AI 整合到應用程式中。

**Google Gemini 1.5 發布**

Google 推出 Gemini 1.5 模型，最引人注目的是高達 1M token 的上下文視窗。Gemini 1.5 在多模態任務上展現出色能力，尤其擅長長文件理解和影片分析。

**開源模型 Mistral 與 Mixtral 崛起**

法國 AI 新創 Mistral AI 發布了 Mixtral 8x22B，這是基於專家混合（MoE）架構的開源模型。Mixtral 在推理能力上接近閉源模型，並可部署於消費級硬體。這標誌著開源 AI 模型的重大進步。

**Stable Diffusion 3 發布**

Stability AI 發布 Stable Diffusion 3，採用全新的擴散 Transformer 架構，在文字理解與圖像品質上大幅提升。新模型支援多主題生成和精確的文字渲染。

### 開發工具與雲端服務

**VS Code 1.88 登場**

微軟發布 VS Code 1.88，加入多 Tab 拖拽重新排序、Copilot 聊天改進以及 GitHub Copilot 的擴展 API。新版本還支援使用 Profile 進行更靈活的開發環境配置。

**Docker 25.0 發布**

Docker 發布 25.0 版本，帶來了 Docker Init 指令，可一鍵生成容器化專案配置。新版的 Compose 支援 GPU 加速和更細粒度的資源管理，對 AI 開發者尤為實用。

**GitHub Actions 工作流程升級**

GitHub Actions 推出了 Composite Actions 的增強版本，支援巢狀工作流程和條件式步驟跳過。這大大簡化了 CI/CD 管線的維護。

### 業界動態

- **Apple Vision Pro 上市**：蘋果於 2 月正式開賣 Vision Pro 頭戴裝置，開發者開始探索 visionOS 上的 3D 空間應用開發
- **React Native 0.74 發布**：新架構（New Architecture）預設啟用，效能大幅提升
- **WebGPU 在 Chrome 中預設啟用**：為 Web 應用程式的 GPU 運算開啟新篇章
- **Flutter 3.19**：Dart 3.3 帶來新的類型修飾符和 Records 特性

### 標準與規範

- **ECMAScript 2024 最終草案**：正式納入 `Array.prototype.groupBy` 和 Promise.withResolvers
- **HTML 規範的最近更新**：新增 `search` 事件和 `popover` API
- **CSS 嵌套語法正式納入規範**：讓前端開發者終於可以使用巢狀 CSS 語法
