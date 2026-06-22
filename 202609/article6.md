# no_std Rust：沒有標準庫的 Rust 程式設計

## 1. 什麼是 no_std 與為什麼需要它

Rust 的標準庫（std）提供了我們習以為常的各種抽象：`Vec`、`HashMap`、`File`、`println!`、執行緒、網路 socket 等等。但這些功能依賴於底層作業系統的支援——記憶體分配器、檔案系統、執行緒排程器，缺一不可。

然而，並非所有 Rust 程式都跑在完整的作業系統之上。微控制器（MCU）、韌體、核心模組、UEFI 開機載入程式——這些環境沒有 OS，沒有 libc，甚至沒有堆記憶體。在這些場景下，標準庫根本無法編譯。

這就是 `no_std` 登場的時候。在 Rust 中，只要在 crate 根加上 `#![no_std]`，就能告訴編譯器：「我不要標準庫，請只給我語言核心與基礎型別。」這份克制換來的是極小的二進位體積、零開銷的抽象，以及能在 bare-metal 環境中運行的能力。

`no_std` 不是 Rust 的子語言，而是 Rust 的核心。它強迫程式設計師直面資源的本質——沒有自動的 GC、沒有隱藏的記憶體分配、沒有魔術。

## 2. `#![no_std]` 與核心 crate（core、alloc）

當你宣告 `#![no_std]` 時，`std` 被拒於門外，但 `core` 仍然可用。`core` crate 是標準庫中與作業系統無關的子集，包含：

- 基本型別：`Option`、`Result`、`Iterator`、`Clone`、`Copy`
- 原子操作與記憶體操作：`core::sync::atomic`、`core::ptr`、`core::mem`
- 基礎 trait：`From`、`Into`、`Display`、`Debug`、`PartialEq`
- 切片、陣列、`str` 的操作
- `#[panic_handler]` 的基礎設施

```rust
// 最簡單的 no_std 程式
#![no_std]

#[panic_handler]
fn panic(_info: &core::panic::PanickInfo) -> ! {
    loop {}
}
```

如果程式需要堆記憶體（例如動態集合），可以選擇性地啟用 `alloc` crate。`alloc` 提供了 `Box`、`Vec`、`String`、`Arc` 等型別，但它要求你提供一個全域的記憶體分配器：

```rust
// 啟用 alloc
#![no_std]

extern crate alloc;

use alloc::vec::Vec;
use alloc::string::String;

#[global_allocator]
static ALLOCATOR: MyAllocator = MyAllocator;
```

把標準庫想像成一個三層蛋糕：`core` 在最底層，`alloc` 在中間，`std` 在最上層。`no_std` 只是切掉了最上面那一層——而你可以選擇性地吃中間那一塊。

## 3. 沒有標準庫的世界：沒有 Vec、沒有 HashMap、沒有 IO

在純 `no_std` 環境中（不使用 `alloc`），你沒有：

- **動態集合**：沒有 `Vec`、`HashMap`、`String`。你只能使用固定大小的陣列、切片、以及 `core` 提供的 `Cell`、`RefCell`（僅單執行緒）。
- **檔案 IO**：沒有 `File`、`Read`、`Write`。這些 trait 在 `std` 中定義，依靠檔案描述子。
- **標準輸出**：沒有 `println!`。如果你想把字元送到序列埠或 JTAG，你必須自己實作輸出函式，然後用 `write!` 巨集來替代。
- **時間與執行緒**：沒有 `Instant`、`SystemTime`、`Thread`。

這聽起來很可怕，但實際上嵌入式開發者每天都在做這件事。策略很簡單：**靜態分配優先**。

```rust
// 在 no_std + no_alloc 下，用固定陣列代替 Vec
let mut buffer: [u8; 256] = [0; 256];
let mut len = 0;

fn push_byte(buf: &mut [u8; 256], len: &mut usize, byte: u8) -> Result<(), ()> {
    if *len >= buf.len() {
        return Err(()); // 溢位，就像 Vec 的 push 失敗時
    }
    buf[*len] = byte;
    *len += 1;
    Ok(())
}
```

對於更複雜的場景，可以選用 `heapless` 生態系中的固定容量資料結構（後文詳述）。

## 4. 如何提供自訂的 panic_handler 與 alloc_error_handler

在 `no_std` 環境中，`panic!` 不會觸發標準庫的展開邏輯（因為沒有棧展開）。你必須自己定義 panic 行為：

```rust
// 最常見的做法：無窮迴圈或觸發斷點
#[panic_handler]
fn panic(_info: &core::panic::PanickInfo) -> ! {
    // Cortex-M 的 BKPT 指令
    #[cfg(target_arch = "arm")]
    core::arch::asm!("bkpt");
    loop {}
}
```

如果你使用 `alloc` crate，還需要提供 `alloc_error_handler`：

```rust
#![feature(alloc_error_handler)]

#[alloc_error_handler]
fn alloc_error(layout: core::alloc::Layout) -> ! {
    // 記憶體不足時的處理
    loop {}
}
```

> **注意**：截至 Rust 2024 edition，`alloc_error_handler` 仍然是 unstable 功能，需啟用 `#![feature(alloc_error_handler)]`。在 stable Rust 中，可以依賴全域分配器自行處理錯誤。

比較完整的嵌入式專案通常會引入 `panic-halt` 或 `panic-abort` 這類輔助 crate：

```toml
[dependencies]
panic-halt = "0.2"
```

這些 crate 幫你寫好了 `#[panic_handler]`，只要引入就能直接使用。

## 5. 使用 embedded-hal 編寫平台無關的驅動程式

`embedded-hal` 是 Rust 嵌入式生態系的關鍵抽象層。它定義了一組硬體抽象 trait，讓驅動程式可以與具體 MCU 解耦：

- **數位 I/O**：`OutputPin`、`InputPin`、`ToggleableOutputPin`
- **通訊協定**：`I2c`、`Spi`、`Serial`（read/write）
- **延遲**：`blocking::delay::DelayMs`、`DelayUs`

寫驅動的人只需要依賴 `embedded-hal` 的 trait，不需要知道最終跑在 STM32 還是 nRF52840 上。

```rust
use embedded_hal::digital::v2::OutputPin;

pub struct Led<P>
where
    P: OutputPin,
{
    pin: P,
}

impl<P> Led<P>
where
    P: OutputPin,
{
    pub fn new(pin: P) -> Self {
        Self { pin }
    }

    pub fn on(&mut self) -> Result<(), P::Error> {
        self.pin.set_high()
    }

    pub fn off(&mut self) -> Result<(), P::Error> {
        self.pin.set_low()
    }
}
```

這個 `Led` 結構體完全不知道底層是哪顆晶片，它只要求 `P` 實現了 `OutputPin` trait——這就是平台無關的精髓。

## 6. 實際案例：編寫一個 no_std 的 LED 驅動

讓我們用完整的程式碼展示一個真實的 `no_std` LED 驅動，並加上簡易的 PWM 呼吸燈效果。

```rust
//! 平台無關的 RGB LED 驅動（no_std）
#![no_std]

use embedded_hal::digital::v2::OutputPin;
use embedded_hal::PwmPin;

/// 一顆普通的單色 LED
pub struct Led<P: OutputPin> {
    pin: P,
}

impl<P: OutputPin> Led<P> {
    pub fn new(pin: P) -> Self {
        Self { pin }
    }

    pub fn on(&mut self) -> Result<(), P::Error> {
        self.pin.set_high()
    }

    pub fn off(&mut self) -> Result<(), P::Error> {
        self.pin.set_low()
    }

    pub fn toggle(&mut self) -> Result<(), P::Error> {
        self.pin.toggle()
    }

    /// 簡單的延遲閃爍（Timer 需要 platform-specific，此處僅示意）
    pub fn blink(&mut self, delay_ms: u16) -> Result<(), P::Error> {
        self.on()?;
        // 實際延遲需依賴 platform bsp 或 cortex_m::asm::delay
        self.off()
    }
}

/// 支援 PWM 調光的 LED
pub struct PwmLed<P: PwmPin> {
    pwm: P,
}

impl<P: PwmPin> PwmLed<P> {
    pub fn new(pwm: P) -> Self {
        Self { pwm }
    }

    /// 設定亮度（0.0 ~ 1.0）
    pub fn set_brightness(&mut self, level: f32) {
        let max = self.pwm.get_max_duty();
        let duty = (max as f32 * level.clamp(0.0, 1.0)) as u16;
        self.pwm.set_duty(duty);
    }

    /// 呼吸燈效果
    pub fn breathe(&mut self, steps: u32) {
        for i in 0..steps {
            let t = i as f32 / steps as f32;
            // 使用正弦曲線讓呼吸更平滑
            let level = (t * core::f32::consts::PI * 2.0).sin() * 0.5 + 0.5;
            self.set_brightness(level);
        }
    }
}
```

在具體的 MCU 上使用這個驅動：

```rust
// 以 STM32F4 為例，使用 stm32f4xx-hal
use stm32f4xx_hal::gpio::{gpioc::PC13, Output, PushPull};
use stm32f4xx_hal::pac::Peripherals;

let dp = Peripherals::take().unwrap();
let gpioc = dp.GPIOC.split();
let pin = gpioc.pc13.into_push_pull_output();
let mut led = Led::new(pin);
led.on().unwrap();
```

## 7. no_std 生態系總覽

Rust 的 `no_std` 生態系已經相當成熟，以下是幾個關鍵類別：

### 硬體抽象層

| crate | 用途 |
|-------|------|
| `embedded-hal` | 定義標準的硬體抽象 trait |
| `cortex-m` | Cortex-M 架構的低階操作 |
| `riscv` | RISC-V 架構的暫存器操作 |
| `stm32f4xx-hal` / `nrf52840-hal` | 具體 MCU 的 HAL 實作 |

### 資料結構

| crate | 用途 |
|-------|------|
| `heapless` | 固定容量的 `Vec`、`String`、`HashMap`、`LinearMap`（無 alloc） |
| `arrayvec` | 基於固定陣列的 `ArrayVec` |
| `tinyvec` | 另一種固定容量 Vec 實作 |
| `linked_list` | 無分配的鏈結串列 |

### 非同步與中斷

| crate | 用途 |
|-------|------|
| `nb` | 非阻塞 I/O 的抽象（基於 poll） |
| `embassy` | 現代 async/await 嵌入式框架 |
| `cortex-m-rt` | Cortex-M 的中斷向量表與啟動程式碼 |

### 實用工具

| crate | 用途 |
|-------|------|
| `panic-halt` | 無窮迴圈的 panic handler |
| `panic-abort` | 直接 abort 的 panic handler |
| `panic-semihosting` | 透過 semihosting 輸出 panic 訊息 |
| `cortex-m-log` | 基於 `log` crate 的嵌入式日誌 |
| `defmt` | 高效率的嵌入式格式化日誌 |

### 從範例出發

實際專案建議從 `cortex-m-quickstart` 或 `embassy` 的範本開始：

```bash
cargo generate --git https://github.com/rust-embedded/cortex-m-quickstart
```

這個範本已經配好 `memory.x`、`cargo config`、以及完整的 `no_std` 建置鏈。

## 結語

`no_std` 不是閹割版的 Rust，而是回歸本質的 Rust。當你移除標準庫的便利時，留下的不是殘缺，而是對硬體完全的掌控。從小小的 LED 驅動到完整的 RTOS，Rust 的 `no_std` 生態系讓嵌入式開發者終於能享受零成本抽象與記憶體安全兼得的美好。

下次當你翻開一顆 MCU 的 datasheet 時，試試用 `#![no_std]` 開始你的專案——你會發現，少了標準庫的世界，其實比你想像的更寬廣。
