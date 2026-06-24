#!/usr/bin/env python3
"""Transformer 與注意力機制示範"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


def scaled_dot_product_attention(query, key, value, mask=None):
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1))
    scores = scores / math.sqrt(d_k)

    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)

    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, value), weights


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.wq = nn.Linear(d_model, d_model)
        self.wk = nn.Linear(d_model, d_model)
        self.wv = nn.Linear(d_model, d_model)
        self.dense = nn.Linear(d_model, d_model)

    def split_heads(self, x, batch_size):
        x = x.view(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(1, 2)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        q = self.split_heads(self.wq(query), batch_size)
        k = self.split_heads(self.wk(key), batch_size)
        v = self.split_heads(self.wv(value), batch_size)

        if mask is not None:
            mask = mask.unsqueeze(1)

        attn_output, attn_weights = scaled_dot_product_attention(q, k, v, mask)

        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, -1, self.d_model * self.num_heads)

        return self.dense(attn_output), attn_weights


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]


def demo():
    print("=== Transformer 注意力機制示範 ===\n")

    d_model = 64
    num_heads = 4
    batch_size = 2
    seq_length = 5

    attn = MultiHeadAttention(d_model, num_heads)

    q = torch.randn(batch_size, seq_length, d_model)
    k = torch.randn(batch_size, seq_length, d_model)
    v = torch.randn(batch_size, seq_length, d_model)

    output, weights = attn(q, k, v)

    print(f"輸入 Q/K/V 形狀: {q.shape}")
    print(f"輸出形狀: {output.shape}")
    print(f"注意力權重形狀: {weights.shape}")
    print(f"\n注意力權重（第一個样本，第一個頭）:")
    print(weights[0, 0].detach().numpy())

    print("\n--- 位置編碼示範 ---")
    pos_enc = PositionalEncoding(d_model)
    x = torch.randn(1, 10, d_model)
    encoded = pos_enc(x)
    print(f"原始輸入形狀: {x.shape}")
    print(f"加入位置編碼後: {encoded.shape}")


if __name__ == "__main__":
    demo()