# 1. 機器學習框架概覽

## 框架的基本功能

機器學習框架提供了：
- **張量運算**：多維陣列的高效計算
- **自動微分**：梯度計算的自動化
- **模型定義**：神經網路層的封裝
- **優化器**：參數更新的演算法
- **GPU 加速**：CUDA/cuDNN 整合

## 框架比較矩陣（2020 年初）

| 特性 | TensorFlow 2.x | PyTorch 1.4/1.5 | JAX |
|------|----------------|-----------------|-----|
| 開發者 | Google | Facebook | Google |
| 發布年份 | 2015 | 2016 | 2018 |
| 計算圖 | Eager + TF.function | 動態（Eager） | 追蹤（pmap/jit） |
| API 風格 | Keras (高階) | Pythonic (中階) | NumPy (低階) |
| 生態系 | 完整 | 中等 | 較小但快速成長 |
| 研究採用 | 高 | 極高 | 增加中 |
| 生產部署 | 優秀 | 良好 | 較少 |

## 張量運算比較

### NumPy 風格（相同）

```python
import numpy as np

# 三者都支援類似的語法
a = np.array([1, 2, 3])
b = a * 2
```

### TensorFlow

```python
import tensorflow as tf

a = tf.constant([1, 2, 3])
b = a * 2
```

### PyTorch

```python
import torch

a = torch.tensor([1, 2, 3])
b = a * 2
```

### JAX

```python
import jax.numpy as jnp

a = jnp.array([1, 2, 3])
b = a * 2
```

## GPU 支援

### TensorFlow

```python
# 自動使用 GPU
gpus = tf.config.list_physical_devices('GPU')
with tf.device('/GPU:0'):
    result = tf.matmul(a, b)
```

### PyTorch

```python
# 自動使用 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
a = a.to(device)
result = torch.matmul(a, b)
```

### JAX

```python
# 使用 jax.device_put 或 pmap
from jax import jit

@jit
def f(a, b):
    return a @ b
```

## 自動微分

### TensorFlow

```python
x = tf.Variable(2.0)
with tf.GradientTape() as tape:
    y = x ** 2
grad = tape.gradient(y, x)
```

### PyTorch

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)
```

### JAX

```python
from jax import grad

def f(x):
    return x ** 2

grad_f = grad(f)
print(grad_f(2.0))
```

## 參考資源

- https://www.google.com/search?q=TensorFlow+PyTorch+JAX+comparison+features+2020
- https://www.google.com/search?q=deep+learning+framework+history+TensorFlow+PyTorch+2015-2020
- https://www.google.com/search?q=machine+learning+framework+NumPy+API+autograd+2020