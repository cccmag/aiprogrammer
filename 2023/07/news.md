# 本月新知

## 2023 年 7 月程式與 AI 技術動態

### 程式語言與框架

**Rust 1.71 穩定版發布**

Rust 團隊於 7 月發布 Rust 1.71 穩定版，主要亮點包括將 `C-unwind` ABI 穩定化，使得 Rust 與 C 語言之間的例外處理更加安全可靠。此外，新版改進了 `const` 上下文中的功能支援，以及提升了編譯器效能。

**Python 3.12 進入 Beta 階段**

Python 3.12 於 7 月進入 Beta 階段，預計 10 月發布正式版。新特性包括更靈活的 f-string 語法、`type` 語句的增強，以及 `@override` 裝飾器的引入。效能方面，Python 3.12 的解釋器速度比 3.11 提升了約 10%。

**Google 發布 Android 14 Beta 4**

Android 14 於 7 月達到平台穩定性里程碑。新版本帶來衛星通訊支援、更好的隱私控制，以及對折疊螢幕和平板電腦的介面最佳化。開發者現在可以開始為應用程式進行最終相容性測試。

**TypeScript 5.1 正式發布**

微軟於 7 月發布 TypeScript 5.1，這是 TypeScript 5.0 之後的第一個次要版本更新。主要改進包括對 `undefined` 回呼函式的更好型別推斷、`@link` JSDoc 標籤的支援，以及對 `Promise` 相關操作的型別推斷增強。

### AI 與機器學習

**Meta 開源 Llama 2**

7 月 18 日，Meta 正式開源 Llama 2 大型語言模型，這是 Llama 1 的重大升級。Llama 2 有 70 億、130 億和 700 億三種參數規模，採用商業友善的許可證（Llama 2 Community License），允許商業使用。這標誌著開源 LLM 進入新紀元，引發了開源 AI 社群的巨大迴響。Llama 2 在許多基準測試中表現接近 GPT-3.5。

**OpenAI 推出 GPT-4 API 給所有開發者**

OpenAI 於 7 月宣布 GPT-4 API 正式向所有付費開發者開放。在此之前，GPT-4 API 僅限受邀者使用。此舉大幅擴展了 GPT-4 的應用範圍，促進了新一輪的 AI 應用開發浪潮。

**Anthropic 發布 Claude 2**

Anthropic 於 7 月發布 Claude 2，這是 Claude 1.3 的升級版本。Claude 2 支援更長的上下文（100K tokens），在程式碼生成、推理和安全性方面有顯著提升。Claude 2 的 API 價格與 GPT-4 相當，但在某些任務上表現更具競爭力。

**LangChain 框架持續火熱**

LangChain 框架在 7 月迎來爆發性成長。該框架提供了構建基於 LLM 的應用程式所需的工具和抽象，包括 Prompt 模板、鏈（Chain）和 Agent 系統。社群貢獻了大量第三方整合。

**Hugging Face 發布 Transformers 4.31**

Hugging Face 於 7 月發布 Transformers 4.31，新增對 Llama 2 的原生支援，以及 Flash Attention 2 的整合，顯著提升了訓練和推理速度。

### 開發工具與雲端服務

**GitHub Copilot Chat 公開測試**

GitHub 在 7 月宣布 Copilot Chat 進入公開測試階段。這是一個整合在 IDE 中的 AI 對話助手，讓開發者可以透過自然語言詢問程式碼問題、除錯和重構。

**Cloudflare Workers 支援 Python**

Cloudflare 於 7 月宣布 Workers 平台正式支援 Python 程式語言。這使得 Python 開發者可以在邊緣運算環境中部署無伺服器函式。

**Docker 發布 Compose v2.20**

Docker Compose v2.20 於 7 月發布，新增對 GPU 資源分配的原生支援，以及健康檢查的增強功能。

### 業界動態

- **Twitter 改名為 X**：7 月 23 日，Elon Musk 宣布將 Twitter 品牌改為 X，並推出新的標誌
- **Meta 推出 Threads**：7 月 5 日，Meta 正式推出 Threads 社群平台，上線首周註冊用戶突破 1 億
- **特斯拉自駕晶片 Dojo 投產**：特斯拉宣布 Dojo 超級電腦開始生產，專注於自動駕駛 AI 訓練
- **IBM 和 NASA 發布地理空間 AI 模型**：聯合發布開源的地理空間基礎模型，基於 Harmony 衛星資料

### 標準與規範

- **HTTP/3 採用率突破 30%**：基於 QUIC 協定的 HTTP/3 在全球網站中的採用率持續成長
- **WebAuthn 層級 3 草案發布**：W3C 發布 Web 認證 API 的新版本草案
- **ISO 發布量子安全密碼學標準**：ISO 正式發布基於晶格的密碼學標準 ISO/IEC 14888-4

### 安全事件

- **Move 語言漏洞導致 7000 萬美元損失**：Sui 和 Aptos 使用的 Move 語言生態系統中的漏洞被利用
- **Chrome 緊急修補零日漏洞**：Google 發布 Chrome 115，修補多個高危險性漏洞
- **Zyxel 防火牆漏洞遭大規模利用**：CVE-2023-33010 影響多款 Zyxel 設備
