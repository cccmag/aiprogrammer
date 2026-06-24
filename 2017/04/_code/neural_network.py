import numpy as np


def relu(z):
    return np.maximum(0, z)


def relu_gradient(z):
    return (z > 0).astype(float)


def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)


class NeuralNetwork:
    def __init__(self, layer_sizes, learning_rate=0.01):
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []
        self._init_weights()

    def _init_weights(self):
        np.random.seed(42)
        self.weights = []
        self.biases = []
        for i in range(len(self.layer_sizes) - 1):
            w = np.random.randn(self.layer_sizes[i], self.layer_sizes[i + 1]) * \
                np.sqrt(2.0 / self.layer_sizes[i])
            b = np.zeros((1, self.layer_sizes[i + 1]))
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, X):
        self.activations = [X]
        A = X
        for i in range(len(self.weights)):
            Z = A @ self.weights[i] + self.biases[i]
            if i < len(self.weights) - 1:
                A = relu(Z)
            else:
                A = softmax(Z)
            self.activations.append(A)
        return A

    def compute_loss(self, Y_pred, Y_true):
        m = Y_true.shape[0]
        loss = -np.sum(Y_true * np.log(Y_pred + 1e-8)) / m
        return loss

    def backward(self, Y_true):
        m = Y_true.shape[0]
        delta = self.activations[-1] - Y_true
        for i in reversed(range(len(self.weights))):
            dW = self.activations[i].T @ delta / m
            dB = np.sum(delta, axis=0, keepdims=True) / m
            if i > 0:
                delta = delta @ self.weights[i].T
                delta *= relu_gradient(self.activations[i])
            self.weights[i] -= self.learning_rate * dW
            self.biases[i] -= self.learning_rate * dB

    def fit(self, X, Y, epochs=100, verbose=True):
        for epoch in range(epochs):
            Y_pred = self.forward(X)
            loss = self.compute_loss(Y_pred, Y)
            self.backward(Y_true=Y)
            if verbose and (epoch + 1) % 20 == 0:
                print(f"Epoch {epoch + 1}, Loss: {loss:.4f}")
        return loss

    def predict(self, X):
        return np.argmax(self.forward(X), axis=1)


def demo():
    np.random.seed(42)
    X = np.random.randn(100, 2)
    y = (X[:, 0] * X[:, 1] > 0).astype(int)
    Y = np.eye(2)[y]

    net = NeuralNetwork([2, 8, 4, 2], learning_rate=0.1)
    print("Training neural network on synthetic data...")
    net.fit(X, Y, epochs=200, verbose=True)

    predictions = net.predict(X)
    accuracy = np.mean(predictions == y)
    print(f"Final training accuracy: {accuracy:.4f}")
    print("Demo completed successfully!")


if __name__ == "__main__":
    demo()