#!/usr/bin/env python3
"""MLP from scratch: backprop, activations, train on XOR"""

import math, random

random.seed(42)

# ---------------------------------------------------------------------------
# Activation functions
# ---------------------------------------------------------------------------
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_prime(x):
    s = sigmoid(x)
    return s * (1.0 - s)

def relu(x):
    return x if x > 0 else 0.0

def relu_prime(x):
    return 1.0 if x > 0 else 0.0

def gelu(x):
    return 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)))

def gelu_prime(x):
    tanh_arg = math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)
    tanh_val = math.tanh(tanh_arg)
    sech2 = 1.0 - tanh_val * tanh_val
    inner = math.sqrt(2.0 / math.pi) * (1.0 + 0.134145 * x**2)
    return 0.5 * (1.0 + tanh_val) + 0.5 * x * sech2 * inner

def tanh(x):
    return math.tanh(x)

def tanh_prime(x):
    t = math.tanh(x)
    return 1.0 - t * t

# ---------------------------------------------------------------------------
# Layer
# ---------------------------------------------------------------------------
class Layer:
    def __init__(self, n_in, n_out, activation='sigmoid'):
        self.w = [[random.uniform(-1, 1) for _ in range(n_in)] for _ in range(n_out)]
        self.b = [random.uniform(-1, 1) for _ in range(n_out)]
        acts = {
            'sigmoid': (sigmoid, sigmoid_prime),
            'relu': (relu, relu_prime),
            'gelu': (gelu, gelu_prime),
            'tanh': (tanh, tanh_prime),
        }
        self.fn, self.fn_prime = acts[activation]

    def forward(self, x):
        self.x = x  # cache
        self.z = [sum(w * xi for w, xi in zip(row, x)) + b for row, b in zip(self.w, self.b)]
        self.a = [self.fn(v) for v in self.z]
        return self.a

    def backward(self, dz):
        # dz: gradient w.r.t. a (next layer's partial)
        # convert to gradient w.r.t. z
        if dz is not None:
            dz = [d * self.fn_prime(z) for d, z in zip(dz, self.z)]
        else:
            dz = [self.fn_prime(z) for z in self.z]
        self.dz = dz
        # gradients for params
        self.dw = [[d * xi for xi in self.x] for d in dz]
        self.db = dz[:]
        # gradient w.r.t. x (to pass backward)
        dx = [sum(self.w[j][i] * dz[j] for j in range(len(dz))) for i in range(len(self.x))]
        return dx

    def update(self, lr):
        for j in range(len(self.w)):
            for i in range(len(self.w[j])):
                self.w[j][i] -= lr * self.dw[j][i]
            self.b[j] -= lr * self.db[j]

# ---------------------------------------------------------------------------
# MLP
# ---------------------------------------------------------------------------
class MLP:
    def __init__(self, sizes, activations):
        assert len(sizes) == len(activations) + 1
        self.layers = [Layer(sizes[i], sizes[i+1], activations[i]) for i in range(len(activations))]

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, y):
        # output layer: loss = MSE => dL/da = (a - y)
        out = self.layers[-1].a
        dz = [2 * (o - t) for o, t in zip(out, y)]
        for layer in reversed(self.layers):
            dz = layer.backward(dz)

    def update(self, lr=0.5):
        for layer in self.layers:
            layer.update(lr)

    def train(self, X, Y, epochs=10000, lr=0.5, verbose=True):
        for epoch in range(epochs):
            total_loss = 0.0
            for x, y in zip(X, Y):
                pred = self.forward(x)
                self.backward(y)
                self.update(lr)
                total_loss += sum((p - t)**2 for p, t in zip(pred, y))
            if verbose and epoch % 2000 == 0:
                print(f"epoch {epoch:5d}  loss {total_loss:.6f}")

    def predict(self, X):
        return [self.forward(x) for x in X]


def demo():
    print("=" * 50)
    print("MLP from scratch — XOR problem")
    print("=" * 50)

    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    Y = [[0], [1], [1], [0]]

    print("\n--- Sigmoid MLP (2-4-1) ---")
    mlp = MLP([2, 4, 1], ['sigmoid', 'sigmoid'])
    mlp.train(X, Y, epochs=10000, lr=0.5)
    for x, y in zip(X, Y):
        p = mlp.forward(x)
        print(f"  {x} -> {p[0]:.4f}  (expected {y[0]})")

    print("\n--- ReLU MLP (2-8-1) ---")
    mlp2 = MLP([2, 8, 1], ['relu', 'sigmoid'])
    mlp2.train(X, Y, epochs=10000, lr=0.3)
    for x, y in zip(X, Y):
        p = mlp2.forward(x)
        print(f"  {x} -> {p[0]:.4f}  (expected {y[0]})")

    print("\n--- Tanh MLP (2-4-1) ---")
    mlp3 = MLP([2, 4, 1], ['tanh', 'sigmoid'])
    mlp3.train(X, Y, epochs=10000, lr=0.5)
    for x, y in zip(X, Y):
        p = mlp3.forward(x)
        print(f"  {x} -> {p[0]:.4f}  (expected {y[0]})")

    print("\n--- GELU MLP (2-6-1) ---")
    mlp4 = MLP([2, 6, 1], ['gelu', 'sigmoid'])
    mlp4.train(X, Y, epochs=10000, lr=0.3)
    for x, y in zip(X, Y):
        p = mlp4.forward(x)
        print(f"  {x} -> {p[0]:.4f}  (expected {y[0]})")

    print("\nAll done!")


if __name__ == '__main__':
    demo()
