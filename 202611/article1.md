# 嵌入式 Rust 入門指南 — no_std、cortex-m-rt、embedded-hal 從零開始

## 前言

如果你寫過 C 語言的嵌入式程式，你會懷念它的簡單——但也會痛恨它讓你手動管理每一個記憶體細節。Rust 給了你一條不同的路：編譯器在你知道出錯之前就阻止了你。本篇文章從零開始建立嵌入式 Rust 開發環境。

## 建立專案

```bash
cargo new --bin blinky
cd blinky
```

編輯 `Cargo.toml` 加入相依套件：

```toml
[dependencies]
cortex-m = "0.7"
cortex-m-rt = "0.7"
embedded-hal = "1.0"

# 選擇 MCU 的 PAC crate
[dependencies.stm32f4xx-hal]
features = ["rt"]
version = "0.18"
```

## no_std 與 no_main

嵌入式程式沒有作業系統，因此不能使用標準庫：

```rust
#![no_std]
#![no_main]

use cortex_m_rt::entry;

#[entry]
fn main() -> ! {
    loop {}
}
```

`#![no_main]` 告訴 Rust 我們不使用標準的 main 簽名。`#[entry]` 是 cortex-m-rt 提供的屬性，標記程式的進入點。

## panic_handler

沒有標準庫就沒有預設的 panic 行為：

```rust
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}
```

在真實專案中，建議使用 `panic-halt`（無操作）、`panic-semihosting`（輸出到除錯器）或 `panic-itm`（輸出到 ITM 追蹤）。

## GPIO Blinky 完整範例

```rust
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use stm32f4xx_hal::{
    prelude::*,
    pac,
    gpio::gpioa::Parts,
};

#[entry]
fn main() -> ! {
    let dp = pac::Peripherals::take().unwrap();
    let rcc = dp.RCC.constrain();
    let clocks = rcc.cfgr.sysclk(48.MHz()).freeze();

    let gpioa = dp.GPIOA.split();
    let mut led = gpioa.pa5.into_push_pull_output();

    loop {
        led.set_high();
        cortex_m::asm::delay(8_000_000);
        led.set_low();
        cortex_m::asm::delay(8_000_000);
    }
}
```

## embedded-hal 抽象層

embedded-hal 定義了跨平台的硬體 abstract trait。換成不同的 MCU 只需更換 HAL crate：

```rust
use embedded_hal::digital::OutputPin;

fn blink<T: OutputPin>(led: &mut T, delay: u32) {
    led.set_high().unwrap();
    cortex_m::asm::delay(delay);
    led.set_low().unwrap();
    cortex_m::asm::delay(delay);
}
```

## 編譯與執行

```bash
# 安裝目標
rustup target add thumbv7em-none-eabihf

# 建置
cargo build --target thumbv7em-none-eabihf --release

# 燒錄（使用 probe-rs）
probe-rs run target/thumbv7em-none-eabihf/release/blinky
```

## 關鍵概念回顧

1. **no_std**：不使用作業系統依賴的標準庫，僅用 core crate
2. **cortex-m-rt**：提供啟動碼、中斷向量表、記憶體初始化
3. **embedded-hal**：抽象的硬體周邊 trait，實現跨平台可攜性
4. **PAC → HAL → BSP**：三層架構從暫存器到開發板層層抽象

## 延伸閱讀

- [The Embedded Rust Book](https://www.google.com/search?q=embedded+Rust+book)
- [cortex-m-rt 快速入門](https://www.google.com/search?q=cortex-m-rt+Rust)
- [STM32F4xx-HAL](https://www.google.com/search?q=stm32f4xx-hal+Rust)
