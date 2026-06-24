# 焦點文章 7：從零開始建構神經網路

## 前言

理解神經網路最好的方式是從零實現它。本章節將使用 Python 和 NumPy 從頭建構一個多層感知器，理解每個元件的運作原理。

## 網路結構

我們將實現一個三層 MLP：
- 輸入層：784 個神經元（MNIST 影像大小）
- 隱藏層：128 個神經元
- 輸出層：10 個神經元（數字 0-9）

## 初始化

```python
import numpy as np

class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            # Xavier 初始化
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
```

## 前向傳播

```python
    def forward(self, X):
        self.activations = [X]
        A = X
        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            Z = A @ w + b
            if i < len(self.weights) - 1:  # 隱藏層使用 ReLU
                A = np.maximum(0, Z)
            else:  # 輸出層使用 Softmax
                A = self.softmax(Z)
            self.activations.append(A)
        return A

    def softmax(self, Z):
        exp_z = np.exp(Z - np.max(Z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
```

## 損失函數

使用交叉熵損失：

```python
    def compute_loss(self, Y_pred, Y_true):
        m = Y_true.shape[0]
        loss = -np.sum(Y_true * np.log(Y_pred + 1e-9)) / m
        return loss
```

## 反向傳播

```python
    def backward(self, Y_true):
        m = Y_true.shape[0]
        delta = Y_pred - Y_true
        for i in reversed(range(len(self.weights))):
            dW = self.activations[i].T @ delta / m
            dB = np.sum(delta, axis=0, keepdims=True) / m
            if i > 0:
                delta = delta @ self.weights[i].T
                delta *= (self.activations[i] > 0)  # ReLU 梯度
            self.weights[i] -= self.lr * dW
            self.biases[i] -= self.lr * dB
```

## 訓練循環

```python
    def fit(self, X, Y, epochs, lr=0.01, batch_size=64):
        self.lr = lr
        for epoch in range(epochs):
            # Mini-batch
            indices = np.random.permutation(X.shape[0])
            for start in range(0, X.shape[0], batch_size):
                batch_idx = indices[start:start+batch_size]
                X_batch = X[batch_idx]
                Y_batch = Y[batch_idx]
                Y_pred = self.forward(X_batch)
                self.backward(Y_batch)
            loss = self.compute_loss(Y_pred, Y_batch)
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
```

## 預測

```python
    def predict(self, X):
        return np.argmax(self.forward(X), axis=1)
```

## 使用範例

```python
# 建立網路
net = NeuralNetwork([784, 128, 10])

# 訓練
net.fit(X_train, Y_train, epochs=100, lr=0.01)

# 預測
predictions = net.predict(X_test)
```

## 總結

從零實現神經網路加深了對每個元件的理解。現代深度學習框架如 TensorFlow 和 PyTorch 提供了更高層次的抽象，但理解底層原理對調試與最佳化至關重要。

## 延伸閱讀

- https://www.google.com/search?q=implement+neural+network+from+scratch+numpy
- https://www.google.com/search?q=backpropagation+implementation+python