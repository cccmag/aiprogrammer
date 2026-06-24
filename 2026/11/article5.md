# 低功耗設計與最佳化 — 睡眠模式、喚醒源、堆疊分析

## 為什麼低功耗重要

在電池供電的物聯網裝置中，功耗直接決定了產品壽命。一顆 CR2032 鈕扣電池（225 mAh）如果系統耗電 100 µA，只能工作約 3 個月；若降低到 10 µA，則可工作近 3 年。

## Cortex-M 睡眠模式

ARM Cortex-M 提供四種主要的電源模式：

### Sleep Mode

最低延遲的睡眠模式，任何中斷都可以喚醒：

```rust
use cortex_m::asm;

// WFI (Wait For Interrupt)
asm::wfi();

// WFE (Wait For Event)
asm::wfe();
```

### Deep Sleep Mode

關閉 CPU 時脈，保留 SRAM 內容：

```rust
use cortex_m::peripheral::SCB;

SCB::set_sleepdeep();
asm::wfi();
```

### Standby Mode

最低功耗模式，僅保留 RTC 和備用暫存器：

```rust
// STM32 HAL 範例
pwr.standby_mode(true);
pwr.enter_standby();
```

## 喚醒源配置

典型 IoT 感測器節點的工作週期：

```rust
#[entry]
fn main() -> ! {
    configure_sensor();
    configure_radio();

    loop {
        // 進入睡眠模式
        configure_rtc_alarm(30);  // 30 秒後喚醒
        pwr.enter_standby();

        // 喚醒後從這裡繼續 (Standby 模式會重置)
        sensor.measure();
        radio.send(sensor.data());
    }
}
```

## 周邊時脈管理

未使用的周邊應該關閉時脈：

```rust
// 啟用時脈
rcc.apb2.enr().modify(|_, w| w.usart1en().enabled());

// 使用完畢後關閉
rcc.apb2.enr().modify(|_, w| w.usart1en().disabled());
```

Rust 的 RAII 模式可以自動管理時脈啟用/關閉。

## 堆疊使用量分析

堆疊溢位是嵌入式系統中最難以除錯的錯誤之一。Rust 提供靜態分析工具：

```bash
# 使用 cargo-call-stack
cargo install cargo-call-stack
cargo call-stack
```

輸出範例：

```
max stack usage: 384 bytes
  main: 128 bytes
  timer_handler (priority 2): 96 bytes
  uart_handler (priority 1): 72 bytes
  interrupt_nesting: +88 bytes
```

## 編譯期最佳化

```toml
[profile.release]
opt-level = "s"           # 針對體積最佳化
lto = "fat"               # 完整連結時最佳化
codegen-units = 1         # 禁用並行 codegen
strip = "symbols"         # 移除符號表
panic = "abort"           # panic 時直接中止（不 unwinding）
```

## 實戰案例：紐扣電池溫濕度感測器

| 元件 | 工作電流 | 睡眠電流 | 工作時間/週期 |
|------|---------|---------|-------------|
| STM32L0 | 1.5 mA | 0.3 µA | 10 ms / 60 s |
| BME280 | 1.0 mA | 0.1 µA | 5 ms / 60 s |
| LoRa (SX1276) | 20 mA | 0.2 µA | 100 ms / 60 s |

平均功耗：`(1.5+1.0+20)*0.115s/60s + (0.3+0.1+0.2)*59.885s/60s ≈ 43 µA`

理論電池壽命：`225 mAh / 43 µA ≈ 5200 小時 ≈ 7 個月`

## 延伸閱讀

- [ARM Cortex-M 低功耗模式指南](https://www.google.com/search?q=ARM+Cortex-M+low+power+modes+guide)
- [STM32L0 電源管理](https://www.google.com/search?q=STM32L0+power+management+Rust)
- [Rust embedded 最佳化技巧](https://www.google.com/search?q=Rust+embedded+optimization+binary+size)
