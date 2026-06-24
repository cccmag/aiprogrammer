# UART/SPI/I2C 通訊實戰 — 輪詢/中斷/DMA 模式對比

## UART：最基本序列通訊

UART（Universal Asynchronous Receiver/Transmitter）是非同步通訊的基礎。

### 輪詢模式

```rust
fn uart_polling(uart: &mut impl serial::Write<u8>) {
    for byte in b"Hello World\n" {
        nb::block!(uart.write(*byte)).unwrap();
    }
}
```

### 中斷模式（搭配 embassy）

```rust
#[embassy_executor::task]
async fn uart_task(mut uart: Uart<'static, USART1>) {
    loop {
        let byte = uart.read().await.unwrap();
        uart.write(byte).await.unwrap();
    }
}
```

### DMA 模式

```rust
// 配置 DMA 通道
let mut dma = DMA::new(dp.DMA1);
let mut uart = serial::Uart::new(
    dp.USART1, tx, rx, 115_200.bps(), clocks
);

// DMA 自動傳送整段緩衝區
let buffer: [u8; 256] = [0; 256];
uart.write_dma(&buffer).await.unwrap();
```

## SPI：高速同步通訊

SPI 常用於顯示器、SD 卡、無線模組：

```rust
use embedded_hal::spi::SpiDevice;

fn write_display<SPI: SpiDevice<u8>>(spi: &mut SPI, data: &[u8]) {
    spi.write(data).unwrap();
}
```

SPI 時脈速度通常可達 10–50 MHz，遠高於 UART 和 I2C。

## I2C：雙線多裝置總線

I2C 是感測器最常見的介面：

```rust
use embedded_hal::i2c::I2c;

fn read_sensor<I2C: I2c>(i2c: &mut I2C, addr: u8) -> u16 {
    let mut buf = [0u8; 2];
    i2c.write_read(addr, &[0x00], &mut buf).unwrap();
    u16::from_be_bytes(buf)
}
```

I2C 的地址機制允許多達 127 個裝置共用同一條兩線總線。

## 傳輸模式取捨

| 面向 | Polling | Interrupt | DMA |
|------|---------|-----------|-----|
| 程式碼複雜度 | 低 | 中 | 高 |
| 每 byte CPU 開銷 | 100% | ~20% | ~0% |
| 反應延遲 | 取決於 poll 頻率 | 即時 | 即時 |
| 記憶體使用 | 無額外 | 需 ISR 堆疊 | 需 DMA buffer |
| 適合場景 | 簡單除錯輸出 | UART 命令解析 | 音訊/顯示更新 |

## blocking vs async

embedded-hal 同時提供兩種模式：

**blocking**：

```rust
let result: nb::Result<u8, Error> = uart.read();
match result {
    Ok(byte) => process(byte),
    Err(nb::Error::WouldBlock) => {},
    Err(nb::Error::Other(e)) => error_handler(e),
}
```

**async**：

```rust
async fn read_loop(uart: &mut impl embedded_hal_async::serial::Read<u8>) {
    loop {
        let byte = uart.read().await.unwrap();
        process(byte).await;
    }
}
```

Async 模式讓多個通訊協定可以自然地並行執行。

## 常見感測器驅動模式

```rust
pub trait Sensor {
    type Error;
    fn init(&mut self) -> Result<(), Self::Error>;
    fn read(&mut self) -> Result<SensorData, Self::Error>;
}

impl<I2C: I2c<u8>> Sensor for Bme280<I2C> {
    fn init(&mut self) -> Result<(), Self::Error> { ... }
    fn read(&mut self) -> Result<SensorData, Self::Error> { ... }
}
```

## 延伸閱讀

- [embedded-hal 序列通訊](https://www.google.com/search?q=embedded-hal+serial+UART+SPI+I2C)
- [I2C 協定入門](https://www.google.com/search?q=I2C+protocol+beginner+guide)
- [STM32 DMA 應用](https://www.google.com/search?q=STM32+DMA+UART+SPI)
