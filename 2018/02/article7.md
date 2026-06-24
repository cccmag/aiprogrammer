# 類神經網路原理

## 簡介

類神經網路（Neural Network）受人腦神經元啟發，是深度學習的基礎。本篇介紹神經元模型、網路結構和學習演算法。

## 神經元模型

### M-P 神經元

```
輸入 x1 ──┐
輸入 x2 ──┤
輸入 x3 ──┼──→ Σ (加權和) → 激活函數 → 輸出
         │
權重 w1 ──┤
權重 w2 ──┤
權重 w3 ──┘
偏差 b ───────────→
```

### 數學表示

```
output = activation(sum(xi * wi) + b)
```

### Python 實作

```python
import numpy as np

class Neuron:
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size)
        self.bias = np.random.randn()

    def forward(self, x):
        z = np.dot(x, self.weights) + self.bias
        return self.activation(z)

    def activation(self, z):
        return 1 / (1 + np.exp(-z))  # Sigmoid

x = np.array([1.0, 2.0, 3.0])
neuron = Neuron(3)
output = neuron.forward(x)
print(f"輸出: {output}")
```

## 激活函數

### Sigmoid

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
```

適用於二元分類，輸出 0-1。

### Tanh

```python
def tanh(z):
    return np.tanh(z)
```

輸出 -1 到 1，收斂較快。

### ReLU（線性整流單元）

```python
def relu(z):
    return np.maximum(0, z)
```

現今最常用，計算快速。

### Softmax

```python
def softmax(z):
    exp_z = np.exp(z - np.max(z))  # 數值穩定化
    return exp_z / exp_z.sum()
```

用於多類別分類，輸出機率分布。

## 網路結構

### 多層感知器（MLP）

```
輸入層 ───→ 隱藏層 1 ───→ 隱藏層 2 ───→ 輸出層
 (784)        (256)         (128)         (10)
```

```python
# 使用 Keras 建構 MLP
from keras.models import Sequential
from keras.layers import Dense

model = Sequential([
    Dense(256, activation='relu', input_shape=(784,)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])
```

### 前饋傳播（Forward Propagation）

```python
import numpy as np

# 簡化版前饋網路
def forward(X, weights, biases):
    activations = [X]

    for w, b in zip(weights, biases):
        z = np.dot(activations[-1], w) + b
        a = relu(z)
        activations.append(a)

    return activations
```

## 損失函數

### 均方誤差（MSE）

用於迴歸問題：

```python
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

### 交叉熵（Cross-Entropy）

用於分類問題：

```python
def cross_entropy(y_true, y_pred):
    epsilon = 1e-15  # 避免 log(0)
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred))
```

## 梯度下降

### 學習過程

```
1. 前饋傳播：計算預測輸出
2. 計算損失：衡量預測與實際的差距
3. 反向傳播：計算梯度
4. 更新權重：沿梯度方向調整
```

### 梯度下降更新

```python
# 權重更新公式
# w = w - learning_rate * gradient

learning_rate = 0.01

for epoch in range(1000):
    # 前饋
    y_pred = forward(X)

    # 計算梯度
    gradients = compute_gradients(X, y_true, y_pred)

    # 更新權重
    for w in weights:
        w -= learning_rate * w.grad
```

### 批次大小

- **SGD**：每筆資料更新一次
- **Mini-batch**：每批次更新一次
- **Batch**：整個資料集更新一次

## 反向傳播

```python
# 簡化版反向傳播
def backward(y_true, y_pred, activations, weights):
    m = y_true.shape[0]

    # 輸出層梯度
    delta = y_pred - y_true

    gradients = []
    for i in range(len(weights)-1, -1, -1):
        # 計算梯度
        grad = np.dot(activations[i].T, delta) / m

        # 反向傳播
        delta = np.dot(delta, weights[i].T)
        delta = delta * relu_derivative(activations[i])

        gradients.append(grad)

    return gradients[::-1]
```

## 訓練技巧

### 正規化

防止過擬合：

```python
from keras.regularizers import l2

model.add(Dense(256, activation='relu',
                kernel_regularizer=l2(0.01)))
```

### Dropout

隨機關閉部分神經元：

```python
from keras.layers import Dropout

model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))  # 50% 的神經元會被關閉
```

### Early Stopping

當驗證集 loss 不再下降時停止訓練：

```python
from keras.callbacks import EarlyStopping

early_stop = EarlyStopping(monitor='val_loss', patience=10)
model.fit(X_train, y_train, callbacks=[early_stop])
```

## 練習題

1. 實現一個單層神經元進行 AND 運算
2. 實現 Sigmoid 和 ReLU 函數
3. 手動實現前饋傳播
4. 理解梯度的物理意義