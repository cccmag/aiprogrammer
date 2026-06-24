# 優化器：SGD、Adam、RMSprop

## 1. 梯度下降變體

### Batch Gradient Descent

```python
# 完整梯度（每次更新使用全部資料）
for i in range(epochs):
    grads = compute_full_gradient(X, y, model)
    theta = theta - learning_rate * grads
```

### Stochastic Gradient Descent (SGD)

```python
# 隨機梯度（每次更新使用一個樣本）
for i in range(epochs):
    for j in range(n_samples):
        idx = np.random.randint(n_samples)
        grads = compute_gradient(X[idx:idx+1], y[idx:idx+1], model)
        theta = theta - learning_rate * grads
```

### Mini-batch SGD

```python
# 小批量梯度（每次更新使用一批樣本）
for i in range(epochs):
    indices = np.random.permutation(n_samples)
    for start in range(0, n_samples, batch_size):
        batch_idx = indices[start:start+batch_size]
        grads = compute_gradient(X[batch_idx], y[batch_idx], model)
        theta = theta - learning_rate * grads
```

## 2. 動量（Momentum）

### 加速收斂

```python
class Momentum:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None

    def update(self, theta, grads):
        if self.v is None:
            self.v = np.zeros_like(theta)
        self.v = self.momentum * self.v + grads
        return theta - self.lr * self.v
```

動量累積過去的梯度方向，加速收斂並減少震盪。

## 3. RMSprop

### 自適應學習率

```python
class RMSprop:
    def __init__(self, lr=0.01, rho=0.9, epsilon=1e-8):
        self.lr = lr
        self.rho = rho
        self.epsilon = epsilon
        self.E = None

    def update(self, theta, grads):
        if self.E is None:
            self.E = np.zeros_like(theta)
        self.E = self.rho * self.E + (1 - self.rho) * grads ** 2
        return theta - self.lr * grads / (np.sqrt(self.E) + self.epsilon)
```

## 4. Adam

### 結合動量與 RMSprop

```python
class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None  # 第一動量估計
        self.v = None  # 第二動量估計
        self.t = 0     # 時間步

    def update(self, theta, grads):
        self.t += 1
        if self.m is None:
            self.m = np.zeros_like(theta)
            self.v = np.zeros_like(theta)

        # 更新動量估計
        self.m = self.beta1 * self.m + (1 - self.beta1) * grads
        self.v = self.beta2 * self.v + (1 - self.beta2) * grads ** 2

        # 偏差校正
        m_hat = self.m / (1 - self.beta1 ** self.t)
        v_hat = self.v / (1 - self.beta2 ** self.t)

        return theta - self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)
```

## 5. 比較與選擇

| 優化器 | 優點 | 缺點 | 適用場景 |
|--------|------|------|----------|
| SGD | 收斂穩定 | 收斂慢、易震盪 | 大型資料集 |
| Momentum | 加速收斂 | 需要調整動量 | 一般情況 |
| RMSprop | 自適應學習率 | 對初始學習率敏感 | RNN、非穩態 |
| Adam | 收斂快、穩定 | 可能泛化能力差 | 首選預設 |

## 6. 學習率排程

```python
# 指數衰減
lr = lr_0 * (decay_rate ** (epoch / decay_steps))

# Step 衰減
if epoch % step_size == 0:
    lr = lr * factor

# 余弦退火
lr = lr_min + (lr_max - lr_min) * (1 + cos(pi * t / T)) / 2
```

## 7. 小結

Adam 因其收斂快、穩定性，成為 2018 年的首選優化器。但最新研究指出 SGD + Momentum 在某些任務上有更好的泛化能力。

---

**參考資料**
- [Adam Optimizer Paper](https://www.google.com/search?q=Adam+optimizer+paper+2015)
- [Optimization for Deep Learning](https://www.google.com/search?q=deep+learning+optimizer+sgd+adam+comparison)