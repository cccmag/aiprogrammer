# 文章集錦

## Rust & WebAssembly — 從瀏覽器到雲端的統一執行期

### 程式相關（5 篇）

#### 1. [瀏覽器中的 WebAssembly — 從 WebGL 到 WebGPU 的實戰應用](article1.md)

WASM 在瀏覽器中的應用從 WebGL 到 WebGPU 的演進。涵蓋 Canvas 2D 高效渲染、WebGL 著色器操作、WebGPU 計算管線、以及 JS-WASM-GPU 三層架構的記憶體管理最佳化策略。

#### 2. [WASI 深入探討 — 系統介面實戰](article2.md)

WASI 系統介面的實戰應用，從能力模型、檔案系統操作、網路程式設計、時鐘與環境變數，到自訂 WASI 介面實作。包含完整的 HTTP 伺服器範例和外掛系統載入流程。

#### 3. [WASM 元件模型實戰 — WIT 與元件組合](article3.md)

WASM Component Model 的實戰應用。從 WIT 多層次介面組織、cargo-component 使用、元件實作模式，到靜態與動態元件組合策略。包含企業級外掛系統架構設計。

#### 4. [WASM 執行期比較 — wasmtime vs wasmer 深入分析](article4.md)

兩大獨立 WASM 執行期的架構、效能、生態比較。從 Cranelift vs LLVM 後端、冷啟動時間、WASI 支援度、到應用場景建議，提供選擇執行期的完整參考。

#### 5. [邊緣運算實戰 — 用 Rust + WASM 打造邊緣應用](article5.md)

使用 Rust + WASM 建構生產級邊緣應用的完整流程。包含 WIT 介面定義、圖片處理元件實作、邊緣平台比較（Fastly/Cloudflare/Spin）、無狀態設計模式、和快取策略。

### AI 相關（5 篇）

#### 6. [跨語言 WASM 開發 — Python/Go/Rust 協作實戰](article6.md)

多語言 WASM 元件協作的完整案例。從共用 WIT 介面設計、Rust 核心處理、Go 並發報表生成、Python 主機協調，到 GitLab CI 多語言建置管線和跨語言挑戰解決方案。

#### 7. [WASM 安全模型 — 沙箱、能力與供應鏈安全](article7.md)

WASM 安全模型的三層架構：指令級沙箱隔離、WASI 能力模型的最小權限原則、供應鏈安全的簽章與驗證。涵蓋旁路攻擊風險、執行期資源限制、和安全部署最佳實踐。

#### 8. [WASM 工具鏈 — wasm-pack, wit-bindgen, cargo-component](article8.md)

三組核心 WASM 開發工具的深入介紹。從 wasm-pack 的瀏覽器建置流程、wit-bindgen 的多語言綁定生成、cargo-component 的元件建置管理，到完整的 CI/CD 工作流程整合。

#### 9. [AI 推論在 WASM 上的實戰應用](article9.md)

在 WASM 中執行 ML 模型推論的完整解決方案。涵蓋 Candle 框架整合、ONNX Runtime Web 使用、瀏覽器 LLM 推論實作、模型量化策略、和跨平台的效能基準測試。

#### 10. [WASM 效能最佳化 — 從編譯到執行的全面調校](article10.md)

WASM 效能最佳化的系統性探討。從 Rust 編譯設定（LTO、最佳化等級）、WASM 二進制最佳化（wasm-opt、去除死程式碼）、執行期最佳化（記憶體管理、邊界開銷），到 WASM 專屬的程式設計技巧。

---

*所有文章均可在各期目錄中透過連結存取。*
