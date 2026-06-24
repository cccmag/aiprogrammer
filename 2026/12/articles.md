# 文章集錦

## Rust WebAssembly 實戰專輯

### 程式相關（5 篇）

#### 1. [WebAssembly 入門與 Rust 整合](article1.md)

WebAssembly 從 MVP 到 3.0 的演進歷程、WASM 堆疊機模型與二進位格式解析、Rust 編譯到 WASM 的完整工具鏈（rustup、wasm-pack、wasm-opt）。包含最簡 WASM 模組的編譯與執行範例。

#### 2. [wasm-bindgen DOM 操作實戰](article2.md)

wasm-bindgen 的核心機制與繫結生成原理、Rust 與 JavaScript 之間的自動型別橋接、DOM 元素操作與事件處理的完整案例。包含用 Rust 建立互動式 Web 應用的實戰程式碼。

#### 3. [高效能 Canvas 渲染](article3.md)

使用 Rust + WASM 進行 Canvas 2D 影像處理、大量資料視覺化、WebGL 渲染管線整合。分析 JS-Rust 邊界開銷的最佳化策略——批次傳輸、共享記憶體、零複製技術。

#### 4. [WASI 與邊緣運算](article4.md)

WASI 架構設計與能力模型、wasmtime/WasmEdge 執行期的使用、檔案系統與網路存取的 WASI 介面。包含從瀏覽器到命令列的 WASM 移植案例。

#### 5. [WebAssembly 元件模型](article5.md)

元件模型的設計動機與 WIT 介面定義語言、跨語言 WASM 模組的組合與連結、模組依賴管理與版本化。包含 Rust↔AssemblyScript 的跨語言元件組合案例。

### AI 相關（5 篇）

#### 6. [AI 輔助 WASM 模組優化](article6.md)

LLM 生成 WASM 友好的 Rust 程式碼、AI 自動化編譯設定與最佳化參數調整、WASM 二進位體積與效能的智慧化分析。包含 Claude/GPT 輔助開發的實戰經驗。

#### 7. [瀏覽器中的 ML 推論](article7.md)

ONNX Runtime Web 的 WASM 後端架構、在瀏覽器中執行機器學習模型推論、WasmEdge 的 AI 推論框架、WebGPU 與 WASM 的協同優化。

#### 8. [邊緣 Serverless 框架比較](article8.md)

Cloudflare Workers、Fastly Compute、Fermyon Spin 三大邊緣運算平台的 WASM 支援對比、冷啟動效能、狀態管理方案、部署流程與生態差異。

#### 9. [跨語言 WASM 互通性](article9.md)

Rust、C、Go、AssemblyScript 四種語言編譯到 WASM 的實戰比較、ABI 相容性策略、共用記憶體與序列化協定。包含多語言模組協作的完整案例。

#### 10. [WebAssembly 安全模型](article10.md)

WASM 沙箱的隔離機制與限制、能力模型（capability model）的實作原理、旁路攻擊（side-channel）的潛在風險與防護措施、安全部署的最佳實踐。
