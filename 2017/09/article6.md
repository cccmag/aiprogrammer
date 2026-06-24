# 最佳化理論基礎

## 最佳化問題

最佳化問題是找到使目標函數最小化（或最大化）的變數值。

minimize f(x)
subject to g(x) = 0
           h(x) >= 0

## 無制約優化

### 梯度下降

```python
def gradient_descent(gradient_fn, x_init, lr=0.1, n_iter=100, tolerance=1e-6):
    x = x_init
    for i in range(n_iter):
        grad = gradient_fn(x)
        x_new = x - lr * grad

        if abs(x_new - x) < tolerance:
            print(f"Converged at iteration {i}")
            break

        x = x_new
    return x

# 範例：f(x) = x^2, grad = 2x
def f(x):
    return x ** 2

def grad_f(x):
    return 2 * x

x_opt = gradient_descent(grad_f, x_init=10)
print(f"Optimal x: {x_opt}")
```

## 牛頓法

使用二階導數（Hessian）加速收斂。

```python
def newton_method(f, grad_f, hess_f, x_init, n_iter=10):
    x = x_init
    for _ in range(n_iter):
        g = grad_f(x)
        h = hess_f(x)
        x = x - g / h
    return x

# f(x) = x^2
# grad = 2x
# hess = 2
x_opt = newton_method(f, grad_f, lambda x: 2, x_init=10)
print(f"Optimal x: {x_opt}")
```

## 制約優化

### 拉格朗日乘數

```python
def lagrange_multiplier():
    """
    minimize f(x, y) = x^2 + y^2
    subject to g(x, y) = x + y - 1 = 0

    Lagrangian: L = x^2 + y^2 + λ(x + y - 1)

    ∂L/∂x = 2x + λ = 0  => x = -λ/2
    ∂L/∂y = 2y + λ = 0  => y = -λ/2
    ∂L/∂λ = x + y - 1 = 0  => -λ/2 - λ/2 = 0 => λ = 0 => x = y = 0

    但約束是 x + y = 1，所以正確解是 x = y = 0.5
    """
    pass
```

## 梯度下降變體

### Momentum

```python
def gradient_descent_momentum(gradient_fn, x_init, lr=0.1, momentum=0.9, n_iter=100):
    x = x_init
    v = 0

    for _ in range(n_iter):
        grad = gradient_fn(x)
        v = momentum * v - lr * grad
        x = x + v

    return x
```

### RMSProp

自適應學習率。

```python
def rmsprop(gradient_fn, x_init, lr=0.01, decay=0.9, eps=1e-8, n_iter=100):
    x = x_init
    g_sq = 0

    for _ in range(n_iter):
        grad = gradient_fn(x)
        g_sq = decay * g_sq + (1 - decay) * grad ** 2
        x = x - lr * grad / (np.sqrt(g_sq) + eps)

    return x
```

## 約束處理

### 罰函數法

```python
def penalty_method(objective_fn, constraint_fn, x_init, penalty=10, n_iter=100):
    x = x_init

    for _ in range(n_iter):
        # 添加約束懲罰
        def augmented(x):
            return objective_fn(x) + penalty * constraint_fn(x) ** 2

        # 使用梯度下降優化 augmented 函數
        x = gradient_descent(lambda x: x * 2 + penalty * 2 * constraint_fn(x), x)

        penalty *= 10  # 增加懲罰

    return x
```

## 限制記憶體

L-BFGS 是一種近似牛頓法，適合中等規模問題。

```python
from scipy.optimize import minimize

def objective(x):
    return (x[0] - 1) ** 2 + (x[1] - 2.5) ** 2

result = minimize(objective, x0=[0, 0], method='L-BFGS-B')
print(result.x)
```

## 總結

最佳化理論是機器學習的基礎：
- 梯度下降是最基本的優化器
- 牛頓法利用二階資訊加速收斂
- 現代方法如 Adam 結合多種技術
- 約束優化需要特殊處理