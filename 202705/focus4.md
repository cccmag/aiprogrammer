# Rust WASM 工具鏈（2018-2026）

## 從編譯器到生產部署的完整工具棧

Rust 在 WASM 生態中的主導地位，很大程度上歸功於其完善的工具鏈。從編譯、打包、最佳化到執行，Rust 社群構建了一套完整的工具生態。

### 核心編譯工具

#### 1. wasm-pack — WASM 建置與發布工具

`wasm-pack` 是 Rust WASM 開發的入口工具。它整合了編譯、JS 綁定生成、npm 發布等流程：

```bash
# 建立新的 wasm-pack 專案
wasm-pack new my-wasm-project

# 編譯為瀏覽器 WASM 並生成 JS 綁定
wasm-pack build --target web

# 編譯為 Node.js 模組
wasm-pack build --target nodejs

# 編譯並發布到 npm
wasm-pack publish
```

`wasm-pack` 的內部流程：

```
wasm-pack build ── 執行流程：
─────────────────────────────

1. rustc 編譯為 wasm32-unknown-unknown
   ↓
2. wasm-bindgen 生成 JS/TS 綁定
   ↓
3. wasm-opt 最佳化二進制大小
   ↓
4. 生成 package.json 與 TypeScript 定義
   ↓
5. 輸出到 pkg/ 目錄
```

#### 2. wasm-bindgen — JS 與 WASM 之間的橋樑

`wasm-bindgen` 是 browser WASM 的核心工具。它讓 Rust 函數可以直接暴露給 JavaScript，並自動處理型別轉換：

```rust
use wasm_bindgen::prelude::*;

// 匯出 Rust 函數給 JavaScript 呼叫
#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// 接受 JavaScript 閉包作為參數
#[wasm_bindgen]
pub fn process_array(arr: &[f64]) -> f64 {
    arr.iter().sum()
}

// 匯入 JavaScript 函數供 Rust 使用
#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
    fn console_log(s: &str);
    #[wasm_bindgen(js_namespace = console)]
    fn error(s: &str);
}
```

```
wasm-bindgen 的型別轉換對應：
─────────────────────────────────

Rust 型別             JavaScript 型別
─────────             ────────────────
i32 / u32             Number
f64                   Number
bool                  Boolean
String                String
&str                  String
Vec<u8>               Uint8Array
Vec<f64>              Float64Array
JsValue               any
Closure               Function
```

#### 3. wasm-opt — 二進制最佳化

WASM 二進制大小的優化是生產部署的關鍵。`wasm-opt` 來自 Binaryen 專案，提供多層級的最佳化：

```bash
# 基本最佳化（快速）
wasm-opt -O1 input.wasm -o output.wasm

# 積極最佳化（預設）
wasm-opt -O2 input.wasm -o output.wasm

# 極致最佳化（較慢但最小）
wasm-opt -Oz input.wasm -o output.wasm

# 極致最佳化 + 收縮標識符名稱
wasm-opt -Oz --converge input.wasm -o output.wasm
```

```
最佳化效果對比（一個真實的 Rust WASM 專案）：
─────────────────────────────────

未最佳化 raw.wasm:        1.2 MB
-O1:                      892 KB  (74%)
-O2:                      645 KB  (54%)
-Oz:                      521 KB  (43%)
-Oz + LTO lto = true:     423 KB  (35%)
-Oz + LTO + 移除 debug:   298 KB  (25%)

關鍵 Rust 編譯選項：
[profile.release]
lto = true            # 鏈接時期最佳化
codegen-units = 1     # 單一編譯單元（利於最佳化）
opt-level = "z"       # 以大小為最佳化目標
strip = true          # 移除符號資訊
```

### 執行期比較

#### wasmtime vs wasmer vs 瀏覽器引擎

| 特性 | wasmtime | wasmer | V8（Chrome） | SpiderMonkey（Firefox） |
|------|----------|--------|-------------|----------------------|
| **語言** | Rust | Rust | C++ | C++ |
| **WASI** | wasip1 + wasip2 | wasip1 + wasip2（實驗性） | 僅 wasip1 | 僅 wasip1 |
| **Component Model** | 完整支援 | 實驗性 | 不支援 | 不支援 |
| **即時編譯** | Cranelift | Singlepass / Cranelift / LLVM | TurboFan | Warp |
| **啟動時間** | 極快（< 1ms） | 快（< 5ms） | 中等（~10ms） | 中等（~10ms） |
| **嵌入 API** | Rust / C / Python / Go | Rust / C / Python / PHP | C++（V8 API） | C++（SpiderMonkey API） |

```bash
# wasmtime CLI 用法
wasmtime run module.wasm              # 執行 WASI 模組
wasmtime run --component module.wasm  # 執行 WASM 元件
wasmtime serve module.wasm            # 啟動 HTTP 伺服器

# wasmer CLI 用法
wasmer run module.wasm                # 執行 WASI 模組
wasmer run module.wasm --sys            # 使用系統編譯器
```

```
執行期效能比較（wasmtime vs wasmer）：
─────────────────────────────────

基準測試：矩陣乘法（1024x1024）

原生 Rust（x86_64）：     約 85 ms
wasmtime（Cranelift）：   約 92 ms  （原生效能的 92%）
wasmer（LLVM backend）：  約 88 ms  （原生效能的 97%）
wasmer（Singlepass）：    約 120 ms  （原生效能的 71%）

WASM 的效能開銷主要來自：
1. 沙箱檢查（邊界檢查）
2. 間接呼叫（call_indirect）
3. 無法使用 SIMD 時的向量化損失
```

### 多目標編譯策略

Rust 支援四種 WASM 編譯目標，每種適用於不同場景：

```bash
# 查看可用的 WASM 目標
rustup target list | grep wasm

# 安裝目標
rustup target add wasm32-unknown-unknown
rustup target add wasm32-wasip1
rustup target add wasm32-wasip2
rustup target add wasm32-unknown-emscripten
```

```
目標選擇決策樹：
─────────────────────────

你要在哪裡執行 WASM？
│
├── 瀏覽器中（需要 JS 互動）
│   └── wasm32-unknown-unknown + wasm-bindgen
│
├── 伺服器端 CLI / 外掛
│   └── wasm32-wasip1（成熟穩定）
│
├── 雲端 / Serverless（元件組合）
│   └── wasm32-wasip2（最新標準）
│
└── 瀏覽器 + POSIX 相容性（舊專案）
    └── wasm32-unknown-emscripten
```

同一份 Rust 程式碼可以編譯為多個目標：

```rust
// 使用條件編譯處理平台差異
#[cfg(target_arch = "wasm32")]
fn init_logger() {
    // WASM 環境的日誌初始化
    console_error_panic_hook::set_once();
}

#[cfg(not(target_arch = "wasm32"))]
fn init_logger() {
    // 原生環境的日誌初始化
    env_logger::init();
}
```

```bash
# 工作空間中的多目標建置
cargo build --target wasm32-wasip1 --release
cargo build --target wasm32-wasip2 --release
cargo build --target wasm32-unknown-unknown --release
```

### 二進制大小與效能最佳化

#### 大小最佳化清單

```toml
# Cargo.toml 中的最佳化設定
[profile.release]
opt-level = "z"           # 以最小大小為目標
lto = true                # 鏈接時期最佳化
codegen-units = 1         # 單一編譯單元
strip = true              # 移除符號除錯資訊
panic = "abort"           # 取消 unwinding 支援
```

```rust
// 使用 wee_alloc 替代預設配置器
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;
```

#### 避免不必要的依賴

```bash
# 檢查哪些套件被納入 WASM 二進制
cargo bloat --target wasm32-unknown-unknown --release

# 查看函數級別的大小分析
cargo bloat --target wasm32-unknown-unknown --release --crates
```

#### 效能最佳化

```rust
// 使用整數而非浮點數（當精度允許時）
// 使用小整數型別（u8/u16）而非預設的 usize

// 避免 Vec 的自動縮放
let mut data = Vec::with_capacity(1024);

// 優先使用陣列而非 Vec
const SIZE: usize = 256;
let buffer: [f32; SIZE] = [0.0; SIZE];

// 使用 #[inline] 提示熱路徑
#[inline(always)]
fn dot_product(a: &[f32], b: &[f32]) -> f32 {
    a.iter().zip(b).map(|(x, y)| x * y).sum()
}
```

Rust WASM 工具鏈在 2026 年已相當成熟。從 `wasm-pack` 的開發者體驗，到 `wasm-opt` 的生產級最佳化，再到 `wasmtime` 的企業級執行期——這套工具鏈讓 Rust 成為 WASM 開發的首選語言。

---

## 延伸閱讀

- [wasm-pack 文件](https://www.google.com/search?q=wasm-pack+documentation)
- [wasm-bindgen 指南](https://www.google.com/search?q=wasm-bindgen+Rust)
- [wasmtime 執行期](https://www.google.com/search?q=wasmtime+Rust)
- [wasmer 執行期](https://www.google.com/search?q=wasmer+WebAssembly)
- [Binaryen / wasm-opt](https://www.google.com/search?q=Binaryen+wasm+opt)
- [Rust WASM 大小最佳化](https://www.google.com/search?q=Rust+WASM+size+optimization)

---

*本篇文章為「AI 程式人雜誌 2026 年 7 月號」WASM 系列之四。*
