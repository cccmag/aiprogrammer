# 程式實作：WASM 元件與主機 — 元件模型模式

## 簡介

本實作展示 WASM Component Model 的核心設計模式：介面定義（WIT）、客戶端實作（Guest）、主機執行期（Host）、元件組合（Composition）。完整程式碼在 `_code/src/lib.rs`。

## 核心概念

### 1. WIT 風格的介面定義

WASM 元件模型使用 WIT（WebAssembly Interface Types）定義跨語言介面。在 Rust 中，我們用 traits 模擬：

```wit
// math.wit — WIT 介面定義
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
}
```

對應的 Rust trait：

```rust
pub trait MathGuest {
    fn matmul(&self, a: &Matrix, b: &Matrix) -> Result<Matrix, String>;
    fn relu(&self, x: &Matrix) -> Matrix;
}
```

### 2. 客戶端實作（Guest）

Guest 是編譯為 WASM 的元件。它實作 `MathGuest` trait：

```rust
pub struct WasmGuest;

impl MathGuest for WasmGuest {
    fn matmul(&self, a: &Matrix, b: &Matrix) -> Result<Matrix, String> {
        // 標準矩陣乘法
        // ...
    }
    fn relu(&self, x: &Matrix) -> Matrix {
        let data: Vec<f32> = x.data.iter().map(|&v| v.max(0.0)).collect();
        Matrix::new(data, x.rows, x.cols)
    }
}
```

### 3. 主機介面（Host）

Host 是 WASM 元件匯入的系統功能：

```rust
pub trait MathHost {
    fn log(&self, message: &str);
    fn random_f32(&self) -> f32;
}
```

### 4. 主機執行期

模擬 wasmtime 的元件載入與執行：

```rust
pub struct HostRuntime<G: MathGuest, H: MathHost> {
    guest: G,
    host: H,
}

impl<G: MathGuest, H: MathHost> HostRuntime<G, H> {
    pub fn run_inference(&self, input: &Matrix, weight: &Matrix, bias: &Matrix) -> Result<Matrix, String> {
        self.host.log("step 1: matmul");
        let z = self.guest.matmul(input, weight)?;
        let z_plus_b = add_matrices(&z, bias);
        self.host.log("step 2: relu");
        let a = self.guest.relu(&z_plus_b);
        self.host.log("step 3: softmax");
        Ok(self.guest.softmax(&a))
    }
}
```

### 5. 元件組合

在 WASM 元件模型中，可以將多個元件組合為管線：

```rust
pub struct Pipeline<A: MathGuest, B: MathGuest> {
    component_a: A,
    component_b: B,
}

impl<A: MathGuest, B: MathGuest> Pipeline<A, B> {
    pub fn compose(&self, a: &Matrix, b: &Matrix) -> Result<Matrix, String> {
        let mid = self.component_a.matmul(a, b)?;
        Ok(self.component_b.relu(&mid))
    }
}
```

### 6. 線性記憶體抽象

WASM 的線性記憶體模型在 Rust 中的對應：

```rust
pub struct LinearMemory {
    data: Vec<u8>,
}

impl LinearMemory {
    pub fn read_f32(&self, offset: usize) -> f32 { ... }
    pub fn write_f32(&mut self, offset: usize, val: f32) { ... }
}
```

## 完整執行

```bash
cd _code
cargo build
cargo test    # 9 個測試全部通過
cargo run     # 執行推論管線
```

輸出範例：
```
Input matrix (2x3):
[  1.00,   2.00,   3.00]
[  4.00,   5.00,   6.00]

[host] === WASM component inference ===
[host]   step 1: matmul(input, weight)
[host]   step 2: add bias
[host]   step 3: relu activation
[host]   step 4: softmax output

Output matrix (2x2):
[  0.35,   0.65]
[  0.18,   0.82]
```

## 與真實 WASM 工具鏈的對應

| 本範例 | 真實 WASM 生態 |
|--------|---------------|
| `MathGuest` trait | `wit-bindgen` 從 WIT 生成的 trait |
| `WasmGuest` | 編譯為 `wasm32-wasip2` 的元件 |
| `HostRuntime` | `wasmtime` + `wasmtime-wasi` |
| `MathHost::log` | `wasi:logging/logging` |
| `Pipeline` | 元件組合與鏈接 |
| `LinearMemory` | WASM 線性記憶體 + `memory.grow` |

## 擴展練習

1. **加入 wasmtime**：將 `HostRuntime` 改為實際使用 `wasmtime` 載入 `.wasm` 檔案
2. **WIT 檔案**：編寫完整的 WIT 並用 `wit-bindgen` 生成綁定
3. **多語言組合**：用不同語言（C、Rust、TinyGo）撰寫元件並組合
4. **WASI 整合**：使用 `wasmtime-wasi` 讓 WASM 元件存取檔案系統
5. **效能測試**：比較原生 vs WASM 的 matmul 效能
