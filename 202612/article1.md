# WebAssembly 入門與 Rust 整合

## 1. 引言

WebAssembly（WASM）是過去十年 Web 平台最重要的變革之一。它讓瀏覽器可以以接近原生的速度執行 C、C++、Rust 等語言編譯的程式碼，開啟了從未想過的可能性——影片編輯、3D 渲染、密碼學運算、資料庫查詢，全都可以在瀏覽器中流暢執行。而 Rust 是 WebAssembly 的第一公民，其無 GC、零成本抽象的特性與 WASM 的設計理念完美契合。

## 2. 從 MVP 到 3.0：WebAssembly 的演進

### 2.1 MVP（2017）

最初版本的 WebAssembly 只提供四種基本功能：線性記憶體、函式匯出與匯入、基本數值型別（i32、i64、f32、f64）、以及條件分支與迴圈的控制流。MVP 雖然簡單，但已經證明 WASM 可以在瀏覽器中達到接近原生的效能。

### 2.2 後續擴充（2018-2023）

MVP 之後，WASM 陸續加入了 multi-value（多回傳值）、bulk memory（大量記憶體操作）、reference types（參照型別）、fixed-width SIMD（128 位元 SIMD）等提案。這些擴充讓 WASM 從「可用的最小集合」成長為「真正實用的編譯目標」。

### 2.3 WASM 3.0（2024-2026）

2024 年的 WASM 3.0 是最重大的版本升級，引入了兩項核心功能：

- **GC（垃圾回收）**：讓 Java、Kotlin、Dart 等高階語言可以直接編譯到 WASM，無需捆綁自己的 GC 執行期。Rust 雖然不需要 GC，但 WASM GC 讓 WASM 與 JavaScript 之間的物件共享更加高效。
- **Exception Handling（例外處理）**：WASM 層級的 try/catch，讓語言可以拋出例外跨越 JS-WASM 邊界。

## 3. WASM 堆疊機模型與二進位格式

WebAssembly 是一個基於堆疊的虛擬機。指令從堆疊上彈出運算元，執行操作，然後將結果壓回堆疊。

```
i32.const 3       ;; 將 3 壓入堆疊
i32.const 4       ;; 將 4 壓入堆疊
i32.add           ;; 彈出兩個值，相加，將結果壓回
```

這種設計的二進位編碼極為緊湊——每條指令通常只有一個位元組。一個簡單的加法函式編譯後的 WASM 二進位體積可能只有 30-50 位元組。

## 4. Rust 編譯到 WASM 的工具鏈

### 4.1 安裝與設定

```bash
# 安裝 WASM 編譯目標
rustup target add wasm32-unknown-unknown

# 安裝 wasm-pack（推薦的工具鏈）
cargo install wasm-pack
```

### 4.2 使用 wasm-pack 建置

```bash
# 建置為 Web 目標（生成 ES module）
wasm-pack build --target web

# 建置為 Node.js 目標（生成 CommonJS）
wasm-pack build --target nodejs

# 最佳化二進位大小
wasm-pack build --target web --release
```

`wasm-pack` 不僅編譯，還會自動生成 JavaScript 膠水程式碼、TypeScript 型別定義、以及 `package.json`。

### 4.3 手動編譯流程

```bash
# 只編譯 WASM 二進位
cargo build --target wasm32-unknown-unknown --release

# 使用 wasm-opt 進一步最佳化
wasm-opt -Oz -o output.wasm target/wasm32-unknown-unknown/release/myapp.wasm
```

### 4.4 專案結構

一個標準的 Rust+WASM 專案：

```
my-wasm-project/
├── Cargo.toml
├── src/
│   └── lib.rs          # WASM 匯出函式
├── pkg/                # wasm-pack 輸出目錄
│   ├── my_project_bg.wasm
│   ├── my_project.js
│   ├── my_project.d.ts
│   └── package.json
└── www/                # 前端測試頁面
    ├── index.html
    └── index.js
```

## 5. 最簡 WASM 模組範例

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let (mut a, mut b) = (0u64, 1u64);
            for _ in 2..=n {
                let next = a + b;
                a = b;
                b = next;
            }
            b
        }
    }
}

#[wasm_bindgen]
pub fn factorial(n: u32) -> u64 {
    (1..=n as u64).product()
}
```

在 JavaScript 中使用：

```javascript
import init, { fibonacci, factorial } from './pkg/my_project.js';

await init();
console.log(fibonacci(20));  // 6765
console.log(factorial(10));  // 3628800
```

## 6. wasm-bindgen 的角色

wasm-bindgen 是 Rust-WASM 生態的關鍵基礎設施。它自動生成三類程式碼：

1. **型別轉換程式碼**：將 Rust 的數值、字串、陣列轉換為 JavaScript 可理解的型別
2. **記憶體管理程式碼**：在線性記憶體中分配和釋放 Rust 物件
3. **生命週期管理程式碼**：確保 Rust 物件在 JavaScript 持有參照期間不會被釋放

## 7. 結語

WebAssembly 已經從 MVP 的「最小可行產品」成長為一個功能完備的編譯目標。Rust 以其無 GC、小體積、強型別的特性，成為 WASM 生態中最受歡迎的語言。接下來的文章將深入探索 wasm-bindgen、DOM 操作、Canvas 渲染等實戰主題。

---

## 延伸閱讀

- [WebAssembly 官方網站](https://www.google.com/search?q=WebAssembly+official+site)
- [Rust and WebAssembly Book](https://www.google.com/search?q=Rust+and+WebAssembly+book)
- [wasm-pack 文件](https://www.google.com/search?q=wasm-pack+documentation)
- [WebAssembly 3.0 新特性](https://www.google.com/search?q=WebAssembly+3.0+features)
