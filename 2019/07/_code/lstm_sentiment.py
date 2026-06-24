#!/usr/bin/env python3
"""LSTM Sentiment Analysis Demo"""

import torch
import torch.nn as nn

VOCAB_SIZE = 10000
EMBED_DIM = 128
HIDDEN_DIM = 256
NUM_LAYERS = 2
DROPOUT = 0.3
MAX_SEQ_LEN = 100

class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers, dropout):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.fc1 = nn.Linear(hidden_dim * 2, hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        hidden_concat = torch.cat([hidden[-2], hidden[-1]], dim=1)
        out = self.fc1(hidden_concat)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        return self.sigmoid(out).squeeze()

def demo():
    print("=" * 60)
    print("LSTM 情緒分析模型演示")
    print("=" * 60)

    print("\n[1] 初始化模型...")
    model = SentimentLSTM(
        vocab_size=10000,
        embed_dim=EMBED_DIM,
        hidden_dim=HIDDEN_DIM,
        num_layers=NUM_LAYERS,
        dropout=DROPOUT
    )
    print(f"   模型參數數量: {sum(p.numel() for p in model.parameters()):,}")

    print("\n[2] 前向傳播測試...")
    dummy_input = torch.randint(0, 10000, (32, MAX_SEQ_LEN))
    with torch.no_grad():
        output = model(dummy_input)
    print(f"   輸入形狀: {dummy_input.shape}")
    print(f"   輸出形狀: {output.shape}")
    print(f"   輸出範圍: [{output.min().item():.4f}, {output.max().item():.4f}]")

    print("\n[3] 演示完成!")

if __name__ == "__main__":
    demo()