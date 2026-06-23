# 本月新知

## 2026 年 12 月程式與 AI 技術動態

### WebAssembly 生態

**WebAssembly 3.1 進入候選階段**

W3C 宣布 WebAssembly 3.1 規範進入候選推薦階段。3.1 新增了尾呼叫優化（tail call optimization）、自訂註解區段標準化、以及改善的 exception handling API。這些功能讓 WASM 更適合編譯函數式語言和實現更高效的錯誤傳播。

**wasm-pack 3.0 發布**

Mozilla 發布 wasm-pack 3.0，包含多項重大更新：原生的 TypeScript 型別生成、改善的 treeshaking 支援、以及自動化的多目標建置（同時輸出 web、nodejs、no-modules 三種目標）。新版本還整合了 wasm-opt 的二進位最佳化。

**WASI Preview 3 草案公布**

WASI 子群組公布 Preview 3 草案，最大的變化是引入非同步網路 socket 和 clock 介面，並完全基於元件模型重構所有 API。Preview 3 預計在 2027 年中成為新的穩定基準。

**Cloudflare Workers 全面支援 WASM 元件模型**

Cloudflare 宣布 Workers 平台全面支援 WebAssembly 元件模型，開發者可以直接上傳 .wasm 元件而非 JavaScript 膠水程式碼。WIT 定義的介面在 Workers 邊緣節點上可以直接被路由和呼叫。

### 程式語言與框架

**Rust 1.85 穩定版發布**

Rust 1.85 本月穩定，引入了原生的 WASM component model 支援——rustc 可以直接編譯出符合元件模型規範的 .wasm 檔案，無需額外的工具鏈處理。此外，新的 `#[link(kind = "wasm")]` 屬性讓 Rust 可以直接匯入其他 WASM 元件的函式。

**C 語言「Safe C」提案初稿發布**

WG14 Safe C 研究小組發布了第一版技術提案，將 borrow checker 風格的註解引入 C 語言。提案建議在指標型別上附加 `[[borrowed]]` 和 `[[owned]]` 屬性，讓編譯器可以在編譯期檢測懸置指標。這被視為 C 語言史上最大的語法變革。

**Swift 7 新增 WASM 一等公民支援**

Swift 7 發布，將 WebAssembly 列為與 Linux、macOS 同等的一級編譯目標。Swift 的靜態鏈結和值語義型別系統使其在 WASM 上表現出色——編譯後體積僅為 Rust 版本的 1.2 倍。

### AI 與機器學習

**Claude 6 具備 WASM 生成與分析能力**

Anthropic 發布 Claude 6，新增了針對 WebAssembly 的專項能力：可以直接生成、分析和最佳化 .wasm 二進位碼。Claude 6 可以讀取 WASM 的二進位格式並精確指出潛在的效能瓶頸和安全漏洞。

**ONNX Runtime Web 2.0 採用 WASM 元件模型**

ONNX Runtime Web 2.0 發布，全面採用 WASM 元件模型重新架構。模型推論引擎被拆為多個可獨立部署的 WASM 元件——前處理、推論、後處理各自封裝，可根據模型需求動態組合。

**瀏覽器中的 LoRA 微調成為現實**

得益於 WebGPU 和 WASM 的協同優化，瀏覽器中可以直接執行 LoRA（Low-Rank Adaptation）微調。使用者無需上傳資料到雲端，在瀏覽器本地即可完成小型模型的微調，這對隱私敏感場景意義重大。

### 邊緣運算

**Fastly Compute 平台支援 WASM 狀態管理**

Fastly 宣布其邊緣運算平台 Compute@Edge 新增狀態管理 SDK，開發者可以在 WASM 模組中使用 Key-Value 儲存和會話資料，無需額外的邊緣資料庫服務。SDK 基於 WASI Preview 3 的 async 介面。

**Spin 3.0 框架發布**

Fermyon 發布 Spin 3.0，完全基於 WebAssembly 元件模型和 WASI Preview 2。Spin 3.0 引入了「多模組應用」的概念——一個應用由多個 WASM 元件組成，元件之間透過 WIT 介面通訊。Spin 3.0 還支援 AOT 編譯，將冷啟動時間壓縮到 200 微秒以下。

### 開發工具

**VS Code WASM 除錯器正式版**

微軟發布 VS Code 的 WebAssembly 除錯器正式版，支援原始碼映射、斷點、變數檢視、以及線性記憶體瀏覽。開發者可以直接在 VS Code 中除錯 Rust+WASM 專案，無需瀏覽器開發者工具。

**cargo-component 穩定**

cargo-component 工具——用於建置 WebAssembly 元件的 Cargo 子命令——達到 1.0 穩定版。它自動處理 WIT 檔案的解析、元件元資料的生成、以及跨語言依賴解析。

### 業界動態

- **Mozilla 重組 WASM 團隊**：專注於將 Servo 引擎的部分元件編譯為 WASM，目標是讓瀏覽器元件可以被非 Mozilla 專案重用
- **ARM 發表 WASM 硬體加速方案**：在下一代 Cortex 核心中加入 WASM 指令集的硬體加速單元，預計 2028 年上市
- **Docker 支援 WASM 作為容器執行期**：Docker Desktop 可以原生執行 .wasm 檔案，使用 wasmtime 作為執行期
- **美國國防部採用 WASM 作為嵌入式安全執行期**：基於 WASM 的沙箱模型和最小權限原則，用於無人機和感測器節點的軟體更新
