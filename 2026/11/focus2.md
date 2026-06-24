# GPIO 與中斷控制（2018–2026）

## 暫存器層級 GPIO 操作

MCU GPIO 的核心是記憶體映射暫存器。以 STM32F4 的 GPIOA 為例：

```rust
// 直接暫存器存取（透過 PAC crate）
let gpioa = unsafe { &*pac::GPIOA::ptr() };
gpioa.moder.modify(|_, w| w.moder5().output());
gpioa.bsrr.write(|w| w.bs5().set_bit());  // set high
```

Rust 的 PAC crate（由 svd2rust 生成）提供了型別安全的暫存器操作 API，防止對唯讀暫存器進行寫入。

## embedded-hal GPIO trait

embedded-hal 定義了跨平台的 GPIO trait：

```rust
use embedded_hal::digital::{OutputPin, InputPin};

impl OutputPin for GpioPin {
    fn set_high(&mut self) -> Result<(), Self::Error> { ... }
    fn set_low(&mut self) -> Result<(), Self::Error> { ... }
}
```

## NVIC 中斷控制器

ARM Cortex-M 的 NVIC 支援巢狀向量中斷：

```rust
use cortex_m::peripheral::NVIC;

let mut nvic = NVIC::new();
NVIC::unmask(pac::Interrupt::USART1);
// 中斷發生時，ISR 被自動呼叫
```

## 外部中斷（EXTI）

EXIT 允許 GPIO 引腳觸發中斷：

- 邊緣觸發（上升/下降/雙邊緣）
- 軟體觸發
- 事件輸出（不需 CPU 干預即可觸發其他周邊）

## 型別安全設計

Rust 嵌入式的一大優勢：不同 GPIO 模式用不同型別表示：

```rust
let pa5 = gpioa.split().5;           // 初始為 Input
let pa5 = pa5.into_push_pull_output(); // 型別變為 Output
// pa5.is_low(); // 編譯錯誤 — Output 不支援讀取
```

## 關鍵里程碑

- **2018**：embedded-hal 定義 GPIO trait
- **2019**：svd2rust 開始生成型別安全暫存器存取
- **2021**：cortex-m 提供 NVIC 安全封裝
- **2024**：async GPIO trait 加入 embedded-hal

## 延伸閱讀

- [STM32 GPIO 暫存器說明](https://www.google.com/search?q=STM32+GPIO+register+map)
- [ARM Cortex-M NVIC 文件](https://www.google.com/search?q=Cortex-M+NVIC+programming)
- [embedded-hal GPIO](https://www.google.com/search?q=embedded-hal+GPIO+trait)
