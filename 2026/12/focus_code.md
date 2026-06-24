# mini-wasm：從 Rust 到 WebAssembly 的計算核心

## 概述

mini-wasm 是一個展示 Rust 如何編譯到 WebAssembly 的計算核心專案。所有函式都設計為在 `wasm32-unknown-unknown` 目標下無痛編譯——沒有 `std::io`、沒有系統呼叫、只有純粹的資料處理。

專案展示四類典型的 WASM 計算模式：

1. **純數值計算** — add、factorial、fibonacci、is_prime
2. **線性代數** — dot_product、matrix_multiply
3. **影像處理** — grayscale、brightness
4. **資料轉換** — count_words、base64_encode/decode

## 核心概念

### 1. 純函式：WASM 的天然搭配

WASM 模組最適合純計算任務——給定輸入，回傳輸出，沒有副作用。這也是 Rust 函式在 WASM 中最自然的使用方式：

```rust
#[wasm_bindgen]
pub fn add(a: i32, b: i32) -> i32 { a + b }

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
```

這些函式沒有 GC 開銷、沒有隱藏配置——編譯後的 WASM 二進位體積極小。

### 2. 線性記憶體模型

WebAssembly 使用線性記憶體作為與 JavaScript 的主要溝通通道。mini-wasm 模擬了這個概念：

```rust
static mut LINEAR_MEMORY: [u8; 65536] = [0u8; 65536];

pub fn memory_write(offset: usize, data: &[u8]) {
    assert!(offset + data.len() <= 65536,
        "WASM memory write out of bounds");
    unsafe {
        LINEAR_MEMORY[offset..offset + data.len()].copy_from_slice(data);
    }
}
```

在真實 WASM 中，`wasm-bindgen` 會自動管理線性記憶體中的字串和陣列配置。但理解記憶體模型對於處理大量資料至關重要：

| 資料大小 | JS-WASM 傳遞方式 | 開銷 |
|---------|----------------|-----|
| 小（<1KB） | 直接在邊界複製 | 可忽略 |
| 中（1KB-1MB） | 寫入線性記憶體傳遞指標 | 一次複製 |
| 大（>1MB） | 傳遞指標，直接操作線性記憶體 | 零複製 |

### 3. 影像處理管線

瀏覽器中的 Canvas 影像處理是 WASM 最常見的應用場景之一：

```rust
pub fn grayscale(pixels: &[u8]) -> Vec<u8> {
    pixels.chunks_exact(4).map(|rgba| {
        let gray = (rgba[0] as u32 * 77
                  + rgba[1] as u32 * 150
                  + rgba[2] as u32 * 29) / 256;
        [gray as u8, gray as u8, gray as u8, rgba[3]]
    }).flatten().collect()
}
```

這在 JavaScript 中也可以實作，但 WASM 版本在處理百萬畫素級影像時，效能差距可達 2-5 倍。

### 4. 資料轉換與編碼

base64 編解碼展示了典型的資料轉換模式——純計算、無狀態、輸入輸出明確：

```rust
pub fn base64_encode(data: &[u8]) -> String {
    const CHARS: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ\
                           abcdefghijklmnopqrstuvwxyz\
                           0123456789+/";
    // 每 3 個位元組編碼為 4 個 base64 字元
}
```

### 5. 編譯到 WASM

要將這個專案編譯到 WebAssembly：

```bash
# 安裝 WASM 目標
rustup target add wasm32-unknown-unknown

# 使用 wasm-pack（自動處理繫結）
wasm-pack build --target web

# 或手動編譯
cargo build --target wasm32-unknown-unknown --release
```

`wasm-pack` 會自動生成：
- `pkg/mini_wasm_bg.wasm` — 編譯後的 WASM 二進位
- `pkg/mini_wasm.js` — JavaScript 膠水程式碼
- `pkg/package.json` — npm 套件描述

## WASM 建置對照

| 建置步驟 | 指令 | 產出 |
|---------|------|------|
| 原生編譯 | `cargo build` | 原生二進位 |
| WASM 編譯 | `cargo build --target wasm32-unknown-unknown` | `.wasm` 檔案 |
| 完整打包 | `wasm-pack build --target web` | `pkg/` 目錄 |
| Node.js 用 | `wasm-pack build --target nodejs` | CommonJS 模組 |
| 無綁定 | `wasm-pack build --target no-modules` | 傳統 script 載入 |

## 測試

```
running 14 tests
test tests::test_add ... ok
test tests::test_base64_encode ... ok
test tests::test_base64_roundtrip ... ok
test tests::test_brightness ... ok
test tests::test_count_words ... ok
test tests::test_dot_product ... ok
test tests::test_factorial ... ok
test tests::test_fibonacci ... ok
test tests::test_grayscale ... ok
test tests::test_is_prime ... ok
test tests::test_matrix_multiply ... ok
test tests::test_memory_isolation ... ok
test tests::test_memory_read_write ... ok
test tests::test_memory_write_oob ... ok
test result: ok. 14 passed; 0 failed
```

## 執行結果

```
=== mini-wasm: WebAssembly Computation Kernel Demo ===

--- arithmetic ---
  add(2, 3)      = 5
  factorial(10)  = 3628800
  fibonacci(20)  = 6765
  is_prime(97)   = true
  is_prime(100)  = false

--- linear algebra ---
  dot_product    = 50
  matrix (2x2)   = [58.0, 64.0, 139.0, 154.0]

--- image processing (simulated RGBA) ---
  grayscale      = (140, 140, 140, 255)
  brightness(+80)= (180, 230, 255, 255)

--- string processing ---
  count_words    = 4
  base64 encode  = UnVzdCArIFdBU00=
  base64 decode  = Rust + WASM

--- linear memory ---
  memory[0..30]   = 'Hello from WASM linear memory!'

=== demo completed ===
```

## mini-wasm 教會我們的事

### 1. WASM 是計算加速器，不是完整應用平台

WASM 擅長純粹的計算任務。DOM 操作、網路請求、裝置 API 仍然需要 JavaScript 的協助。`wasm-bindgen` 的作用就是搭建這個橋樑。

### 2. 邊界開銷是真實的

每次 JS-Rust 邊界呼叫都有微小但可測量的開銷。將工作批次化（一次傳入大量資料，一次回傳大量結果）比頻繁的小型呼叫更高效。

### 3. 線性記憶體需要理解

雖然 `wasm-bindgen` 隱藏了大部分記憶體管理細節，但在處理大型陣列或高效能場景時，理解線性記憶體的配置與釋放機制是必要的。

### 4. 先寫純函式，再決定目標平台

mini-wasm 的所有函式在原生 Rust 和 WASM 目標下都可以編譯和測試。這種「先寫邏輯，後決定平台」的模式是 Rust 跨平台開發的最佳實踐。

---

## 延伸閱讀

- [完整程式碼](_code/src/lib.rs)
- [Rust and WebAssembly Book](https://www.google.com/search?q=Rust+and+WebAssembly+book)
- [wasm-bindgen 指南](https://www.google.com/search?q=wasm-bindgen+guide)
- [wasm-pack 文件](https://www.google.com/search?q=wasm-pack+documentation)
- [WebAssembly 線性記憶體](https://www.google.com/search?q=WebAssembly+linear+memory)
