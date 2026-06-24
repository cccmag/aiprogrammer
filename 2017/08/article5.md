# 梯度下降演算法

## 優化的基本概念

機器學習的目標是最小化（或最大化）一個目標函數。梯度下降是最常用的優化方法。

```python
# 假設目標函數
def f(x):
    return x**2

# 梯度（導數）
def gradient(x):
    return 2 * x
```

## 基本梯度下降

```python
def gradient_descent(gradient_fn, x_init, learning_rate, n_iterations):
    x = x_init
    history = [x]

    for _ in range(n_iterations):
        grad = gradient_fn(x)
        x = x - learning_rate * grad
        history.append(x)

    return x, history

# 最小化 f(x) = x^2
# 梯度：f'(x) = 2x
# 最小值在 x = 0

x_init = 10
learning_rate = 0.1
n_iterations = 50

x_opt, history = gradient_descent(gradient, x_init, learning_rate, n_iterations)
print(f"最優解: x = {x_opt:.6f}")
print(f"最小值: f(x) = {x_opt**2:.6f}")
```

## 學習率的影響

```python
import numpy as np

def f(x):
    return x**2

def gradient(x):
    return 2 * x

def run_gradient_descent(lr, n_iter=20):
    x = 10
    history = [x]
    for _ in range(n_iter):
        x = x - lr * gradient(x)
        history.append(x)
    return history

print("學習率過大 (lr=1.1，可能震盪或發散):")
history = run_gradient_descent(1.1)
print(f"  最終 x: {history[-1]:.2f}")

print("\n學習率適當 (lr=0.1):")
history = run_gradient_descent(0.1)
print(f"  最終 x: {history[-1]:.6f}")

print("\n學習率過小 (lr=0.01，收斂慢):")
history = run_gradient_descent(0.01)
print(f"  最終 x: {history[-1]:.2f}")
```

## 批量梯度下降

使用全部資料計算梯度。

```python
# 線性迴歸的梯度下降

def compute_gradient(X, y, w):
    """計算均方誤差損失的梯度"""
    n = len(y)
    predictions = X @ w
    error = predictions - y
    gradient = (2/n) * X.T @ error
    return gradient

def batch_gradient_descent(X, y, learning_rate=0.01, n_iterations=1000):
    n, d = X.shape
    w = np.zeros(d)

    for _ in range(n_iterations):
        grad = compute_gradient(X, y, w)
        w = w - learning_rate * grad

    return w
```

## 隨機梯度下降（SGD）

每次使用一個樣本。

```python
import random

def sgd(X, y, learning_rate=0.01, n_iterations=1000):
    n, d = X.shape
    w = np.zeros(d)

    for _ in range(n_iterations):
        i = random.randint(0, n-1)  # 隨機選擇一個樣本
        xi, yi = X[i:i+1], y[i:i+1]

        prediction = xi @ w
        error = prediction - yi
        grad = 2 * xi.T @ error

        w = w - learning_rate * grad.flatten()

    return w
```

## Mini-batch 梯度下降

每次使用一批樣本。

```python
def mini_batch_gd(X, y, batch_size=32, learning_rate=0.01, n_iterations=1000):
    n, d = X.shape
    w = np.zeros(d)

    for _ in range(n_iterations):
        indices = np.random.choice(n, batch_size, replace=False)
        X_batch, y_batch = X[indices], y[indices]

        prediction = X_batch @ w
        error = prediction - y_batch
        grad = (2/batch_size) * X_batch.T @ error

        w = w - learning_rate * grad

    return w
```

## 動量（Momentum）

加速收斂，避免震盪。

```python
def gd_with_momentum(gradient_fn, x_init, lr=0.01, momentum=0.9, n_iter=100):
    x = x_init
    v = 0

    for _ in range(n_iter):
        grad = gradient_fn(x)
        v = momentum * v - lr * grad  # 動量更新
        x = x + v

    return x
```

## Adam 優化器（2014）

自適應學習率方法。

```python
def adam(gradient_fn, x_init, lr=0.001, beta1=0.9, beta2=0.999,
         epsilon=1e-8, n_iter=1000):
    x = x_init
    m = 0  # 第一動量
    v = 0  # 第二動量
    t = 0

    for i in range(1, n_iter + 1):
        t += 1
        grad = gradient_fn(x)

        m = beta1 * m + (1 - beta1) * grad  # 更新第一動量
        v = beta2 * v + (1 - beta2) * grad**2  # 更新第二動量

        m_hat = m / (1 - beta1**t)  # 偏差修正
        v_hat = v / (1 - beta2**t)

        x = x - lr * m_hat / (np.sqrt(v_hat) + epsilon)

    return x
```

## 收斂判斷

```python
def should_stop(old_loss, new_loss, tolerance=1e-6):
    return abs(new_loss - old_loss) < tolerance
```

## 總結

梯度下降是機器學習優化的核心：
- **批量 GD**：穩定，但慢
- **SGD**：快，但震盪
- **Mini-batch GD**：平衡速度與穩定性
- **Momentum**：加速收斂
- **Adam**：目前最流行的自適應方法

選擇合適的學習率與優化器對訓練成功至關重要。