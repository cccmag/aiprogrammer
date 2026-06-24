# 4. JAX 函式式深度學習

## JAX 設計理念

JAX 不是傳統意義上的深度學習框架，而是一個用於高效數值計算的函式庫。它結合了 Autograd（自動微分）與 XLA（高效編譯），提供了獨特的函式式程式設計模型。

## 核心概念

### 1. 純函式式
JAX 函式應該沒有副作用，這讓並行化與編譯優化更容易。

### 2. 無狀態轉換
`jit`、`grad`、`pmap` 等轉換以函式方式套用。

### 3. 與 NumPy API 相容
熟悉 NumPy 的開發者可以無痛轉移到 JAX。

## 基本使用

```python
import jax
import jax.numpy as jnp
from jax import grad, jit

# 簡單的梯度計算
def sum_of_squares(x):
    return jnp.sum(x ** 2)

grad_sum_of_squares = grad(sum_of_squares)
print(grad_sum_of_squares(jnp.array([1.0, 2.0, 3.0])))
# 輸出：[2. 4. 6.]
```

## 即時編譯 (JIT)

```python
def slow_function(x):
    # 複雜的計算
    for _ in range(100):
        x = jnp.sin(x) + jnp.cos(x)
    return x

# JIT 編譯版本
fast_function = jit(slow_function)
```

## 自動向量化 (vmap)

```python
from jax import vmap

# 單一預測
def predict(params, x):
    return jnp.dot(x, params['w']) + params['b']

# 向量化預測（批次）
batched_predict = vmap(predict, in_axes=(None, 0))
```

## 自動並行化 (pmap)

```python
from jax import pmap

@pmap
def distributed_train_step(params, batch):
    # 在多個 GPU 上執行
    return params
```

## 學習率排程

```python
from jax import random

def create_learning_rate_schedule():
    def schedule(step):
        return 0.01 * (0.1 ** (step / 10000))
    return schedule
```

## 與 NumPy 的差異

```python
import numpy as np

# NumPy：可變陣列
np_array = np.array([1, 2, 3])
np_array[0] = 100  # OK

# JAX：不可變
jax_array = jnp.array([1, 2, 3])
# jax_array[0] = 100  # 錯誤！
jax_array = jax_array.at[0].set(100)  # 正確
```

## Flax：JAX 的神經網路庫

```python
# Flax 是 JAX 的高階庫，用於定義神經網路
# 安裝：pip install flax
```

## 適用場景

JAX 特別適合：
- 需要極致效能的研究
- 偏好函式式程式設計的開發者
- 需要精確梯度控制的任務

## 參考資源

- https://www.google.com/search?q=JAX+Google+functional+deep+learning+tutorial+2020
- https://www.google.com/search?q=JAX+autograd+XLA+jit+vmap+pmap+2020
- https://www.google.com/search?q=Flax+JAX+neural+network+library+2020