# 激活函數比較

## 常用激活函數總覽

| 函數 | 公式 | 輸出範圍 | 梯度消失 | 計算效率 |
|------|------|----------|----------|----------|
| Sigmoid | 1/(1+e^-z) | (0,1) | 嚴重 | 中 |
| Tanh | (e^z-e^-z)/(e^z+e^-z) | (-1,1) | 中等 | 中 |
| ReLU | max(0,z) | [0,∞) | 輕微 | 高 |
| Leaky ReLU | max(0.01z,z) | (-∞,∞) | 無 | 高 |
| ELU | z if z>0 else α(e^z-1) | (-α,∞) | 無 | 中 |
| SELU | λ * ELU | (-λα,∞) | 無 | 中 |
| Swish | z * sigmoid(βz) | (-0.31,∞) | 輕微 | 中 |
| Mish | z * tanh(softplus(z)) | (-0.31,∞) | 無 | 中 |

## 數學實現

```python
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def tanh(z):
    return np.tanh(z)

def relu(z):
    return np.maximum(0, z)

def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

def elu(z, alpha=1.0):
    return np.where(z > 0, z, alpha * (np.exp(z) - 1))

def selu(z, alpha=1.67326, scale=1.0507):
    return scale * elu(z, alpha)

def swish(z, beta=1.0):
    return z * sigmoid(beta * z)

def mish(z):
    return z * np.tanh(np.log(1 + np.exp(z)))
```

## 繪製所有激活函數

```python
import matplotlib.pyplot as plt

z = np.linspace(-5, 5, 100)

functions = {
    'Sigmoid': sigmoid,
    'Tanh': tanh,
    'ReLU': relu,
    'Leaky ReLU': leaky_relu,
    'ELU': elu,
    'Swish': swish,
    'Mish': mish
}

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for ax, (name, func) in zip(axes[:7], functions.items()):
    ax.plot(z, func(z))
    ax.set_title(name)
    ax.grid(True)
    ax.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    ax.axvline(x=0, color='r', linestyle='--', alpha=0.3)

axes[7].axis('off')
plt.tight_layout()
plt.show()
```

## 梯度行為比較

```python
def plot_gradients():
    z = np.linspace(-5, 5, 100)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for name, func in [('ReLU', relu), ('Leaky ReLU', leaky_relu)]:
        gradient = np.gradient(func(z), z)
        axes[0].plot(z, gradient, label=name)

    axes[0].set_title('ReLU vs Leaky ReLU 梯度')
    axes[0].legend()
    axes[0].grid(True)

    for name, func in [('Sigmoid', sigmoid), ('Tanh', tanh), ('Swish', swish)]:
        gradient = np.gradient(func(z), z)
        axes[1].plot(z, gradient, label=name)

    axes[1].set_title('Sigmoid, Tanh, Swish 梯度')
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()

plot_gradients()
```

## 各函數的導數

```python
def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)

def tanh_derivative(z):
    return 1 - np.tanh(z) ** 2

def relu_derivative(z):
    return (z > 0).astype(float)

def leaky_relu_derivative(z, alpha=0.01):
    return np.where(z > 0, 1, alpha)

def elu_derivative(z, alpha=1.0):
    return np.where(z > 0, 1, elu(z, alpha) + alpha)

def swish_derivative(z, beta=1.0):
    s = sigmoid(beta * z)
    return beta * s + (1 - beta * z) * s * (1 - s)
```

## 使用時機

- **隱藏層**：ReLU（預設）、Leaky ReLU、ELU
- **輸出層（迴歸）**：線性（無激活）
- **輸出層（二元分類）**：Sigmoid
- **輸出層（多類分類）**：Softmax

## 實驗：不同激活函數效能

```python
from tensorflow import keras
from tensorflow.keras import layers

def create_model(activation):
    model = keras.Sequential([
        layers.Dense(128, activation=activation, input_shape=(784,)),
        layers.Dense(64, activation=activation),
        layers.Dense(10, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

activations = ['relu', 'sigmoid', 'tanh', 'elu']

for activation in activations:
    model = create_model(activation)
    model.fit(x_train, y_train, epochs=5, verbose=0)
    _, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"{activation}: {accuracy:.2%}")
```

## 參考資源

- https://www.google.com/search?q=activation+function+ReLU+sigmoid+tanh+comparison+2019
- https://www.google.com/search?q=Swish+Mish+activation+function+neural+network+2019
- https://www.google.com/search?q=neural+network+activation+function+selection+guideline+2019