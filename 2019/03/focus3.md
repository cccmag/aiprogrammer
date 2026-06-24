# 3. 激活函數

## 為什麼需要激活函數？

如果沒有激活函數，多層網路只是線性變換的組合，無法學習非線性模式。

```
沒有激活函數: y = W3 * W2 * W1 * x = W * x (線性)
有激活函數: y = activation(W3 * activation(W2 * activation(W1 * x))) (非線性)
```

## Sigmoid 函數

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

```python
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

z = np.linspace(-10, 10, 100)
plt.figure(figsize=(10, 6))
plt.plot(z, sigmoid(z))
plt.title('Sigmoid Activation Function')
plt.xlabel('z')
plt.ylabel('sigmoid(z)')
plt.grid(True)
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5)
plt.axvline(x=0, color='r', linestyle='--', alpha=0.5)
plt.show()
```

特點：
- 輸出範圍 (0, 1)
- 常用於二元分類輸出層
- 梯度消失問題（梯度趨近於 0）

## Tanh 函數

$$\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$$

```python
def tanh(z):
    return np.tanh(z)

plt.figure(figsize=(10, 6))
plt.plot(z, tanh(z))
plt.title('Tanh Activation Function')
plt.xlabel('z')
plt.ylabel('tanh(z)')
plt.grid(True)
plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
plt.show()
```

特點：
- 輸出範圍 (-1, 1)
- 以 0 為中心，收斂更快
- 仍有梯度消失問題

## ReLU 函數

$$ReLU(z) = max(0, z)$$

```python
def relu(z):
    return np.maximum(0, z)

plt.figure(figsize=(10, 6))
plt.plot(z, relu(z))
plt.title('ReLU Activation Function')
plt.xlabel('z')
plt.ylabel('ReLU(z)')
plt.grid(True)
plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
plt.show()
```

特點：
- 計算高效
- 緩解梯度消失問題
- 但會有「死亡 ReLU」問題（梯度為 0）

## Leaky ReLU

$$LeakyReLU(z) = max(0.01z, z)$$

```python
def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

plt.figure(figsize=(10, 6))
plt.plot(z, leaky_relu(z))
plt.title('Leaky ReLU Activation Function')
plt.xlabel('z')
plt.ylabel('LeakyReLU(z)')
plt.grid(True)
plt.show()
```

## ELU（Exponential Linear Unit）

```python
def elu(z, alpha=1.0):
    return np.where(z > 0, z, alpha * (np.exp(z) - 1))

plt.figure(figsize=(10, 6))
plt.plot(z, elu(z))
plt.title('ELU Activation Function')
plt.xlabel('z')
plt.ylabel('ELU(z)')
plt.grid(True)
plt.show()
```

## Softmax 函數

$$\ softmax(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}} $$

```python
def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=-1, keepdims=True)

z = np.array([2.0, 1.0, 0.1])
print(f"Softmax: {softmax(z)}")
print(f"總和: {softmax(z).sum()}")
```

用途：
- 多類分類的輸出層
- 輸出為機率分佈

## 激活函數比較

| 函數 | 輸出範圍 | 梯度消失 | 計算效率 |
|------|----------|----------|----------|
| Sigmoid | (0, 1) | 嚴重 | 中 |
| Tanh | (-1, 1) | 中等 | 中 |
| ReLU | [0, ∞) | 輕微 | 高 |
| Leaky ReLU | (-∞, ∞) | 無 | 高 |
| ELU | (-α, ∞) | 無 | 中 |
| Softmax | (0, 1) | 嚴重 | 中 |

## 選擇建議

- **隱藏層**：ReLU（預設）、Leaky ReLU、ELU
- **二元分類輸出層**：Sigmoid
- **多類分類輸出層**：Softmax
- **迴歸輸出層**：線性（或不使用激活）

## 參考資源

- https://www.google.com/search?q=activation+function+ReLU+sigmoid+tanh+neural+network+2019
- https://www.google.com/search?q=softmax+activation+function+multi+class+classification+2019
- https://www.google.com/search?q=ReLU+vanishing+gradient+problem+neural+network+2019