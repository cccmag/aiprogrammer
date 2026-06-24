# I2C 通訊協定解析

## I2C 基礎

I2C（Inter-Integrated Circuit）是一種序列匯流排通訊協定：

- **兩條線**：SDA（資料）和 SCL（時脈）
- **主從架構**：一個主設備，多個從設備
- **地址分派**：每個從設備有唯一地址

## 硬體連接

```
Arduino          感測器
  A4 (SDA) ──── SDA
  A5 (SCL) ──── SCL
  5V      ──── VCC
  GND     ──── GND

（所有裝置的 VCC 和 GND 共同連接）
```

## 位址格式

```
7 位元地址 + 1 位元讀/寫標誌

讀取：  地址 << 1 | 1
寫入：  地址 << 1 | 0
```

常見的掃描程式碼：

```python
import smbus2

bus = smbus2.SMBus(1)

for addr in range(0x03, 0x78):
    try:
        bus.read_byte(addr)
        print(f"Found device at 0x{addr:02X}")
    except:
        pass
```

## I2C 速率

| 模式 | 速率 |
|------|------|
| 標準模式 | 100 kHz |
| 快速模式 | 400 kHz |
| 快速模式+ | 1 MHz |
|高速模式 | 3.4 MHz |

## Arduino I2C 程式設計

```cpp
#include <Wire.h>

#define DEVICE_ADDRESS 0x68

void setup() {
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  // 請求資料
  Wire.requestFrom(DEVICE_ADDRESS, 14);

  // 讀取資料
  while (Wire.available()) {
    byte data = Wire.read();
    Serial.print(data, HEX);
    Serial.print(" ");
  }

  delay(1000);
}
```

## 常見 I2C 感測器地址

| 感測器 | 地址 |
|--------|------|
| BMP180 | 0x77 |
| MPU-6050 | 0x68 |
| ADXL345 | 0x53 |
| DS3231 RTC | 0x68 |
| OLED 顯示器 | 0x3C |

## 除錯技巧

1. **確認連接**：SDA、SCL、VCC、GND
2. **檢查地址**：使用 I2C 掃描器
3. **確認電壓**：3.3V 或 5V
4. **使用上拉電阻**：如果感測器沒有內建

## 常見問題

**Q: I2C 找不到裝置？**
A: 檢查連接和地址是否正確

**Q: 讀取資料錯誤？**
A: 確認讀取的位元組數量

**Q: 時脈變慢？**
A: 降低 I2C 速率

## 小結

I2C 是嵌入式系統中最常用的通訊協定之一，適合連接多種感測器。掌握 I2C 原理和程式設計，是進行物聯網開發的基礎。

---

## 延伸閱讀

- [I2C Protocol Guide](https://www.google.com/search?q=I2C+protocol+tutorial)
- [I2C Arduino Reference](https://www.google.com/search?q=Wire+library+arduino+i2c)