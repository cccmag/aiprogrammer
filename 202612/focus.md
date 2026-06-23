# 本期焦點

## Rust WebAssembly 實戰 — 從瀏覽器到邊緣運算

### 引言

WebAssembly（WASM）是過去十年 Web 平台最重要的變革之一。它讓瀏覽器可以以接近原生的速度執行 C、C++、Rust 等語言編譯的程式碼，開啟了從未想過的可能性——影片編輯、3D 渲染、密碼學運算、資料庫查詢，全都可以在瀏覽器中流暢執行。

而 Rust 是 WebAssembly 的第一公民。Rust 的 `wasm-pack` 工具鏈讓編譯到 WASM 的體驗無比流暢，沒有 GC 且二進位體積極小的特性恰好是 WASM 最理想的搭配。更重要的是——Rust 的所有權模型在 WASM 的線性記憶體模型中也發揮著關鍵作用。

本期將帶領你從 WebAssembly 的核心概念開始，深入 Rust + WASM 的開發實戰，最後探索 WASI 和邊緣運算等新興應用場景。

---

## 大綱

* [程式：實作 mini-wasm — 從 Rust 到 WebAssembly 的計算核心](focus_code.md)
   - 無 GC 的純計算函式
   - 線性記憶體操作
   - FFI 風格的匯出/匯入
   - 字串與陣列在 WASM 邊界的傳遞

1. [WebAssembly 基礎（2017-2026）](focus1.md)
   - WASM MVP 到 3.0 的演進
   - 堆疊機模型與二進位格式
   - Rust 編譯到 WASM 的工具鏈

2. [wasm-bindgen 與 DOM 操作（2018-2026）](focus2.md)
   - wasm-bindgen 的自動繫結生成
   - JavaScript 與 Rust 的型別橋接
   - DOM 操作與事件處理

3. [效能關鍵應用（2019-2026）](focus3.md)
   - Canvas 與 WebGL 渲染
   - 大量資料處理與視覺化
   - 避免 JS-Rust 邊界開銷

4. [WebAssembly System Interface（2019-2026）](focus4.md)
   - WASI 架構與能力模型
   - 檔案系統與網路存取
   - wasmtime / WasmEdge 執行期

5. [邊緣運算與 Serverless WASM（2021-2026）](focus5.md)
   - Cloudflare Workers / Fastly Compute
   - Spin 框架與 Fermyon
   - 邊緣資料庫與狀態管理

6. [WebAssembly 元件模型（2022-2026）](focus6.md)
   - 元件模型與 WIT 介面定義
   - 跨語言 WASM 模組組合
   - 模組連結與依賴管理

7. [AI + WebAssembly（2024-2026）](focus7.md)
   - 瀏覽器中的 ML 推論（ONNX Runtime / WasmEdge）
   - 邊緣 AI：在終端裝置執行推論
   - AI 輔助 WASM 模組生成

---

## WebAssembly 層次

```
JavaScript (嵌入器環境)
      │  wasm-bindgen 橋接
Rust WASM 模組 (計算核心)
      │  wasm-pack 編譯
Rust 原始碼 (.rs 檔案)
      │
LLVM 後端 → .wasm 二進位
```

## 濃縮回顧

### WebAssembly 的關鍵里程碑

- **2015**：開始醞釀，由 Mozilla、Google、Microsoft、Apple 聯合推動
- **2017**：MVP 版本在四大瀏覽器同時支援
- **2018**：wasm-bindgen 發布，Rust + WASM 開發體驗成熟
- **2019**：WASI 規範發布，WASM 走出瀏覽器
- **2021**：Cloudflare Workers 支援 WASM，邊緣運算起飛
- **2023**：WASI Preview 2 + 元件模型
- **2024**：WASM 3.0 新增 GC 與例外處理
- **2026**：WebAssembly 成為雲端運算的一級公民

### Rust 為何是 WASM 的最佳搭檔？

| 特性 | Rust | C/C++ | Go | AssemblyScript |
|------|------|-------|-----|---------------|
| 二進位大小 | 極小 | 小 | 大 | 中 |
| GC 需求 | 無 | 無 | 有 | 有 |
| 記憶體安全 | 編譯期保證 | 人工管理 | GC | GC |
| 工具鏈體驗 | 極佳 | 可 | 可 | 佳 |
| 非同步支援 | 完善 | 有限 | 完善 | 佳 |

### Rust 編譯到 WASM 的工具鏈

```bash
# 安裝目標
rustup target add wasm32-unknown-unknown

# 編譯
cargo build --target wasm32-unknown-unknown --release

# 使用 wasm-pack（推薦）
wasm-pack build --target web
wasm-pack build --target nodejs
```

`wasm-pack` 不僅編譯，還會自動生成 JavaScript 膠水程式碼和 `package.json`。

### wasm-bindgen 的型別橋接

Rust 和 JavaScript 之間的型別轉換是 WASM 開發的核心挑戰。wasm-bindgen 解決了這個問題：

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[wasm_bindgen]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

支援的型別映射：
| Rust | JavaScript |
|------|-----------|
| `i32` / `u32` | `number` |
| `f64` | `number` |
| `bool` | `boolean` |
| `String` | `string` |
| `&str` | `string`（唯讀） |
| `Vec<T>` | `Array` |
| `JsValue` | `any` |

### 線性記憶體模型

WebAssembly 使用線性記憶體（linear memory）——一個巨大的可變位元組陣列。Rust 編譯器自動管理這個記憶體，但開發者需要理解邊界：

```
┌──────────────────────────────┐
│ Rust WASM 堆疊 / 堆積       │ ← wasm-bindgen 自動管理
├──────────────────────────────┤
│ JS WASM 傳遞的資料          │ ← 需要手動編組（從線性記憶體複製）
├──────────────────────────────┤
│ 靜態資料（唯讀）            │
└──────────────────────────────┘
```

大量資料在 JS 和 WASM 之間傳遞時，複製開銷可能成為瓶頸。

### 邊緣運算的革命

WASM 在邊緣運算中的優勢：

1. **冷啟動極快**：數毫秒級，遠快於容器
2. **安全隔離**：WASM 的能力模型比容器更精細
3. **多語言**：同一個邊緣平台可以執行 Rust、C、Go 寫的模組
4. **輕量級**：一個 WASM 模組通常只有數十 KB

```rust
// 使用 Spin SDK 的邊緣應用
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

#[http_component]
fn handle_request(req: Request) -> anyhow::Result<impl IntoResponse> {
    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/plain")
        .body("Hello from the edge!")
        .build())
}
```

---

**下一步**：[程式實作](focus_code.md) → [WebAssembly 基礎](focus1.md)

## 延伸閱讀

- [Rust and WebAssembly Book](https://www.google.com/search?q=Rust+and+WebAssembly+book)
- [wasm-pack 官方文件](https://www.google.com/search?q=wasm-pack+documentation)
- [WebAssembly 元件模型](https://www.google.com/search?q=WebAssembly+component+model)
- [WASI 規範](https://www.google.com/search?q=WASI+specification)
- [Fermyon Spin 框架](https://www.google.com/search?q=Fermyon+Spin+framework)
