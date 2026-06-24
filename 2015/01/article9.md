# 開源硬體運動：Arduino 與 Raspberry Pi

## 前言

開源硬體在 2015 年持續發展，Arduino 和 Raspberry Pi 成為創客運動的核心工具。

## Arduino

```cpp
// Arduino 範例：閃爍 LED
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
```

## Raspberry Pi

```python
# Raspberry Pi 範例：GPIO 控制
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

while True:
    GPIO.output(11, True)
    time.sleep(1)
    GPIO.output(11, False)
    time.sleep(1)
```

## IoT 應用

```
2015 年 IoT 發展重點：
──────────────────────
- 智慧家庭
- 穿戴裝置
- 工業物聯網
- 農業自動化
```

## 結語

開源硬體降低了創新門檻，讓更多人能夠參與軟硬整合的開發。

---

## 延伸閱讀

- [Arduino 官方網站](https://www.google.com/search?q=Arduino+open+source+hardware)
- [Raspberry Pi 官方網站](https://www.google.com/search?q=Raspberry+Pi+single+board+computer)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*