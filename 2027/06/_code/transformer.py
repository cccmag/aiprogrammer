import numpy as np

# ---------------------------------------------------------------------------
# Mini Transformer — from scratch in Python
# ---------------------------------------------------------------------------

class LayerNorm:
    """Layer Normalization"""
    def __init__(self, d_model, eps=1e-6):
        self.gamma = np.ones(d_model)
        self.beta = np.zeros(d_model)
        self.eps = eps

    def forward(self, x):
        # x shape: (seq_len, d_model)
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        self.x = x
        self.mean = mean
        self.var = var
        return self.gamma * (x - mean) / np.sqrt(var + self.eps) + self.beta

    def backward(self, dout):
        N, D = self.x.shape
        x_norm = (self.x - self.mean) / np.sqrt(self.var + self.eps)
        dgamma = (dout * x_norm).sum(axis=(0,))
        dbeta = dout.sum(axis=(0,))
        dx = self.gamma * dout
        # Simplified backward for LayerNorm
        return dx

class MultiHeadAttention:
    """Multi-Head Self-Attention"""
    def __init__(self, d_model, n_heads, d_ff=None):
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        assert d_model % n_heads == 0

        # Q, K, V projection matrices
        self.W_q = np.random.randn(d_model, d_model) * 0.02
        self.W_k = np.random.randn(d_model, d_model) * 0.02
        self.W_v = np.random.randn(d_model, d_model) * 0.02
        self.W_o = np.random.randn(d_model, d_model) * 0.02

    def forward(self, x, mask=None):
        # x shape: (seq_len, d_model)
        seq_len, d_model = x.shape
        self.x = x
        self.seq_len = seq_len

        # Project to Q, K, V
        Q = x @ self.W_q  # (seq_len, d_model)
        K = x @ self.W_k
        V = x @ self.W_v

        # Reshape for multi-head: (seq_len, n_heads, d_k)
        self.Q = Q.reshape(seq_len, self.n_heads, self.d_k).transpose(1, 0, 2)
        self.K = K.reshape(seq_len, self.n_heads, self.d_k).transpose(1, 0, 2)
        self.V = V.reshape(seq_len, self.n_heads, self.d_k).transpose(1, 0, 2)

        # Scaled dot-product attention
        scores = self.Q @ self.K.transpose(0, 2, 1) / np.sqrt(self.d_k)
        if mask is not None:
            scores = scores + mask  # causal mask

        self.attn = np.exp(scores - scores.max(axis=-1, keepdims=True))
        self.attn = self.attn / self.attn.sum(axis=-1, keepdims=True)

        # Weighted sum
        context = self.attn @ self.V  # (n_heads, seq_len, d_k)
        context = context.transpose(1, 0, 2).reshape(seq_len, d_model)

        # Output projection
        self.output = context @ self.W_o
        return self.output

    def get_attention_weights(self):
        """Return attention weights for visualization"""
        return self.attn  # (n_heads, seq_len, seq_len)

class FeedForward:
    """Position-wise Feed-Forward Network"""
    def __init__(self, d_model, d_ff):
        self.W_1 = np.random.randn(d_model, d_ff) * 0.02
        self.W_2 = np.random.randn(d_ff, d_model) * 0.02

    def forward(self, x):
        self.x = x
        self.h = np.maximum(0, x @ self.W_1)  # ReLU
        return self.h @ self.W_2

class TransformerBlock:
    """One Transformer decoder block"""
    def __init__(self, d_model, n_heads, d_ff):
        self.attention = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)

    def forward(self, x, mask=None):
        # Self-attention with residual + norm
        x = x + self.attention.forward(self.norm1.forward(x), mask)
        # FFN with residual + norm
        x = x + self.ffn.forward(self.norm2.forward(x))
        return x

# ---------------------------------------------------------------------------
# Positional Encoding
# ---------------------------------------------------------------------------

def sinusoidal_encoding(seq_len, d_model):
    """Sinusoidal positional encoding"""
    pos = np.arange(seq_len)[:, np.newaxis]
    i = np.arange(d_model)[np.newaxis, :]
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / d_model)
    pe = pos * angle_rates
    pe[:, 0::2] = np.sin(pe[:, 0::2])
    pe[:, 1::2] = np.cos(pe[:, 1::2])
    return pe

# ---------------------------------------------------------------------------
# Mini Transformer Language Model
# ---------------------------------------------------------------------------

class MiniTransformer:
    """A minimal decoder-only transformer language model"""
    def __init__(self, vocab_size, d_model=64, n_heads=4, n_layers=3, d_ff=256):
        self.d_model = d_model
        self.token_embedding = np.random.randn(vocab_size, d_model) * 0.02
        self.layers = [TransformerBlock(d_model, n_heads, d_ff) for _ in range(n_layers)]
        self.norm = LayerNorm(d_model)
        self.lm_head = np.random.randn(d_model, vocab_size) * 0.02
        self.vocab_size = vocab_size

    def forward(self, tokens):
        """Forward pass, returns logits for each position"""
        seq_len = len(tokens)
        # Token embeddings + positional encoding
        x = self.token_embedding[tokens] + sinusoidal_encoding(seq_len, self.d_model)
        # Causal mask
        mask = np.triu(np.full((seq_len, seq_len), -1e9), k=1)
        mask = mask[np.newaxis, :, :]  # (1, seq_len, seq_len) for broadcasting over heads
        # Transformer layers
        for layer in self.layers:
            x = layer.forward(x, mask)
        x = self.norm.forward(x)
        # Project to vocabulary
        logits = x @ self.lm_head
        return logits

    def generate(self, start_tokens, max_len=50, temperature=1.0):
        """Generate text given start tokens"""
        tokens = list(start_tokens)
        for _ in range(max_len):
            logits = self.forward(tokens)
            next_logits = logits[-1] / temperature
            probs = np.exp(next_logits - np.max(next_logits))
            probs = probs / probs.sum()
            next_token = np.random.choice(len(probs), p=probs)
            tokens.append(next_token)
        return tokens

    def compute_loss(self, tokens):
        """Compute cross-entropy loss for training"""
        logits = self.forward(tokens[:-1])
        log_probs = logits - np.max(logits, axis=-1, keepdims=True)
        log_probs = log_probs - np.log(np.exp(log_probs).sum(axis=-1, keepdims=True))
        target = tokens[1:]
        loss = -np.mean(log_probs[np.arange(len(target)), target])
        return loss

# ---------------------------------------------------------------------------
# Simple text generation demo
# ---------------------------------------------------------------------------

def demo():
    # Tiny character-level vocabulary
    chars = " abcdefghijklmnopqrstuvwxyz.,!?\n"
    vocab_size = len(chars)
    char_to_idx = {c: i for i, c in enumerate(chars)}
    idx_to_char = {i: c for i, c in enumerate(chars)}

    def encode(s):
        return np.array([char_to_idx[c] for c in s])

    def decode(tokens):
        return ''.join(idx_to_char[t] for t in tokens)

    model = MiniTransformer(vocab_size, d_model=32, n_heads=2, n_layers=2, d_ff=64)

    # Tiny training corpus
    corpus = "hello world.\nthe cat sat on the mat.\nit is a sunny day.\n"
    "deep learning is fun.\ntransformer models are powerful.\n"
    tokens = encode(corpus)

    print("=== Mini Transformer Demo ===\n")

    # Train for a few steps
    print(f"Vocabulary size: {vocab_size}")
    print(f"Corpus length: {len(tokens)} characters")
    print(f"Corpus: {repr(corpus)}\n")

    for step in range(200):
        loss = model.compute_loss(tokens)
        if step % 50 == 0:
            print(f"step {step:3d}, loss = {loss:.4f}")
        # Simple gradient descent (one step)
        logits = model.forward(tokens[:-1])
        dlogits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        dlogits = dlogits / dlogits.sum(axis=-1, keepdims=True)
        target = tokens[1:]
        dlogits[np.arange(len(target)), target] -= 1
        dlogits /= len(target)
        # Simplified update: just update lm_head for demo
        x = model.norm.forward(
            model.layers[1].forward(
                model.layers[0].forward(
                    model.token_embedding[tokens[:-1]] + sinusoidal_encoding(len(tokens) - 1, model.d_model),
                    np.triu(np.full((len(tokens) - 1, len(tokens) - 1), -1e9), k=1)[np.newaxis, :, :]
                ),
                np.triu(np.full((len(tokens) - 1, len(tokens) - 1), -1e9), k=1)[np.newaxis, :, :]
            )
        )
        model.lm_head -= 0.01 * (x.T @ dlogits)

    print("\n--- Generation after training ---")
    start = encode("hello")
    generated = model.generate(list(start), max_len=40, temperature=1.2)
    print(f"Prompt: {repr(corpus[:30])}...")
    print(f"Generated: {decode(generated)}")

if __name__ == "__main__":
    demo()
