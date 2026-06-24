# 權重初始化

## 為什麼初始化重要？

不當的初始化會導致梯度消失或爆炸，影響網路訓練。

## 零初始化（不建議）

所有權重設為零會導致對稱性問題：

```python
def zeros_initialization(fan_in, fan_out):
    return np.zeros((fan_in, fan_out))

w = zeros_initialization(784, 128)
print(f"零初始化: {w.shape}, 均值={w.mean()}")
```

## 隨機初始化

```python
def random_initialization(fan_in, fan_out):
    return np.random.randn(fan_in, fan_out)

w = random_initialization(784, 128)
print(f"隨機初始化: 均值={w.mean():.3f}, 標準差={w.std():.3f}")
```

## Xavier/Glorot 初始化

適用於 Sigmoid 和 Tanh：

$$W \sim N\left(0, \sqrt{\frac{2}{n_{in} + n_{out}}}\right)$$

```python
def xavier_initialization(fan_in, fan_out):
    std = np.sqrt(2.0 / (fan_in + fan_out))
    return np.random.randn(fan_in, fan_out) * std

w = xavier_initialization(784, 128)
print(f"Xavier 初始化: 均值={w.mean():.3f}, 標準差={w.std():.3f}")
```

## He 初始化

適用於 ReLU：

$$W \sim N\left(0, \sqrt{\frac{2}{n_{in}}}\right)$$

```python
def he_initialization(fan_in, fan_out):
    std = np.sqrt(2.0 / fan_in)
    return np.random.randn(fan_in, fan_out) * std

w = he_initialization(784, 128)
print(f"He 初始化: 均值={w.mean():.3f}, 標準差={w.std():.3f}")
```

## LeCun 初始化

適用於 SELU：

$$W \sim N\left(0, \sqrt{\frac{1}{n_{in}}}\right)$$

```python
def lecun_initialization(fan_in, fan_out):
    std = np.sqrt(1.0 / fan_in)
    return np.random.randn(fan_in, fan_out) * std

w = lecun_initialization(784, 128)
print(f"LeCun 初始化: 均值={w.mean():.3f}, 標準差={w.std():.3f}")
```

## 均勻分佈初始化

```python
def uniform_initialization(fan_in, fan_out, limit=1.0):
    return np.random.uniform(-limit, limit, (fan_in, fan_out))

def xavier_uniform(fan_in, fan_out):
    limit = np.sqrt(6.0 / (fan_in + fan_out))
    return np.random.uniform(-limit, limit, (fan_in, fan_out))

def he_uniform(fan_in, fan_out):
    limit = np.sqrt(6.0 / fan_in)
    return np.random.uniform(-limit, limit, (fan_in, fan_out))
```

## 比較初始化方法

```python
import matplotlib.pyplot as plt

def compare_initializations():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    initializations = {
        'Random': lambda i, o: np.random.randn(i, o) * 0.1,
        'Xavier': lambda i, o: np.random.randn(i, o) * np.sqrt(2.0 / (i + o)),
        'He': lambda i, o: np.random.randn(i, o) * np.sqrt(2.0 / i),
        'Zeros': lambda i, o: np.zeros((i, o))
    }

    fan_in, fan_out = 784, 128

    for ax, (name, init_func) in zip(axes.flat, initializations.items()):
        weights = init_func(fan_in, fan_out).flatten()
        ax.hist(weights, bins=50, alpha=0.7)
        ax.set_title(f'{name} Initialization\nmean={weights.mean():.4f}, std={weights.std():.4f}')
        ax.set_xlabel('Weight Value')
        ax.set_ylabel('Frequency')
        ax.grid(True)

    plt.tight_layout()
    plt.show()

compare_initializations()
```

## Keras 中的初始化

```python
from tensorflow.keras import layers
from tensorflow.keras.initializers import GlorotUniform, HeNormal

model = keras.Sequential([
    layers.Dense(128, activation='relu',
                 kernel_initializer=GlorotUniform(),
                 input_shape=(784,)),
    layers.Dense(64, activation='relu',
                 kernel_initializer=HeNormal()),
    layers.Dense(10, activation='softmax')
])
```

## SELU 與 Alpha Dropout

SELU 需要配合 LeCun 初始化和 Alpha Dropout 才能保證 Self-Normalizing 特性：

```python
model = keras.Sequential([
    layers.Dense(128, activation='selu',
                 kernel_initializer='lecun_normal',
                 input_shape=(784,)),
    layers.AlphaDropout(0.1),
    layers.Dense(64, activation='selu',
                 kernel_initializer='lecun_normal'),
    layers.AlphaDropout(0.1),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

## 初始化對訓練的影響

```python
def experiment_initializations():
    results = {}

    for name, init in [
        ('Random', 'random_normal'),
        ('Xavier', 'glorot_uniform'),
        ('He', 'he_uniform')
    ]:
        model = keras.Sequential([
            layers.Dense(128, activation='relu',
                        kernel_initializer=init,
                        input_shape=(784,)),
            layers.Dense(64, activation='relu',
                        kernel_initializer=init),
            layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam',
                     loss='sparse_categorical_crossentropy')

        history = model.fit(x_train, y_train, epochs=5, verbose=0)
        _, acc = model.evaluate(x_test, y_test, verbose=0)
        results[name] = acc
        print(f"{name}: {acc:.2%}")

    return results

experiment_initializations()
```

## 參考資源

- https://www.google.com/search?q=weight+initialization+Xavier+He+neural+network+2019
- https://www.google.com/search?q=Glorot+initialization+vs+He+initialization+2019
- https://www.google.com/search?q=neural+network+initialization+gradient+vanishing+2019