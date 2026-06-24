# WebAssembly 的演進（2015-2026）

## 從瀏覽器實驗到統一執行期

WebAssembly 的願景在十年間從「瀏覽器中的高效能二進制格式」擴展為「跨平台統一執行期」。這段演進可分為三個階段：瀏覽器原生、系統介面標準化、元件化生態。

### 2015-2017：MVP — 瀏覽器的二進制標準

2015 年，WASM 在 W3C 社群組中首次公開展示。目標很明確：為 JavaScript 提供一個高效能的編譯目標，讓 C/C++ 和 Rust 程式碼能在瀏覽器中以接近原生的速度執行。

```
WASM MVP 設計目標：
─────────────────────────

├── 二進制格式（.wasm）：緊湊、可快速解析
├── 線性記憶體：連續的位元組陣列，只能透過指令存取
├── 表（Table）：間接函數呼叫的基礎
├── 僅四種基本型別：i32、i64、f32、f64
├── 安全沙箱：無存取檔案系統、網路的能力
└── 必須透過 JavaScript（JS API）與 DOM 互動
```

2017 年，四大瀏覽器（Chrome、Firefox、Safari、Edge）同步實作了 WASM MVP，這是瀏覽器史上首次達成跨引擎的二進制格式共識。

關鍵特徵：**WASM 在瀏覽器中只是一個被沙箱隔離的計算單元**。它不能直接操作 DOM，不能發出 HTTP 請求，不能存取檔案——所有 I/O 都必須透過 JavaScript 橋接。

### 2019-2023：WASI — 走出瀏覽器

WASI（WebAssembly System Interface）的誕生從根本上改變了 WASM 的應用範疇。由 Mozilla 的 Lin Clark 和 Till Schneidereit 主導，WASI 定義了 WASM 模組與作業系統互動的標準介面：

```
WASI 能力模型：
─────────────────────────

WASM 模組（wasm32-wasip1）
    │
    ├── 【能力】fd_read / fd_write
    ├── 【能力】path_open（若有權限）
    ├── 【能力】clock_time_get
    └── 【能力】random_get
            │
            ▼
    WASI 執行期（wasmtime / wasmer）
            │
            ▼
    主機作業系統
```

WASI 預覽 1（wasip1）在 2019 年發布，引入「能力為基礎的安全模型」（Capability-based Security）——WASM 模組預設沒有任何系統存取權限，必須由主機明確授予。

2023 年的 WASI 預覽 2（wasip2）是重大升級：引入 `wit` 介面定義語言、支援非同步操作、統一的流與錯誤處理。

### 2022-2026：Component Model — 語言中立的元件生態

WASM Component Model 解決了 WASM 生態中長期存在的問題：**如何讓不同語言編譯的 WASM 模組互相呼叫**。

```
WASM 生態層次 (2026)：
─────────────────────────

┌────────────────────────────────────────┐
│          應用 / Serverless              │
│  Cloudflare Workers / Fastly / AWS     │
├────────────────────────────────────────┤
│       WASM 元件（Component Model）      │
│  語言互通、版本管理、組合鏈接            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ Rust    │ │  Go     │ │ Python  │  │
│  │ 元件    │ │ 元件    │ │ 元件    │  │
│  └────┬────┘ └────┬────┘ └────┬────┘  │
├───────┴────────────┴───────────┴───────┤
│   WASI（系統介面層）                     │
│   檔案 / 網路 / 時鐘 / 亂數              │
├────────────────────────────────────────┤
│   WASM 核心（指令集 + 線性記憶體）       │
├────────────────────────────────────────┤
│   執行期（wasmtime / wasmer / V8）      │
└────────────────────────────────────────┘
```

### Rust 的特殊角色

Rust 在 WASM 生態中的獨特地位來自幾個因素：

| 特性 | 說明 |
|------|------|
| **無 GC 開銷** | Rust 無需垃圾回收器，產生的 WASM 二進制最小 |
| **多目標編譯** | 同一份程式碼可編譯為 `wasm32-unknown-unknown`、`wasm32-wasip1`、`wasm32-wasip2` |
| **零成本抽象** | 高階語言特性在編譯時被消除，不產生執行期開銷 |
| **工具鏈成熟** | `wasm-pack`、`wasm-bindgen`、`wit-bindgen` 等工具由 Rust 社群主導開發 |
| **生態第一** | Rust 是 WASM Component Model 的第一級語言（first-class language） |

多目標編譯範例：

```bash
# 瀏覽器目標（無系統介面）
cargo build --target wasm32-unknown-unknown --release

# WASI 預覽 1（伺服器端）
cargo build --target wasm32-wasip1 --release

# WASI 預覽 2 + Component Model（雲端）
cargo build --target wasm32-wasip2 --release
```

```
WASM 各目標的二進制大小比較（Hello World）：
─────────────────────────────────

wasm32-unknown-unknown:    約 2 KB  （最輕量）
wasm32-wasip1:             約 10 KB （含 WASI 實作）
wasm32-wasip2:             約 15 KB （含元件模型支援）
wasm32-unknown-emscripten: 約 30 KB （含 JS 膠水程式碼）
```

### 2026 年 WASM 生態全景

截至 2026 年，WASM 生態已經相當成熟：

1. **瀏覽器 WASM**：所有現代瀏覽器原生支援，用於遊戲、影像處理、加密、資料壓縮
2. **伺服器 WASM**：Fastly Compute@Edge、Cloudflare Workers、AWS Lambda WASM 支援
3. **邊緣 WASM**：CDN 邊緣節點執行 WASM，提供低延遲運算
4. **外掛系統**：Shopify、Figma、Adobe 等產品使用 WASM 作為外掛執行期
5. **資料管線**：Apache Kafka 等資料平台整合 WASM 作為資料轉換引擎
6. **AI 推論**：瀏覽器與邊緣裝置上的輕量 ML 推論

WASM 的十年演進顯示一個核心趨勢：**從瀏覽器專屬的效能工具，轉變為跨平台、跨語言的統一執行期標準**。而 Rust，作為這個生態的核心語言，將持續主導 WASM 的未來發展。

---

## 延伸閱讀

- [WebAssembly 官方網站](https://www.google.com/search?q=WebAssembly+official+site)
- [WASM MVP 規格](https://www.google.com/search?q=WebAssembly+MVP+specification)
- [WASI 規範](https://www.google.com/search?q=WASI+specification)
- [WASM Component Model 提案](https://www.google.com/search?q=WASM+Component+Model+proposal)
- [Rust + WebAssembly 文件](https://www.google.com/search?q=Rust+WebAssembly+documentation)

---

*本篇文章為「AI 程式人雜誌 2026 年 7 月號」WASM 系列之一。*
