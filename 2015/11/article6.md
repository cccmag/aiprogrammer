# 步進馬達控制原理

## 步進馬達基礎

步進馬達是一種將電脈衝轉換為機械旋轉的馬達：

- **步進角**：每個脈衝旋轉的角度（如 1.8°）
- **保持扭矩**：不通電時的保持力
- **響�應**：由脈衝頻率控制

## 類型

### 單極性（Unipolar）

- 5 或 6 條導線
- 繞線中心抽頭
- 電流單向流動

### 雙極性（Bipolar）

- 4 條導線
- 無中心抽頭
- 電流雙向流動
- 扭矩更高

## 驅動方式

### 全步進（Full Step）

```cpp
// 4 步順序
int sequence[4][4] = {
  {1, 0, 0, 0},
  {0, 1, 0, 0},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
};
```

### 半步進（Half Step）

```cpp
// 8 步順序
int sequence[8][4] = {
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1}
};
```

## ULN2003 驅動

最常用的低成本驅動板：

```cpp
const int IN1 = 8;
const int IN2 = 9;
const int IN3 = 10;
const int IN4 = 11;

int stepSequence[4][4] = {
  {1, 0, 0, 0},
  {0, 1, 0, 0},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
};

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(IN1, stepSequence[i][0]);
    digitalWrite(IN2, stepSequence[i][1]);
    digitalWrite(IN3, stepSequence[i][2]);
    digitalWrite(IN4, stepSequence[i][3]);
    delay(10);
  }
}
```

## A4988 驅動

更精密的驅動器：

```cpp
const int STEP = 3;
const int DIR = 4;

void setup() {
  pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);
}

void step motor(int steps) {
  digitalWrite(DIR, HIGH);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP, LOW);
    delayMicroseconds(1000);
  }
}
```

## 常見問題

**馬達不轉？**
- 檢查電源電壓
- 確認線圈連接正確
- 檢查脈衝訊號

**方向錯誤？**
- 交換任意兩條線

**發熱過多？**
- 降低電壓
- 增加散熱

## 小結

步進馬達適合需要精確定位的應用，如 3D 列印機、CNC 機台。選擇合適的驅動器和電源供應器是成功的關鍵。

---

## 延伸閱讀

- [Stepper Motor Basics](https://www.google.com/search?q=stepper+motor+basics+tutorial)
- [A4988 Driver Tutorial](https://www.google.com/search?q=A4988+driver+tutorial)