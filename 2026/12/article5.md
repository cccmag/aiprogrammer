# WebAssembly 元件模型

## 1. 引言

傳統的 WASM 模組只有一個二進位檔案，沒有型別資訊、沒有介面宣告、沒有依賴管理。這使得多個 WASM 模組之間的組合非常困難。WebAssembly 元件模型（Component Model）解決了這個問題——它為 WASM 生態帶來了一套完整的模組化系統。

## 2. 元件模型設計動機

### 2.1 問題：傳統 WASM 模組的困境

```
問題 1：介面不明確
  WASM 匯出一個函式 i32 add(i32, i32)
  但沒有說明參數的語意、回傳值的範圍

問題 2：依賴管理困難
  模組 A 需要呼叫模組 B 的函式
  但沒有標準的宣告方式

問題 3：記憶體隔離
  每個模組有自己的線性記憶體
  跨模組資料傳遞需要序列化
```

### 2.2 元件模型的解決方案

元件模型引入了三個核心概念：

1. **WIT 介面定義語言**：標準的介面描述格式
2. **元件（Component）**：包含 WIT 定義的 WASM 模組
3. **模組連結（Module Linking）**：元件之間的動態組合

## 3. WIT 介面定義語言

WIT（WebAssembly Interface Types）是元件模型的介面描述語言：

```wit
// calculator.wit
package example:calculator@1.0.0;

interface math {
    add: func(a: s32, b: s32) -> s32;
    fibonacci: func(n: u32) -> u64;
}

world calculator-world {
    export math;
    import console: interface {
        log: func(msg: string);
    };
}
```

WIT 支援的型別：

| WIT 型別 | Rust 對應 | JavaScript 對應 |
|----------|-----------|---------------|
| `s32`/`u32` | `i32`/`u32` | `number` |
| `s64`/`u64` | `i64`/`u64` | `BigInt` |
| `float32`/`float64` | `f32`/`f64` | `number` |
| `bool` | `bool` | `boolean` |
| `string` | `String` | `string` |
| `list<T>` | `Vec<T>` | `Array` |
| `record` | `struct` | `Object` |
| `variant` | `enum` | `union` |

## 4. 實戰：跨語言元件組合

### 4.1 定義 WIT 介面

```wit
// processing.wit
package example:data-processing@1.0.0;

interface transform {
    record point {
        x: float64,
        y: float64,
        z: float64,
    }
    rotate: func(points: list<point>, angle: float64) -> list<point>;
    scale: func(points: list<point>, factor: float64) -> list<point>;
}

world processing-world {
    export transform;
}
```

### 4.2 Rust 實作

```rust
// 由 cargo-component 自動從 WIT 生成繫結
wit_bindgen::generate!({
    path: "./wit",
    world: "processing-world",
});

struct ProcessingComponent;

impl ProcessingWorld for ProcessingComponent {
    fn rotate(points: Vec<Point>, angle: f64) -> Vec<Point> {
        let cos = angle.cos();
        let sin = angle.sin();
        points.into_iter().map(|p| Point {
            x: p.x * cos - p.y * sin,
            y: p.x * sin + p.y * cos,
            z: p.z,
        }).collect()
    }

    fn scale(points: Vec<Point>, factor: f64) -> Vec<Point> {
        points.into_iter().map(|p| Point {
            x: p.x * factor,
            y: p.y * factor,
            z: p.z * factor,
        }).collect()
    }
}

export!(ProcessingComponent);
```

### 4.3 AssemblyScript 消費

```typescript
// 消費 Rust 元件的 AssemblyScript 程式
import { Point, Transform } from 'example:data-processing/transform';

class Consumer {
    process(): Point[] {
        const points: Point[] = [
            { x: 1.0, y: 0.0, z: 0.0 },
            { x: 0.0, y: 1.0, z: 0.0 },
        ];
        const rotated = Transform.rotate(points, 3.14159 / 2);
        return Transform.scale(rotated, 2.0);
    }
}
```

## 5. 模組連結與依賴管理

### 5.1 靜態連結

編譯時將所有依賴元件合併為一個二進位：

```bash
wasm-tools compose -o combined.wasm transform.wasm consumer.wasm
```

### 5.2 動態連結

執行期根據需求載入元件：

```bash
wasmtime --component combined.wasm
```

### 5.3 依賴解析

元件模型支援語意化版本管理：

```wit
// 宣告依賴
package example:app@1.0.0;
use example:data-processing@^1.0.0;
```

## 6. 元件模型的工具鏈

| 工具 | 用途 |
|------|------|
| `cargo-component` | Rust 的元件建置工具 |
| `wasm-tools` | WASM 二進位操作與組合 |
| `jco` | JavaScript 的元件工具鏈 |
| `component-bindgen-go` | Go 語言的元件綁定生成 |

## 7. 元件模型的應用場景

1. **外掛系統**：應用程式可以動態載入 WASM 元件作為外掛
2. **微服務**：每個服務封裝為一個 WASM 元件，由編排器動態組合
3. **多語言混合**：不同語言編寫的元件通過 WIT 介面協作
4. **邊緣函式組合**：Serverless 平台上的函式由多個小元件組合而成

## 8. 結語

元件模型是 WebAssembly 生態最重要的發展之一。它為 WASM 帶來了標準化的介面描述、型別安全的跨語言互通、以及模組化的依賴管理。對於建構大型 WASM 應用，元件模型是必備的基礎設施。

---

## 延伸閱讀

- [WebAssembly 元件模型規範](https://www.google.com/search?q=WebAssembly+component+model)
- [WIT 介面定義語言](https://www.google.com/search?q=WIT+interface+definition+language)
- [cargo-component 指南](https://www.google.com/search?q=cargo-component+guide)
- [wasm-tools 文件](https://www.google.com/search?q=wasm-tools+documentation)
