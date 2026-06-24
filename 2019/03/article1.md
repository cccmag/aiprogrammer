# NumPy 神經網路實作

## 從零實作神經網路

本章詳細說明如何使用 NumPy 從零實作一個完整的神經網路。

## 網路架構

```python
import numpy as np

class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        self.weights = []
        self.biases = []

        for i in range(self.num_layers - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
```

## 激活函數

```python
def sigmoid(self, z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def sigmoid_derivative(self, a):
    return a * (1 - a)

def relu(self, z):
    return np.maximum(0, z)

def relu_derivative(self, z):
    return (z > 0).astype(float)

def tanh(self, z):
    return np.tanh(z)

def tanh_derivative(self, z):
    return 1 - np.tanh(z) ** 2
```

## 前饋傳播

```python
def forward(self, X):
    self.activations = [X]
    self.z_values = []

    for i in range(len(self.weights)):
        z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
        self.z_values.append(z)

        if i == len(self.weights) - 1:
            a = self.softmax(z)
        elif activation == 'relu':
            a = self.relu(z)
        else:
            a = self.sigmoid(z)

        self.activations.append(a)

    return self.activations[-1]
```

## 反向傳播

```python
def backward(self, y, learning_rate):
    m = y.shape[0]

    delta = self.activations[-1] - y
    gradients = []

    for i in range(len(self.weights) - 1, -1, -1):
        dw = np.dot(self.activations[i].T, delta) / m
        db = np.sum(delta, axis=0, keepdims=True) / m

        gradients.insert(0, (dw, db))

        if i > 0:
            delta = np.dot(delta, self.weights[i].T)

            if activation == 'relu':
                delta *= self.relu_derivative(self.z_values[i-1])
            else:
                delta *= self.sigmoid_derivative(self.activations[i])

    for i, (dw, db) in enumerate(gradients):
        self.weights[i] -= learning_rate * dw
        self.biases[i] -= learning_rate * db
```

## 完整類別

```python
class NeuralNetwork:
    def __init__(self, layer_sizes, activation='relu'):
        self.layer_sizes = layer_sizes
        self.activation = activation
        self.num_layers = len(layer_sizes)
        self.weights = []
        self.biases = []

        for i in range(self.num_layers - 1):
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

    def forward(self, X):
        self.activations = [X]
        self.z_values = []

        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            self.z_values.append(z)

            if i == len(self.weights) - 1:
                a = self.softmax(z)
            elif self.activation == 'relu':
                a = self.relu(z)
            else:
                a = self.sigmoid(z)

            self.activations.append(a)

        return self.activations[-1]

    def backward(self, y, learning_rate):
        m = y.shape[0]
        y_onehot = np.eye(10)[y] if len(y.shape) == 1 else y

        delta = self.activations[-1] - y_onehot

        for i in range(len(self.weights) - 1, -1, -1):
            dw = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m

            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db

            if i > 0:
                delta = np.dot(delta, self.weights[i].T)
                if self.activation == 'relu':
                    delta *= self.relu_derivative(self.z_values[i-1])
                else:
                    delta *= self.sigmoid_derivative(self.activations[i])

    def fit(self, X, y, epochs=100, learning_rate=0.01, batch_size=32):
        for epoch in range(epochs):
            indices = np.random.permutation(len(X))

            for start in range(0, len(X), batch_size):
                end = min(start + batch_size, len(X))
                batch_idx = indices[start:end]

                self.forward(X[batch_idx])
                self.backward(y[batch_idx], learning_rate)

            if epoch % 10 == 0:
                loss = self.compute_loss(X, y)
                accuracy = self.evaluate(X, y)
                print(f"Epoch {epoch}: Loss = {loss:.4f}, Accuracy = {accuracy:.2%}")

    def predict(self, X):
        return np.argmax(self.forward(X), axis=1)

    def evaluate(self, X, y):
        return np.mean(self.predict(X) == y)

    def compute_loss(self, X, y):
        output = self.forward(X)
        y_onehot = np.eye(10)[y]
        return -np.mean(y_onehot * np.log(output + 1e-8))
```

## 使用範例

```python
from tensorflow.keras.datasets import mnist

(x_train, y_train), _ = mnist.load_data()
x_train = x_train.reshape(-1, 784).astype('float32') / 255.0

nn = NeuralNetwork([784, 128, 64, 10], activation='relu')
nn.fit(x_train[:1000], y_train[:1000], epochs=50, learning_rate=0.1)
```

## 參考資源

- https://www.google.com/search?q=neural+network+NumPy+implementation+from+scratch+2019
- https://www.google.com/search?q=backpropagation+NumPy+Python+tutorial+2019
- https://www.google.com/search?q=neural+network+softmax+cross+entropy+2019