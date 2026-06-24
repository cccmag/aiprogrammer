# 本月新知

## 2027 年 5 月 WebAssembly 與 Rust 技術動態

### WebAssembly 生態

**WASI Preview 3 正式發布**

WASI 子群組宣布 WASI Preview 3 正式成為穩定規範。Preview 3 最大的變革是完全基於 Component Model 重構所有 API，並引入了非同步網路 socket、非同步檔案 I/O、以及標準化的執行緒模型。這標誌著 WASM 在伺服器端的能力正式與原生應用看齊。

**Component Model 1.0 規範凍結**

W3C WASM 社群組宣布 Component Model 1.0 規範進入凍結狀態，預計 2027 年下半年成為正式推薦標準。這意味著 WIT 介面定義語言、Canonical ABI、元件組合機制將不再有重大變更，生態系統可以開始大規模投資。

**wasmtime 18.0 發布**

Bytecode Alliance 發布 wasmtime 18.0，主要更新包括：Cranelift 後端支援 ARM SVE（可擴展向量擴充）、WASI Preview 3 完整實作、以及全新的記憶體管理引擎（效能提升約 15%）。新版本還引入了動態燃料機制，讓主機可以更精確地控制 WASM 模組的資源消耗。

**WASM Registry 公開測試**

WASM Registry（暫名 Warg）開放公開測試。這是一個類似 npm/crates.io 的 WASM 元件倉儲，支援 WIT 版本管理、簽章驗證、依賴解析。Bytecode Alliance 和 Fermyon 聯合推動此專案，目標是成為 WASM 生態的官方套件管理器。

**llama.cpp 官方 WASM 支援**

llama.cpp 專案正式發布 WASM 後端，支援在瀏覽器和邊緣裝置上執行量化後的 LLM。WASM 後端使用 Candle 和自訂矩陣運算核心，在 M3 Max 上可達到約 15 tokens/sec 的生成速度（int4 量化 7B 模型）。

### Rust 生態

**Rust 1.90 穩定版發布**

Rust 1.90 本月穩定，亮點包括：`wasm32-wasip2` 達到 Tier 1 支援等級（與 x86_64 Linux 同等）、原生執行緒支援在 WASM 目標上實現、以及新的 `#[wasm_bindgen]` 屬性巨集語法改進。

**cargo-component 2.0 發布**

cargo-component 2.0 引入工作空間層級的 WIT 依賴管理、原生 WASM Registry 客戶端、以及多目標同時建置支援。新版本還整合了 wasm-opt 和 wasm-tools，無需手動執行額外的最佳化步驟。

**Tokio 支援 WASM 目標**

Tokio 非同步執行期正式支援 `wasm32-wasip2` 目標。開發者現在可以在 WASM 中使用完整的 Tokio 生態（包括 tokio::net、tokio::fs、tokio::sync），這對於伺服器端 WASM 應用的開發體驗是重大提升。

### AI 與機器學習

**WebNN API 進入 CR 階段**

W3C 宣布 Web Neural Network API（WebNN）進入候選推薦階段。WebNN 為瀏覽器中的 ML 推論提供了標準化的硬體加速 API，與 WASM 的協同使用將大幅提升瀏覽器 AI 應用的效能。

**Candle 0.8 支援 WASM 量化推論**

Hugging Face 發布 Candle 0.8，新增對 WASM 目標的量化推論支援。新版本支援 int4 和 int8 量化模型的自動載入與執行，並利用了 WASM SIMD 128 加速矩陣運算。

**WasmEdge 加入 WASI-NN 發起者行列**

WasmEdge 執行期正式加入 WASI-NN 子群組，貢獻其 GPU 加速推論的經驗。WASI-NN 預計在 2027 下半年完成 GPU 加速的標準化，讓 WASM ML 推論可以充分利用 GPU/NPU 硬體。

### 邊緣運算與雲端

**AWS Lambda 宣布 WASM 支援公開預覽**

AWS Lambda 宣布 WASM 作為新的執行期選項進入公開預覽。開發者可以將 Rust 編譯的 WASM 元件直接部署為 Lambda 函數，冷啟動時間壓縮到 5ms 以下。Lambda WASM 執行期使用 wasmtime 並支援 WASI Preview 2。

**Cloudflare Workers 達到 1 百萬 WASM 函數**

Cloudflare 宣布其 Workers 平台部署的 WASM 函數數量突破 100 萬。平台支援的語言包括 Rust、Go、C、C++、AssemblyScript 和 Zig。WASM 函數的平均冷啟動時間為 0.8ms。

**Fastly 收購 Component Model 工具鏈公司**

Fastly 宣布收購專注於 WASM Component Model 工具鏈的新創公司，包括 cargo-component 核心維護團隊。這項收購旨在加速 Fastly Compute@Edge 平台的元件模型支援。

### 開發工具

**VS Code WASM 擴充套件更新**

微軟發布 VS Code WASM 擴充套件重大更新，新增 WIT 語法高亮、語意化錯誤檢查、即時預覽元件介面圖，以及整合的 WASM Registry 瀏覽器。

**JetBrains 加入 WASM 開發工具支援**

JetBrains 宣布其所有 IDE（包括 IntelliJ IDEA、CLion、GoLand）將在 2027 Q3 整合 WASM 元件開發支援，包括 WIT 編輯器、WASM 除錯器、以及 cargo-component 整合。

**業界動態**

- **Bytecode Alliance 新增三星與 ARM 為成員**：將共同推動 WASM 在 IoT 和行動裝置上的標準化
- **Mozilla 發表 WASM 在 Firefox 中的硬體加速計畫**：利用 GPU 和 NPU 加速 WASM ML 推論
- **Docker 宣布 WASM 執行期達到 GA**：Docker Desktop 的 WASM 支援正式進入一般可用階段
- **美國能源部採用 WASM 作為超級電腦的沙箱執行期**：用於安全執行使用者提交的科學計算程式碼
