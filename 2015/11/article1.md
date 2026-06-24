# Arduino Uno 開發板詳解

## 硬體規格

Arduino Uno 是最廣泛使用的 Arduino 開發板：

| 項目 | 規格 |
|------|------|
| 微控制器 | ATmega328P |
| 工作電壓 | 5V |
| 輸入電壓 | 7-12V |
| 數位 I/O | 14 腳（6 支援 PWM）|
| 類比輸入 | 6 腳（10 位元 ADC）|
| 時脈頻率 | 16 MHz |
| Flash 記憶體 | 32 KB |
| SRAM | 2 KB |
| EEPROM | 1 KB |

## 針腳分布

```
                    USB
        ┌────────────────────────────┐
        │  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  │
        │                            │
        │  13 ●                     │
        │  GND ●                    │
   LED◀│  SCK●   3.3V ●            │
        │  MISO●  5V ●              │
        │  MOSI●  10 ●              │
        │   SS●   AREF●             │
        └────────────────────────────┘
```

## 供電方式

1. **USB 供電**：5V，500mA
2. **DC 電源jack**：7-12V
3. **Vin 針腳**：7-12V
4. **5V 針腳**：5V（不推薦）

## 保護機制

- 自復保險絲：500mA
- 反向電壓保護
- 過熱保護

## 與其他板子比較

| 型號 | MCU | 時脈 | Flash | I/O |
|------|-----|------|-------|-----|
| Uno | ATmega328P | 16MHz | 32KB | 14 |
| Mega | ATmega2560 | 16MHz | 256KB | 54 |
| Nano | ATmega328P | 16MHz | 32KB | 14 |
| Due | SAM3X8E | 84MHz | 512KB | 54 |

## 小結

Arduino Uno 是入門嵌入式開發的最佳選擇，性價比高、社群資源豐富。

---

## 延伸閱讀

- [Arduino Uno Official Page](https://www.google.com/search?q=Arduino+Uno+official+specifications)
- [ATmega328P Datasheet](https://www.google.com/search?q=ATmega328P+datasheet)