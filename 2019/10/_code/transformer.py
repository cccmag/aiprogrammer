#!/usr/bin/env python3
"""Simple Transformer Self-Attention Implementation"""

import math
import torch
import torch.nn as nn

class PositionalEncoding:
    def __init__(self, d_model, max_len=5000):
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def __call__(self, x):
        return x + self.pe[:, :x.size(1)]

class SimpleSelfAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def split_heads(self, x, batch_size):
        x = x.view(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(1, 2)

    def forward(self, x, mask=None):
        batch_size = x.size(0)

        Q = self.split_heads(self.W_q(x), batch_size)
        K = self.split_heads(self.W_k(x), batch_size)
        V = self.split_heads(self.W_v(x), batch_size)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        weights = torch.softmax(scores, dim=-1)
        attn_output = torch.matmul(weights, V)

        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)

        return self.W_o(attn_output)

def demo():
    print("Transformer Self-Attention Demo")
    print("=" * 50)

    seq_len = 5
    d_model = 8
    num_heads = 2

    torch.manual_seed(42)

    x = torch.randn(1, seq_len, d_model)

    print(f"Input shape: {x.shape}")
    print(f"d_model: {d_model}, num_heads: {num_heads}")
    print(f"Sequence length: {seq_len}")
    print()

    attn = SimpleSelfAttention(d_model, num_heads)
    output = attn(x)

    print(f"Output shape: {output.shape}")
    print(f"Output tensor:\n{output}")
    print()
    print("Self-attention allows each position to attend to all positions")
    print("This is the core mechanism of the Transformer architecture.")

if __name__ == "__main__":
    demo()