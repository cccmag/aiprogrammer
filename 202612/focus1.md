# WebAssembly 基礎

## MVP 到 3.0、堆疊機、Rust 工具鏈（2017-2026）

### 前言

WebAssembly 是過去十年 Web 平台最重要的變革之一。它讓瀏覽器可以以接近原生的速度執行 C、C++、Rust 等語言編譯的程式碼。理解 WASM 的基礎概念——堆疊機模型、二進位格式、線性記憶體——是掌握這項技術的第一步。

### MVP 到 3.0 的演進

**MVP（2017）**：最小可用版本。支援 i32/i64/f32/f64 四種數值型別、線性記憶體、函式匯出/匯入、條件分支和迴圈。雖然功能有限，但已經證明 WASM 可以在瀏覽器中達到接近原生的效能。

**擴充階段（2018-2023）**：陸續加入 multi-value（多回傳值）、bulk memory（大量記憶體操作）、reference types（參照型別）、fixed-width SIMD（128 位元 SIMD）。這些擴充讓 WASM 成為真正的實用編譯目標。

**WASM 3.0（2024）**：引入 GC 和例外處理兩項核心功能。GC 讓 Java、Kotlin 等高階語言可以直接編譯到 WASM；例外處理讓錯誤可以跨越 JS-WASM 邊界傳播。

### 堆疊機模型

WebAssembly 是基於堆疊的虛擬機。程式碼由指令組成，指令從堆疊上彈出運算元，執行操作後將結果壓回：

```
i32.const 10    ;; 壓入 10
i32.const 20    ;; 壓入 20
i32.add         ;; 彈出 20 和 10，壓入 30
```

這種模型的二進位編碼極為緊湊。一個加法函式可能只需要 4-5 個位元組。

### 線性記憶體模型

WASM 使用線性記憶體——一個巨大的可變位元組陣列。所有資料（字串、陣列、物件）都儲存在這塊記憶體中。

```
┌──────────────────────────────────────┐
│ Rust WASM 堆疊 / 堆積               │ ← wasm-bindgen 自動管理
├──────────────────────────────────────┤
│ JS 與 WASM 之間傳遞的資料           │ ← 從線性記憶體複製
├──────────────────────────────────────┤
│ 靜態資料（唯讀）                     │
└──────────────────────────────────────┘
```

大量資料傳遞時，複製開銷可能成為瓶頸。進階的零複製技術透過傳遞指標來避免複製。

### Rust 編譯到 WASM 的工具鏈

```bash
# 安裝目標
rustup target add wasm32-unknown-unknown

# 編譯
cargo build --target wasm32-unknown-unknown --release

# 使用 wasm-pack（推薦）
wasm-pack build --target web
```

`wasm-pack` 不僅編譯，還會自動生成 JavaScript 膠水程式碼、TypeScript 型別定義和 `package.json`。

### 工具鏈比較

| 步驟 | 指令 | 產出 |
|------|------|------|
| 原生編譯 | `cargo build` | 原生二進位 |
| WASM 編譯 | `cargo build --target wasm32-unknown-unknown` | `.wasm` 檔案 |
| 打包 | `wasm-pack build --target web` | `pkg/` 目錄 |
| 最佳化 | `wasm-opt -Oz input.wasm -o output.wasm` | 最佳化後的 .wasm |

### 小結

WebAssembly 的基礎概念——堆疊機、線性記憶體、型別安全——從 MVP 至今沒有改變。WASM 3.0 的 GC 和例外處理是重大的功能擴充，但核心設計仍然保持簡潔和高效。

---

**下一步**：[wasm-bindgen 與 DOM](focus2.md)

## 延伸閱讀

- [WebAssembly 規範](https://www.google.com/search?q=WebAssembly+specification)
- [Rust and WebAssembly Book](https://www.google.com/search?q=Rust+and+WebAssembly+book)
- [wasm-pack 文件](https://www.google.com/search?q=wasm-pack+documentation)
