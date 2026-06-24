# 活化函數：ReLU、sigmoid、tanh 與更多

## 前言

活化函數（Activation Function）是類神經網路非線性能力的關鍵。如果沒有活化函數，不管網路有多少層，都只是線性變換。

## 常見活化函數

### 1. Sigmoid

```
σ(x) = 1 / (1 + e^(-x))
```

- 輸出範圍：(0, 1)
- 特點：平滑、梯度連續
- 缺點：梯度消失、計算成本高、非零均值

### 2. Tanh（雙曲正切）

```
tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
```

- 輸出範圍：(-1, 1)
- 特點：零均值
- 缺點：仍然有梯度消失問題

### 3. ReLU（線性修正單元）

```
ReLU(x) = max(0, x)
```

- 輸出範圍：[0, ∞)
- 特點：計算高效、緩解梯度消失
- 缺點：死亡 ReLU 問題

### 4. Leaky ReLU

```
LeakyReLU(x) = max(0.01x, x)
```

- 解決死亡 ReLU 問題
- 允許小的負梯度流通

## 比較

```
┌─────────────────────────────────────────────────────┐
│              活化函數比較                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│   Sigmoid:      ╭──╮                               │
│                ╱    ╲                              │
│     ─────────╱      ╲─────────                    │
│              0       1                             │
│                                                     │
│   Tanh:        ╱╲                                  │
│               ╱  ╲                                 │
│     ─────────╱    ╲──────────                      │
│             -1     1                               │
│                                                     │
│   ReLU:       ╱                                     │
│              ╱                                     │
│     ───────╱────────────                          │
│            0                                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Python 實現

```python
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(0, x)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def elu(x, alpha=1.0):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))
```

## 如何選擇

| 場景 | 推薦活化函數 |
|------|--------------|
| 隱藏層 | ReLU（預設） |
| 二分類輸出 | Sigmoid |
| 多分類輸出 | Softmax |
| 輸出需要負值 | Tanh |

## 梯度消失問題

梯度消失是深層網路的主要挑戰：

```python
# Sigmoid 的梯度
def sigmoid_gradient(x):
    s = sigmoid(x)
    return s * (1 - s)
```

當 x 很大或很小時，sigmoid 的梯度趨近於 0，導致前面層的權重几乎無法更新。

ReLU 的優勢在於其梯度要么是 0，要么是 1，不會有梯度消失問題。

## 結語

選擇正確的活化函數對網路的訓練至關重要。ReLU 是目前最常用的活化函數，但根據具體任務，sigmoid、tanh 或其他變體可能更合適。

下一篇文章將介紹反向傳播演算法，這是訓練類神經網路的核心。

---

## 延伸閱讀

- [活化函數詳解](https://www.google.com/search?q=activation+functions+neural+network)
- [ReLU 變體比較](https://www.google.com/search?q=Leaky+ReLU+ELU+activation)
- [深度學習中的梯度消失](https://www.google.com/search?q=vanishing+gradient+problem)

---

*本篇文章為「AI 程式人雜誌 2018 年 5 月號」類神經網路導論系列之一。*