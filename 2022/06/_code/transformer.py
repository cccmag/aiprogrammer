import numpy as np

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = np.dot(Q, K.T) / np.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, -1e9, scores)
    weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    weights = weights / np.sum(weights, axis=-1, keepdims=True)
    return np.dot(weights, V), weights

class PositionalEncoding:
    def __init__(self, d_model, max_len=100):
        pe = np.zeros((max_len, d_model))
        pos = np.arange(max_len)[:, np.newaxis]
        div = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))
        pe[:, 0::2] = np.sin(pos * div)
        pe[:, 1::2] = np.cos(pos * div)
        self.pe = pe[np.newaxis, :, :]

    def __call__(self, x):
        return x + self.pe[:, :x.shape[1], :]

class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_q = np.random.randn(d_model, d_model) * 0.01
        self.W_k = np.random.randn(d_model, d_model) * 0.01
        self.W_v = np.random.randn(d_model, d_model) * 0.01
        self.W_o = np.random.randn(d_model, d_model) * 0.01

    def __call__(self, x, mask=None):
        batch, seq, d_model = x.shape
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v

        Q = Q.reshape(batch, seq, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        K = K.reshape(batch, seq, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        V = V.reshape(batch, seq, self.num_heads, self.d_k).transpose(0, 2, 1, 3)

        scores = (Q @ K.transpose(0, 1, 3, 2)) / np.sqrt(self.d_k)
        if mask is not None:
            scores = np.where(mask, -1e9, scores)
        weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        weights = weights / np.sum(weights, axis=-1, keepdims=True)

        out = weights @ V
        out = out.transpose(0, 2, 1, 3).reshape(batch, seq, d_model)
        return out @ self.W_o

class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.01
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * 0.01
        self.b2 = np.zeros(d_model)

    def __call__(self, x):
        return x @ self.W1 @ self.W2 + self.b2

def layer_norm(x, eps=1e-6):
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)

class TransformerBlock:
    def __init__(self, d_model, num_heads, d_ff):
        self.attn = MultiHeadAttention(d_model, num_heads)
        self.ff = FeedForward(d_model, d_ff)

    def __call__(self, x, mask=None):
        a = self.attn(x, mask)
        x = layer_norm(x + a)
        f = self.ff(x)
        return layer_norm(x + f)

def demo():
    np.random.seed(42)
    batch, seq, d_model = 1, 4, 8
    x = np.random.randn(batch, seq, d_model) * 0.1
    pe = PositionalEncoding(d_model)
    x = pe(x)
    print("After positional encoding:", x.shape)

    block = TransformerBlock(d_model, num_heads=2, d_ff=16)
    out = block(x)
    print("Transformer block output:", out.shape)

    Q, K, V = x[0], x[0], x[0]
    result, weights = scaled_dot_product_attention(Q, K, V)
    print("Attention weights shape:", weights.shape)
    print("Attention output shape:", result.shape)
    print("Demo OK")

if __name__ == "__main__":
    demo()
