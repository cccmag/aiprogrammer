# Rust 2026 Edition：async/await 與嵌入式生態系大升級

## 前言

Rust 語言的第三個 Edition——Rust 2026 Edition——於 2026 年 3 月正式發布。這是自 Rust 2018 Edition 以來最重要的里程碑，帶來了開發者期待已久的語言特性改進和生態系統升級。本文將深入解析這次更新的核心亮點。

## async/await 語法大革命

### 問題的由來

Rust 的 async/await 功能自 2019 年 stable 之後，雖然功能完整，但存在一些不夠直覺的設計：

1. `async fn` 必須回傳 `impl Future`
2. `await` 無法在 `match` 分支中使用
3. 生命週期與 async 的互動複雜

### 新版帶來的改變

Rust 2026 Edition 對 async/await 進行了大刀闊斧的改革：

```rust
// 舊版：async fn 必須明確返回 impl Trait
async fn fetch_data() -> impl Future<Output = Result<String, Error>> {
    async { /* ... */ }
}

// 新版：直接返回類型
async fn fetch_data() -> Result<String, Error> {
    let response = reqwest::get("https://api.example.com").await?;
    let text = response.text().await?;
    Ok(text)
}
```

### await 在 match 中的使用

```rust
// 新版終於支援
let result = match some_async_value().await {
    Ok(data) => process(data),
    Err(e) => handle_error(e),
};
```

### Async Traits 正式穩定

```rust
use async_trait::async_trait;

// 舊版需要透過 async_trait 宏
#[async_trait]
trait DataProcessor {
    async fn process(&self, data: Vec<u8>) -> Result<(), Error>;
}

// 新版原生支援
trait DataProcessor {
    async fn process(&self, data: Vec<u8>) -> Result<(), Error>;
}
```

## 錯誤處理的新紀元

### ? Operator 的增強

```rust
// 新版允許在更多情境使用 ?
fn main() -> Result<(), Error> {
    let config = load_config().try_fold(String::new(), |acc, line| {
        Ok(acc + &line)
    })?;
    
    println!("Config: {}", config);
    Ok(())
}
```

### Error 的泛型支援

```rust
use std::error::Error;

// 新版允許錯誤類型的泛型約束
async fn connect(url: &str) -> Result<Connection, impl Error + Send + Sync> {
    // ...
}
```

## 嵌入式生態系大升級

### 對 ARM Cortex-M55 的完整支援

Rust 2026 Edition 正式將 ARM Cortex-M55 處理器列入 Tier 1 支援等級，這意味著：

- 完整的標準庫支援
- 穩定的 Cargo 目標支援
- 官方的 Cargo 測試基礎設施

```toml
# Cargo.toml
[target.thumbv8m.main-none-eabihf]
runner = 'probe-run --chip ARM Cortex-M55'
```

### RISC-V 硬體除錯支援

嵌入式團隊還帶來了對 RISC-V 架構的硬體除錯支援，配合 OpenOCD 和 J-Link，開發者可以直接在 VS Code 中進行單步除錯。

```rust
#![no_std]
#![no_main]

use panic_halt as _;

#[rtic::app(device = "rv32i")]
mod app {
    use rtic::CYCCNT;

    #[shared]
    struct Shared {}

    #[local]
    struct Local {}

    #[init]
    fn init(_: init::Context) -> (Shared, Local, init::Monotonics) {
        rtic::pend(Interrupt::UART0);
        (Shared {}, Local {}, init::Monotonics::new(cortex_m::Peripherals::take().unwrap()))
    }
}
```

### 嵌入式 Async Runtime

新加入的 `embedded-async` crate 提供了一個輕量級的 async runtime，專為資源受限的嵌入式系統設計：

```rust
use embedded_async::runtime;

#[runtime]
async fn sensor_reading() {
    let mut sensor = Sensor::new(i2c_bus).await;
    let reading = sensor.read_temperature().await.unwrap();
    println!("Temperature: {}°C", reading);
}
```

## 效能優化

### 更快的編譯速度

Rust 2026 Edition 帶來了新一代的編譯器前端，改用基於 MLIR 的優化流程。根據官方基準測試：

- 增量編譯速度提升約 30%
- 全量編譯速度提升約 15%
- 記憶體使用減少約 20%

### Link-Time Optimization 增強

新版 LTO（Link-Time Optimization）支援更細粒度的優化控制：

```toml
[profile.release]
lto = "thin"  # 新增 thin LTO 選項
```

## 結語

Rust 2026 Edition 是一次意義重大的更新，不僅解決了長期困擾開發者的 async/await 痛點，還大幅強化了嵌入式開發體驗。隨著 AI 和 IoT 應用的蓬勃發展，Rust 在這些領域的競爭力將更加強勁。建議開發者開始在新專案中嘗試這些新特性，為未來做好準備。

---

**延伸閱讀**

- [Rust 2026 Edition RFC](https://github.com/rust-lang/rfcs/pulls?q=is%3Apr+label%3AE-rust-2026)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/)
- [Rust Embedded Book](https://doc.rust-lang.org/embedded book/)
