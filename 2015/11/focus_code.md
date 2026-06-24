# Arduino 與 Raspberry Pi 範例

## 概述

本程式展示 Arduino 和 Raspberry Pi 的基本應用，包括環境感測器讀取、馬達控制和網路連線。這些範例涵蓋了嵌入式系統開發的核心概念。

## 專案結構

```
_code/
├── arduino_examples/      # Arduino 程式碼
│   ├── blink.cpp         # LED 閃爍
│   ├── sensor_read.cpp   # 感測器讀取
│   └── motor_control.cpp  # 馬達控制
├── raspberry_pi/          # Raspberry Pi 程式碼
│   ├── gpio_example.py   # GPIO 控制
│   ├── i2c_sensor.py     # I2C 感測器
│   └── mqtt_client.py    # MQTT 用戶端
└── test.sh               # 測試執行腳本
```

## Arduino 範例

### LED 閃爍

```cpp
const int LED_PIN = 13;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
```

### 感測器讀取

```cpp
const int SENSOR_PIN = A0;
const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int value = analogRead(SENSOR_PIN);
  Serial.println(value);

  if (value > 500) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  delay(100);
}
```

### 馬達控制

```cpp
const int ENA = 9;
const int IN1 = 8;
const int IN2 = 7;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void loop() {
  // 正轉
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 200);
  delay(2000);

  // 停止
  analogWrite(ENA, 0);
  delay(1000);
}
```

## Raspberry Pi 範例

### GPIO 控制

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
LED_PIN = 11

GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

### I2C 感測器

```python
import smbus2
import time

bus = smbus2.SMBus(1)
address = 0x77

def read_bmp180():
    bus.write_byte_data(address, 0xF4, 0x2E)
    time.sleep(0.005)
    data = bus.read_word_data(address, 0xF6)
    return data

while True:
    print(f"Raw: {read_bmp180()}")
    time.sleep(1)
```

### MQTT 用戶端

```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with {rc}")
    client.subscribe("home/sensor/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqtt-dashboard.com", 1883)
client.loop_start()

while True:
    client.publish("home/sensor/temperature", "25.5")
    time.sleep(5)
```

## 執行方式

```bash
# Arduino 程式需要透過 Arduino IDE 上傳到開發板

# Raspberry Pi 程式可以直接執行
cd _code/raspberry_pi
python3 gpio_example.py
python3 i2c_sensor.py
python3 mqtt_client.py

# 執行測試
./test.sh
```

## 延伸挑戰

1. 修改 LED 閃爍頻率為可調整
2. 連接 DHT11 感測器讀取溫濕度
3. 實作馬達速度控制（使用 PWM）
4. 建立完整的 MQTT 溫溼度監控系統

---

## 延伸閱讀

- [Arduino Reference](https://www.google.com/search?q=Arduino+reference)
- [Raspberry Pi GPIO Guide](https://www.google.com/search?q=Raspberry+Pi+GPIO+tutorial)
- [MQTT Python Tutorial](https://www.google.com/search?q=paho+mqtt+tutorial)