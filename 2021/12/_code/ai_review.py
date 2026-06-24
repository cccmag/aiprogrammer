import numpy as np
import math


class AttentionMechanism:
    def __init__(self, d_model: int):
        self.d_model = d_model

    def forward(self, query, key, value, mask=None):
        scores = np.dot(query, key.T) / math.sqrt(self.d_model)

        if mask is not None:
            scores = scores + mask

        attention_weights = self.softmax(scores)
        output = np.dot(attention_weights, value)
        return output, attention_weights

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


class SimpleLanguageModel:
    def __init__(self, vocab_size: int, d_model: int):
        self.embedding = np.random.randn(vocab_size, d_model) * 0.01
        self.d_model = d_model

    def next_token_prediction(self, context_ids):
        context_vector = np.mean(self.embedding[context_ids], axis=0)
        logits = np.dot(self.embedding, context_vector)
        probabilities = self.softmax(logits)
        return probabilities

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)


class ContrastiveLearning:
    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim

    def contrastive_loss(self, anchor, positive, negative, temperature=0.5):
        anchor = self.l2_normalize(anchor)
        positive = self.l2_normalize(positive)
        negative = self.l2_normalize(negative)

        pos_sim = np.dot(anchor, positive) / temperature
        neg_sim = np.dot(anchor.reshape(1, -1), negative.T) / temperature

        logits = np.concatenate([pos_sim.reshape(-1, 1), neg_sim.reshape(1, -1)], axis=1)
        labels = np.zeros(1, dtype=int)
        loss = self.cross_entropy(logits, labels)
        return loss

    def l2_normalize(self, x):
        return x / (np.linalg.norm(x, axis=-1, keepdims=True) + 1e-8)

    def cross_entropy(self, logits, labels):
        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
        nll = -np.log(probs[np.arange(len(labels)), labels] + 1e-8)
        return np.mean(nll)


class RewardModel:
    def __init__(self):
        self.weights = np.random.randn(10) * 0.01

    def predict_reward(self, response_features):
        return np.dot(response_features, self.weights)

    def update_from_preference(self, preferred_response, rejected_response, lr=0.01):
        preferred_reward = self.predict_reward(preferred_response)
        rejected_reward = self.predict_reward(rejected_response)

        if preferred_reward > rejected_reward:
            pass
        else:
            gradient = preferred_response - rejected_response
            self.weights += lr * gradient


class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros(layer_sizes[i+1])
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, x):
        self.activations = [x]
        current = x

        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            current = np.dot(current, w) + b
            if i < len(self.weights) - 1:
                current = np.maximum(0, current)
            self.activations.append(current)

        return current

    def backward(self, y_pred, y_true, lr=0.01):
        grad = y_pred - y_true

        for i in reversed(range(len(self.weights))):
            grad_w = np.dot(self.activations[i].T, grad)
            grad_b = np.sum(grad, axis=0)

            if i > 0:
                grad = np.dot(grad, self.weights[i].T)
                grad = grad * (self.activations[i] > 0).astype(float)

            self.weights[i] -= lr * grad_w
            self.biases[i] -= lr * grad_b

    def train_step(self, x, y, lr=0.01):
        y_pred = self.forward(x)
        self.backward(y_pred, y, lr)
        return np.mean((y_pred - y) ** 2)


def demo():
    print("=== Attention Mechanism Demo ===")
    attention = AttentionMechanism(d_model=4)

    query = np.random.randn(1, 4)
    key = np.random.randn(3, 4)
    value = np.random.randn(3, 4)

    output, weights = attention.forward(query, key, value)
    print(f"Attention output shape: {output.shape}")
    print(f"Attention weights: {weights}")

    print("\n=== Language Model Demo ===")
    vocab_size = 100
    d_model = 32
    lm = SimpleLanguageModel(vocab_size, d_model)

    context = [1, 2, 3, 4, 5]
    probs = lm.next_token_prediction(context)
    print(f"Vocabulary size: {vocab_size}")
    print(f"Next token probabilities shape: {probs.shape}")
    print(f"Top probability: {np.max(probs):.4f}")

    print("\n=== Contrastive Learning Demo ===")
    cl = ContrastiveLearning(embedding_dim=64)

    anchor = np.random.randn(64)
    positive = anchor + np.random.randn(64) * 0.1
    negative = np.random.randn(10, 64)

    loss = cl.contrastive_loss(anchor, positive, negative, temperature=0.5)
    print(f"Contrastive loss: {loss:.4f}")

    print("\n=== Reward Model Demo ===")
    reward_model = RewardModel()

    response = np.random.randn(10)
    reward = reward_model.predict_reward(response)
    print(f"Reward prediction: {reward:.4f}")

    print("\n=== Neural Network Demo ===")
    nn = NeuralNetwork([4, 8, 4])
    x = np.random.randn(2, 4)
    y = np.random.randn(2, 4)

    print("Training neural network...")
    for epoch in range(5):
        loss = nn.train_step(x, y, lr=0.1)
        if epoch % 2 == 0:
            print(f"Epoch {epoch}: Loss = {loss:.4f}")

    print("\nDemo OK")


if __name__ == "__main__":
    demo()