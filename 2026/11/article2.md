# GPIO 與中斷程式設計 — 暫存器操作、NVIC、外部中斷

## 暫存器層級的 GPIO 操作

在最底層，GPIO 是透過記憶體映射暫存器控制的。以 STM32F4 的 GPIOA 為例，每個 GPIO 埠有 10 個 32-bit 暫存器：

| 暫存器 | 功能 | 偏移 |
|--------|------|------|
| MODER | 模式（Input/Output/Alternate/Analog） | 0x00 |
| OTYPER | 輸出類型（Push-Pull/Open-Drain） | 0x04 |
| OSPEEDR | 輸出速度 | 0x08 |
| PUPDR | 上下拉電阻 | 0x0C |
| IDR | 輸入資料 | 0x10 |
| ODR | 輸出資料 | 0x14 |
| BSRR | 位元設定/重設 | 0x18 |
| LCKR | 鎖定 | 0x1C |
| AFRL/AFRH | 替代功能選擇 | 0x20/0x24 |

## PAC crate 的安全存取

svd2rust 生成的 PAC crate 在編譯期防止常見的暫存器操作錯誤：

```rust
// 設定 PA5 為輸出模式（型別安全寫法）
gpioa.moder.modify(|r, w| {
    w.moder5().bits(r.moder5().bits() & !0b11 | 0b01)
});
// 設定 BSRR 的 BS5 位元（set high）
gpioa.bsrr.write(|w| w.bs5().set_bit());
```

## 使用 embedded-hal 的高階 API

日常開發中不需要直接操作暫存器：

```rust
use stm32f4xx_hal::gpio::GpioExt;

let gpioa = dp.GPIOA.split();
let mut led = gpioa.pa5.into_push_pull_output();

// 完整中斷配置
let mut button = gpioa.pa0.into_pull_up_input();
button.make_interrupt_source(&mut syscfg);
button.enable_interrupt(&mut exti);
button.trigger_on_edge(&mut exti, Edge::Rising);

NVIC::unmask(Interrupt::EXTI0);
```

## NVIC 中斷控制器

ARM Cortex-M 的 NVIC 支援巢狀中斷：

```rust
use cortex_m::peripheral::NVIC;

// 啟用中斷
NVIC::unmask(Interrupt::EXTI0);

// 設定優先權
NVIC::set_priority(Interrupt::EXTI0, 1);

// 在全球 ISR 中處理
#[interrupt]
fn EXTI0() {
    // 不需鎖 — 這個中斷無法被自身搶佔
    static mut pressed: bool = false;
    *pressed = !*pressed;
}
```

## 中斷 vs 輪詢

輪詢模式：

```rust
loop {
    if button.is_low() {
        led.set_high();
    } else {
        led.set_low();
    }
}
```

中斷模式：

```rust
static SHOULD_TOGGLE: AtomicBool = AtomicBool::new(false);

#[interrupt]
fn EXTI0() {
    SHOULD_TOGGLE.store(true, Ordering::SeqCst);
}

#[entry]
fn main() -> ! {
    loop {
        if SHOULD_TOGGLE.swap(false, Ordering::SeqCst) {
            led.toggle();
        }
    }
}
```

中斷模式讓 CPU 在等待按鍵時可以進入睡眠或執行其他任務。

## 型別系統防止錯誤

Rust 的型別系統在 GPIO 上提供了 C 語言無法比擬的安全性：

```rust
// 編譯器阻止你在 Input pin 上 set_high()
let led: PA5<Output<PushPull>> = gpioa.pa5.into_push_pull_output();
// led.is_low(); // 編譯錯誤！Output pin 沒有 is_low()

let btn: PA0<Input<PullUp>> = gpioa.pa0.into_pull_up_input();
// btn.set_high(); // 編譯錯誤！Input pin 沒有 set_high()
```

## 延伸閱讀

- [ARM Cortex-M NVIC 程式設計](https://www.google.com/search?q=ARM+Cortex-M+NVIC+programming+guide)
- [STM32 GPIO 暫存器說明](https://www.google.com/search?q=STM32+GPIO+registers+datasheet)
- [embedded-hal digital traits](https://www.google.com/search?q=embedded-hal+digital+pin+trait)
