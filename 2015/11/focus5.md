# 馬達控制與致動器

## 前言

馬達和致動器是物聯網系統中實現物理動作的關鍵元件。從簡單的開關閥門到複雜的機械手臂，都需要馬達來產生運動。

## 馬達類型

### 直流馬達（DC Motor）

最基礎的馬達類型，直接使用直流電源：

- **轉速**：由電壓控制
- **轉向**：由電流方向控制
- **應用**：風扇、玩具、輪椅

### 伺服馬達（Servo Motor）

可以精確控制角度的馬達：

- **角度範圍**：通常是 0-180° 或 0-360°
- **控制訊號**：PWM
- **應用**：機器關節、RC 飛機

### 步進馬達（Stepper Motor）

每次移動一個固定角度（步進）：

- **精確定位**：不需要位置感測器
- **高扭矩**：適合 CNC、3D 列印
- **應用**：3D 列印機、CNC 機台

## 直流馬達控制

### 基本控制

```cpp
// Arduino DC 馬達控制
const int MOTOR_PIN = 9;

void setup() {
  pinMode(MOTOR_PIN, OUTPUT);
}

void loop() {
  // PWM 控制轉速 0-255
  analogWrite(MOTOR_PIN, 128);  // 半速
  delay(2000);
  analogWrite(MOTOR_PIN, 255);  // 全速
  delay(2000);
  analogWrite(MOTOR_PIN, 0);    // 停止
  delay(2000);
}
```

### 方向控制（H 橋）

使用 H 橋電路控制直流馬達正反轉：

```cpp
// H 橋馬達驅動
const int ENA = 9;
const int IN1 = 8;
const int IN2 = 7;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void motorForward(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);
}

void motorReverse(int speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, speed);
}

void motorStop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
}

void loop() {
  motorForward(200);  // 正轉
  delay(2000);
  motorStop();
  delay(1000);
  motorReverse(200);  // 反轉
  delay(2000);
  motorStop();
  delay(1000);
}
```

### 常見 H 橋晶片

- **L298N**：雙 H 橋，支援 2A 電流
- **L293D**：雙 H 橋，支援 0.6A 電流
- **TB6612FNG**：雙 H 橋，支援 1.2A 電流

## 伺服馬達控制

### Arduino Servo 程式庫

```cpp
#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 9;

void setup() {
  myServo.attach(SERVO_PIN);
}

void loop() {
  myServo.write(0);      // 0 度
  delay(1000);
  myServo.write(90);      // 90 度
  delay(1000);
  myServo.write(180);     // 180 度
  delay(1000);
}
```

### 控制訊號

```
     ┌─────────────────────────────┐
     │                             │
 HIGH├─┐                         ┌─┤
     │ │         20ms            │ │
 LOW └─┘                         └─┘
       └───────┬────────┬────────┘
               │  1.5ms │  (0度)
           (0.5ms)     (2.5ms)
           (180度)
```

### 360 度伺服馬達

```cpp
#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 9;

void setup() {
  myServo.attach(SERVO_PIN);
}

void loop() {
  // 0-90 是逆時針
  // 90 是停止
  // 90-180 是順時針
  myServo.write(0);    // 全速逆時針
  delay(2000);
  myServo.write(90);   // 停止
  delay(1000);
  myServo.write(180);  // 全速順時針
  delay(2000);
}
```

## 步進馬達控制

### 步進馬達類型

| 類型 | 線數 | 特點 |
|------|------|------|
| 單極性 | 5/6 | 繞線簡單，效率低 |
| 雙極性 | 4 | 效率高，需要 H 橋 |

### Arduino ULN2003 驅動

```cpp
#include <Stepper.h>

const int STEPS = 2048;  // 28BYJ-48 每圈步數
const int IN1 = 8;
const int IN2 = 9;
const int IN3 = 10;
const int IN4 = 11;

Stepper myStepper(STEPS, IN1, IN3, IN2, IN4);

void setup() {
  myStepper.setSpeed(10);  // RPM
}

void loop() {
  myStepper.step(STEPS);   // 順時針一圈
  delay(1000);
  myStepper.step(-STEPS);  // 逆時針一圈
  delay(1000);
}
```

### A4988 驅動範例

```cpp
const int STEP_PIN = 3;
const int DIR_PIN = 4;
const int ENABLE_PIN = 5;

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);  // 啟用馬達
}

void loop() {
  // 順時針 1000 步
  digitalWrite(DIR_PIN, HIGH);
  for (int i = 0; i < 1000; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000);
  }
  delay(1000);

  // 逆時針 1000 步
  digitalWrite(DIR_PIN, LOW);
  for (int i = 0; i < 1000; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000);
  }
  delay(1000);
}
```

## PWM 控制原理

PWM（Pulse Width Modulation）是一種用數位訊號類比類比輸出的技術：

```cpp
// Arduino PWM
analogWrite(pin, value);  // value: 0-255

// 頻率：Arduino Uno 的 PWM 頻率
// 腳位 5, 6: 980 Hz
// 腳位 9, 10: 490 Hz
```

### PWM 應用

- 馬達轉速控制
- LED 亮度控制
- 音量控制
- 舵機角度控制

## 馬達驅動電路

### 為什麼需要驅動電路？

微控制器 GPIO 無法直接提供馬達所需電流：
- Arduino GPIO：40mA（最大）
- 小型馬達：通常需要 200mA 以上
- 大型馬達：可能需要 10A 以上

### 電晶體驅動

適用於小功率直流馬達：

```cpp
const int MOTOR_PIN = 9;
const int TRANSISTOR_PIN = 2;

void setup() {
  pinMode(MOTOR_PIN, OUTPUT);
  digitalWrite(TRANSISTOR_PIN, HIGH);  // 啟用電晶體
}

void loop() {
  int speed = map(analogRead(A0), 0, 1023, 0, 255);
  analogWrite(MOTOR_PIN, speed);
}
```

### MOSFET 驅動

適用於中等功率直流馬達：

```
┌─────────────────┐
│    Arduino      │
│                 │
│    Pin 9 ───────┐
│                 │       ┌────┐
│                 │       │    │
│                 └───────│ 10K│
│                         │    │
│                         └──┬─┘
│                            │
│    ┌───────────────────────┼──────────┐
│    │                       Gate       │
│    │     ┌─────────────────┴────────┐ │
│    │     │         MOSFET           │ │
│    │     │        (IRF540N)          │ │
│    │     │                         │ │
│    │     │    ┌───────────────┐    │ │
└────┼─────┼────┤   Drain       │    │ │
     │     │    │  ────────────  │    │ │
     │     │    │       ○       │    │ │
     │     │    │    Source     │    │ │
     │     │    └───────────────┘    │ │
     │     └────────────────────────┘ │
     │                                  │
     │         Motor                    │
     └──────────────────────────────────┘
```

## 其他致動器

### 電磁閥（Solenoid）

```cpp
const int SOLENOID_PIN = 9;

void setup() {
  pinMode(SOLENOID_PIN, OUTPUT);
}

void loop() {
  digitalWrite(SOLENOID_PIN, HIGH);  // 啟動
  delay(500);
  digitalWrite(SOLENOID_PIN, LOW);   // 釋放
  delay(1000);
}
```

### 氣泵和水泵

```cpp
// 幫浦控制（與馬達相同）
const int PUMP_PIN = 9;

void setup() {
  pinMode(PUMP_PIN, OUTPUT);
}

void pumpWater(int duration) {
  digitalWrite(PUMP_PIN, HIGH);
  delay(duration);
  digitalWrite(PUMP_PIN, LOW);
}
```

## 安全注意事項

1. **過電流保護**：使用適當額定電流的驅動晶片
2. **續流二極體**：直流馬達會產生反向 EMF，需要保護二極體
3. **散熱**：大功率馬達需要散熱片或風扇
4. **供電分開**：馬達供電和邏輯供電分開，避免干擾

## 小結

馬達控制是嵌入式系統的重要應用。正確選擇和使用馬達驅動電路，可以確保系統穩定運行：

1. **直流馬達**：簡單的速度控制，適合一般應用
2. **伺服馬達**：精確的角度控制
3. **步進馬達**：精確的位置控制，不需要回授

理解馬達類型和驅動方式，是設計可靠硬體系統的基礎。

---

**下一步**：[嵌入式系統網路連接](focus6.md)

## 延伸閱讀

- [DC Motor Control Tutorial](https://www.google.com/search?q=DC+motor+control+arduino+tutorial)
- [Servo Motor Guide](https://www.google.com/search?q=servo+motor+control+arduino)
- [Stepper Motor Tutorial](https://www.google.com/search?q=stepper+motor+arduino+tutorial)