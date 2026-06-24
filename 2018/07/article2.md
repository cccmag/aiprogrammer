# 反向傳播演算法詳解

## 1. 梯度下降優化

### 損失函數與優化目標

神經網路的訓練目標是最小化損失函數：

```python
# 均方誤差損失
def mse_loss(y_pred, y_true):
    return np.mean((y_pred - y_true) ** 2)

# 交叉熵損失
def cross_entropy_loss(y_pred, y_true):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred))
```

### 梯度下降更新

```python
# 梯度下降更新規則
W = W - learning_rate * gradient
```

## 2. 鏈式法則

### 複合函數的導數

反向傳播的核心是鏈式法則：

```python
# 假設：z = f(g(x))
# 則：dz/dx = dz/dg * dg/dx

# 例如：loss = softmax(w2 * relu(w1 * x))
# d_loss/d_w1 = d_loss/d_softmax * d_softmax/d_z2 * d_z2/d_relu * d_relu/d_z1 * d_z1/d_w1
```

## 3. 反向傳播推導

### 兩層網路的反向傳播

```python
def backward(X, y, a1, a2, W2):
    m = X.shape[0]

    # 輸出層梯度
    dz2 = a2 - y  # softmax + cross_entropy 的梯度
    dW2 = (1/m) * np.dot(a1.T, dz2)
    db2 = (1/m) * np.sum(dz2, axis=0, keepdims=True)

    # 隱藏層梯度
    da1 = np.dot(dz2, W2.T)
    dz1 = da1 * (a1 > 0)  # ReLU 梯度
    dW1 = (1/m) * np.dot(X.T, dz1)
    db1 = (1/m) * np.sum(dz1, axis=0, keepdims=True)

    return dW1, db1, dW2, db2
```

## 4. 矩陣形式推導

### 通用公式

對於層 l 的梯度：

```python
# 前向傳播快取
# z[l] = W[l] @ a[l-1] + b[l]
# a[l] = activation(z[l])

# 反向傳播
# da[l] = W[l+1].T @ dz[l+1]
# dz[l] = da[l] * activation_gradient(z[l])
# dW[l] = (1/m) * dz[l] @ a[l-1].T
# db[l] = (1/m) * sum(dz[l])
```

## 5. 實作要點

### 數值穩定性

```python
# Softmax 數值穩定版本
def softmax(z):
    z_shifted = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z_shifted)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

# Log Softmax（cross-entropy 用）
def log_softmax(z):
    z_shifted = z - np.max(z, axis=1, keepdims=True)
    return z_shifted - np.log(np.sum(np.exp(z_shifted), axis=1, keepdims=True))
```

### 梯度檢查

```python
# 數值梯度檢查
def gradient_check(model, X, y, epsilon=1e-7):
    for param_name, param in model.params.items():
        grad_numerical = np.zeros_like(param)
        for i in range(param.size):
            param_flat = param.flatten()
            param_flat[i] += epsilon
            param_reshaped = param_flat.reshape(param.shape)
            loss_plus = compute_loss(model, X, y, {param_name: param_reshaped})
            param_flat[i] -= 2*epsilon
            loss_minus = compute_loss(model, X, y, {param_name: param_reshaped})
            grad_numerical.flat[i] = (loss_plus - loss_minus) / (2*epsilon)
        # 比較 grad_numerical 與 model.grads[param_name]
```

## 6. 小結

反向傳播是深度學習的核心演算法，本質上是鏈式法則在計算圖上的高效實現。理解其數學推導對除錯和最佳化至關重要。

---

**參考資料**
- [Backpropagation Explained](https://www.google.com/search?q=backpropagation+explained+derivation)
- [Chain Rule Calculus](https://www.google.com/search?q=chain+rule+backpropagation+neural+network)