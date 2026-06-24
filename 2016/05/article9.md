# WebAssembly 的崛起

## 什麼是 WebAssembly？

WebAssembly（Wasm）是一種便攜式的二進位指令格式，可以在瀏覽器中以接近原生的速度執行。

## Wasm 的設計目標

- **便攜**：跨瀏覽器、跨平臺
- **高效**：接近原生效能
- **安全**：記憶體沙箱
- **可驗證**：類型安全

## 與 JavaScript 的關係

```
JavaScript → JS 引擎（V8/SpiderMonkey）
     ↓
    解析 → JIT 編譯 → 執行

WebAssembly → Wasm 引擎
     ↓
   解碼 → JIT 編譯 → 執行
```

## Rust 編譯為 Wasm

```rust
// src/lib.rs
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

編譯：
```bash
rustup target add wasm32-unknown-unknown
cargo build --target wasm32-unknown-unknown
```

## C/C++ 編譯為 Wasm

```c
// hello.c
#include <emscripten.h>

EMSCRIPTEN_KEEPALIVE
int square(int x) {
    return x * x;
}
```

編譯：
```bash
emcc hello.c -o hello.wasm
```

## 在瀏覽器中使用

```javascript
// 載入 Wasm 模組
fetch('module.wasm')
    .then(response => response.arrayBuffer())
    .then(bytes => WebAssembly.instantiate(bytes))
    .then(result => {
        const { add, square } = result.instance.exports;
        console.log(add(1, 2));
        console.log(square(5));
    });
```

## Wasm 的優點

### 高效能

- 接近原生的執行速度
- 適合遊戲、影像處理、編譯器等重度運算

### 跨平臺

- 一次編譯，到處運行
- 可以用任何語言編寫

### 安全

- 記憶體沙箱
- 無法直接訪問系統 API

## Wasm 在 2016 年

2016 年 Wasm MVP 規範完成：

- 主流瀏覽器支援
- Emscripten 工具鏈成熟
- 越來越多專案開始使用

延伸閱讀：
- [Google 搜尋：WebAssembly tutorial](https://www.google.com/search?q=WebAssembly+tutorial)
- [Google 搜尋：Rust WebAssembly](https://www.google.com/search?q=Rust+WebAssembly)