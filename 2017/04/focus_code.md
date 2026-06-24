# 程式碼範例：從零實現神經網路

## 程式碼說明

本目录包含从零实现神经网络的完整代码，使用纯 Python 和 NumPy，不依赖任何深度学习框架。

## 檔案清單

- `neural_network.py` - 神經網路實現
- `test.sh` - 測試腳本

## 主要功能

1. **神經網路類別**：多層感知器實現
2. **激活函數**：ReLU、Sigmoid、Softmax
3. **損失函數**：交叉熵損失
4. **反向傳播**：完整的梯度計算與參數更新
5. **訓練功能**：Mini-batch 梯度下降

## 使用方式

```bash
python3 neural_network.py
```

## 重點程式碼

### 初始化（Xavier 方法）

```python
def _init_weights(self):
    np.random.seed(42)
    self.weights = []
    self.biases = []
    for i in range(len(self.layer_sizes) - 1):
        w = np.random.randn(self.layer_sizes[i], self.layer_sizes[i+1]) * \
            np.sqrt(2.0 / self.layer_sizes[i])
        b = np.zeros((1, self.layer_sizes[i+1]))
        self.weights.append(w)
        self.biases.append(b)
```

### ReLU 激活函數

```python
def relu(z):
    return np.maximum(0, z)

def relu_gradient(z):
    return (z > 0).astype(float)
```

### Softmax 輸出層

```python
def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)
```

### 訓練過程

```python
def train(self, X, y, epochs=100, learning_rate=0.01):
    for epoch in range(epochs):
        # Forward pass
        A = X
        caches = [A]
        for w, b in zip(self.weights, self.biases):
            Z = A @ w + b
            caches.append(Z)
            A = softmax(Z) if Z is last layer else relu(Z)

        # Compute loss
        loss = -np.mean(np.sum(y * np.log(A + 1e-8), axis=1))

        # Backward pass
        # ... (見 neural_network.py 完整實現)
```

## 測試

執行 `python3 neural_network.py` 將訓練一個簡單的 MLP 在模擬數據上，顯示損失的收斂過程。

## 延伸學習

- 嘗試調整隱藏層大小與層數
- 實現不同的激活函數
- 添加 L2 正則化和 Dropout