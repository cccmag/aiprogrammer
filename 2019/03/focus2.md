# 2. 多層感知器 MLP

## MLP 架構

多層感知器（Multi-Layer Perceptron）由輸入層、多個隱藏層與輸出層組成。

```
輸入層(4) → 隱藏層1(8) → 隱藏層2(4) → 輸出層(3)
```

## MLP 解決 XOR

```python
import numpy as np

class MLP:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def forward(self, X):
        self.activations = [X]

        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            a = self.sigmoid(z)
            self.activations.append(a)

        return self.activations[-1]

    def predict(self, X):
        return (self.forward(X) >= 0.5).astype(int)
```

## 使用 MLP 解決 XOR

```python
X_xor = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y_xor = np.array([[0], [1], [1], [0]])

mlp = MLP([2, 4, 1])

for epoch in range(10000):
    mlp.forward(X_xor)

    output = mlp.activations[-1]
    error = y_xor - output

    for i in range(len(mlp.weights)):
        mlp.weights[i] += 0.5 * np.dot(mlp.activations[i].T, error * output * (1 - output))
        mlp.biases[i] += 0.5 * error.mean(axis=0)

predictions = mlp.predict(X_xor)
print(f"MLP XOR 預測結果:\n{predictions.flatten()}")
print(f"MLP XOR 實際結果:\n{y_xor.flatten()}")
```

## 前饋傳播（Forward Propagation）

```python
def forward_propagation(X, weights, biases):
    activations = [X]

    for w, b in zip(weights, biases):
        z = np.dot(activations[-1], w) + b
        a = sigmoid(z)
        activations.append(a)

    return activations
```

## 層級結構的好處

1. **表示能力**：隱藏層能學習中間表示
2. **非線性**：激活函數引入非線性
3. **通用近似**：MLP 能近似任何連續函數

## 網路容量

網路容量（Network Capacity）由以下因素決定：

- 層數
- 每層神經元數量
- 激活函數類型

容量過小：欠擬合（Underfitting）
容量過大：過擬合（Overfitting）

## 正規化與容量控制

```python
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

for hidden_layers in [[], [10], [10, 10], [10, 10, 10]]:
    layer_sizes = [2] + hidden_layers + [1]
    mlp = MLP(layer_sizes)

    for epoch in range(1000):
        mlp.forward(X_train)
        error = y_train - mlp.activations[-1]
        # 訓練邏輯...

    train_acc = (mlp.predict(X_train) == y_train).mean()
    test_acc = (mlp.predict(X_test) == y_test).mean()
    print(f"層數 {len(hidden_layers)}: 訓練={train_acc:.2%}, 測試={test_acc:.2%}")
```

## 參考資源

- https://www.google.com/search?q=multi+layer+perceptron+MLP+Python+implementation+2019
- https://www.google.com/search?q=neural+network+XOR+problem+solution+hidden+layer+2019
- https://www.google.com/search?q=MLP+architecture+forward+propagation+Python+2019