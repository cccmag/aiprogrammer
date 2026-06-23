# 本期焦點

## Rust 與 WebAssembly — 從瀏覽器到雲端的統一執行期

### 引言

WebAssembly（WASM）在 2017 年首次出現在瀏覽器中，目標是為網頁提供接近原生的效能。但從那時起，它的野心遠不止於瀏覽器。

WASI（WebAssembly System Interface）將 WASM 帶到了伺服器端、邊緣裝置、甚至資料中心。而 WASM Component Model 則定義了語言中立的模組介面，讓不同語言寫的 WASM 模組可以互相呼叫——就像微服務，但沒有網路開銷。

Rust 在 WASM 生態中佔有特殊地位。它擁有：
- 最成熟的 WASM 編譯目標（`wasm32-unknown-unknown`、`wasm32-wasip1`、`wasm32-wasip2`）
- `wasm-bindgen` 和 `wasm-pack` 等成熟的工具鏈
- 對 WASM 元件模型的原生支援（`wit-bindgen`）

本期將探討 WASM 從瀏覽器到雲端的全面應用，涵蓋元件模型、WASI、伺服器端 WASM，以及如何用 Rust 建構跨平台的統一執行期。

---

## 大綱

* [程式：實作 WASM 元件與主機](focus_code.md)
   - WIT 介面定義
   - Rust 編譯為 WASM 元件
   - wasmtime 主機執行
   - 元件組合與鏈接

1. [WebAssembly 的演進（2015-2026）](focus1.md)
   - MVP→ WASI → Component Model 的發展
   - 瀏覽器 WASM vs 伺服器 WASM
   - Rust 在 WASM 生態中的角色

2. [WASI：伺服器端的 WASM（2019-2026）](focus2.md)
   - WASI 的設計哲學
   - wasip1、wasip2 的差異
   - 檔案系統、網路、時鐘存取
   - Rust 的 WASI 支援

3. [WASM Component Model（2022-2026）](focus3.md)
   - 元件模型的動機
   - WIT 介面定義語言
   - 元件組合與鏈接
   - wit-bindgen 與 Rust 整合

4. [Rust WASM 工具鏈（2018-2026）](focus4.md)
   - wasm-pack、wasm-bindgen、wasm-opt
   - wasmtime、wasmer 執行期
   - 多目標編譯策略
   - 大小與效能最佳化

5. [WASM 在雲端：邊緣運算與 Serverless（2020-2026）](focus5.md)
   - WASM 在 CDN 邊緣的應用
   - Fastly Compute@Edge、Cloudflare Workers
   - 沙箱安全與資源隔離
   - Rust + WASM 的 Serverless 架構

6. [跨語言互通：WASM 作為通用膠水（2020-2026）](focus6.md)
   - 多語言 WASM 元件組合
   - 從 Python/JS 呼叫 Rust WASM
   - 從 Rust WASM 呼叫其他語言
   - 實戰案例：混合語言管線

7. [AI + WASM：可攜式推論的未來（2024-2026）](focus7.md)
   - WASM 中的機器學習推論
   - WebNN 與 WASM 的協同
   - 邊緣 AI 模型的跨平台部署
   - Rust WASM + Candle 的輕量推論

---

## WASM 生態層次

```
應用層 (Serverless、邊緣運算、瀏覽器應用)
      │
WASM 元件 (WIT 介面定義、組合、鏈接)
      │
WASI (檔案、網路、時鐘、亂數)
      │
WASM 核心 (指令集、線性記憶體、表)
      │
執行期 (wasmtime / wasmer / 瀏覽器引擎)
```

## 濃縮回顧

### WebAssembly 發展里程碑

| 年份 | 事件 | 意義 |
|------|------|------|
| 2015 | WASM 首次公開展示 | 瀏覽器原生二進制格式的開端 |
| 2017 | WASM MVP 在四大瀏覽器實作 | 生產環境就緒 |
| 2019 | WASI 預覽 1 發布 | WASM 走出瀏覽器 |
| 2022 | WASM Component Model 提案 | 語言中立的模組系統 |
| 2023 | WASI 預覽 2 (wasip2) | 完整的系統介面 |
| 2025 | WASM 在雲端大規模採用 | Fastly、Cloudflare、AWS 支援 |
| 2026 | Component Model 穩定 | 多語言 WASM 生態成熟 |

### Rust 的 WASM 編譯目標

| 目標 | 用途 | 特點 |
|------|------|------|
| `wasm32-unknown-unknown` | 瀏覽器 | 最輕量，無系統介面 |
| `wasm32-wasip1` | 伺服器/CLI | WASI 預覽 1 |
| `wasm32-wasip2` | 元件/雲端 | WASI 預覽 2 + Component Model |
| `wasm32-unknown-emscripten` | 瀏覽器 | Emscripten 工具鏈 |

### WASM 元件的核心模式

```wit
// WIT 介面定義 — wasm-lib.wit
package example:wasm-lib;

interface types {
    record tensor {
        data: list<f32>,
        shape: list<u32>,
    }
}

world inference {
    export compute: func(input: tensor) -> tensor;
}
```

```rust
// Rust 實作 — 使用 wit-bindgen
wit_bindgen::generate!();

struct Inference;

impl Guest for Inference {
    fn compute(input: Tensor) -> Tensor {
        // 在 WASM 中執行推論
        input
    }
}
```

```rust
// 主機端載入 — 使用 wasmtime
let engine = Engine::new(&wasmtime::Config::new())?;
let component = Component::from_file(&engine, "inference.wasm")?;
let instance = linker.instantiate(&mut store, &component)?;
let result = instance.call_compute(&mut store, &input)?;
```

---

**下一步**：[程式實作](focus_code.md) → [WebAssembly 的演進](focus1.md)

## 延伸閱讀

- [WebAssembly 官方網站](https://www.google.com/search?q=WebAssembly+official+site)
- [WASI 規範](https://www.google.com/search?q=WASI+specification)
- [WASM Component Model](https://www.google.com/search?q=WASM+Component+Model)
- [wasmtime 執行期](https://www.google.com/search?q=wasmtime+Rust)
- [wit-bindgen](https://www.google.com/search?q=wit-bindgen+Rust)
