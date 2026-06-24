# 本月新知

## 2026 年 5 月程式與 AI 技術動態

### 程式語言與框架

**Rust 2026 Edition 正式發布**

Rust 團隊於本月發布 Rust 2026 Edition，這是 Rust 語言的第四個重大版本。新版本引入了「所有權 2.0」（Ownership 2.0）機制，在保留記憶體安全保證的同時，大幅降低了所有權傳遞的語法開銷。新的 `& borrow` 語法讓借用檢查器（Borrow Checker）更加智慧，能夠自動推導更複雜的生命週期關係。此外，Rust 2026 還原生支援非同步迭代器（Async Iterator）和協程（Coroutines），簡化了非同步程式設計。

**WebAssembly GC 正式支援**

W3C 於本月宣布 WebAssembly 垃圾回收（Wasm GC）提案正式成為核心標準。這意味著 Java、Kotlin、Dart、Python 等需要垃圾回收的語言，可以直接編譯到 WebAssembly 並在瀏覽器中高效執行。Wasm GC 引入了 `struct`、`array` 和 `i31` 等新型別，以及對應的垃圾回收指令。主流瀏覽器均已支援，Firefox 和 Chrome 的實作在基準測試中達到了原生效能的 80-95%。

**Bun 2.0 發布**

Bun 團隊於本月發布 Bun 2.0，這是最快的 JavaScript 執行環境的重大更新。Bun 2.0 引入了自研的 JavaScript 編譯器「Bun JIT」，取代了先前的 JavaScriptCore 引擎，在伺服器端渲染和 API 回應時間上提升了 3-5 倍。新的外掛系統允許使用 Rust 和 Zig 編寫原生擴展。套件管理器現在完全相容 npm 生態，並引入了「石英鏡像」（Quartz Mirror）加速全球套件下載。

**Mojo 1.0 正式登場**

Modular 公司於本月發布 Mojo 1.0，這是專門為 AI 開發設計的程式語言的首個穩定版本。Mojo 融合了 Python 的易用語法與 MLIR（多層中間表示法）的高效能編譯能力。Mojo 1.0 引入了原生的張量型別（Tensor Type）、自動微分（Automatic Differentiation）的語言層級支援，以及無縫的 GPU/TPU 編譯。Mojo 可以在不修改程式碼的情況下，將 Python 風格的程式碼編譯為 CUDA 或 ROCm 後端。

**TypeScript 6.0 發布**

微軟於本月發布 TypeScript 6.0，這是 TypeScript 語言的一次重大升級。新版本引入了「依賴型別」（Dependent Types），允許型別依賴於執行期的值——這讓 TypeScript 的型別系統達到了依賴型別語言（如 Idris、Liquid Haskell）的表達力。此外，TypeScript 6.0 還引入了「編譯期巨集」（Compile-time Macros），類似 Rust 的 `macro_rules!`，允許在編譯期進行程式碼生成。

### AI 與機器學習

**OpenAI GPT-6 發布**

OpenAI 於本月正式發布 GPT-6，這是迄今為止最大、最先進的語言模型。GPT-6 擁有約 10 兆參數，採用全新的「稀疏專家混合」（Sparse MoE）架構，每次推理僅激活約 5000 億參數。GPT-6 在多模態能力上取得了重大突破——它原生支援文字、圖片、音訊、影片的任意組合輸入與輸出。在 MMLU-Pro、HumanEval 5.0 和 MMMU 等基準測試中，GPT-6 超越了人類專家水準。

**AI Agent 框架生態成熟**

2026 年 5 月，AI Agent 框架進入了生態成熟期。LangChain 發布了 3.0 版本，引入了「語意路由器」（Semantic Router）和「自適應 Agent」（Adaptive Agent）概念；Microsoft 的 AutoGen 2.0 支援動態多代理拓撲；CrewAI 成為了最受歡迎的輕量級多代理框架。值得注意的是，Y Combinator 孵化的多家 Agent 框架新創公司獲得了總計超過 5 億美元的融資。

**Meta Llama 4 正式發布**

Meta 於本月發布 Llama 4 系列模型，包括 Llama 4-8B、Llama 4-70B 和 Llama 4-405B 三個規模。Llama 4 採用了「多模態原生訓練」策略，從訓練初期就同時處理文字、圖片和音訊資料。Llama 4-405B 在多項基準測試中與 GPT-6 和 Gemini 3.0 處於同一梯隊。Meta 繼續沿用開源策略，所有模型權重在非商業許可下免費提供。

**MCP 協議成為業界標準**

Model Context Protocol（MCP）在本月被 ISO/IEC 正式採納為國際標準。MCP 最初由 Anthropic 於 2024 年底提出，旨在標準化 AI 模型與外部工具之間的互動介面。2025-2026 年間，MCP 被 OpenAI、Google、Microsoft 等主要 AI 廠商廣泛採用。標準化後的 MCP 2.0 引入了工具發現（Tool Discovery）、安全沙箱（Sandbox）和交易隔離（Transaction Isolation）等企業級功能。

**AI 代理安全框架發布**

多家機構聯合發布了「AI 代理安全框架」（AI Agent Security Framework, AASF）1.0。該框架由 OWASP、MITRE 和世界經濟論壇共同制定，定義了 AI 代理的六大安全維度：工具許可權管理、提示注入防護、行為邊界控制、資料隱私保護、審計追蹤和故障安全機制。這是全球首個針對 AI 代理安全的產業標準。

### 開發工具與雲端服務

**GitHub Copilot X 全面升級**

GitHub 宣布 Copilot X 的全面升級，整合了 GPT-6 作為底層模型。新版本支援「Agent 模式」（Agent Mode）——Copilot 可以自主規劃、執行程式碼改動、執行測試並修正錯誤，實現了從「程式碼補全」到「自主開發」的飛躍。

**Amazon Q Developer 2.0**

AWS 發布 Amazon Q Developer 2.0，這是一個整合了程式碼生成、除錯、程式碼審查和基礎設施管理的 AI 開發助理。2.0 版本引入了「多檔案感知」能力，可以在整個專案上下文中理解程式碼結構並進行重構建議。

### 業界動態

- **微軟開源 BitNet b1.58**：1.58 位元三元權重量化技術，在保持效能的同時大幅降低推理成本
- **Google DeepMind 發表 AlphaFold 4**：可預測蛋白質與核酸、小分子的複合結構
- **Hugging Face 收購 Replicate**：強化模型部署基礎設施
- **Apple 推出 Foundation Models 3.0**：裝置端 AI 模型重大升級

### 標準與規範

- **ISO 正式發布 Safe Rust 標準**：定義了安全 Rust 子集的正式規範
- **W3C 啟動 Web Neural Network API 2.0 標準化**：針對瀏覽器端 AI 推理的新標準
- **IEEE 發布 AI Agent 互操作性標準**：定義了不同廠商 Agent 之間的通訊協定
