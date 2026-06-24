# 1. 感知器原理

## 感知器歷史

感知器由 Frank Rosenblatt 在 1957 年提出，是類神經網路的基礎單元。早期被視為能夠學習任何任務的萬能模型，但很快就發現了其局限性（Minsky & Papert, 1969）。

## 感知器模型

感知器接收多個輸入，每個輸入有其對應權重：

```
     x1 ── w1 ─┐
     x2 ── w2 ─┼─→ Σ ──→ activation ──→ output
     x3 ── w3 ─┘         ↑
                      bias
```

## 數學表示

```
z = w1*x1 + w2*x2 + w3*x3 + b
y = activation(z)
```

## 從零實作感知器

```python
import numpy as np

class Perceptron:
    def __init__(self, n_inputs):
        self.weights = np.random.randn(n_inputs) * 0.01
        self.bias = 0

    def forward(self, x):
        z = np.dot(x, self.weights) + self.bias
        return self.step_function(z)

    def step_function(self, z):
        return np.where(z >= 0, 1, 0)

    def predict(self, X):
        return np.array([self.forward(x) for x in X])
```

## AND 邏輯閘學習

```python
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y = np.array([0, 0, 0, 1])

perceptron = Perceptron(n_inputs=2)

for epoch in range(100):
    for x, label in zip(X, y):
        prediction = perceptron.forward(x)
        error = label - prediction

        perceptron.weights += 0.1 * error * x
        perceptron.bias += 0.1 * error

predictions = perceptron.predict(X)
print(f"預測結果: {predictions}")
print(f"實際結果: {y}")
```

## 感知器收斂定理

感知器收斂定理證明：如果資料線性可分，感知器必定在有限步驟內收斂。

## 感知器的局限性

感知器只能解決線性可分問題，無法解決 XOR 問題：

```python
X_xor = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y_xor = np.array([0, 1, 1, 0])

perceptron = Perceptron(n_inputs=2)
for epoch in range(100):
    for x, label in zip(X_xor, y_xor):
        prediction = perceptron.forward(x)
        error = label - prediction
        perceptron.weights += 0.1 * error * x
        perceptron.bias += 0.1 * error

predictions = perceptron.predict(X_xor)
print(f"XOR 預測結果: {predictions}")
print(f"XOR 實際結果: {y_xor}")
print("感知器無法解決 XOR 問題！")
```

## 突破線性限制

解決方案：使用多層感知器（MLP），透過隱藏層學習非線性表示。

## 參考資源

- https://www.google.com/search?q=perceptron+neural+network+原理+Python+2019
- https://www.google.com/search?q=perceptron+learning+algorithm+implementation+2019
- https://www.google.com/search?q=perceptron+XOR+problem+linear+separable+2019