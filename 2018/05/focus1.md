# 感知器與神經元模型：人工神經元的起源

## 前言

類神經網路的概念起源於對生物神經系統的模拟。讓我們從最基礎的人工神經元說起。

## 生物神經元

```
┌─────────────────────────────────────────────────────┐
│                   生物神經元                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│    樹突 ─────► 細胞體 ────► 軸突                   │
│   (輸入)      (處理)      (輸出)                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

- **樹突**：接收其他神經元的信號
- **細胞體**：處理接收到的信號
- **軸突**：將輸出信號傳遞給其他神經元

## McCulloch-Pitts 神經元

1943 年，Warren McCulloch 和 Walter Pitts 提出了第一個人工神經元模型。

### 模型定義

```
output = 1 if (Σw_i * x_i + b) > θ
        0 otherwise
```

其中：
- x_i 是輸入
- w_i 是權重
- b 是偏置
- θ 是閾值

### Python 實現

```python
import numpy as np

def mcp_neuron(inputs, weights, bias, threshold):
    z = np.dot(inputs, weights) + bias
    return 1 if z > threshold else 0

# 測試：AND 運算
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
weights = np.array([0.5, 0.5])
bias = -0.75
threshold = 0

for x in inputs:
    print(f'{x} -> {mcp_neuron(x, weights, bias, threshold)}')
```

## 感知器（Perceptron）

1958 年，Frank Rosenblatt 發明了感知器，這是第一個能學習的類神經網路。

### 感知器學習規則

```
w_i = w_i + η * (y - ŷ) * x_i
```

其中 η 是學習率，y 是真實輸出，ŷ 是預測輸出。

### Python 實現

```python
class Perceptron:
    def __init__(self, n_inputs, learning_rate=0.1):
        self.weights = np.zeros(n_inputs)
        self.bias = 0
        self.lr = learning_rate

    def predict(self, x):
        z = np.dot(x, self.weights) + self.bias
        return 1 if z > 0 else 0

    def fit(self, X, y, epochs=100):
        for _ in range(epochs):
            for x_i, y_i in zip(X, y):
                pred = self.predict(x_i)
                error = y_i - pred
                self.weights += self.lr * error * x_i
                self.bias += self.lr * error
```

## 感知器的限制

### XOR 問題

感知器無法解決 XOR 問題：

| x1 | x2 | XOR |
|----|----|-----|
| 0  | 0  | 0   |
| 0  | 1  | 1   |
| 1  | 0  | 1   |
| 1  | 1  | 0   |

```
┌─────────────────────────────────────────────────────┐
│                   XOR 問題                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│         1 ◄───────────────► 0                     │
│         │                 │                        │
│         │    XOR 問題      │                        │
│         │   (非線性可分)   │                        │
│         ▼                 ▼                        │
│         0 ───────────────► 1                       │
│                                                     │
│   感知器只能解決線性可分的問題                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Minsky 的批評

1969 年，Marvin Minsky 和 Seymour Papert 在《感知器》一書中指出了這一限制，導致類神經網路研究陷入停滯。

## 解決方案：多層感知器

為了解決 XOR 問題，我們需要加入隱藏層，構成多層感知器（MLP）。

```
┌─────────────────────────────────────────────────────┐
│              兩層感知器解決 XOR                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│   輸入層     隱藏層     輸出層                       │
│                                                     │
│    x1 ──┬──► h1 ──┬──►                              │
│         │        │                                  │
│         └──► h2 ──┴──► y                            │
│    x2 ──┘                                           │
│                                                     │
│   隱藏層的神經元可以學習非線性決策邊界                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 結語

感知器雖然簡單，但它開創了類神經網路研究的先河。雖然感知器無法解決 XOR 問題，但這一限制促使研究者發明多層感知器，最終導致了深度學習的興起。

下一篇文章將介紹多層感知器（MLP）的原理和應用。

---

## 延伸閱讀

- [感知器歷史](https://www.google.com/search?q=perceptron+history+Rosenblatt)
- [McCulloch-Pitts 神經元](https://www.google.com/search?q=McCulloch+Pitts+neuron+1943)
- [XOR 問題證明](https://www.google.com/search?q=perceptron+XOR+proof+Minsky)

---

*本篇文章為「AI 程式人雜誌 2018 年 5 月號」類神經網路導論系列之一。*