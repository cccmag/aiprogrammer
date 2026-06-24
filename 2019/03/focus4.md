# 4. 反向傳播演算法

## 反向傳播原理

反向傳播（Backpropagation）是訓練神經網路的核心演算法，透過鏈式法則計算損失函數對每個參數的梯度。

## 鏈式法則

$$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial w}$$

## 代碼實作

```python
import numpy as np

class MLP:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        self.gradients = {'weights': [], 'biases': []}

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def sigmoid_derivative(self, a):
        return a * (1 - a)

    def forward(self, X):
        self.activations = [X]
        self.z_values = []

        for w, b in zip(self.weights, self.biases):
            z = np.dot(self.activations[-1], w) + b
            self.z_values.append(z)
            a = self.sigmoid(z)
            self.activations.append(a)

        return self.activations[-1]

    def backward(self, X, y, learning_rate):
        m = X.shape[0]

        delta = self.activations[-1] - y

        for i in range(len(self.weights) - 1, -1, -1):
            dw = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m

            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db

            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * self.sigmoid_derivative(self.activations[i])

    def fit(self, X, y, epochs=1000, learning_rate=0.1):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, learning_rate)

            if epoch % 100 == 0:
                loss = np.mean((output - y) ** 2)
                print(f"Epoch {epoch}: Loss = {loss:.6f}")

    def predict(self, X):
        return (self.forward(X) >= 0.5).astype(int)
```

## 訓練 MLP

```python
X_xor = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y_xor = np.array([[0], [1], [1], [0]])

mlp = MLP([2, 4, 1])
mlp.fit(X_xor, y_xor, epochs=1000, learning_rate=0.5)

predictions = mlp.predict(X_xor)
print(f"\n預測結果:\n{predictions.flatten()}")
print(f"實際結果:\n{y_xor.flatten()}")
```

## 反向傳播數學推導

### 前饋階段

```
z^[1] = x * W^[1] + b^[1]
a^[1] = sigmoid(z^[1])

z^[2] = a^[1] * W^[2] + b^[2]
a^[2] = sigmoid(z^[2])

... (更多層)

z^[L] = a^[L-1] * W^[L] + b^[L]
a^[L] = sigmoid(z^[L])
```

### 輸出層梯度

假設使用 MSE 損失函數：
$$L = \frac{1}{2}(y - \hat{y})^2$$

對輸出層的梯度：
$$\frac{\partial L}{\partial a^{[L]}} = -(y - a^{[L]})$$
$$\frac{\partial L}{\partial z^{[L]}} = \frac{\partial L}{\partial a^{[L]}} \cdot \frac{\partial a^{[L]}}{\partial z^{[L]}}$$

### 隱藏層梯度

$$\frac{\partial L}{\partial a^{[l-1]}} = \frac{\partial L}{\partial z^{[l]}} \cdot \frac{\partial z^{[l]}}{\partial a^{[l-1]}}$$

### 權重更新

$$W^{[l]} = W^{[l]} - \alpha \cdot \frac{\partial L}{\partial W^{[l]}}$$

## 梯度消失問題

當網路層數增加時，梯度在反向傳播過程中會指数衰減，導致前面的層難以學習。

解決方案：
- 使用 ReLU 激活函數
- Batch Normalization
- 殘差連接（ResNet）
- LSTM/GRU（序列模型）

## 參考資源

- https://www.google.com/search?q=backpropagation+neural+network+Python+implementation+2019
- https://www.google.com/search?q=backpropagation+chain+rule+gradient+descent+2019
- https://www.google.com/search?q=vanishing+gradient+problem+backpropagation+2019