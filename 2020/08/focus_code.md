# 實作：簡化的 Transformer

## 程式概述

本程式中，我們將用 Python 實作一個簡化的 Transformer 架構，包含核心的注意力機制和位置編碼。

## 實作內容

1. **位置編碼（Positional Encoding）**
2. **Scaled Dot-Product Attention**
3. **Multi-Head Attention**
4. **完整的 Transformer 區塊**

```python
#!/usr/bin/env python3
"""簡化版 Transformer 實作"""

import math
import numpy as np

class PositionalEncoding:
    def __init__(self, d_model, max_len=5000):
        self.d_model = d_model
        pe = np.zeros((max_len, d_model))
        for pos in range(max_len):
            for i in range(0, d_model, 2):
                pe[pos, i] = math.sin(pos / (10000 ** (i / d_model)))
                if i + 1 < d_model:
                    pe[pos, i + 1] = math.cos(pos / (10000 ** (i / d_model)))
        self.pe = pe

    def get_encoding(self, seq_len):
        return self.pe[:seq_len]

class ScaledDotProductAttention:
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / (np.sum(exp_x, axis=-1, keepdims=True) + 1e-8)

    def forward(self, Q, K, V, mask=None):
        d_k = Q.shape[-1]
        scores = np.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        if mask is not None:
            scores = np.where(mask == 0, -1e9, scores)
        attn_weights = self.softmax(scores)
        output = np.matmul(attn_weights, V)
        return output, attn_weights

class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_Q = np.random.randn(d_model, d_model) * 0.1
        self.W_K = np.random.randn(d_model, d_model) * 0.1
        self.W_V = np.random.randn(d_model, d_model) * 0.1
        self.W_O = np.random.randn(d_model, d_model) * 0.1

    def split_heads(self, x, batch_size):
        x = x.reshape(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(0, 2, 1, 3)

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.shape[0]
        Q = np.dot(Q, self.W_Q)
        K = np.dot(K, self.W_K)
        V = np.dot(V, self.W_V)
        Q = self.split_heads(Q, batch_size)
        K = self.split_heads(K, batch_size)
        V = self.split_heads(V, batch_size)
        attn_output, attn_weights = ScaledDotProductAttention().forward(Q, K, V, mask)
        attn_output = attn_output.transpose(0, 2, 1, 3).reshape(batch_size, -1, self.d_model)
        output = np.dot(attn_output, self.W_O)
        return output, attn_weights

class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.1
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * 0.1
        self.b2 = np.zeros(d_model)

    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, x):
        x = np.dot(x, self.W1) + self.b1
        x = self.relu(x)
        x = np.dot(x, self.W2) + self.b2
        return x

class TransformerBlock:
    def __init__(self, d_model, num_heads, d_ff):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = FeedForward(d_model, d_ff)
        self.norm1 = lambda x: x
        self.norm2 = lambda x: x

    def forward(self, x, mask=None):
        attn_output, _ = self.attention.forward(x, x, x, mask)
        x = x + attn_output
        x = self.norm1(x)
        ff_output = self.feed_forward.forward(x)
        x = x + ff_output
        x = self.norm2(x)
        return x

class SimpleTransformer:
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff):
        self.embeddings = np.random.randn(vocab_size, d_model) * 0.1
        self.pos_encoding = PositionalEncoding(d_model)
        self.layers = [TransformerBlock(d_model, num_heads, d_ff) for _ in range(num_layers)]

    def forward(self, token_ids):
        x = self.embeddings[token_ids]
        seq_len = token_ids.shape[1]
        pos_enc = self.pos_encoding.get_encoding(seq_len)
        x = x + pos_enc
        for layer in self.layers:
            x = layer.forward(x)
        return x

def demo():
    print("=" * 50)
    print("Simplified Transformer Demo")
    print("=" * 50)

    vocab_size = 1000
    d_model = 64
    num_heads = 4
    num_layers = 2
    d_ff = 256
    seq_len = 5
    batch_size = 2

    transformer = SimpleTransformer(vocab_size, d_model, num_heads, num_layers, d_ff)

    token_ids = np.random.randint(0, vocab_size, size=(batch_size, seq_len))
    print(f"\nInput shape: {token_ids.shape}")

    output = transformer.forward(token_ids)
    print(f"Output shape: {output.shape}")

    pos_enc = PositionalEncoding(d_model)
    print(f"\nPositional encoding shape: {pos_enc.pe.shape}")

    attn = MultiHeadAttention(d_model, num_heads)
    print(f"Multi-head attention: {num_heads} heads, d_k={d_model//num_heads}")

    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    demo()