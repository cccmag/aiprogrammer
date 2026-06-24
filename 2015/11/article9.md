# 功耗優化技巧

## 功耗基礎

### 電流 vs 電壓

- 功耗 = 電壓 × 電流
- 降低任一者都可以減少功耗

### 休眠模式

```cpp
// Arduino Uno - 沒有內建休眠功能

// ESP8266 深度睡眠
void deepSleep() {
  ESP.deepSleep(10e6);  // 10 秒
}

// ESP32
void lightSleep() {
  esp_sleep_enable_timer_wakeup(1000000);
  esp_light_sleep_start();
}
```

## 功耗測量

### 萬用電表

```bash
# 串聯連接萬用電表（設定在 mA 或 uA 檔位）
```

### 電流感測器

```cpp
// INA219 電流感測器
#include <Wire.h>
#include <INA219.h>

INA219 ina219;

void setup() {
  ina219.begin();
  Serial.begin(9600);
}

void loop() {
  float current = ina219.getCurrent_mA();
  Serial.println(current);
  delay(100);
}
```

## 優化策略

### 1. 降低時脈頻率

```cpp
// Arduino Uno - 8MHz（使用外部震盪器）

// ESP32 - 調整 CPU 頻率
setCpuFrequencyMhz(80);  // 降低到 80MHz
```

### 2. 關閉不需要的功能

```cpp
// 關閉 WiFi
WiFi.mode(WIFI_OFF);

// 關閉藍牙（ESP32）
btStop();

// 關閉 ADC
adc_power_off();
```

### 3. 使用中斷

```cpp
volatile bool flag = false;

void change() {
  flag = true;
}

void setup() {
  attachInterrupt(digitalPinToInterrupt(2), change, RISING);
}

void loop() {
  if (flag) {
    // 處理事件
    flag = false;
  } else {
    // 進入休眠
    esp_light_sleep_start();
  }
}
```

### 4. 優化程式碼

```cpp
// 不好：每次 loop 都呼叫
void loop() {
  Serial.print("Value: ");
  Serial.println(readSensor());
  delay(1000);
}

// 好：減少序列輸出頻率
void loop() {
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 1000) {
    Serial.println(readSensor());
    lastPrint = millis();
  }
}
```

## 睡眠模式比較

| 模式 | 功耗 | 喚醒方式 |
|------|------|----------|
| 正常 | 15-70mA | - |
| 空轉 | 30mA | - |
| 睡眠 | 0.1mA | 中斷 |
| 深度睡眠 | 0.01mA | RESET |

## 電池供電設計

### 常用電池

| 電池 | 電壓 | 容量 | 特點 |
|------|------|------|------|
| AA 鹼性 | 1.5V | 2000mAh | 容易購買 |
| 鋰離子 | 3.7V | 2000mAh | 可充電 |
| 鋰聚合物 | 3.7V | 可定制 | 輕量 |
| CR2032 | 3V | 220mAh | 銀離子 |

### 升壓/降壓

```cpp
// 5V 感測器用 3.3V 供電
// 使用低壓差穩壓器 (LDO)
```

## 小結

功耗優化是物聯網裝置設計的重要環節。選擇合適的休眠模式、優化程式碼、合理設計硬體，可以大幅延長電池壽命。

---

## 延伸閱讀

- [ESP32 Power Management](https://www.google.com/search?q=ESP32+power+consumption+optimization)
- [Arduino Power Saving](https://www.google.com/search?q=arduino+power+consumption+optimization)