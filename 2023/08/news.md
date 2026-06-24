# 本月新知

## 2023 年 8 月程式與 AI 技術動態

### 程式語言與框架

**Rust 1.70 與 1.71 穩定版發布**

Rust 團隊於七月至八月間接連發布 1.70 與 1.71 版本。1.70 引入了 `OnceCell` 與 `OnceLock` 的穩定化，為全域延遲初始化提供了標準解法。1.71 則著重於 C-compatible `enum` 佈局的改進，以及 `C-unwind` ABI 的初步支援，簡化 Rust 與 C++ 互動的錯誤處理。

**TypeScript 5.2 發布**

微軟於八月發布 TypeScript 5.2，新增 `using` 關鍵字與顯式資源管理（Explicit Resource Management）功能，借鑑 C# 的 `using` 語法。開發者可以定義 `[Symbol.dispose]` 方法，讓物件在超出作用域時自動清理資源，大幅簡化檔案和網路連線的管理。

**WebAssembly GC 提案進入 Phase 4**

WebAssembly 社群於本月宣布垃圾回收（GC）提案正式進入 Phase 4（標準化階段）。WASM GC 允許編譯器直接產生高階語言的物件配置和型別檢查程式碼，無需捆綁自帶的 GC runtime。這對 Kotlin/WASM 和 Dart/WASM 的開發有深遠影響。

**Swift 5.9 正式版登場**

Apple 於 WWDC 2023 預覽的 Swift 5.9 在本月正式發布，重點包括 Macros（巨集系統）、`borrowing` 與 `consuming` 所有權修飾字，以及對 C++ 互操作的強化。巨集系統使開發者可以在編譯期操作 AST，大幅減少樣板程式碼。

**Python 3.12 beta 進入最後階段**

Python 3.12 的 beta 測試進入尾聲，預計十月正式發布。新版本帶來了更快的 `asyncio`、改良的錯誤訊息、以及對 PEP 695（型別參數語法）的支援。特別值得注意的是，Python 3.12 的直譯器速度相較 3.11 提升約 5-10%。

### AI 與機器學習

**Llama 2 開源震撼業界**

Meta 於七月下旬開源 Llama 2，並在八月持續引發熱潮。不同於僅供研究的 Llama 1，Llama 2 採用商業友好的授權條款，允許企業免費使用。7B、13B 和 70B 三種規模在眾多基準測試中與 GPT-3.5 匹敵，徹底改變了開源 LLM 的格局。

**LangChain 0.1 框架成熟**

LangChain 於八月發布 0.1 版，API 趨於穩定，並引入了 LangServe 用於部署 LLM 應用，以及 LangSmith 用於除錯和監控。這個版本的發布標誌著 LLM 應用開發框架從實驗走向生產。

**Hugging Face Transformers 4.30 支援 Llama 2**

Hugging Face 在八月初發布 Transformers 4.30，完整支援 Llama 2 模型的推論與微調。同時，PEFT（Parameter-Efficient Fine-Tuning）庫加入 QLoRA 支援，使開發者可以在單張 A100 GPU 上微調 70B 參數的模型。

**Stable Diffusion XL 1.0**

Stability AI 於七月發布 Stable Diffusion XL 1.0（SDXL），這是影像生成模型的一次飛躍。SDXL 採用雙模型架構（base + refiner），生成 1024×1024 的高品質圖片，在構圖、細節和文字渲染方面顯著優於先前版本。

**NeMo Guardrails 開源**

NVIDIA 開源 NeMo Guardrails 框架，為 LLM 應用提供對話安全防護層。開發者可以定義主題限制、事實檢查規則和對話流向控制，防止模型產生有害或不準確的回應。

### 開發工具與雲端服務

**GitHub Copilot Chat 正式上線**

GitHub 於七月宣布 Copilot Chat（基於 GPT-4）正式開放給所有 Copilot 企業訂閱者。開發者可以在 IDE 中直接向 AI 提問、解釋程式碼、重構和產生測試。

**Docker Compose v2.20**

Docker Compose v2.20 引入了全新的 `docker compose watch` 命令，支援即時同步和熱重載，大幅改善本地開發體驗。新的 GPU 加速支援讓容器化 AI 訓練更加便捷。

### 業界動態

- **Google 合併 AI 團隊**：Google 將 DeepMind 與 Google Brain 合併為 Google DeepMind，集中力量應對 OpenAI 和微軟的競爭
- **Red Hat 停止維護 CentOS 8**：CentOS 8 於 2023 年 8 月正式 EOL，標誌著 CentOS 系列的時代終結
- **Meta 開源 MusicGen**：Meta 發布 MusicGen 文字轉音樂模型，支援基於文字或旋律生成音樂
- **JetBrains 發布 AI Assistant**：JetBrains 推出自家的 AI Assistant 插件，整合在 IntelliJ IDEA 和 PyCharm 中

### 標準與規範

- **C23 標準正式發布**：ISO C 委員會發布 C23（ISO/IEC 9899:2023），引入 `nullptr`、`constexpr`、`#elifdef` 和 `bool` 內建型別
- **OpenAPI 4.0 草案**：OpenAPI Initiative 公布 4.0 草案，採用 JSON Schema 2020-12
- **WASI 0.2 階段**：WASI 0.2 進入穩定階段，定義了標準化的 system interface
