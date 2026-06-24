# 嵌入式 Rust

## no_std、embedded-hal、cortex-m（2017-2026）

### 前言

嵌入式系統是 Rust 最初設計的目標場景之一。與 Web 服務不同，嵌入式系統的資源極其有限——可能只有 16KB 的 RAM 和 64KB 的 Flash——沒有作業系統、沒有檔案系統、沒有堆分配。

### no_std：沒有標準庫的世界

Rust 的標準庫（std）假設有底層作業系統支援。在嵌入式系統中，這個假設不成立。因此 Rust 提供了一個「最小核心」——`core`：

```rust
// std 環境：有作業系統
use std::fs::File;
use std::thread;

// no_std 環境：沒有作業系統
#![no_std]  // 告訴編譯器不使用標準庫

// 只能使用 core:: 中的型別
use core::cell::RefCell;
use core::sync::atomic::{AtomicU32, Ordering};
```

**std 與 core 的差異**：

| 功能 | std | core | 說明 |
|------|-----|------|------|
| Vec、String | ✅ | ❌ | 需要堆分配器 |
| Box、Rc | ✅ | ❌ | 需要 alloc crate |
| 檔案 I/O | ✅ | ❌ | 需要 OS |
| 執行緒 | ✅ | ❌ | 需要 OS |
| 基本型別 | ✅ | ✅ | i32、f32 等 |
| 迭代器 | ✅ | ✅ | Iterator trait |
| Cell/RefCell | ✅ | ✅ | 內部可變性 |
| Atomic | ✅ | ✅ | 原子操作 |

### embedded-hal：硬體抽象層

embedded-hal 是 Rust 嵌入式生態的核心抽象，類似於 Linux 的 VFS 層——它定義了一組通用的硬體操作 trait：

```rust
// embedded-hal 的核心 trait
pub trait DigitalOutputPin {
    type Error;
    fn set_high(&mut self) -> Result<(), Self::Error>;
    fn set_low(&mut self) -> Result<(), Self::Error>;
}

pub trait DelayUs {
    fn delay_us(&mut self, us: u32);
}

pub trait I2cBus {
    type Error;
    fn read(&mut self, addr: u8, buf: &mut [u8]) -> Result<(), Self::Error>;
    fn write(&mut self, addr: u8, buf: &[u8]) -> Result<(), Self::Error>;
}
```

這種抽象層的設計讓 Rust 的嵌入式程式碼可以跨平台：

```rust
// 與平台無關的 LED 閃爍程式
fn blink_led(led: &mut impl DigitalOutputPin, delay: &mut impl DelayUs) {
    loop {
        led.set_high().ok();
        delay.delay_us(500_000); // 500ms
        led.set_low().ok();
        delay.delay_us(500_000);
    }
}

// 可以在任何平台上使用
// - STM32F4: impl DigitalOutputPin for PA5 { ... }
// - nRF52:   impl DigitalOutputPin for P0_13 { ... }
// - ESP32:   impl DigitalOutputPin for Gpio2 { ... }
```

### 實際的嵌入式專案結構

一個典型的 Rust 嵌入式專案：

```
my-embedded-project/
├── Cargo.toml          # 依賴 + target 設定
├── .cargo/config.toml  # 指定編譯目標
├── memory.x            # 記憶體佈局（連結器腳本）
├── build.rs            # 建置腳本
└── src/
    └── main.rs         # 主程式
```

**.cargo/config.toml**：

```toml
[target.thumbv7em-none-eabihf]
runner = "arm-none-eabi-gdb"
rustflags = ["-C", "link-arg=-Tmemory.x"]

[build]
target = "thumbv7em-none-eabihf"  # Cortex-M4F
```

**Cargo.toml**：

```toml
[dependencies]
cortex-m = "0.7"          # Cortex-M 核心支援
cortex-m-rt = "0.7"       # 啟動程式碼
embedded-hal = "1.0"      # 硬體抽象層
panic-halt = "0.2"        # panic 處理（停止）
```

### 完整的 LED 範例

```rust
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use stm32f4xx_hal::{pac, prelude::*};
use panic_halt as _;

#[entry]
fn main() -> ! {
    // 取得周邊存取權
    let dp = pac::Peripherals::take().unwrap();
    
    // 初始化 GPIO（PA5 通常連接到內建 LED）
    let gpioa = dp.GPIOA.split();
    let mut led = gpioa.pa5.into_push_pull_output();
    
    // 初始化延遲
    let mut delay = dp.TIM1.delay_us();
    
    loop {
        led.set_high().unwrap();
        delay.delay_ms(500);
        led.set_low().unwrap();
        delay.delay_ms(500);
    }
}
```

**關鍵點**：
- `#![no_std]`：不使用標準庫
- `#![no_main]`：自訂入口點（非 OS 的 main）
- `#[entry]`：RT 提供的入口宏
- `Peripherals::take()`：單例模式，確保安全存取硬體

### 嵌入式生態的成長

| 年份 | 里程碑 |
|------|--------|
| 2017 | embedded-hal 草案 |
| 2018 | cortex-m-quickstart 範本 |
| 2019 | 社群 HAL crate 大量出現 |
| 2020 | embedded-hal 1.0 |
| 2022 | async/await 在嵌入式中的應用 |
| 2024 | RTIC v3、Tock OS 3.0 |
| 2026 | Cortex-M85 支援、航空級認證 |

### 小結

Rust 的嵌入式生態已經從「能不能用」發展到「好不好用」。no_std + embedded-hal + 廠商 HAL crate 的組合讓 Rust 成為嵌入式開發的可行選擇，特別是在需要記憶體安全的場景。

與 C 相比，Rust 提供了：
- 編譯器保證的記憶體安全
- 現代語言特性（trait、泛型、模式匹配）
- 無 GC 的零成本抽象
- Send/Sync 保證的中斷安全

---

**下一步**：[裸機程式設計](focus2.md)

## 延伸閱讀

- [The Embedded Rust Book](https://www.google.com/search?q=embedded+Rust+book)
- [Discovery: Embedded Rust](https://www.google.com/search?q=discovery+embedded+Rust)
- [cortex-m-quickstart](https://www.google.com/search?q=cortex+m+quickstart+Rust)
