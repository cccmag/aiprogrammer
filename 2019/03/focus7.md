# 7. 實戰：手寫數字辨識

## 專案概述

本實作使用 MLP 對 MNIST 手寫數字資料集進行分類。MNIST 是機器學習領域最著名的入門資料集之一。

## MNIST 資料集

MNIST 包含 70,000 張 28x28 灰階手寫數字圖片：
- 訓練集：60,000 張
- 測試集：10,000 張
- 10 個類別（0-9）

## 從零實作 MLP（NumPy）

```python
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist

class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def sigmoid_derivative(self, a):
        return a * (1 - a)

    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, z):
        return (z > 0).astype(float)

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def forward(self, X, activation='relu'):
        self.activations = [X]

        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]

            if i == len(self.weights) - 1:
                a = self.softmax(z)
            elif activation == 'relu':
                a = self.relu(z)
            else:
                a = self.sigmoid(z)

            self.activations.append(a)

        return self.activations[-1]

    def backward(self, y_onehot, learning_rate=0.01):
        m = y_onehot.shape[0]

        delta = self.activations[-1] - y_onehot

        for i in range(len(self.weights) - 1, -1, -1):
            dw = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m

            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db

            if i > 0:
                if activation == 'relu':
                    delta = np.dot(delta, self.weights[i].T) * self.relu_derivative(self.activations[i])
                else:
                    delta = np.dot(delta, self.weights[i].T) * self.sigmoid_derivative(self.activations[i])

    def fit(self, X, y, epochs=10, learning_rate=0.01, batch_size=32):
        y_onehot = np.eye(10)[y]

        for epoch in range(epochs):
            indices = np.random.permutation(len(X))

            for start in range(0, len(X), batch_size):
                end = min(start + batch_size, len(X))
                batch_idx = indices[start:end]

                X_batch = X[batch_idx]
                y_batch = y_onehot[batch_idx]

                self.forward(X_batch)
                self.backward(y_batch, learning_rate)

            if epoch % 2 == 0:
                predictions = self.predict(X)
                accuracy = np.mean(predictions == y)
                print(f"Epoch {epoch}: Accuracy = {accuracy:.2%}")

    def predict(self, X):
        output = self.forward(X)
        return np.argmax(output, axis=1)
```

## 使用 MLP 訓練

```python
print("載入 MNIST 資料集...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

print(f"訓練集: {x_train.shape}, 標籤: {y_train.shape}")
print(f"測試集: {x_test.shape}, 標籤: {y_test.shape}")

print("\n訓練 MLP 模型...")
nn = NeuralNetwork([784, 256, 128, 10])
nn.fit(x_train, y_train, epochs=20, learning_rate=0.1, batch_size=64)

accuracy = np.mean(nn.predict(x_test) == y_test)
print(f"\n測試集準確率: {accuracy:.2%}")
```

## 使用 Keras 實作

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

print("載入 MNIST 資料集...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 784).astype('float32') / 255.0
x_test = x_test.reshape(-1, 784).astype('float32') / 255.0

print("\n建立 Keras 模型...")
model = keras.Sequential([
    layers.Dense(256, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\n訓練模型...")
history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)

print("\n評估模型...")
test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=1)
print(f"測試集準確率: {test_accuracy:.2%}")
```

## 預測結果視覺化

```python
predictions = model.predict(x_test)
predicted_labels = np.argmax(predictions, axis=1)

fig, axes = plt.subplots(3, 3, figsize=(10, 10))
for i, ax in enumerate(axes.flat):
    ax.imshow(x_test[i].reshape(28, 28), cmap='gray')
    ax.set_title(f'預測: {predicted_labels[i]}, 實際: {y_test[i]}')
    ax.axis('off')

plt.tight_layout()
plt.show()
```

## 預測錯誤分析

```python
errors = np.where(predicted_labels != y_test)[0]
print(f"預測錯誤數量: {len(errors)}")

fig, axes = plt.subplots(3, 3, figsize=(10, 10))
for i, ax in enumerate(axes.flat):
    if i < len(errors):
        idx = errors[i]
        ax.imshow(x_test[idx].reshape(28, 28), cmap='gray')
        ax.set_title(f'預測: {predicted_labels[idx]}, 實際: {y_test[idx]}')
        ax.axis('off')

plt.tight_layout()
plt.show()
```

## 訓練歷史

```python
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='訓練損失')
plt.plot(history.history['val_loss'], label='驗證損失')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('訓練與驗證損失')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='訓練準確率')
plt.plot(history.history['val_accuracy'], label='驗證準確率')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('訓練與驗證準確率')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
```

## 參考資源

- https://www.google.com/search?q=MNIST+handwritten+digit+classification+neural+network+2019
- https://www.google.com/search?q=Keras+MNIST+MLP+tutorial+deep+learning+2019
- https://www.google.com/search?q=MNIST+CNN+accuracy+benchmark+deep+learning+2019