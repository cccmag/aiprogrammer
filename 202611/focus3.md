# 通訊協定 UART/SPI/I2C（2018–2026）

## UART 非同步序列通訊

UART 是最基礎的序列通訊協定。embedded-hal 的 `serial` trait：

```rust
use embedded_hal::serial::{Read, Write};

fn echo<Serial: Read<u8> + Write<u8>>(serial: &mut Serial) {
    if let Ok(byte) = serial.read() {
        serial.write(byte).ok();
    }
}
```

## SPI 同步序列通訊

SPI 使用主從架構，四線制（SCK、MOSI、MISO、CS）：

```rust
pub trait SpiDevice<Word> {
    fn read(&mut self, words: &mut [Word]) -> Result<(), Self::Error>;
    fn write(&mut self, words: &[Word]) -> Result<(), Self::Error>;
    fn transfer(&mut self, read: &mut [Word], write: &[Word]) -> Result<(), Self::Error>;
}
```

SPI 的優勢：全雙工、時脈可達數十 MHz，適合高速資料傳輸。

## I2C 雙線通訊

I2C 使用 SDA 和 SCL 兩線，支援多主機和多從機：

```rust
pub trait I2c<Word> {
    fn read(&mut self, addr: u8, buffer: &mut [Word]) -> Result<(), Self::Error>;
    fn write(&mut self, addr: u8, bytes: &[Word]) -> Result<(), Self::Error>;
    fn write_read(&mut self, addr: u8, bytes: &[Word], buffer: &mut [Word]) -> Result<(), Self::Error>;
}
```

I2C 的優勢：僅需兩條線、支援多裝置匯流排，適合感測器連接。

## 傳輸模式對比

| 模式 | CPU 使用率 | 複雜度 | 適合場景 |
|------|-----------|--------|---------|
| Polling | 100%（等待） | 低 | 簡單週期性讀取 |
| Interrupt | 僅收發瞬間 | 中 | 低頻事件驅動 |
| DMA | 幾乎 0% | 高 | 大量連續資料 |

## blocking vs async

embedded-hal 同時提供 blocking 和 async 版本的通訊 trait：

- **blocking**：`nb::Result` 回傳，需要手動輪詢或等待
- **async**：使用 `.await` 語法，搭配 embassy 執行器自動管理

## 常見感測器驅動模式

大多數感測器驅動遵循統一的初始化—讀取模式：

```rust
pub struct Bme280<BUS> { bus: BUS }
impl<BUS: I2c<u8>> Bme280<BUS> {
    pub fn new(bus: BUS) -> Self { ... }
    pub fn measure(&mut self) -> Result<Measurement, Error> { ... }
}
```

## 延伸閱讀

- [embedded-hal serial trait](https://www.google.com/search?q=embedded-hal+serial+trait)
- [STM32 USART 應用筆記](https://www.google.com/search?q=STM32+USART+interrupt+DMA)
- [I2C 協定規範](https://www.google.com/search?q=I2C+protocol+specification)
