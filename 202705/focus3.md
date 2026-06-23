# WASM Component Model（2022-2026）

## 語言中立的元件生態

WASM Component Model 是 WebAssembly 生態中最具野心的擴展。它解決了一個根本問題：如何讓不同語言編譯的 WASM 模組能夠直接互相呼叫——不像微服務那樣透過序列化和網路，而是在同一個程序內以近乎原生的效率溝通。

### 為什麼需要元件模型？

在 Component Model 出現前，WASM 生態面臨三個核心問題：

```
問題 1：語言互通困難
─────────────────────────

Rust 編譯的 WASM（wasm32-unknown-unknown）：
  匯出函數：add(a: i32, b: i32) -> i32
  └── 只能處理 i32/i64/f32/f64 四種基本型別

Go 編譯的 WASM：
  匯出函數：add(a: i64, b: i64) -> i64
  └── 型別不同，需要額外轉換層

若要傳遞「字串」或「陣列」：
  - 必須透過線性記憶體傳遞指標
  - 呼叫方與被呼叫方必須共享記憶體配置策略
  - 實質上需要雙方使用同一種語言的工具鏈


問題 2：無版本管理
─────────────────────────

module_v1.wasm  匯出：process(data: i32) -> i32
module_v2.wasm  匯出：process_v2(data: i64) -> i64

主機程式無法區分版本，必須手動維護命約約定。


問題 3：無法組合
─────────────────────────

元件 A（過濾器）  ←  無法直接連結  →  元件 B（轉換器）

必須由主機程式（通常是 JavaScript 或 Rust）手動協調：
1. 呼叫 A 的 filter 函數
2. 檢查回傳值
3. 若通過則將資料傳給 B
4. 無法在 WASM 層級定義組合邏輯
```

### WIT 介面定義語言

Component Model 的核心是 WIT（WebAssembly Interface Types）——一種語言中立的介面定義語言。WIT 讓開發者以高層次的型別系統定義元件的輸入輸出：

```wit
// wasi-http.wit — WASI 的 HTTP 介面
package wasi:http@0.2.0;

interface types {
    record request {
        method: method,
        uri: string,
        headers: list<tuple<string, string>>,
        body: option<stream<u8>>,
    }

    record response {
        status: u16,
        headers: list<tuple<string, string>>,
        body: option<stream<u8>>,
    }

    variant method {
        get,
        post(string),
        put(string),
        delete,
        patch(string),
        head,
        options,
    }

    variant error {
        invalid-url(string),
        timeout,
        connection-error(string),
        protocol-error(string),
    }
}

world proxy {
    import incoming-handler;
    export outgoing-handler;
}
```

WIT 的關鍵特性：

| 特性 | 說明 |
|------|------|
| **語言中立** | 不依賴任何特定語言的語法或執行期 |
| **可組合** | 多個 `world` 可以合併為更大的元件 |
| **版本管理** | 語義化版本（`@0.2.0`），向後相容性檢查 |
| **型別豐富** | 字串、列表、記錄、變體、選項、結果、串流 |
| **自動綁定** | 工具從 WIT 自動生成各語言的型別安全綁定 |

### 元件組合與鏈接機制

Component Model 的組合機制是透過「導入」（import）和「匯出」（export）來實現的：

```
元件組合示意圖：
─────────────────────────

                ┌──────────────────────────────┐
                │         組合器（Composer）       │
                │                                │
                │  ┌──────────────────┐          │
                │  │  資料轉換元件      │          │
                │  │  (Rust / WASM)    │          │
                │  │                   │          │
                │  │  import: raw-data │          │
                │  │  export: json     │          │
                │  └────────┬─────────┘          │
                │           │                     │
                │  ┌────────▼─────────┐          │
                │  │  ML 推論元件       │          │
                │  │  (Python / WASM)  │          │
                │  │                   │          │
                │  │  import: json     │          │
                │  │  import: model    │          │
                │  │  export: result   │          │
                │  └────────┬─────────┘          │
                │           │                     │
                │  ┌────────▼─────────┐          │
                │  │  輸出格式化元件    │          │
                │  │  (Go / WASM)     │          │
                │  │                   │          │
                │  │  import: result   │          │
                │  │  export: report   │          │
                │  └──────────────────┘          │
                └──────────────────────────────┘
```

在實作層面，元件組合是透過「自適應」（adapter）機制實現的——當兩個元件的介面不完全匹配時，編譯器會自動插入轉換層：

```wit
// 鏈接時的自適應轉換
// 元件 A 匯出：process(data: list<u8>) -> list<u8>
// 元件 B 導入：transform(input: string) -> string

// 組合器自動插入：
// - 位元組串流 → UTF-8 字串 的編碼轉換
// - 錯誤處理的對應
// - 記憶體配置器的統一
```

### wit-bindgen 與 Rust 的深度整合

`wit-bindgen` 是 Component Model 生態中最關鍵的工具。它讀取 WIT 檔案，自動生成特定語言的型別安全綁定。

Rust 的整合流程：

```wit
// math.wit
package example:math;

interface types {
    record matrix {
        data: list<f32>,
        rows: u32,
        cols: u32,
    }
}

world inference {
    export matmul: func(a: matrix, b: matrix) -> matrix;
    export relu: func(x: matrix) -> matrix;
    export softmax: func(x: matrix) -> list<f32>;
}
```

```rust
// lib.rs — wit-bindgen 生成的 Rust 綁定
wit_bindgen::generate!({
    path: "./wit/math.wit",
    world: "inference",
});

// 開發者只需實作 Generated 的 Guest trait
struct InferenceComponent;

impl Guest for InferenceComponent {
    fn matmul(a: Matrix, b: Matrix) -> Matrix {
        assert_eq!(a.cols, b.rows, "矩陣維度不匹配");
        let mut data = vec![0.0_f32; (a.rows * b.cols) as usize];
        // 標準矩陣乘法
        for i in 0..a.rows {
            for j in 0..b.cols {
                let mut sum = 0.0;
                for k in 0..a.cols {
                    sum += a.data[(i * a.cols + k) as usize]
                        * b.data[(k * b.cols + j) as usize];
                }
                data[(i * b.cols + j) as usize] = sum;
            }
        }
        Matrix { data, rows: a.rows, cols: b.cols }
    }

    fn relu(x: Matrix) -> Matrix {
        let data = x.data.iter().map(|&v| v.max(0.0)).collect();
        Matrix { data, rows: x.rows, cols: x.cols }
    }

    fn softmax(x: Matrix) -> Vec<f32> {
        let max = x.data.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
        let exps: Vec<f32> = x.data.iter().map(|&v| (v - max).exp()).collect();
        let sum: f32 = exps.iter().sum();
        exps.iter().map(|&e| e / sum).collect()
    }
}

// 導出元件介面
export!(InferenceComponent);
```

編譯與執行：

```bash
# 編譯為 WASM 元件
cargo build --target wasm32-wasip2 --release

# 使用 wasmtime 執行
wasmtime run \
  --component \
  --invoke matmul \
  inference.wasm
```

### 2026 年的元件生態

截至 2026 年，WASM Component Model 已經形成完整的生態：

1. **WIT 已成為標準介面定義語言**：類似於 IDL 在 CORBA/gRPC 中的地位
2. **WASM 註冊表（WASM Registry）**：類似 npm/crates.io 的元件倉儲
3. **多語言支援成熟**：Rust、Go、Python、C、C#、Kotlin 均可編譯為 WASM 元件
4. **工具鏈完備**：`wasm-tools`、`wit-bindgen`、`jco`（JavaScript 工具）構成完整的開發工具棧

Component Model 代表了 WASM 從「編譯目標」到「元件生態系統」的質變。它不是一個效能最佳化——而是一個關於**組合性**與**互通性**的架構革命。

---

## 延伸閱讀

- [WASM Component Model](https://www.google.com/search?q=WASM+Component+Model)
- [WIT 介面定義語言](https://www.google.com/search?q=WIT+interface+definition+language)
- [wit-bindgen](https://www.google.com/search?q=wit-bindgen+Rust)
- [WASM 元件組合](https://www.google.com/search?q=WASM+component+composition)
- [wasm-tools](https://www.google.com/search?q=wasm+tools+component+model)

---

*本篇文章為「AI 程式人雜誌 2026 年 7 月號」WASM 系列之三。*
