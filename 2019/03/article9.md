# Batch Normalization

## 為什麼需要 Batch Normalization？

深度網路中，前面層的參數變化會導致後面層輸入分佈改變（Internal Covariate Shift），增加訓練難度。

## Batch Normalization 原理

對每個 mini-batch 進行標準化：

$$\mu_B = \frac{1}{m}\sum_{i=1}^{m}x_i$$
$$\sigma_B^2 = \frac{1}{m}\sum_{i=1}^{m}(x_i - \mu_B)^2$$
$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$$
$$y_i = \gamma\hat{x}_i + \beta$$

## 從零實作 BatchNorm

```python
import numpy as np

class BatchNormalization:
    def __init__(self, momentum=0.99, epsilon=1e-8):
        self.momentum = momentum
        self.epsilon = epsilon
        self.gamma = None
        self.beta = None
        self.running_mean = None
        self.running_var = None

    def forward(self, x, training=True):
        if self.gamma is None:
            self.gamma = np.ones(x.shape[1])
            self.beta = np.zeros(x.shape[1])
            self.running_mean = np.zeros(x.shape[1])
            self.running_var = np.ones(x.shape[1])

        if training:
            batch_mean = np.mean(x, axis=0)
            batch_var = np.var(x, axis=0)

            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * batch_mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * batch_var

            x_normalized = (x - batch_mean) / np.sqrt(batch_var + self.epsilon)
        else:
            x_normalized = (x - self.running_mean) / np.sqrt(self.running_var + self.epsilon)

        return self.gamma * x_normalized + self.beta

    def backward(self, gradient):
        x_normalized = (self.x - self.mean) / np.sqrt(self.var + self.epsilon)

        d_gamma = np.sum(gradient * x_normalized, axis=0)
        d_beta = np.sum(gradient, axis=0)

        return gradient * self.gamma
```

## Keras 中的 BatchNormalization

```python
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(64, input_shape=(784,)),
    layers.BatchNormalization(),
    layers.Activation('relu'),
    layers.Dense(64),
    layers.BatchNormalization(),
    layers.Activation('relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()
```

## BatchNorm 的效果

```python
def compare_with_without_batchnorm():
    from tensorflow.keras.datasets import mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
    x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

    model_without_bn = keras.Sequential([
        layers.Dense(128, input_shape=(784,)),
        layers.Activation('relu'),
        layers.Dense(64),
        layers.Activation('relu'),
        layers.Dense(10, activation='softmax')
    ])

    model_with_bn = keras.Sequential([
        layers.Dense(128, input_shape=(784,)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dense(64),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dense(10, activation='softmax')
    ])

    model_without_bn.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    model_with_bn.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

    print("訓練不含 BatchNorm 的模型...")
    history_without = model_without_bn.fit(x_train, y_train, epochs=5, verbose=0)

    print("訓練含 BatchNorm 的模型...")
    history_with = model_with_bn.fit(x_train, y_train, epochs=5, verbose=0)

    acc_without = model_without_bn.evaluate(x_test, y_test, verbose=0)[1]
    acc_with = model_with_bn.evaluate(x_test, y_test, verbose=0)[1]

    print(f"無 BatchNorm 測試準確率: {acc_without:.2%}")
    print(f"有 BatchNorm 測試準確率: {acc_with:.2%}")

compare_with_without_batchnorm()
```

## BatchNorm 的優點

1. **加速收斂**：可以使用更高的學習率
2. **穩定梯度**：減少梯度消失/爆炸
3. **正規化效果**：有一定的 Dropout 效果
4. **對初始化較不敏感**

## 訓練與推論模式

```python
model = keras.Sequential([
    layers.Dense(64, input_shape=(784,)),
    layers.BatchNormalization(),
    layers.Activation('relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

model.fit(x_train, y_train, epochs=5)

predictions = model.predict(x_test)
```

## Moving Average

BatchNorm 使用指數移動平均來估計全域統計量：

```python
running_mean = 0.99 * running_mean + 0.01 * batch_mean
running_var = 0.99 * running_var + 0.01 * batch_var
```

## Layer Normalization（比較）

Layer Normalization 對單一樣本的所有特徵進行標準化：

```python
def layer_norm(x):
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + 1e-8)
```

| 特性 | BatchNorm | LayerNorm |
|------|-----------|-----------|
| 標準化維度 | Batch 維度 | 特徵維度 |
| 需要 Batch | 是 | 否 |
| RNN 適用 | 否 | 是 |
| GAN 適用 | 是 | 一般 |

## 參考資源

- https://www.google.com/search?q=batch+normalization+neural+network+原理+2019
- https://www.google.com/search?q=BatchNormalization+Keras+TensorFlow+tutorial+2019
- https://www.google.com/search?q=batch+normalization+vs+layer+normalization+2019