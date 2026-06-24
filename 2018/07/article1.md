# 神經網路基礎：從感知機到多層網路

## 1. 感知機：最簡單的神經元

### 生物神經元的簡化模型

感知機（Perceptron）由 Frank Rosenblatt 在 1957 年提出，是最簡單的神經網路模型：

```python
# 感知機偽程式碼
def perceptron(inputs, weights, bias):
    # 加權求和
    z = sum(i * w for i, w in zip(inputs, weights)) + bias
    # 階梯函數
    return 1 if z > 0 else 0
```

### 感知機的局限性

感知機只能處理線性可分的問題，無法解決 XOR 問題：

```python
# XOR 問題：感知機無法解決
x_data = [[0, 0], [0, 1], [1, 0], [1, 1]]
y_data = [0, 1, 1, 0]  # XOR：相同為 0，相異為 1
```

## 2. 多層感知機（MLP）

### 隱藏層的引入

增加隱藏層後，網路可以學習非線性決策邊界：

```python
# 多層感知機示意
class MLP:
    def __init__(self, input_size, hidden_size, output_size):
        # 輸入層到隱藏層
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros(hidden_size)
        # 隱藏層到輸出層
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros(output_size)
    
    def relu(self, z):
        return np.maximum(0, z)
    
    def forward(self, x):
        # 隱藏層
        self.z1 = np.dot(x, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        # 輸出層
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
```

## 3. 前饋傳播

### 訊號傳遞過程

輸入訊號從輸入層經過隱藏層到輸出層，每層都會經過線性變換和非線性激活：

```python
import numpy as np

def forward(X, W1, b1, W2, b2):
    # 隱藏層線性變換
    z1 = np.dot(X, W1) + b1
    # 隱藏層激活（ReLU）
    a1 = np.maximum(0, z1)
    # 輸出層線性變換
    z2 = np.dot(a1, W2) + b2
    # 輸出層激活（Softmax）
    a2 = np.exp(z2) / np.sum(np.exp(z2), axis=1, keepdims=True)
    return a2
```

## 4. 網路容量與表示能力

### 寬度 vs 深度

| 設計策略 | 優點 | 缺點 |
|----------|------|------|
| 寬網路（多神經元） | 單層可表示任意函數 | 參數量大幅增加 |
| 深網路（多層） | 參數效率高，層次化表示 | 訓練困難 |

## 5. 小結

從感知機到多層網路，神經網路解決了線性不可分的問題。現代深度學習的基礎就是堆疊多層非線性變換，讓網路能學習複雜的表示。

---

**參考資料**
- [Neural Network Introduction](https://www.google.com/search?q=perceptron+neural+network+history)
- [MLP Architecture](https://www.google.com/search?q=multilayer+perceptron+tensorflow+keras)