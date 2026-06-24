import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def cross_entropy_loss(y_pred, y_true):
    epsilon = 1e-12
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.sum(y_true * np.log(y_pred))

def compute_loss_gradient(y_pred, y_true):
    return y_pred - y_true

class SimpleLayer:
    def __init__(self, input_size, output_size, activation='relu'):
        self.W = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
        self.b = np.zeros(output_size)
        self.activation = activation
        self.x_cache = None
        self.output_cache = None

    def forward(self, x):
        self.x_cache = x
        z = np.dot(x, self.W) + self.b
        self.z_cache = z

        if self.activation == 'sigmoid':
            self.output_cache = sigmoid(z)
        elif self.activation == 'relu':
            self.output_cache = relu(z)
        elif self.activation == 'softmax':
            self.output_cache = softmax(z)
        else:
            self.output_cache = z
        return self.output_cache

    def backward(self, grad_output):
        if self.activation == 'relu':
            grad_activation = relu_derivative(self.z_cache)
        elif self.activation == 'sigmoid':
            grad_activation = sigmoid_derivative(self.z_cache)
        else:
            grad_activation = 1

        grad_z = grad_output * grad_activation
        grad_W = np.dot(self.x_cache.T, grad_z)
        grad_b = np.sum(grad_z, axis=0)
        grad_x = np.dot(grad_z, self.W.T)

        return grad_x, grad_W, grad_b

class SimpleNetwork:
    def __init__(self, layer_sizes):
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            if i == len(layer_sizes) - 2:
                act = 'softmax'
            else:
                act = 'relu'
            self.layers.append(SimpleLayer(layer_sizes[i], layer_sizes[i+1], act))

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, y_pred, y_true):
        grad = compute_loss_gradient(y_pred, y_true)
        grads = []

        for layer in reversed(self.layers):
            grad_x, grad_W, grad_b = layer.backward(grad)
            grads.insert(0, (grad_W, grad_b))
            grad = grad_x

        return grads

    def update_weights(self, grads, learning_rate):
        for layer, (grad_W, grad_b) in zip(self.layers, grads):
            layer.W -= learning_rate * grad_W
            layer.b -= learning_rate * grad_b

def sgd_update(layer, grad_W, grad_b, lr, momentum=0.9):
    if not hasattr(sgd_update, 'velocity_W'):
        sgd_update.velocity_W = {}
        sgd_update.velocity_b = {}

    if layer not in sgd_update.velocity_W:
        sgd_update.velocity_W[layer] = np.zeros_like(grad_W)
        sgd_update.velocity_b[layer] = np.zeros_like(grad_b)

    sgd_update.velocity_W[layer] = momentum * sgd_update.velocity_W[layer] - lr * grad_W
    sgd_update.velocity_b[layer] = momentum * sgd_update.velocity_b[layer] - lr * grad_b

    layer.W += sgd_update.velocity_W[layer]
    layer.b += sgd_update.velocity_b[layer]

def adam_update(layer, grad_W, grad_b, lr, t,
                beta1=0.9, beta2=0.999, eps=1e-8):
    if not hasattr(adam_update, 'm_W'):
        adam_update.m_W = {}
        adam_update.m_b = {}
        adam_update.v_W = {}
        adam_update.v_b = {}

    if layer not in adam_update.m_W:
        adam_update.m_W[layer] = np.zeros_like(grad_W)
        adam_update.m_b[layer] = np.zeros_like(grad_b)
        adam_update.v_W[layer] = np.zeros_like(grad_W)
        adam_update.v_b[layer] = np.zeros_like(grad_b)

    adam_update.m_W[layer] = beta1 * adam_update.m_W[layer] + (1 - beta1) * grad_W
    adam_update.m_b[layer] = beta1 * adam_update.m_b[layer] + (1 - beta1) * grad_b
    adam_update.v_W[layer] = beta2 * adam_update.v_W[layer] + (1 - beta2) * (grad_W ** 2)
    adam_update.v_b[layer] = beta2 * adam_update.v_b[layer] + (1 - beta2) * (grad_b ** 2)

    m_hat_W = adam_update.m_W[layer] / (1 - beta1 ** t)
    m_hat_b = adam_update.m_b[layer] / (1 - beta1 ** t)
    v_hat_W = adam_update.v_W[layer] / (1 - beta2 ** t)
    v_hat_b = adam_update.v_b[layer] / (1 - beta2 ** t)

    layer.W -= lr * m_hat_W / (np.sqrt(v_hat_W) + eps)
    layer.b -= lr * m_hat_b / (np.sqrt(v_hat_b) + eps)

def apply_dropout(x, dropout_rate):
    mask = np.random.binomial(1, 1 - dropout_rate, x.shape) / (1 - dropout_rate)
    return x * mask

def demo():
    np.random.seed(42)

    X = np.random.randn(8, 4)
    y_true = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0],
                        [0, 0, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)

    network = SimpleNetwork([4, 8, 6, 3])

    print("Forward pass test:")
    y_pred = network.forward(X)
    print("Output shape:", y_pred.shape)
    print("Output sum (should be ~1 per row):", y_pred.sum(axis=1))

    loss = cross_entropy_loss(y_pred, y_true)
    print("Initial loss:", loss)

    print("\nBackward pass test:")
    grads = network.backward(y_pred, y_true)
    print("Number of gradient tuples:", len(grads))
    print("Gradient W[0] shape:", grads[0][0].shape)

    print("\nWeight update (SGD):")
    network.update_weights(grads, 0.01)
    y_pred_new = network.forward(X)
    loss_new = cross_entropy_loss(y_pred_new, y_true)
    print("Loss after update:", loss_new)
    print("Loss decreased:", loss_new < loss)

    print("\nDemo OK")

if __name__ == "__main__":
    demo()