# Rust 嵌入式生態深度解析 — embedded-hal、HAL crate、BSP

## 三層架構總覽

Rust 嵌入式生態將驅動程式分為清晰的層次：

```
應用程式碼（你的邏輯）
    ↑ embedded-hal trait
HAL crate（晶片系列級實作）
    ↑ PAC 安全介面
PAC crate（svd2rust 生成）
    ↑ 記憶體映射
MCU 硬體暫存器
```

## PAC：Peripheral Access Crate

PAC 是最底層的抽象，由 `svd2rust` 工具從晶片廠商提供的 SVD（System View Description）檔案自動生成。

```bash
svd2rust -i STM32F407.svd --target cortex-m
```

生成的程式碼特點：

```rust
// 型別安全暫存器存取
pac.GPIOA.moder.modify(|_, w| w.moder5().output());
// 錯誤：w.moder6().bits(0b11) 如果該欄位只接受 0b00/0b01 則編譯錯誤
```

PAC 層提供了對硬體最直接的存取路徑，同時透過 Rust 型別系統防止許多常見錯誤。

## HAL：Hardware Abstraction Layer

HAL crate 基於 PAC 實作 `embedded-hal` trait：

```rust
use embedded_hal::digital::OutputPin;

impl OutputPin for gpioa::PA5<Output<PushPull>> {
    type Error = Infallible;

    fn set_high(&mut self) -> Result<(), Self::Error> {
        self.regs.bsrr.write(|w| w.bs5().set_bit());
        Ok(())
    }

    fn set_low(&mut self) -> Result<(), Self::Error> {
        self.regs.bsrr.write(|w| w.br5().set_bit());
        Ok(())
    }
}
```

常見的 HAL crate：

| MCU 系列 | HAL crate | embedded-hal 支援 |
|----------|----------|------------------|
| STM32F4 | stm32f4xx-hal | v1.0 |
| STM32H7 | stm32h7xx-hal | v1.0 |
| ESP32 | esp-hal | v1.0 + async |
| RP2040 | rp2040-hal | v1.0 |
| nRF52 | nrf-hal | v1.0 |
| AVR | avr-hal | v0.2 |

## BSP：Board Support Package

BSP 針對特定開發板進行整合：

```rust
// stm32f4-discovery BSP
let board = stm32f4_discovery::Board::new();
let mut led = board.leds.green;  // 對應 PD12
let mut button = board.button;   // 對應 PA0
```

BSP 預先定義了開發板上的 pin mapping，開發者不需要查詢電路圖。

## embedded-hal trait 分類

```rust
// 數位 I/O
pub trait OutputPin { fn set_high(&mut self) -> Result<(), Self::Error>; }
pub trait InputPin { fn is_high(&self) -> Result<bool, Self::Error>; }

// 序列通訊
pub mod serial { pub trait Read<Word>; pub trait Write<Word>; }
pub mod i2c { pub trait I2c<Word>; }
pub mod spi { pub trait SpiDevice<Word>; }

// PWM
pub trait PwmPin { fn set_duty(&mut self, duty: u16); }

// ADC
pub trait Adc { fn read(&mut self) -> Result<u16, Self::Error>; }
```

## async embedded-hal

2024 年引入的 async trait 為嵌入式非同步開發鋪平了道路：

```rust
use embedded_hal_async::spi::SpiDevice;

async fn read_sensor(spi: &mut impl SpiDevice<u8>) -> Result<u16, Error> {
    let mut buf = [0u8; 2];
    spi.transfer(&mut buf, &[0x00, 0x00]).await?;
    Ok(u16::from_be_bytes(buf))
}
```

搭配 embassy 執行器，可以實現多個周邊的自然並行操作。

## 選擇 HAL crate 的考量

1. **維護狀態**：檢查 GitHub 上的最後更新時間和 issue 回覆速度
2. **embedded-hal 版本**：確認是否支援 v1.0（2023 年穩定）
3. **async 支援**：如果需要非同步操作，確認是否支援 async trait
4. **文件品質**：是否提供範例程式碼和 API 文件
5. **測試覆蓋率**：HAL crate 的測試覆蓋率反映了其可靠程度

## 延伸閱讀

- [embedded-hal 官方倉庫](https://www.google.com/search?q=embedded-hal+Rust+GitHub)
- [svd2rust 使用教學](https://www.google.com/search?q=svd2rust+Rust+embedded)
- [選擇嵌入式 Rust HAL](https://www.google.com/search?q=choosing+embedded+Rust+HAL+crate)
