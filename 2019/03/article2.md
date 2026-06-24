# MSE 與交叉熵損失函數

## 損失函數的重要性

損失函數衡量模型預測與實際值的差異，是訓練過程中最小化的目標。

## 均方誤差（MSE）

$$MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

```python
import numpy as np

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def mse_derivative(y_true, y_pred):
    return 2 * (y_pred - y_true) / len(y_true)

y_true = np.array([1.0, 2.0, 3.0, 4.0])
y_pred = np.array([1.1, 1.9, 3.2, 3.8])

error = mse(y_true, y_pred)
print(f"MSE: {error:.4f}")
```

## 交叉熵（Cross Entropy）

### 二元交叉熵（Binary Cross Entropy）

$$BCE = -\frac{1}{n}\sum_{i=1}^{n}[y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)]$$

```python
def binary_cross_entropy(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

y_true = np.array([0, 0, 1, 1])
y_pred = np.array([0.1, 0.2, 0.8, 0.9])

bce = binary_cross_entropy(y_true, y_pred)
print(f"Binary Cross Entropy: {bce:.4f}")
```

### 分類交叉熵（Categorical Cross Entropy）

$$CCE = -\sum_{i=1}^{n}\sum_{c=1}^{C}y_{ic}\log(\hat{y}_{ic})$$

```python
def categorical_cross_entropy(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.sum(y_true * np.log(y_pred))

y_true = np.array([[0, 0, 1], [1, 0, 0]])
y_pred = np.array([[0.1, 0.2, 0.7], [0.8, 0.1, 0.1]])

cce = categorical_cross_entropy(y_true, y_pred)
print(f"Categorical Cross Entropy: {cce:.4f}")
```

## Sparse Categorical Cross Entropy

當標籤是整數而非 one-hot 向量時使用：

```python
def sparse_categorical_cross_entropy(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    n = len(y_true)
    loss = -np.log(y_pred[np.arange(n), y_true])
    return np.mean(loss)

y_true = np.array([2, 0])
y_pred = np.array([[0.1, 0.2, 0.7], [0.8, 0.1, 0.1]])

scce = sparse_categorical_cross_entropy(y_true, y_pred)
print(f"Sparse CCE: {scce:.4f}")
```

## 比較 MSE 與 Cross Entropy

| 特性 | MSE | Cross Entropy |
|------|-----|---------------|
| 用途 | 迴歸 | 分類 |
| 梯度 | 容易梯度消失 | 梯度更穩定 |
| 輸出層 | 線性激活 | Softmax/Sigmoid |

## Cross Entropy 的梯度

使用 Cross Entropy 搭配 Sigmoid：

```python
def sigmoid_cross_entropy(z, y):
    a = 1 / (1 + np.exp(-z))
    return a - y

z = np.array([0.5, -0.3, 2.0])
y = np.array([1, 0, 1])

gradient = sigmoid_cross_entropy(z, y)
print(f"梯度: {gradient}")
```

使用 Cross Entropy 搭配 Softmax：

```python
def softmax_cross_entropy(z, y):
    exp_z = np.exp(z - np.max(z))
    softmax = exp_z / np.sum(exp_z)
    return softmax - y

z = np.array([[0.5, -0.3, 2.0], [-0.1, 0.8, -0.5]])
y = np.array([[0, 0, 1], [1, 0, 0]])

gradient = softmax_cross_entropy(z, y)
print(f"梯度: {gradient}")
```

## 實驗比較

```python
import matplotlib.pyplot as plt
import numpy as np

def compare_loss_functions():
    targets = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    predictions = np.linspace(0.01, 0.99, 100)

    mse_losses = []
    bce_losses = []

    for p in predictions:
        pred = np.array([p, p, p, p, p, p, p, p])
        mse_losses.append(mse(targets, pred))

        pred_clipped = np.clip(pred, 1e-15, 1-1e-15)
        bce = -np.mean(targets * np.log(pred_clipped) +
                      (1 - targets) * np.log(1 - pred_clipped))
        bce_losses.append(bce)

    plt.figure(figsize=(10, 6))
    plt.plot(predictions, mse_losses, label='MSE', linewidth=2)
    plt.plot(predictions, bce_losses, label='Binary Cross Entropy', linewidth=2)
    plt.xlabel('Predicted Probability')
    plt.ylabel('Loss')
    plt.title('MSE vs Binary Cross Entropy')
    plt.legend()
    plt.grid(True)
    plt.show()

compare_loss_functions()
```

## Keras 中的損失函數

```python
from tensorflow import keras

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

常用損失函數：
- `sparse_categorical_crossentropy`：多類分類
- `binary_crossentropy`：二元分類
- `mse` 或 `mae`：迴歸

## 參考資源

- https://www.google.com/search?q=MSE+cross+entropy+loss+function+neural+network+2019
- https://www.google.com/search?q=categorical+cross+entropy+softmax+gradient+2019
- https://www.google.com/search?q=loss+function+regression+classification+2019