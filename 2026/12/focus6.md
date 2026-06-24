# WebAssembly 元件模型

## WIT、跨語言組合、模組連結（2022-2026）

### 前言

傳統 WASM 模組只有一個二進位檔案，沒有介面宣告、沒有型別資訊、沒有依賴管理。這使得多模組組合非常困難。元件模型（Component Model）為 WASM 生態帶來了標準化的模組化系統。

### 為什麼需要元件模型？

```
傳統 WASM 的問題：
  1. 介面不明確 ── 只知道函式簽名，不知道語意
  2. 依賴管理困難 ── 沒有標準的依賴宣告
  3. 記憶體隔離 ── 跨模組資料傳遞需序列化
  4. 版本管理 ── 沒有語意化版本

元件模型的解決方案：
  1. WIT 介面定義 ── 標準的介面描述語言
  2. 元件封裝 ── 包含 WIT 定義的 WASM 模組
  3. Canonical ABI ── 標準化的型別轉換
  4. 模組連結 ── 靜態/動態組合
```

### WIT 介面定義語言

```wit
package example:math@1.0.0;

interface calculations {
    add: func(a: s32, b: s32) -> s32;
    fibonacci: func(n: u32) -> u64;
}

world math-world {
    export calculations;
    import logger: interface {
        log: func(msg: string);
    };
}
```

### 跨語言元件組合

Rust 實作：

```rust
wit_bindgen::generate!({ path: "./wit", world: "math-world" });

struct MathComponent;

impl MathWorld for MathComponent {
    fn add(a: i32, b: i32) -> i32 { a + b }
    fn fibonacci(n: u32) -> u64 { /* ... */ }
}

export!(MathComponent);
```

AssemblyScript 消費：

```typescript
import { Calculations } from 'example:math/calculations';

const result = Calculations.add(3, 4);
console.log(result); // 7
```

### 模組連結

```bash
# 靜態連結：編譯時合併
wasm-tools compose -o combined.wasm math.wasm app.wasm

# 執行動態連結的元件
wasmtime --component combined.wasm
```

### 工具鏈

| 工具 | 用途 |
|------|------|
| `cargo-component` | Rust 元件建置 |
| `wasm-tools` | 二進位操作與組合 |
| `jco` | JavaScript 工具鏈 |
| `componentize-js` | JS → 元件編譯 |

### 小結

元件模型是 WASM 生態最重要的進展之一。它為 WASM 帶來了標準化的介面描述、型別安全的跨語言互通、和模組化的依賴管理。WIT + Canonical ABI + wasm-tools 組合正在建立 WASM 的「npm 生態系統」。

---

**下一步**：[AI + WebAssembly](focus7.md)

## 延伸閱讀

- [元件模型規範](https://www.google.com/search?q=WebAssembly+component+model)
- [WIT 介面定義](https://www.google.com/search?q=WIT+interface+definition)
- [cargo-component](https://www.google.com/search?q=cargo-component)
- [Canonical ABI](https://www.google.com/search?q=Canonical+ABI+WebAssembly)
