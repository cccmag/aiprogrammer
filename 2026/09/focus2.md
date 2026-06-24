# 裸機程式設計

## 從零啟動、中斷向量表、記憶體映射（2018-2026）

### 前言

「裸機」（bare-metal）程式設計是最底層的系統程式設計——沒有作業系統、沒有執行時期、沒有標準庫。程式碼直接執行在硬體上，從 CPU reset 的第一條指令開始。

### 啟動流程

一個典型的 ARM Cortex-M 啟動流程：

```
硬體 Reset
  ┊
CPU 從 0x0000_0000 讀取初始堆疊指標 (MSP)
  ┊
CPU 從 0x0000_0004 讀取 Reset Handler 位址
  ┊
執行 Reset Handler
  ┊
初始化資料段 (.data) 和 BSS 段 (.bss)
  ┊
呼叫 main()
```

在 Rust 中，這個流程由 `cortex-m-rt` crate 處理：

```rust
// cortex-m-rt 自動生成：
// 1. 中斷向量表
// 2. Reset Handler
// 3. 記憶體初始化

// 使用者只需要：
#[entry]
fn main() -> ! {
    loop {}
}
```

### 中斷向量表

中斷向量表是裸機程式的核心資料結構——它告訴 CPU 每個中斷發生時該跳轉到哪裡：

```rust
// cortex-m-rt 生成的中斷向量表（簡化）
#[link_section = ".vector_table.exceptions"]
#[used]
static EXCEPTIONS: [unsafe extern "C" fn(); 16] = [
    _start,             // 0x00: Stack Pointer (initial)
    ResetTrampoline,    // 0x04: Reset
    NMI,                // 0x08: NMI
    HardFaultT,         // 0x0C: Hard Fault
    // ...
];
```

### 記憶體映射暫存器（MMIO）

系統程式設計的核心操作之一——透過特定記憶體位址來控制硬體：

```rust
// 典型的 GPIO 暫存器定義（沒有使用任何 crate）
#[repr(C)]
struct GpioRegisters {
    moder: u32,   // 0x00: Mode register
    otyper: u32,  // 0x04: Output type
    ospeedr: u32, // 0x08: Output speed
    pupdr: u32,   // 0x0C: Pull-up/pull-down
    idr: u32,     // 0x10: Input data
    odr: u32,     // 0x14: Output data
    bsrr: u32,    // 0x18: Bit set/reset
}

const GPIOA_BASE: usize = 0x4002_0000;

// 存取記憶體映射暫存器需要 unsafe！
fn set_gpio_high(pin: u8) {
    let gpio = unsafe { &*(GPIOA_BASE as *const GpioRegisters) };
    // BSRR: 低 16 位元設定位元
    unsafe { core::ptr::write_volatile(&gpio.bsrr as *const u32 as *mut u32, 1 << pin) };
}
```

### 安全的 MMIO 封裝

裸機程式設計的最佳實踐是將 MMIO 操作封裝在安全的 Rust 抽象中：

```rust
/// 安全的 GPIO Pin 抽象
pub struct GpioPin {
    pin: u8,
}

impl GpioPin {
    pub fn new(pin: u8) -> Self {
        // 初始化暫存器（需要 unsafe）
        let gpio = unsafe { &*GPIO_PTR };
        unsafe {
            // 設定為輸出模式
            gpio.moder.write_volatile(gpio.moder.read_volatile() | (0b01 << (pin * 2)));
        }
        GpioPin { pin }
    }
    
    pub fn set_high(&mut self) {
        let gpio = unsafe { &*GPIO_PTR };
        unsafe {
            gpio.bsrr.write_volatile(1 << self.pin);
        }
    }
    
    pub fn set_low(&mut self) {
        let gpio = unsafe { &*GPIO_PTR };
        unsafe {
            gpio.bsrr.write_volatile(1 << (self.pin + 16));
        }
    }
}

// 使用時不需要 unsafe！
fn blink() {
    let mut led = GpioPin::new(5);
    loop {
        led.set_high();
        delay(500);
        led.set_low();
        delay(500);
    }
}
```

### panic 處理

在裸機環境中，panic 的處理方式與有 OS 的環境不同：

```rust
// 方式 1：暫停
use panic_halt as _;
// panic 時無限迴圈

// 方式 2：印出訊息（需要 UART）
use panic_semihosting as _;
// panic 時透過除錯器輸出訊息

// 方式 3：重置
use panic_reset as _;
// panic 時重置系統
```

### 異常處理

```rust
// 自訂 Hard Fault Handler
#[exception]
fn HardFault(frame: &cortex_m::peripheral::SCB::HardFaultRegisters) {
    // 記錄錯誤資訊
    // ...（可能需要 UART 輸出）
    loop {}  // 停止
}
```

### 裸機程式的完整範例

```rust
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use panic_halt as _;

// 模擬的 UART 暫存器
const UART_BASE: usize = 0x4000_1000;

#[repr(C)]
struct UartRegs {
    dr: u32,     // 資料暫存器
    sr: u32,     // 狀態暫存器
}

fn uart_send(c: u8) {
    let uart = unsafe { &* (UART_BASE as *const UartRegs) };
    // 等待傳送緩衝區空閒
    while unsafe { uart.sr.read_volatile() } & (1 << 7) == 0 {}
    unsafe { uart.dr.write_volatile(c as u32) };
}

fn uart_print(s: &str) {
    for c in s.bytes() {
        uart_send(c);
    }
}

#[entry]
fn main() -> ! {
    uart_print("Hello from bare-metal Rust!\n");
    
    loop {
        uart_print(".");
        delay(1_000_000);  // 簡單的軟體延遲
    }
}

fn delay(cycles: u32) {
    // 軟體延遲（不精確但簡單）
    for _ in 0..cycles {
        unsafe { core::ptr::read_volatile(&0xE000_E010 as *const u32) };
    }
}
```

### 常見的裸機挑戰

**1. 中斷優先權**：
```rust
// 設定中斷優先權
unsafe { cortex_m::peripheral::NVIC::unmask(Interrupt::USART1) };
NVIC::set_priority(Interrupt::USART1, 2);
```

**2. 臨界區段**：
```rust
// 禁用中斷（進入臨界區段）
cortex_m::interrupt::free(|_| {
    // 在這個閉包內，中斷被禁用
    // 安全地存取共用資料
});
```

**3. 單例模式**：
```rust
// 使用 take() 確保只能取得一次
let dp = pac::Peripherals::take().unwrap();
// 第二次呼叫會 panic
```

### 小結

裸機程式設計是系統程式設計的本源。Rust 在裸機領域的支援讓開發者可以在沒有作業系統的情況下，享受記憶體安全、零成本抽象和現代語言特性。

關鍵文件：
- **cortex-m-rt**：啟動程式碼和中斷向量表
- **cortex-m**：暫存器存取和核心功能
- **embedded-hal**：硬體抽象層

---

**下一步**：[unsafe Rust](focus3.md)

## 延伸閱讀

- [Bare-metal Rust](https://www.google.com/search?q=bare+metal+Rust)
- [Writing an OS in Rust](https://www.google.com/search?q=writing+an+OS+in+Rust)
- [Cortex-M 程式設計](https://www.google.com/search?q=Cortex-M+Rust+programming)
