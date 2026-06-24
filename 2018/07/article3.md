# 激活函數：ReLU、Sigmoid、tanh

## 1. 為什麼需要激活函數？

沒有激活函數，多層網路只是線性變換的組合，無法學習複雜模式。

```python
# 沒有激活函數：多層等於單層
# y = W3 @ W2 @ W1 @ x = W_effective @ x
# 永遠是線性變換

# 有了激活函數：
# y = activation(W3 @ activation(W2 @ activation(W1 @ x)))
# 可以學習非線性模式
```

## 2. Sigmoid 函數

### 公式與特性

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_gradient(z):
    s = sigmoid(z)
    return s * (1 - s)
```

- **輸出範圍**：(0, 1)
- **優點**：平滑、可微、輸出可解釋為機率
- **缺點**：梯度消失（兩端趨近於 0）、非零中心、計算成本高

## 3. Tanh 函數

### 公式與特性

```python
def tanh(z):
    return np.tanh(z)

def tanh_gradient(z):
    return 1 - np.tanh(z) ** 2
```

- **輸出範圍**：(−1, 1)
- **優點**：零中心、收斂快
- **缺點**：梯度消失問題仍然存在

## 4. ReLU 函數

### 公式與特性

```python
def relu(z):
    return np.maximum(0, z)

def relu_gradient(z):
    return (z > 0).astype(float)
```

- **輸出範圍**：[0, +∞)
- **優點**：計算快速、緩解梯度消失問題
- **缺點**：Dying ReLU（負半軸梯度為 0）、非零中心

## 5. Leaky ReLU 與 PReLU

### 解決 Dying ReLU 問題

```python
def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

def prelu(z, alpha):
    # alpha 可學習參數
    return np.where(z > 0, z, alpha * z)
```

## 6. ELU 函數

```python
def elu(z, alpha=1.0):
    return np.where(z > 0, z, alpha * (np.exp(z) - 1))
```

- 輸出接近零中心
- 對負值有小幅輸出，避免 dead neuron

## 7. 比較表

| 函數 | 輸出範圍 | 梯度特性 | 計算成本 |
|------|----------|----------|----------|
| Sigmoid | (0,1) | 兩端消失 | 中 |
| Tanh | (−1,1) | 兩端消失 | 中 |
| ReLU | [0,∞) | 正半軸穩定 | 低 |
| Leaky ReLU | (−∞,∞) | 全部存在 | 低 |
| ELU | (−α,∞) | 全部存在 | 中 |

## 8. 選擇建議

- **隱藏層**：首選 ReLU，可嘗試 Leaky ReLU/ELU
- **輸出層（機率）**：Sigmoid（二分類）、Softmax（多分類）
- **輸出層（回歸）**：線性或 ReLU（正值）

## 9. 小結

激活函數為網路引入非線性，是深度學習的關鍵元件。ReLU 因其簡單高效成為隱藏層的首選，但研究，持續探索更好的激活函數。

---

**參考資料**
- [Activation Functions Comparison](https://www.google.com/search?q=activation+functions+relu+sigmoid+tanh+comparison)
- [Dying ReLU Problem](https://www.google.com/search?q=dying+relu+problem+solution)