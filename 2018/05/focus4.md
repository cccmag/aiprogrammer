# 反向傳播演算法：梯度下降與誤差反向傳播

## 前言

反向傳播（Backpropagation）是訓練類神經網路的核心演算法。1986 年由 Rumelhart、Hinton 和 Williams 提出，使得訓練多層網路成為可能。

## 梯度下降法

### 問題定義

找到一組權重 W，使得損失函數 L(W) 最小化。

### 梯度下降更新

```
W = W - η * ∂L/∂W
```

其中 η 是學習率。

## 鏈式法則

反向傳播的基礎是微積分中的鏈式法則：

```
∂L/∂x = ∂L/∂y * ∂y/∂x
```

## 反向傳播推導

### 兩層網路示例

假設網路結構：輸入 → 隱藏層 → 輸出層

```python
# 前向傳播
z1 = np.dot(X, W1) + b1
a1 = sigmoid(z1)
z2 = np.dot(a1, W2) + b2
y_pred = sigmoid(z2)

# 計算損失（均方誤差）
loss = np.mean((y_pred - y)**2)
```

### 反向傳播步驟

```python
# 輸出層梯度
dy_pred = 2 * (y_pred - y) / y.shape[0]
dz2 = dy_pred * sigmoid_gradient(z2)

# 隱藏層梯度
dW2 = np.dot(a1.T, dz2)
db2 = np.sum(dz2, axis=0, keepdims=True)
da1 = np.dot(dz2, W2.T)
dz1 = da1 * sigmoid_gradient(z1)

# 更新權重
dW1 = np.dot(X.T, dz1)
db1 = np.sum(dz1, axis=0, keepdims=True)

W1 -= learning_rate * dW1
W2 -= learning_rate * dW2
```

## 完整實現

```python
class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_gradient(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

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
        y_pred = self.activations[-1]

        # 輸出層梯度
        delta = y_pred - y

        for i in range(len(self.weights) - 1, -1, -1):
            # 計算梯度
            dW = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m

            # 反向傳播 delta
            if i > 0:
                delta = np.dot(delta, self.weights[i].T)
                delta = delta * self.sigmoid_gradient(self.z_values[i-1])

            # 更新權重
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db
```

## 最佳化技巧

### 1. 動量（Momentum）

```python
# 添加動量項
velocity = momentum * velocity - learning_rate * gradient
weights += velocity
```

### 2. RMSprop

```python
# 自適應學習率
cache = decay_rate * cache + (1 - decay_rate) * gradient**2
weights -= learning_rate * gradient / (np.sqrt(cache) + eps)
```

### 3. Adam

結合動量和 RMSprop 的優點：

```python
# Adam 更新規則
m = beta1 * m + (1 - beta1) * gradient
v = beta2 * v + (1 - beta2) * gradient**2
m_hat = m / (1 - beta1**t)
v_hat = v / (1 - beta2**t)
weights -= learning_rate * m_hat / (np.sqrt(v_hat) + eps)
```

## 結語

反向傳播是深度學習的基石。理解反向傳播的原理對於設計和調試神經網路至關重要。

下一篇文章將介紹訓練神經網路的實用技巧。

---

## 延伸閱讀

- [反向傳播詳解](https://www.google.com/search?q=backpropagation+algorithm+tutorial)
- [梯度下降優化](https://www.google.com/search?q=gradient+descent+optimization+Adam)
- [深度學習書中的反向傳播](https://www.google.com/search?q=deep+learning+backpropagation+math)

---

*本篇文章為「AI 程式人雜誌 2018 年 5 月號」類神經網路導論系列之一。*