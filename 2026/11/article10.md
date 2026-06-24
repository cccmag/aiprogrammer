# 嵌入式 Rust 專案架構設計 — 模組化、測試、CI

## 為什麼架構設計重要

嵌入式專案有別於一般軟體專案的三個挑戰：
1. **資源限制**：Flash 和 RAM 都是稀缺資源
2. **硬體耦合**：程式碼必須與特定 MCU 綁定
3. **除錯困難**：沒有標準輸出，JTAG/SWD 是主要除錯手段

良好的架構設計可以讓這些挑戰變得可控。

## 模組化策略

### 分層架構

```
src/
├── main.rs           # 進入點、中斷向量
├── drivers/          # 感測器驅動
│   ├── mod.rs
│   ├── bme280.rs     # BME280 溫濕度感測器
│   └── mpu9250.rs    # 9 軸 IMU
├── hal/              # 硬體抽象實作
│   ├── mod.rs
│   └── pins.rs       # Pin mapping
├── app/              # 應用邏輯
│   ├── mod.rs
│   ├── controller.rs # 控制迴圈
│   └── telemetry.rs  # 資料上報
└── lib.rs            # crate 根
```

### 特徵閘門（Feature Gates）

透過 cargo feature 支援不同硬體平台：

```toml
[features]
stm32f4 = ["stm32f4xx-hal"]
esp32 = ["esp-hal"]
rp2040 = ["rp2040-hal"]
```

```rust
#[cfg(feature = "stm32f4")]
use stm32f4xx_hal as hal;
#[cfg(feature = "esp32")]
use esp_hal as hal;
```

## 泛型驅動設計

透過 embedded-hal trait 實現硬體無關的驅動程式碼：

```rust
pub struct SensorDriver<BUS> {
    bus: BUS,
}

impl<BUS: I2c<u8>> SensorDriver<BUS> {
    pub fn new(bus: BUS) -> Self { ... }
    pub fn read(&mut self) -> Result<Measurement, Error> { ... }
}

// 在不同平台上使用相同驅動
#[cfg(feature = "stm32f4")]
type MySensor = SensorDriver<stm32f4xx_hal::i2c::I2c<USART1>>;
#[cfg(feature = "esp32")]
type MySensor = SensorDriver<esp_hal::i2c::I2C<I2C0>>;
```

## 測試策略

### 單元測試

在沒有硬體的環境中測試純邏輯：

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_moving_average() {
        let mut filter = MovingAverage::<3>::new();
        assert_eq!(filter.update(10.0), 10.0);
        assert_eq!(filter.update(20.0), 15.0);
        assert_eq!(filter.update(30.0), 20.0);
        assert_eq!(filter.update(0.0), 50.0 / 3.0);
    }
}
```

### 模擬測試（Mock）

透過 trait 模擬硬體周邊：

```rust
struct MockI2c {
    responses: Vec<u8>,
}

impl I2c<u8> for MockI2c {
    fn read(&mut self, addr: u8, buf: &mut [u8]) -> Result<(), Self::Error> {
        buf.copy_from_slice(&self.responses);
        Ok(())
    }
    fn write(&mut self, addr: u8, bytes: &[u8]) -> Result<(), Self::Error> {
        Ok(())
    }
    fn write_read(...) -> ...
}

#[test]
fn test_bme280_read() {
    let mut i2c = MockI2c::new();
    i2c.responses = vec![0x50, 0x00]; // 模擬溫度量測值
    let mut sensor = Bme280::new(i2c, 0x76);
    let temp = sensor.read_temperature().unwrap();
    assert!((temp - 20.0).abs() < 0.1);
}
```

### 硬體在迴路測試（HIL）

```rust
#[test]
#[ignore] // 需要實體硬體
fn test_led_blinks() {
    let mut led = PA5::into_push_pull_output();
    led.set_high();
    delay(100.ms());
    led.set_low();
    // 使用示波器或 ADC 驗證波形
}
```

## CI/CD 管線

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions-rs/toolchain@v1
        with:
          target: thumbv7em-none-eabihf
      - run: cargo build --release
      - run: cargo test --lib       # 主機端測試
      - run: cargo clippy --target thumbv7em-none-eabihf
```

## 版本管理策略

```toml
[package]
version = "0.2.1"
edition = "2024"

[dependencies]
# 固定 HAL 版本避免意外行為改變
stm32f4xx-hal = "=0.18.0"
```

建議使用 `Cargo.lock` 鎖定所有相依版本（尤其是嵌入式專案，硬體相容性至關重要）。

## 延伸閱讀

- [Rust 嵌入式專案模板](https://www.google.com/search?q=Rust+embedded+project+template+cortex-m)
- [嵌入式 Rust 測試最佳實務](https://www.google.com/search?q=embedded+Rust+testing+best+practices)
- [Rust CI for embedded](https://www.google.com/search?q=Rust+CI+embedded+systems)
- [cargo-hil 硬體測試框架](https://www.google.com/search?q=cargo-hil+hardware+in+loop+testing)
