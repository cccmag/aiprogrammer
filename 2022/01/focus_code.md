# 從零實作神經網路

## 前言

本篇文章完整實作一個多層感知器（MLP），包含反向傳播演算法和多種啟用函數，並在 XOR 問題上進行測試。全部程式碼約 150 行，不使用任何深度學習框架。

完整的 Python 實作請參考：[_code/neural_net.py](_code/neural_net.py)

## 核心程式碼

### 啟用函數

```python
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def relu(x):
    return x if x > 0 else 0.0

def gelu(x):
    return 0.5 * x * (1.0 + math.tanh(
        math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)))

def tanh(x):
    return math.tanh(x)
```

### 層的實作

```python
class Layer:
    def __init__(self, n_in, n_out, activation='sigmoid'):
        self.w = [[random.uniform(-1, 1) for _ in range(n_in)]
                  for _ in range(n_out)]
        self.b = [random.uniform(-1, 1) for _ in range(n_out)]
        # 選擇啟用函數及其導數
        self.fn, self.fn_prime = activations[activation]

    def forward(self, x):
        self.x = x  # 快取輸入
        self.z = [sum(w*xi for w, xi in zip(row, x)) + b
                  for row, b in zip(self.w, self.b)]
        self.a = [self.fn(v) for v in self.z]
        return self.a

    def backward(self, dz):
        # 轉換為對 z 的梯度
        dz = [d * self.fn_prime(z) for d, z in zip(dz, self.z)]
        self.dz = dz
        # 計算權重梯度
        self.dw = [[d * xi for xi in self.x] for d in dz]
        self.db = dz[:]
        # 傳遞到前一層
        dx = [sum(self.w[j][i] * dz[j] for j in range(len(dz)))
              for i in range(len(self.x))]
        return dx
```

### MLP 類別

```python
class MLP:
    def __init__(self, sizes, activations):
        self.layers = [Layer(sizes[i], sizes[i+1], activations[i])
                       for i in range(len(activations))]

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, y):
        # 均方誤差的梯度
        out = self.layers[-1].a
        dz = [2 * (o - t) for o, t in zip(out, y)]
        for layer in reversed(self.layers):
            dz = layer.backward(dz)

    def train(self, X, Y, epochs=10000, lr=0.5):
        for epoch in range(epochs):
            for x, y in zip(X, Y):
                self.forward(x)
                self.backward(y)
                for layer in self.layers:
                    layer.update(lr)
```

## 執行結果

測試 XOR 問題的四種啟用函數組合：

```
--- Sigmoid MLP (2-4-1) ---
[0, 0] -> 0.0053  (expected 0)
[0, 1] -> 0.9888  (expected 1)
[1, 0] -> 0.9892  (expected 1)
[1, 1] -> 0.0165  (expected 0)
✓ XOR 正確學習！

--- ReLU MLP (2-8-1) ---
[0, 1] -> 0.0000  (expected 1) ← Dead ReLU
其他三筆正確

--- Tanh MLP (2-4-1) ---
全部正確，收斂更快

--- GELU MLP (2-6-1) ---
全部正確，損失最低
```

## 設計要點

### 反向傳播的關鍵

1. **快取中間值**：前向傳播時快取 x、z、a，供反向傳播使用
2. **鏈式法則的正確應用**：每層計算 dL/dz，然後轉換為 dL/dw 和 dL/dx
3. **梯度累積與更新**：每個 batch 後更新權重

### Dead ReLU 現象

ReLU 版本的 MLP 無法正確學習 [0,1]→1 這個模式。這是經典的 Dead ReLU 問題——某些神經元在訓練過程中進入永不恢復的零輸出狀態。

解決方案包括：Leaky ReLU、較小的學習率、更好的初始化。

## 延伸實作方向

- 加入 Dropout 和 BatchNorm
- 實作 Softmax + Cross Entropy 損失
- 使用 CNN 進行圖像分類
- 使用 PyTorch 自動微分框架

---

## 延伸閱讀

- [完整原始碼](_code/neural_net.py)
- [Backpropagation 手算推導](https://www.google.com/search?q=backpropagation+derivation+example)
- [XOR 問題視覺化解釋](https://www.google.com/search?q=XOR+problem+neural+network+visualization)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」補充文章。*
