# 類比與數位轉換

## 為什麼需要轉換？

現實世界是類比的（連續變化），但電腦是數位的（離散值）。因此需要轉換介面。

## ADC（類比轉數位）

### 採樣（Sampling）

根據奈奎斯特定理，採樣頻率必須大於輸入訊號最高頻率的兩倍。

```
f_sampling > 2 × f_signal
```

### 量化（Quantization）

將連續值映射到離散值。

```
解析度 (bits)   解析度 levels    電壓範圍 3.3V 時的 LSB
     8            256            12.9 mV
    10           1024            3.22 mV
    12           4096            0.81 mV
    16          65536            0.05 mV
```

### 編碼（Encoding）

將量化後的值轉換為二進位表示。

```
範例：2.1V (假設範圍 0-3.3V, 8-bit ADC)
LSB = 3.3V / 256 = 12.9mV
Code = 2.1V / 12.9mV ≈ 162 = 10100010
```

### 常見 ADC 架構

| 類型 | 速度 | 解析度 | 功耗 |
|-----|------|-------|-----|
| SAR | 中速 | 高 | 中 |
| Delta-Sigma | 慢速 | 極高 | 低 |
| 雙斜率 | 慢速 | 高 | 低 |
| 快閃（Flash） | 極速 | 中 | 高 |
| 管線（Pipeline） | 高速 | 高 | 中 |

### SAR ADC 原理

```
       ┌──────────┐
Vin ──→│ 比較器   │──→ 結果
       └────┬─────┘
            │
       ┌────┴─────┐
       │  DAC    │
       └────┬─────┘
            │
    ┌───────┴───────┐
    │  控制邏輯     │
    │  (SAR)        │
    └───────────────┘
```

### 重要參數

- **ENOB (Effective Number of Bits)**：實際有效位元數
- **SNR (Signal-to-Noise Ratio)**：訊號雜訊比
- **SINAD**：訊號加雜訊與雜訊比
- **THD (Total Harmonic Distortion)**：總諧波失真

## DAC（數位轉類比）

### 電阻網路 DAC

**R-2R 梯形網路**：

```
Vref ─┤ R ├──┬──┤ 2R ├──┬──┤ 2R ├──┬──→ Vout
       └──┤ 2R ┘  └──┤ 2R ┘  └──┘
       Bit0    Bit1    Bit2
```

輸出電壓：`Vout = Vref × (D/2^n)`

### PWM DAC

使用 PWM 訊號和低通濾波器：

```c
void dac_pwm(float voltage, float vref) {
    float duty = voltage / vref;
    set_pwm_duty(duty);
}
```

### 重要參數

- **解析度**：位元數決定精細度
- **線性度**：DNL、INL
- **穩定時間**：輸出達到最終值的時間

## 應用範例

### MCU 的 ADC 使用

```c
void adc_init() {
    ADCSRA |= (1 << ADEN);          // 啟用 ADC
    ADCSRA |= (1 << ADPS2) | (1 << ADPS1);  // 分頻
    ADMUX |= (1 << REFS0);          // Vref = AVCC
}

uint16_t adc_read(uint8_t ch) {
    ADMUX = (ADMUX & 0xF0) | (ch & 0x0F);
    ADCSRA |= (1 << ADSC);
    while (ADCSRA & (1 << ADSC));
    return ADC;
}
```

## 參考資料

- [ADC 原理](https://www.google.com/search?q=analog+to+digital+converter+原理)
- [DAC 架構](https://www.google.com/search?q=digital+to+analog+converter+types)