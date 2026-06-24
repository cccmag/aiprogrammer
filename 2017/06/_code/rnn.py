import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


class SimpleRNNCell:
    def __init__(self, input_size, hidden_size):
        self.Wx = np.random.randn(hidden_size, input_size) * 0.1
        self.Wh = np.random.randn(hidden_size, hidden_size) * 0.1
        self.b = np.zeros((hidden_size, 1))

    def forward(self, x, h_prev):
        self.x = x
        self.h_prev = h_prev
        self.h = tanh(np.dot(self.Wx, x) + np.dot(self.Wh, h_prev) + self.b)
        return self.h


class LSTMCell:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))

    def forward(self, x, h_prev, C_prev):
        self.x = x
        self.h_prev = h_prev
        self.C_prev = C_prev
        concat = np.vstack((h_prev, x))

        self.f = sigmoid(np.dot(self.Wf, concat) + self.bf)
        self.i = sigmoid(np.dot(self.Wi, concat) + self.bi)
        self.C_tilde = tanh(np.dot(self.Wc, concat) + self.bc)
        self.C = self.f * C_prev + self.i * self.C_tilde
        self.o = sigmoid(np.dot(self.Wo, concat) + self.bo)
        self.h = self.o * tanh(self.C)

        return self.h, self.C


class GRUCell:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        self.Wz = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wr = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wh = np.random.randn(hidden_size, input_size + hidden_size) * 0.1

    def forward(self, x, h_prev):
        self.x = x
        self.h_prev = h_prev
        concat = np.vstack((h_prev, x))

        self.z = sigmoid(np.dot(self.Wz, concat))
        self.r = sigmoid(np.dot(self.Wr, concat))

        concat_r = np.vstack((self.r * h_prev, x))
        self.h_tilde = tanh(np.dot(self.Wh, concat_r))

        self.h = (1 - self.z) * h_prev + self.z * self.h_tilde
        return self.h


def demo():
    np.random.seed(42)
    print("Testing RNN, LSTM, and GRU cells...\n")

    input_size = 10
    hidden_size = 8

    seq_length = 5
    x = np.random.randn(input_size, 1)
    h = np.zeros((hidden_size, 1))
    C = np.zeros((hidden_size, 1))

    print(f"Input shape: {x.shape}")
    print(f"Hidden size: {hidden_size}")
    print(f"Sequence length: {seq_length}\n")

    print("=== Simple RNN ===")
    rnn = SimpleRNNCell(input_size, hidden_size)
    for t in range(seq_length):
        h = rnn.forward(x, h)
        print(f"t={t}: h shape: {h.shape}, h norm: {np.linalg.norm(h):.4f}")

    print("\n=== LSTM ===")
    lstm = LSTMCell(input_size, hidden_size)
    h = np.zeros((hidden_size, 1))
    C = np.zeros((hidden_size, 1))
    for t in range(seq_length):
        h, C = lstm.forward(x, h, C)
        print(f"t={t}: h shape: {h.shape}, h norm: {np.linalg.norm(h):.4f}")

    print("\n=== GRU ===")
    gru = GRUCell(input_size, hidden_size)
    h = np.zeros((hidden_size, 1))
    for t in range(seq_length):
        h = gru.forward(x, h)
        print(f"t={t}: h shape: {h.shape}, h norm: {np.linalg.norm(h):.4f}")

    print("\nDemo completed successfully!")


if __name__ == "__main__":
    demo()