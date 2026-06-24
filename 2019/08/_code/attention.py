#!/usr/bin/env python3
"""Self-Attention Mechanism Demo"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

class SelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        assert embed_dim % num_heads == 0

        self.W_q = nn.Linear(embed_dim, embed_dim)
        self.W_k = nn.Linear(embed_dim, embed_dim)
        self.W_v = nn.Linear(embed_dim, embed_dim)
        self.W_o = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        batch_size, seq_len, embed_dim = x.size()
        Q = self.W_q(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        weights = F.softmax(scores, dim=-1)
        attended = torch.matmul(weights, V)

        attended = attended.transpose(1, 2).contiguous().view(batch_size, seq_len, embed_dim)
        return self.W_o(attended)

def demo():
    print("Self-Attention 演示")
    print("=" * 50)

    embed_dim, num_heads, seq_len = 128, 8, 32
    batch_size = 4

    print(f"[1] 初始化自注意力層...")
    attention = SelfAttention(embed_dim, num_heads)
    print(f"    參數數量: {sum(p.numel() for p in attention.parameters()):,}")

    print(f"\n[2] 測試輸入...")
    x = torch.randn(batch_size, seq_len, embed_dim)
    print(f"    輸入形狀: {x.shape}")

    print(f"\n[3] 前向傳播...")
    with torch.no_grad():
        output = attention(x)
    print(f"    輸出形狀: {output.shape}")

    print(f"\n[4] 演示完成!")

if __name__ == "__main__":
    demo()