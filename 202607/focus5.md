# 生態系統

## 從 WebAssembly 到嵌入式系統（2017-2025）

### Rust 生態的多樣性

Rust 從一個「系統程式語言」出發，但它的生態系統遠遠超出了這個範圍。截至 2026 年，Rust 已經在以下領域建立了豐富的生態：

### WebAssembly：Rust 到瀏覽器

2017 年，WebAssembly 成為第一個瀏覽器中支援的第四種語言（HTML/CSS/JS 之後）。Rust 從一開始就與 Wasm 緊密整合：

```rust
// wasm-bindgen：Rust 與 JavaScript 的橋樑
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct Calculator {
    value: f64,
}

#[wasm_bindgen]
impl Calculator {
    pub fn new(value: f64) -> Calculator {
        Calculator { value }
    }
    
    pub fn compute(&self) -> f64 {
        self.value.sqrt() * std::f64::consts::PI
    }
}
```

**關鍵專案**：
- **wasm-pack**：一鍵編譯 Rust 到 Wasm 的工具
- **wasm-bindgen**：Rust 與 JS 的自動綁定生成
- **Yew/Leptos/Dioxus**：Rust 前端框架，React 的替代方案
- **wasmtime**：Mozilla 的 Wasm 執行時期

Rust + Wasm 的優勢非常明顯：Rust 的零成本抽象意味著 Wasm 二進制很小，沒有 GC 意味著沒有暫停，而所有權模型意味著安全的記憶體操作。

### 嵌入式 Rust

Rust 的「無執行時期」特性使其成為嵌入式開發的理想選擇：

```rust
#![no_std]  // 不使用標準庫
#![no_main] // 不使用 main 函式

use cortex_m_rt::entry;
use stm32f4xx_hal::prelude::*;

#[entry]
fn main() -> ! {
    if let Some(p) = stm32f4xx_hal::stm32::Peripherals::take() {
        let gpioa = p.GPIOA.split();
        let mut led = gpioa.pa5.into_push_pull_output();
        
        loop {
            led.set_high().unwrap();
            cortex_m::asm::delay(8_000_000);
            led.set_low().unwrap();
            cortex_m::asm::delay(8_000_000);
        }
    }
    
    loop {}
}
```

**關鍵專案**：
- **embedded-hal**：硬體抽象層，標準化嵌入式 API
- **RTIC**：即時中斷驅動並行框架
- **rtic-rs**：Rust 的即時作業系統框架
- **Tock OS**：用 Rust 寫的安全嵌入式 OS

### CLI 工具

Rust 在 CLI 工具領域取得了顯著的成功。許多著名的 CLI 工具使用 Rust 重寫：

```bash
# 著名 Rust CLI 工具
ripgrep (rg)    # 取代 grep，更快
fd              # 取代 find，更人性化
bat             # 取代 cat，帶語法高亮
delta           # 取代 diff，更美觀
zoxide          # 取代 cd，學習習慣
just            # 取代 make，更簡潔
starship        # 跨 shell 提示工具
```

這些工具的共同特點：**驚人的速度和極低的記憶體使用**。Rust 的零成本抽象讓 CLI 工具在保持高效能的同時，保證了記憶體安全。

### 基礎設施軟體

Rust 在基礎設施領域的影響力持續增長：

```rust
// 網路服務範例（使用 axum）
use axum::{
    routing::get,
    Router,
};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(|| async { "Hello, World!" }));

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

**著名 Rust 基礎設施專案**：
- **Firecracker**：AWS 的微型 VM，用於 Lambda/Fargate
- **Linkerd 2.x**：服務網格（service mesh）
- **Pingora**：Cloudflare 的新一代代理伺服器（取代 nginx）
- **Warp**：Cloudflare 的邊緣計算平台
- **Rocket**：Rust 的 Web 框架
- **Actix Web**：高效能 HTTP 框架

### 資料庫與資料工程

Rust 在資料工程領域的影響力日益增長：

- **Polars**：DataFrame 程式庫，Pandas 的替代方案（Rust 核心）
- **DataFusion**：內嵌式查詢引擎，類似 Apache Spark 的查詢規劃
- **Arrow**：列式記憶體格式（Apache Arrow 的 Rust 實作）
- **SurrealDB**：Rust 寫的分散式資料庫
- **RisingWave**：Rust 寫的串流處理資料庫

### 遊戲開發

```rust
// Bevy 遊戲引擎（EAS 架構）
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_system(hello_world_system)
        .run();
}

fn hello_world_system() {
    println!("hello world");
}
```

### Rust 生態的成長

| 年份 | crates.io 套件數 | 下載次數 | 主要新增領域 |
|------|-----------------|---------|-------------|
| 2015 | 3,000 | 1 億 | CLI 工具 |
| 2018 | 20,000 | 10 億 | Web 框架 |
| 2021 | 80,000 | 100 億 | Wasm、嵌入式 |
| 2024 | 150,000 | 300 億 | ML、資料工程 |
| 2026 | 200,000+ | 500 億+ | AI 基礎設施 |

### 為什麼這麼多人用 Rust 寫 CLI 和基礎設施？

1. **靜態連結**：單一二進制，無依賴衝突
2. **跨平台**：編譯一次，任何平台運行
3. **高效能**：C/C++ 等級的效能
4. **記憶體安全**：無緩衝區溢位、use-after-free
5. **優秀的錯誤訊息**：Rust 編譯器的錯誤訊息被譽為業界最佳
6. **Cargo 生態**：簡單的依賴管理和構建系統

### 小結

Rust 的生態系統已經從「系統程式語言」擴展到 Web 開發、嵌入式系統、CLI 工具、基礎設施、資料工程、遊戲開發等多個領域。Rust 的核心優勢——效能、安全、零成本抽象——在所有這些領域都發揮了作用。

下一個前沿是 **AI 基礎設施**——Rust 正在成為 AI 工具和框架的首選語言。

---

**下一步**：[Rust 2026 Edition](focus6.md)

## 延伸閱讀

- [Rust WebAssembly Guide](https://www.google.com/search?q=Rust+WebAssembly+guide)
- [The Embedded Rust Book](https://www.google.com/search?q=embedded+Rust+book)
- [Awesome Rust](https://www.google.com/search?q=awesome+Rust)
