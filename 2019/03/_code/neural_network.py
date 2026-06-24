import numpy as np


def demo():
    print("=" * 60)
    print("類神經網路基礎展示")
    print("=" * 60)

    print("\n[1] 感知器 - AND 邏輯閘學習")
    demonstrate_perceptron()

    print("\n[2] MLP - XOR 問題")
    demonstrate_mlp_xor()

    print("\n[3] 激活函數展示")
    demonstrate_activation_functions()

    print("\n[4] 梯度下降收斂")
    demonstrate_gradient_descent()

    print("\n" + "=" * 60)
    print("展示完成")
    print("=" * 60)


class Perceptron:
    def __init__(self, n_inputs):
        self.weights = np.random.randn(n_inputs) * 0.1
        self.bias = 0

    def forward(self, x):
        z = np.dot(x, self.weights) + self.bias
        return 1 if z >= 0 else 0

    def predict(self, X):
        return np.array([self.forward(x) for x in X])


def demonstrate_perceptron():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])

    perceptron = Perceptron(n_inputs=2)

    for epoch in range(100):
        for x, label in zip(X, y):
            prediction = perceptron.forward(x)
            error = label - prediction
            perceptron.weights += 0.1 * error * x
            perceptron.bias += 0.1 * error

    predictions = perceptron.predict(X)
    print(f"最終權重: {perceptron.weights.round(2)}, 偏差: {perceptron.bias:.2f}")
    print(f"預測結果: {predictions}")
    print(f"實際結果: {y}")


class SimpleMLP:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def sigmoid_derivative(self, a):
        return a * (1 - a)

    def forward(self, X):
        self.activations = [X]
        for w, b in zip(self.weights, self.biases):
            z = np.dot(self.activations[-1], w) + b
            a = self.sigmoid(z)
            self.activations.append(a)
        return self.activations[-1]

    def backward(self, y, learning_rate):
        m = y.shape[0]
        delta = self.activations[-1] - y

        for i in range(len(self.weights) - 1, -1, -1):
            dw = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db
            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * self.sigmoid_derivative(self.activations[i])

    def predict(self, X):
        return (self.forward(X) >= 0.5).astype(int).flatten()


def demonstrate_mlp_xor():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    mlp = SimpleMLP([2, 4, 1])

    for epoch in range(5000):
        mlp.forward(X)
        mlp.backward(y, learning_rate=0.5)

    predictions = mlp.predict(X)
    print(f"MLP 預測結果: {predictions}")
    print(f"MLP 實際結果: {y.flatten()}")


def demonstrate_activation_functions():
    z = np.linspace(-5, 5, 20)

    sigmoid = 1 / (1 + np.exp(-z))
    tanh = np.tanh(z)
    relu = np.maximum(0, z)

    print(f"Sigmoid: {[f'{v:.4f}' for v in sigmoid[:5]]}")
    print(f"Tanh: {[f'{v:.4f}' for v in tanh[:5]]}")
    print(f"ReLU: {[f'{v:.4f}' for v in relu[:5]]}")


def demonstrate_gradient_descent():
    def rosenbrock(x, y):
        return (1 - x)**2 + 100 * (y - x**2)**2

    x, y = -2.0, 2.0
    learning_rate = 0.001

    for epoch in range(0, 201, 100):
        loss = rosenbrock(x, y)
        print(f"Epoch {epoch}: Loss = {loss:.4f}")

    print(f"最終位置: ({x:.4f}, {y:.4f})")
    print(f"收斂完成: {loss < 10}")


if __name__ == "__main__":
    demo()