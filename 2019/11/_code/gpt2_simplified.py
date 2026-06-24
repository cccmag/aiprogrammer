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

class TransformerLM(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_encoding = PositionalEncoding(d_model)

        self.decoder_layers = nn.ModuleList([
            nn.TransformerDecoderLayer(d_model, num_heads, dim_feedforward=d_model * 4, dropout=0.1)
            for _ in range(num_layers)
        ])

        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, x, memory_mask=None):
        x = self.token_embedding(x) * math.sqrt(x.size(-1))
        x = self.position_encoding(x)

        for layer in self.decoder_layers:
            x = layer(x, x, tgt_mask=None, tgt_key_padding_mask=None)

        return self.fc(x)

def demo():
    print("Simplified Transformer Language Model Demo")
    print("=" * 50)

    vocab_size = 10000
    d_model = 256
    num_heads = 8
    num_layers = 6

    torch.manual_seed(42)

    model = TransformerLM(vocab_size, d_model, num_heads, num_layers)
    model.eval()

    seq_len = 10
    batch_size = 2
    x = torch.randint(0, vocab_size, (batch_size, seq_len))

    print(f"Vocabulary size: {vocab_size}")
    print(f"Model dimension: {d_model}")
    print(f"Number of heads: {num_heads}")
    print(f"Number of layers: {num_layers}")
    print()
    print(f"Input sequence shape: {x.shape}")

    with torch.no_grad():
        output = model(x)
        logits = output[:, -1, :]
        probabilities = torch.softmax(logits, dim=-1)
        next_token = torch.argmax(probabilities, dim=-1)

    print(f"Output shape: {output.shape}")
    print(f"Next token probabilities shape: {probabilities.shape}")
    print(f"Predicted next tokens: {next_token.tolist()}")
    print()
    print("Note: This is a simplified implementation.")
    print("The actual GPT-2 model uses:")
    print("- 48 layers, 1600 hidden dimension, 25 heads")
    print("- 1.5B parameters total")
    print("- Learned positional embeddings")

if __name__ == "__main__":
    demo()