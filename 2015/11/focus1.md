# Arduino 入門與基本概念

## 前言

Arduino 是一款開源硬體和軟體平台，讓任何人都能輕鬆進入嵌入式系統和物聯網開發的世界。本期將介紹 Arduino 的基礎知識，幫助你邁出嵌入式開發的第一步。

## Arduino 硬體介紹

### Arduino Uno

Arduino Uno 是最經典的 Arduino 開發板：

| 規格 | 數值 |
|------|------|
| 微控制器 | ATmega328P |
| 工作電壓 | 5V |
| 輸入電壓 | 7-12V |
| 數位 I/O | 14 腳（6 支援 PWM）|
| 類比輸入 | 6 腳 |
| 時脈頻率 | 16 MHz |
| Flash 記憶體 | 32 KB |

### 其他常見型號

- **Arduino Mega**：更多 I/O 腳位，適合大型專案
- **Arduino Nano**：體積小，適合空間有限的專案
- **Arduino Leonardo**：原生 USB 支援
- **Arduino Due**：32 位元 ARM 處理器，效能更強

## 開發環境設定

### 安裝 Arduino IDE

1. 從 [arduino.cc](https://www.arduino.cc) 下載 Arduino IDE
2. 安裝驅動程式（Windows 需要，Mac 通常自動識別）
3. 連接 Arduino 板到電腦
4. 選擇正確的板子和連接埠

### 設定ESP8266開發環境

Arduino IDE 支援 ESP8266 開發板：

1. 開啟 Arduino IDE → 檔案 → 偏好設定
2. 在「額外開發板管理員網址」加入：
   ```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```
3. 工具 → 開發板 → 開發板管理員
4. 搜尋「ESP8266」並安裝

## 第一個程式：Blink

```cpp
// Blink - 讓板子上的 LED 閃爍
// 大多數 Arduino 板在腳位 13 有一個內建 LED

void setup() {
  // 初始化設定：這裡設定數位腳位為輸出模式
  pinMode(LED_BUILTIN, OUTPUT);
}

// loop 函數會不斷重複執行
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // 點亮 LED（HIGH 是電壓 level）
  delay(1000);                       // 等待一秒（1000 毫秒）
  digitalWrite(LED_BUILTIN, LOW);   // 熄滅 LED
  delay(1000);                       // 等待一秒
}
```

## Arduino 程式結構

### setup() 函數

在電源開啟或重置後執行一次，用於初始化設定。

```cpp
void setup() {
  Serial.begin(9600);      // 初始化序列埠
  pinMode(13, OUTPUT);     // 設定腳位 13 為輸出
  pinMode(2, INPUT_PULLUP); // 設定腳位 2 為輸入並啟用內部上拉電阻
}
```

### loop() 函數

在 setup() 完成後持續重複執行的主程式邏輯。

```cpp
void loop() {
  // 讀取類比輸入
  int sensorValue = analogRead(A0);

  // 序列輸出
  Serial.println(sensorValue);

  // 延遲
  delay(100);
}
```

## 基本函數

### 數位輸出/輸入

```cpp
// 數位輸出
digitalWrite(pin, value);  // value: HIGH 或 LOW

// 數位輸入
int value = digitalRead(pin);  // 返回 HIGH 或 LOW

// 設定模式
pinMode(pin, mode);  // mode: OUTPUT, INPUT, 或 INPUT_PULLUP
```

### 類比輸入/輸出

```cpp
// 類比輸入（0-1023）
int value = analogRead(pin);  // pin: A0-A5

// 類比輸出（PWM，0-255）
analogWrite(pin, value);
```

### 序列通訊

```cpp
Serial.begin(9600);                    // 初始化序列通訊
Serial.println("Hello, Arduino!");     // 輸出文字並換行
int value = Serial.parseInt();         // 讀取序列輸入的整數
```

## 周邊模組連接

### 麵包板使用

麵包板是實驗電路的重要工具：
- 水平行：相連的孔（紅線標示區域）
- 垂直列：電源匯流排（通常藍線為 GND，紅線為 VCC）

### 連接範例：溫度感測器 LM35

```cpp
const int LM35_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int rawValue = analogRead(LM35_PIN);
  float voltage = rawValue * 5.0 / 1023.0;
  float temperature = voltage * 100.0;  // LM35: 10mV/°C
  Serial.println(temperature);
  delay(1000);
}
```

### 連接範例：LED

```cpp
const int LED_PIN = 9;  // 使用 PWM 腳位

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // 呼吸燈效果
  for (int brightness = 0; brightness <= 255; brightness++) {
    analogWrite(LED_PIN, brightness);
    delay(10);
  }
  for (int brightness = 255; brightness >= 0; brightness--) {
    analogWrite(LED_PIN, brightness);
    delay(10);
  }
}
```

## 常見錯誤排除

### 燒錄錯誤

- 確認正確的開發板和連接埠選擇
- 檢查 USB 連接線是否支援資料傳輸（有些僅供電）
- 確認驅動程式已正確安裝

### 序列埠無輸出

- 確認鮑率設定正確（Serial.begin(9600) 與序列監控視窗一致）
- 檢查是否使用了正確的連接埠

### 電路無反應

- 檢查導線和麵包板連接
- 確認元件極性正確（LED 長腳為陽極）
- 使用萬用電表檢查電壓

## Arduino 與 ESP8266

ESP8266 是一款內建 WiFi 功能的低成本微控制器：

```cpp
#include <ESP8266WiFi.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting...");
  }
  Serial.println("Connected!");
}

void loop() {
  // 保持連線
}
```

## 小結

Arduino 讓嵌入式系統開發變得簡單且平易近人。通過本章的學習，你應該已經能夠：

- 設定 Arduino 開發環境
- 撰寫基本的 Arduino 程式
- 讀取感測器資料
- 控制輸出裝置（如 LED）

下一期我們將介紹 Raspberry Pi，一款更強大的單板電腦。

---

**下一步**：[Raspberry Pi 與單板電腦](focus2.md)

## 延伸閱讀

- [Arduino Official Website](https://www.google.com/search?q=Arduino+official+tutorial)
- [Arduino Reference](https://www.google.com/search?q=Arduino+reference+documentation)
- [Arduino Project Hub](https://www.google.com/search?q=Arduino+project+ideas)