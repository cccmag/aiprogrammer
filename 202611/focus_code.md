# mini-embedded：嵌入式系統模式模擬

## 概述

mini-embedded 是一個使用者空間的嵌入式開發模式展示專案。真實的嵌入式 Rust 開發需要交叉編譯工具鏈和目標硬體，我們用模擬的方式展示嵌入式開發的核心抽象：

1. **GPIO 引腳控制** — 輸出模式（LED）、輸入模式（按鈕）
2. **UART 通訊** — 輪詢模式與中斷模式
3. **硬體定時器** — 週期中斷與溢位回呼
4. **中斷控制器（NVIC）** — IRQ 啟用、掛起、服務
5. **周邊管理** — 統一的 Peripherals 結構

## 核心概念

### 1. GPIO 引腳抽象

嵌入式開發中最基本的操作——控制一個引腳的電位高低：

```rust
struct GpioPin {
    mode: PinMode,   // Input / Output / Alternate / Analog
    state: PinState, // Low / High
}

impl GpioPin {
    fn set_mode(&mut self, mode: PinMode);
    fn set_high(&mut self);
    fn set_low(&mut self);
    fn read(&self) -> PinState;
}
```

模擬中，嘗試在非輸出模式下 `set_high()` 會 panic——這反映了真實 MCU 的硬體行為。在真實的 embedded-hal 中，這種錯誤透過型別系統在編譯期防止：`Output<PushPull>` 和 `Input<Floating>` 是不同的型別。

### 2. UART 輪詢模式

最簡單的通訊方式——CPU 忙等直到資料收發完成：

```rust
let mut uart = SimUart::new(115_200);
uart.write_str("Hello from Rust!\n");
let byte = uart.read_byte();  // 如果沒有資料回傳 None
```

輪詢模式簡單可靠，但在等待過程中浪費 CPU 週期。

### 3. UART 中斷模式

更高效的方式——硬體在收發完成時觸發中斷：

```rust
uart.set_mode(UartMode::Interrupt);
nvic.enable(5);  // USART1 IRQ
```

中斷處理程式在 IRQ 觸發時被呼叫，CPU 在等待期間可以執行其他任務。

### 4. 定時器中斷

硬體定時器是嵌入式系統的時間基礎：

```rust
let mut timer = SimTimer::new(1000);  // 1 秒週期
timer.on_overflow(|| { println!("timer fired!"); });
timer.start();
timer.tick(500);  // 經過 500ms，尚未溢位
timer.tick(600);  // 溢位觸發！
```

真實硬體中，定時器溢位會觸發中斷，CPU 可以在 ISR 中執行定期任務。

### 5. NVIC 中斷控制器

ARM Cortex-M 的巢狀向量中斷控制器（NVIC）管理所有中斷：

| 操作 | 模擬 | 真實 Cortex-M |
|------|------|--------------|
| 啟用中斷 | `nvic.enable(irq)` | `NVIC::unmask(Interrupt)` |
| 掛起中斷 | `nvic.pend(irq)` | 硬體自動或 `NVIC::pend()` |
| 服務中斷 | `nvic.service_next()` | ISR 自動被 CPU 呼叫 |
| 優先權 | FIFO 佇列 | 巢狀優先權搶佔 |

### 6. 周邊存取模式

真實嵌入式 Rust 中，所有周邊通常透過一個 `Peripherals` 結構統一管理：

```rust
let peri = Peripherals::new();
let led = peri.gpioa.pin(5).borrow_mut();
let uart = peri.uart1.borrow_mut();
```

在真實的 `cortex-m` crate 中，`Peripherals::take()` 保證每個周邊只能被取用一次（所有權單一性）。

## embedded-hal trait 對照

模擬中的操作對應到 embedded-hal 的標準 trait：

| 模擬 | embedded-hal trait |
|------|-------------------|
| `set_high()` / `set_low()` | `OutputPin` |
| `read()` | `InputPin` |
| `write_byte()` / `read_byte()` | `serial::Write` / `serial::Read` |
| 中斷 | `serial::Events` |

## 測試

```
running 10 tests
test tests::test_gpio_input ... ok
test tests::test_gpio_output ... ok
test tests::test_gpio_write_input_panics ... ok
test tests::test_all_peripherals ... ok
test tests::test_nvic_disabled_irq_not_pended ... ok
test tests::test_nvic_irq ... ok
test tests::test_pin_out_of_range ... ok
test tests::test_timer_overflow ... ok
test tests::test_uart_polling ... ok
test tests::test_uart_write ... ok
test result: ok. 10 passed; 0 failed
```

## 執行結果

```
=== mini-embedded: Embedded System Patterns Demo ===

--- GPIO: blinking LED ---
  [GPIO]  mode -> Output
  [GPIO]  set HIGH
  [GPIO]  set LOW

--- GPIO: reading button ---
  [GPIO]  mode -> Input

--- UART: polling write ---
  [UART]  TX: 0x48 ('H')
  [UART]  TX: 0x65 ('e')
  [UART]  TX: 0x6c ('l')
  [UART]  TX: 0x6c ('l')
  [UART]  TX: 0x6f ('o')
  [UART]  TX: 0x20 (' ')
  [UART]  TX: 0x66 ('f')
  [UART]  TX: 0x72 ('r')
  [UART]  TX: 0x6f ('o')
  [UART]  TX: 0x6d ('m')
  [UART]  TX: 0x20 (' ')
  [UART]  TX: 0x52 ('R')
  [UART]  TX: 0x75 ('u')
  [UART]  TX: 0x73 ('s')
  [UART]  TX: 0x74 ('t')
  [UART]  TX: 0x21 ('!')
  [UART]  TX: 0x0a ('
')

--- UART: polling read ---
  [UART]  RX: 0x41 ('A')
  [UART]  RX: 0x42 ('B')
  [UART]  RX: 0x43 ('C')

--- UART: interrupt mode ---
  [UART]  mode -> Interrupt

--- Timer: periodic interrupt ---
  [TIMER] started (period: 1000ms)
  [TIMER] overflow!

--- NVIC: interrupt handling ---
  [NVIC]  IRQ5 enabled
  [NVIC]  IRQ5 pended
  [NVIC]  IRQ5 pended
  [ISR]    servicing IRQ5
  [ISR]    servicing IRQ5

--- System info ---
  clock:   72 MHz (simulated)
  flash:   512 KiB
  sram:    128 KiB
  uart:    115200 baud
  timer:   1000 ms period

=== demo completed ===
```

## mini-embedded 教會我們的事

### 1. 抽象是嵌入式開發的核心

GPIO、UART、定時器——這些底層硬體的複雜性透過層層抽象被隱藏。`embedded-hal` 讓同一份應用程式碼可以在 STM32、ESP32、RP2040 上運行。

### 2. 型別安全不是開銷

在 C 中設定 GPIO 通常寫 `GPIOA->ODR |= (1 << 5)`——一個打字錯誤可能燒壞硬體。Rust 的型別系統在編譯期就確保了正確的方向和引腳號。

### 3. 中斷安全需要設計

嵌入式系統中，中斷可以在任何時刻發生。Rust 的 `Send` / `Sync` 特性和 RTIC 的資源模型，在編譯期保證了中斷安全，無需執行期鎖定負擔。

### 4. no_std 不代表功能不足

雖然不能使用標準庫，但 `core` 和 `heapless` 提供了充足的替代方案。Rust 的迭代器、模式匹配、trait 系統在嵌入式環境中同樣有效。

---

## 延伸閱讀

- [完整程式碼](_code/src/main.rs)
- [The Embedded Rust Book](https://www.google.com/search?q=embedded+Rust+book)
- [embedded-hal](https://www.google.com/search?q=embedded-hal+Rust)
- [RTIC 框架入門](https://www.google.com/search?q=RTIC+Rust+introduction)
- [cortex-m-rt 快速入門](https://www.google.com/search?q=cortex-m-rt+Rust)
