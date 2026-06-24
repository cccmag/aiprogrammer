# 機器學習的數學基礎

## 線性代數

### 向量與矩陣

```python
import numpy as np

# 向量
v = np.array([1, 2, 3])

# 矩陣
M = np.array([[1, 2], [3, 4], [5, 6]])

# 矩陣乘法
result = np.dot(M, v)

# 轉置
Mt = M.T
```

### 矩陣運算

```python
# 行列式
det = np.linalg.det(M)

# 逆矩陣
M_inv = np.linalg.inv(M)

# 特徵值與特徵向量
eigenvalues, eigenvectors = np.linalg.eig(M)
```

### 奇異值分解（SVD）

```python
# A = UΣVᵀ
U, s, Vt = np.linalg.svd(M)
```

## 機率統計

### 基本機率

```python
# 條件機率
# P(A|B) = P(A∩B) / P(B)

# 貝氏定理
# P(A|B) = P(B|A) × P(A) / P(B)
```

### 常見分佈

```python
from scipy import stats

# 常態分佈
X = stats.norm(loc=0, scale=1)
sample = X.rvs(1000)

# 最大似然估計
mu, std = stats.norm.fit(sample)
```

### 估計方法

```python
# 點估計
# 均值
mean = np.mean(X)

# 變異數（母體）
var = np.var(X, ddof=0)

# 變異數（樣本）
sample_var = np.var(X, ddof=1)
```

## 資訊理論

### 熵（Entropy）

```python
import scipy.stats as st

def entropy(p):
    return -np.sum(p * np.log2(p))

# 二元熵
p = [0.5, 0.5]
H = entropy(p)  # H = 1
```

### 交叉熵

```python
# H(P, Q) = -Σ P(x) log Q(x)
def cross_entropy(P, Q):
    return -np.sum(P * np.log2(Q))
```

### KL 散度

```python
# D(P||Q) = Σ P(x) log(P(x)/Q(x))
def kl_divergence(P, Q):
    return np.sum(P * np.log2(P / Q))
```

## 最佳化

### 梯度下降

```python
def gradient_descent(f, grad_f, x0, lr=0.1, max_iter=100):
    x = x0
    for _ in range(max_iter):
        x = x - lr * grad_f(x)
    return x
```

### 學習率衰減

```python
# 固定衰減
lr = initial_lr / (1 + decay * epoch)

# 指數衰減
lr = initial_lr * np.exp(-decay * epoch)

# 階梯衰減
lr = initial_lr * (0.5 ** (epoch // drop_every))
```

## 損失函數

### 均方誤差（MSE）

```python
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

### 交叉熵損失

```python
def cross_entropy_loss(y_true, y_pred):
    return -np.mean(y_true * np.log(y_pred))
```

### Hinge 損失

```python
def hinge_loss(y_true, y_pred):
    return np.mean(np.maximum(0, 1 - y_true * y_pred))
```

## 正規化

### L1 正規化（Lasso）

```python
def l1_penalty(W, lambda_):
    return lambda_ * np.sum(np.abs(W))
```

### L2 正規化（Ridge）

```python
def l2_penalty(W, lambda_):
    return lambda_ * np.sum(W ** 2)
```

### Elastic Net

```python
def elastic_net(W, lambda1, lambda2):
    return lambda1 * np.sum(np.abs(W)) + lambda2 * np.sum(W ** 2)
```

## 結論

機器學習的數學基礎包括線性代數、機率統計、資訊理論和最佳化理論。掌握這些數學工具，有助於理解和改進機器學習演算法。

---

**延伸閱讀**

- [類神經網路的基礎理論](article6.md)
- [Machine+learning+math+foundations](https://www.google.com/search?q=machine+learning+math+foundations)