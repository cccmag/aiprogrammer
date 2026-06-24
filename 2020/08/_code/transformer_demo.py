#!/usr/bin/env python3
"""Transformer Demo: Self-Attention and Multi-Head Attention"""

import math
import numpy as np

class PositionalEncoding:
    def __init__(self, d_model, max_len=100):
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

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / (np.sum(exp_x, axis=-1, keepdims=True) + 1e-8)

def attention(Q, K, V):
    d_k = Q.shape[-1]
    scores = np.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    attn_weights = softmax(scores)
    output = np.matmul(attn_weights, V)
    return output, attn_weights

def multi_head_attention(X, num_heads, d_model):
    d_k = d_model // num_heads
    batch_size = X.shape[0]

    W_Q = np.random.randn(d_model, d_model) * 0.1
    W_K = np.random.randn(d_model, d_model) * 0.1
    W_V = np.random.randn(d_model, d_model) * 0.1

    Q = np.dot(X, W_Q)
    K = np.dot(X, W_K)
    V = np.dot(X, W_V)

    Q = Q.reshape(batch_size, num_heads, -1, d_k).transpose(0, 1, 2, 3)
    K = K.reshape(batch_size, num_heads, -1, d_k).transpose(0, 1, 2, 3)
    V = V.reshape(batch_size, num_heads, -1, d_k).transpose(0, 1, 2, 3)

    attn_output, attn_weights = attention(Q, K, V)

    attn_output = attn_output.transpose(0, 2, 1, 3).reshape(batch_size, -1, d_model * num_heads)

    return attn_output

def feed_forward(x, d_ff, d_model):
    W1 = np.random.randn(d_model, d_ff) * 0.1
    b1 = np.zeros(d_ff)
    W2 = np.random.randn(d_ff, d_model) * 0.1
    b2 = np.zeros(d_model)

    x = np.dot(x, W1) + b1
    x = np.maximum(0, x)
    x = np.dot(x, W2) + b2
    return x

def transformer_block(x, num_heads, d_model, d_ff):
    attn_output = multi_head_attention(x, num_heads, d_model)
    x = x + attn_output
    x = x / math.sqrt(2)

    ff_output = feed_forward(x, d_ff, d_model)
    x = x + ff_output
    x = x / math.sqrt(2)
    return x

def demo():
    print("=" * 50)
    print("Transformer Architecture Demo")
    print("=" * 50)

    d_model = 64
    num_heads = 4
    d_ff = 256
    seq_len = 8
    batch_size = 2

    print("\n1. Positional Encoding:")
    print("-" * 30)
    pos_enc = PositionalEncoding(d_model)
    print(f"Shape: {pos_enc.pe.shape}")
    print(f"Sample values (first position): {pos_enc.pe[0, :5]}")

    print("\n2. Multi-Head Attention:")
    print("-" * 30)
    X = np.random.randn(batch_size, seq_len, d_model)
    attn_out = multi_head_attention(X, num_heads, d_model)
    print(f"Input shape: {X.shape}")
    print(f"Output shape: {attn_out.shape}")

    print("\n3. Self-Attention Scores:")
    print("-" * 30)
    Q = np.random.randn(1, num_heads, seq_len, d_model // num_heads)
    K = np.random.randn(1, num_heads, seq_len, d_model // num_heads)
    V = np.random.randn(1, num_heads, seq_len, d_model // num_heads)
    _, attn_weights = attention(Q, K, V)
    print(f"Attention weights shape: {attn_weights.shape}")
    print(f"Attention weights (first head):\n{attn_weights[0, 0]}")

    print("\n4. Transformer Block:")
    print("-" * 30)
    x = np.random.randn(batch_size, seq_len, d_model)
    output = transformer_block(x, num_heads, d_model, d_ff)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")

    print("\n5. Parameter Count:")
    print("-" * 30)
    params_qkv = d_model * d_model * 3
    params_ff = d_model * d_ff + d_ff * d_model
    total_params = (params_qkv + params_ff) * num_heads
    print(f"QKV projection: {params_qkv * num_heads:,}")
    print(f"Feed-forward: {params_ff:,}")
    print(f"Per head: {total_params:,}")

    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    demo()