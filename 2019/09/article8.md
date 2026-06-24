# JAX：Google 的函式式深度學習框架

## 前言

JAX 是 Google 開發的一個函式式深度學習框架，結合了 Autograd 和 XLA，提供了高效且可組合的梯度計算能力。

## JAX 的設計

### 函式變換

```python
import jax
import jax.numpy as jnp

# 自動微分
def loss(params, x, y):
    pred = model(params, x)
    return jnp.mean((pred - y) ** 2)

grad_loss = jax.grad(loss)

# 計算梯度
grads = grad_loss(params, x, y)
```

### XLA 編譯

```python
from jax import jit

@jit
def fast_model(x):
    # JIT 編譯加速
    return model(x)
```

---

## 結語

JAX 的函式式設計吸引了對函式編程感興趣的開發者，提供了一種不同的深度學習編程範式。

---

**延伸閱讀**

- [JAX GitHub](https://www.google.com/search?q=Google+JAX+deep+learning)
- [JAX+tutorial](https://www.google.com/search?q=JAX+tutorial)