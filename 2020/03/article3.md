# JAX 純函式式設計

## 函式轉換（Transformations）

JAX 的核心是函式式轉換：

```python
from jax import grad, jit, vmap, pmap

# 梯度
grad_fn = grad(lambda x: x ** 3)
print(grad_fn(2.0))  # 12.0

# JIT 編譯
@jit
def fast_fn(x):
    return jnp.sum(jnp.sin(x) + jnp.cos(x))
```

## vmap（自動向量化）

```python
from jax import vmap

# 單一預測
def predict_single(params, x):
    return jnp.dot(x, params['w']) + params['b']

# 批次預測
predict_batch = vmap(predict_single, in_axes=(None, 0))

params = {'w': jnp.array([1.0, 2.0]), 'b': 0.5}
x_batch = jnp.array([[1.0, 2.0], [3.0, 4.0]])
predictions = predict_batch(params, x_batch)  # [4.5, 11.5]
```

## pmap（自動並行化）

```python
from jax import pmap

@pmap
def distributed_matmul(x, y):
    return x @ y

# 在多個 GPU 上自動分配
```

## 純函式原則

```python
# 不可變資料
def pure_function(x):
    # x 是輸入，不會被修改
    return x ** 2

# 錯誤示範（副作用）
counter = 0
def impure_function(x):
    global counter
    counter += 1
    return x + counter
```

## 不可變更新

```python
array = jnp.array([1, 2, 3, 4, 5])

# 更新單一元素（不回改原陣列）
new_array = array.at[0].set(10)

# 不可變切片更新
new_array = array.at[1::2].add(100)
```

## 隨機數

```python
from jax import random

key = random.PRNGKey(42)
key, subkey = random.split(key)
x = random.normal(subkey, (3,))
```

## 訓練範例

```python
def loss_fn(params, x, y):
    pred = predict(params, x)
    return jnp.mean((pred - y) ** 2)

# 建立梯度函式
loss_and_grad = jit(grad(loss_fn), static_argnums=1)

# 訓練迴圈
for step in range(1000):
    loss, grads = loss_and_grad(params, x_train, y_train)
    params = {k: v - 0.001 * g for k, g, v in zip(params.keys(), grads.values(), params.values())}
```

## Flax 的簡化

```python
import flax.linen as nn

class MLP(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.Dense(128)(x)
        x = nn.relu(x)
        x = nn.Dense(10)(x)
        return x
```

## 參考資源

- https://www.google.com/search?q=JAX+grad+jit+vmap+tutorial+2020
- https://www.google.com/search?q=JAX+functional+programming+pure+functions+2020
- https://www.google.com/search?q=Flax+JAX+neural+network+MNIST+example+2020