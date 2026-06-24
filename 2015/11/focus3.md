# 感測器與輸入裝置

## 前言

感測器是物聯網系統的感官，將物理世界的信號轉換為電子系統可以處理的資料。選擇合適的感測器是物聯網專案成功的關鍵。

## 感測器分類

### 依輸出類型

| 類型 | 特點 | 範例 |
|------|------|------|
| 類比輸出 | 連續電壓/電流訊號 | LM35（溫度）、光敏電阻 |
| 數位輸出 | 離散訊號（0/1 或匯流排）| DHT11（溫濕度）、DS18B20 |

### 依測量類型

- **環境感測器**：溫度、濕度、氣壓、光照
- **運動感測器**：加速度、陀螺儀、GPS
- **位置感測器**：距離、超音波、紅外線
- **電氣特性**：電壓、電流、電阻

## 常見感測器詳解

### 1. 溫度感測器

#### LM35（類比輸出）

```cpp
// Arduino 程式
const int LM35_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int rawValue = analogRead(LM35_PIN);
  float voltage = rawValue * 5.0 / 1023.0;
  float temperatureC = voltage * 100.0;
  float temperatureF = temperatureC * 9.0 / 5.0 + 32.0;

  Serial.print("Temperature: ");
  Serial.print(temperatureC);
  Serial.print("C / ");
  Serial.print(temperatureF);
  Serial.println("F");

  delay(1000);
}
```

#### DS18B20（數位輸出）

```cpp
#include <OneWire.h>
#include <DallasTemperature.h>

const int ONE_WIRE_BUS = 2;

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);
  Serial.println(tempC);
  delay(1000);
}
```

### 2. 濕度感測器

#### DHT11（數位輸出）

```cpp
#include <dht.h>

dht DHT;

const int DHT11_PIN = 7;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int chk = DHT.read11(DHT11_PIN);

  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);

  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);

  delay(1000);
}
```

### 3. 光照感測器

#### 光敏電阻（LDR）

```cpp
const int LDR_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int lightValue = analogRead(LDR_PIN);
  Serial.println(lightValue);
  delay(100);
}
```

### 4. 距離感測器

#### HC-SR04 超音波感測器

```cpp
const int TRIG_PIN = 9;
const int ECHO_PIN = 10;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(100);
}
```

### 5. 氣壓感測器

#### BMP180（I2C）

```python
# Raspberry Pi Python 程式
import smbus2
import time

class BMP180:
    def __init__(self, address=0x77):
        self.bus = smbus2.SMBus(1)
        self.address = address

    def get_temperature(self):
        self.bus.write_byte_data(self.address, 0xF4, 0x2E)
        time.sleep(0.005)
        data = self.bus.read_word_data(self.address, 0xF6)
        return (data + 30) / 240.0  # 簡化計算

    def get_pressure(self):
        self.bus.write_byte_data(self.address, 0xF4, 0x34)
        time.sleep(0.02)
        data = self.bus.read_byte_data(self.address, 0xF6)
        return data * 256

# 使用
bmp = BMP180()
print(f"Temp: {bmp.get_temperature()} C")
print(f"Pressure: {bmp.get_pressure()} Pa")
```

### 6. 運動感測器

#### MPU-6050（三軸加速度計+陀螺儀）

```python
# Raspberry Pi
import smbus2
import math

class MPU6050:
    def __init__(self, address=0x68):
        self.bus = smbus2.SMBus(1)
        self.address = address
        self.bus.write_byte_data(address, 0x6B, 0)  # 喚醒 MPU6050

    def get_data(self):
        data = self.bus.read_i2c_block_data(self.address, 0x3B, 14)
        accel_x = data[0] << 8 | data[1]
        accel_y = data[2] << 8 | data[3]
        accel_z = data[4] << 8 | data[5]
        return accel_x, accel_y, accel_z

mpu = MPU6050()
print(mpu.get_data())
```

## 通訊協定

### I2C 詳解

I2C（Inter-Integrated Circuit）是一種常用的串列匯流排協定：

**特點**：
- 只需要兩條線（SDA、SCL）
- 支援多個主設備和多個從設備
- 速度：標准模式 100kHz，快速模式 400kHz

**連接方式**：
```
VCC ──── VCC
GND ──── GND
SDA ──── SDA
SCL ──── SCL
```

**Arduino I2C 程式設計**：
```cpp
#include <Wire.h>

void setup() {
  Wire.begin();  // 加入 I2C 匯流排
  Serial.begin(9600);
}

void loop() {
  Wire.requestFrom(0x68, 14);  // 請求 14 位元組
  while (Wire.available()) {
    byte data = Wire.read();
    Serial.print(data, HEX);
    Serial.print(" ");
  }
  delay(1000);
}
```

### SPI 詳解

SPI（Serial Peripheral Interface）是另一種常用的高速介面：

**特點**：
- 四條線（MISO、MOSI、SCK、CS）
- 比 I2C 更快
- 支援全雙工傳輸

**Arduino SPI 程式設計**：
```cpp
#include <SPI.h>

void setup() {
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV2);
}

void loop() {
  byte response = SPI.transfer(0x00);
  delay(100);
}
```

## 類比 vs 數位

### 類比感測器

**優點**：
- 簡單，不需要程式庫
- 連續值，精確度高

**缺點**：
- 需要 ADC（類比轉數位）轉換
- 訊號容易受雜訊影響

### 數位感測器

**優點**：
- 抗雜訊能力強
- 直接與微控制器通訊
- 容易多個串接

**缺點**：
- 需要通訊協定和程式庫
- 有地址衝突風險

## 感測器選擇指南

| 需求 | 推薦感測器 |
|------|-----------|
| 室內溫度 | DHT11、DHT22 |
| 室外/精密溫度 | DS18B20、BMP280 |
| 濕度 | DHT22、Si7021 |
| 氣壓 | BMP180、BMP280 |
| 光照 | BH1750、TSL2561 |
| 距離 | HC-SR04（超聲波）、VL53L0X（雷射）|
| 運動/加速度 | MPU-6050、ADXL345 |

## 小結

感測器是物聯網系統的基礎元件。選擇合適的感測器需要考慮：

1. **測量類型**：需要測量什麼？
2. **精度要求**：需要多精確？
3. **輸出類型**：類比還是數位？
4. **通訊介面**：I2C、SPI 還是單線？
5. **功耗**：是否需要电池供電？
6. **成本**：預算限制？

了解這些基本概念後，你可以開始探索更複雜的感測器和應用場景。

---

**下一步**：[物聯網架構與通訊協定](focus4.md)

## 延伸閱讀

- [Sensor Buying Guide](https://www.google.com/search?q=sensor+buying+guide+arduino)
- [I2C Protocol Tutorial](https://www.google.com/search?q=I2C+protocol+tutorial+arduino)
- [MPU-6050 Tutorial](https://www.google.com/search?q=MPU-6050+accelerometer+tutorial)