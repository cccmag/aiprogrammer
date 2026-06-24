#!/usr/bin/env python3
import math
import torch
import torch.nn as nn

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, num_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.ReLU(),
            nn.Linear(d_model * 4, d_model)
        )

    def forward(self, x, mask=None):
        attn_output, _ = self.attention(x, x, x, attn_mask=mask)
        x = self.norm1(x + attn_output)
        ff_output = self.ff(x)
        x = self.norm2(x + ff_output)
        return x

def demo():
    print("2019 Key Models Implementation Demo")
    print("=" * 50)

    d_model = 256
    num_heads = 8
    seq_len = 10
    batch_size = 2

    block = TransformerBlock(d_model, num_heads)

    x = torch.randn(batch_size, seq_len, d_model)

    print(f"Input shape: {x.shape}")
    print(f"d_model: {d_model}, num_heads: {num_heads}")

    output = block(x)
    print(f"Output shape: {output.shape}")
    print()

    print("2019 Key Models Summary:")
    print("- BERT: Transformer Encoder with MLM + NSP")
    print("- GPT-2: Transformer Decoder with 48 layers, 1.5B params")
    print("- RoBERTa: BERT with optimized training")
    print("- XLNet: Permutation Language Model")
    print("- T5: Text-to-Text Transfer Transformer")

if __name__ == "__main__":
    demo()