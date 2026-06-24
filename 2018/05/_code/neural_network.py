#!/usr/bin/env python3
"""類神經網路基礎實作 - 使用 NumPy"""

import numpy as np

class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_gradient(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

    def forward(self, X):
        self.activations = [X]
        self.z_values = []
        for w, b in zip(self.weights, self.biases):
            z = np.dot(self.activations[-1], w) + b
            self.z_values.append(z)
            a = self.sigmoid(z)
            self.activations.append(a)
        return self.activations[-1]

    def backward(self, y, learning_rate):
        m = y.shape[0]
        delta = self.activations[-1] - y
        for i in range(len(self.weights) - 1, -1, -1):
            dW = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            if i > 0:
                delta = np.dot(delta, self.weights[i].T)
                delta = delta * self.sigmoid_gradient(self.z_values[i-1])
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db

    def fit(self, X, y, epochs=1000, learning_rate=0.1):
        for epoch in range(epochs):
            y_pred = self.forward(X)
            self.backward(y, learning_rate)
            if epoch % 100 == 0:
                loss = np.mean((y_pred - y)**2)
                print(f'Epoch {epoch}: Loss = {loss:.4f}')

    def predict(self, X):
        return (self.forward(X) > 0.5).astype(int)

def demo():
    print('=' * 50)
    print('類神經網路實作')
    print('=' * 50)
    print()

    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    print('XOR 問題訓練：')
    nn = NeuralNetwork([2, 4, 1])
    nn.fit(X, y, epochs=1000, learning_rate=1.0)

    print()
    print('預測結果：')
    predictions = nn.predict(X)
    print(predictions)

if __name__ == '__main__':
    demo()