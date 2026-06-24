# 定時器/PWM/ADC（2019–2026）

## SysTick

ARM Cortex-M 內建 SysTick 定時器，提供精確的系統時基：

```rust
use cortex_m::peripheral::SYST;

let mut syst = SYST::new();
syst.set_clock_source(SystClkSource::Core);
syst.set_reload(72_000_000);  // 1 秒 (72 MHz)
syst.enable_interrupt();
syst.enable_counter();
```

SysTick 通常用作嵌入式 RTOS 的時基中斷。

## 通用定時器

通用定時器（TIMx）比 SysTick 更靈活：

| 功能 | Basic TIM | General TIM | Advanced TIM |
|------|-----------|-------------|-------------|
| 計時 | ✓ | ✓ | ✓ |
| PWM | ✗ | ✓ | ✓ |
| 輸入捕捉 | ✗ | ✓ | ✓ |
| 互補輸出 | ✗ | ✗ | ✓ |
| 煞車功能 | ✗ | ✗ | ✓ |

## PWM 輸出

PWM（脈波寬度調變）用於控制 LED 亮度、舵機角度、馬達轉速：

```rust
let pwm = pwm_channel.into_pwm(50_000.Hz());  // 50kHz PWM
pwm.set_duty(500);   // 設定佔空比
pwm.enable();
```

舵機控制需要 50Hz（20ms 週期）的 PWM 訊號，脈衝寬度 1–2ms 對應 0–180 度。

## ADC 取樣

ADC（類比數位轉換器）將類比電壓轉換為數位值：

```rust
let adc = Adc::new(adc_pin);
let value: u16 = adc.read(&mut adc_pin);  // 回傳 0-4095 (12-bit)
```

ADC 常見配置選項：解析度（8/10/12/16-bit）、取樣時間、連續模式、觸發源。

## DMA 加速

DMA 可以在沒有 CPU 干預下自動搬運 ADC 資料：

```rust
// 設定 ADC + DMA：連續掃描 4 通道
adc.configure_dma(dma_channel, buffer, 4);
adc.start_continuous_conversion();
// DMA 自動將轉換結果填入 buffer，完成後觸發中斷
```

DMA 特別適合高取樣率的感測器資料採集（如音訊、震動分析）。

## 延伸閱讀

- [STM32 定時器概述](https://www.google.com/search?q=STM32+timer+PWM+ADC)
- [ARM SysTick 計時器](https://www.google.com/search?q=ARM+Cortex-M+SysTick+timer)
- [Rust embedded DMA](https://www.google.com/search?q=Rust+embedded+DMA+ADC)
