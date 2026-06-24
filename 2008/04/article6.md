# 類神經網路的基礎理論

## 神經網路的生物靈感

類神經網路（Neural Network）受人腦神經元結構啟發。雖然現在的人工神經網路與生物大腦有極大差異，但核心概念——大量簡單單元的並行計算——仍然保留。

## 神經元的數學模型

### M-P 神經元

1943 年，McCulloch 和 Pitts 提出了第一個神經元數學模型：

```
輸入: x₁, x₂, ..., xₙ
權重: w₁, w₂, ..., wₙ
偏差: b

淨輸入: z = Σ(wᵢ × xᵢ) + b
輸出: y = f(z)  // 啟動函數
```

### 啟動函數

```python
# 階梯函數（早期使用）
def step(x):
    return 1 if x >= 0 else 0

# Sigmoid 函數
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# tanh 函數
def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
```

## Perceptron

### 單層 Perceptron

Frank Rosenblatt 在 1957 年提出 Perceptron：

```python
class Perceptron:
    def __init__(self, n_inputs):
        self.weights = np.random.randn(n_inputs)
        self.bias = 0

    def predict(self, x):
        z = np.dot(x, self.weights) + self.bias
        return 1 if z >= 0 else 0

    def train(self, X, y, epochs=100, lr=0.1):
        for _ in range(epochs):
            for x_i, y_i in zip(X, y):
                prediction = self.predict(x_i)
                error = y_i - prediction
                self.weights += lr * error * x_i
                self.bias += lr * error
```

### 限制

單層 Perceptron 無法解決 XOR 問題，這導致了第一次 AI 寒冬。

## 多層感知器（MLP）

### 結構

```
輸入層          隱藏層          輸出層
┌───┐          ┌───┐
│x₁ │──┐    ┌──│h₁ │──┐    ┌──│y₁ │
└───┘  │    │  └───┘  │    │  └───┘
┌───┐  │    │  ┌───┐  │    │
│x₂ │──┼───→│──│h₂ │──┼───→│
└───┘  │    │  └───┘  │    │
┌───┐  │    │  ┌───┐  │    │
│x₃ │──┘    └──│h₃ │──┘    └──│y₂ │
└───┘          └───┘          └───┘
```

### 向前傳播

```python
def forward(x):
    self.z1 = np.dot(x, self.W1) + self.b1
    self.a1 = np.tanh(self.z1)
    self.z2 = np.dot(self.a1, self.W2) + self.b2
    self.a2 = self.softmax(self.z2)
    return self.a2
```

## 反向傳播

### 梯度下降

反向傳播使用梯度下降來更新權重：

```python
def backward(self, X, y, learning_rate):
    # 輸出層梯度
    delta2 = self.a2 - y

    # 權重更新
    dW2 = np.outer(self.a1, delta2)
    self.W2 -= learning_rate * dW2
    self.b2 -= learning_rate * delta2

    # 隱藏層梯度
    delta1 = delta2.dot(self.W2.T) * (1 - self.a1**2)

    dW1 = np.outer(X, delta1)
    self.W1 -= learning_rate * dW1
    self.b1 -= learning_rate * delta1
```

### 鏈式法則

反向傳播的數學基礎是鏈式法則：

```
∂L/∂W = ∂L/∂a × ∂a/∂z × ∂z/∂W
```

## 訓練技巧

### 權重初始化

```python
# Xavier 初始化
W = np.random.randn(n_in, n_out) * np.sqrt(2.0 / (n_in + n_out))
```

### 正規化

```python
# L2 正規化
loss = cross_entropy + lambda * np.sum(W**2)
```

### 學習率調整

```python
# 學習率衰減
learning_rate = initial_lr / (1 + decay * epoch)
```

## 深度學習的興起

### 為何現在才成功？

1. **資料量**：網路時代提供了大量訓練資料
2. **計算力**：GPU 加速訓練
3. **演算法進步**：ReLU、Dropout、Batch Normalization
4. **軟體框架**：TensorFlow、PyTorch 簡化開發

### 深度網路的優勢

- 自動特徵學習
- 表達能力強
- 可遷移學習

## 結論

類神經網路從 1940 年代的簡單模型，發展到今天的深度學習經歷了曲折的歷程。理解其基礎理論，對於掌握現代深度學習技術至關重要。

---

**延伸閱讀**

- [機器學習的數學基礎](article8.md)
- [Neural+network+tutorial](https://www.google.com/search?q=neural+network+tutorial)