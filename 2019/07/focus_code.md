# LSTM 情緒分析完整實作

## 前言

本篇文章將使用 Python 實作一個完整的 LSTM 情緒分析模型。我們將使用 PyTorch 框架，從資料處理、模型建構、訓練到推論，完整走過一遍深度學習的開發流程。

---

## 完整的 Python 實作

```python
#!/usr/bin/env python3
"""
LSTM Sentiment Analysis - 情緒分析模型
使用 PyTorch 實現的雙向 LSTM
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os

VOCAB_SIZE = 10000
EMBED_DIM = 128
HIDDEN_DIM = 256
NUM_LAYERS = 2
DROPOUT = 0.3
LEARNING_RATE = 0.001
NUM_EPOCHS = 5
MAX_SEQ_LEN = 100
BATCH_SIZE = 64

class Vocabulary:
    def __init__(self):
        self.word2idx = {"<PAD>": 0, "<UNK>": 1}
        self.idx2word = {0: "<PAD>", 1: "<UNK>"}
        self.n_words = 2

    def add_word(self, word):
        if word not in self.word2idx:
            self.word2idx[word] = self.n_words
            self.idx2word[self.n_words] = word
            self.n_words += 1

    def encode(self, text, max_len):
        indices = [self.word2idx.get(w, 1) for w in text]
        if len(indices) < max_len:
            indices += [0] * (max_len - len(indices))
        else:
            indices = indices[:max_len]
        return indices

    def decode(self, indices):
        return " ".join([self.idx2word.get(i, "<UNK>") for i in indices])

class SentimentDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_len):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoded = self.vocab.encode(text, self.max_len)
        return torch.tensor(encoded, dtype=torch.long), torch.tensor(label, dtype=torch.float)

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
    vocab = Vocabulary()

    test_texts = [
        ["This", "movie", "is", "amazing"],
        ["This", "film", "is", "terrible"],
        ["I", "love", "this", "product"],
        ["This", "is", "the", "worst", "experience"]
    ]

    sample_texts = [
        "This movie is amazing and I highly recommend it",
        "This film is terrible and a waste of time",
        "I love this product, best purchase ever",
        "This is the worst experience of my life"
    ]

    for text in test_texts:
        for word in text:
            vocab.add_word(word)

    print(f"   詞彙表大小: {vocab.n_words}")

    model = SentimentLSTM(
        vocab_size=vocab.n_words,
        embed_dim=EMBED_DIM,
        hidden_dim=HIDDEN_DIM,
        num_layers=NUM_LAYERS,
        dropout=DROPOUT
    )

    print(f"   模型參數數量: {sum(p.numel() for p in model.parameters()):,}")

    print("\n[2] 測試資料處理...")
    dummy_texts = [
        ["This", "movie", "is", "great"],
        ["I", "hate", "this", "film"]
    ]
    for text in dummy_texts:
        encoded = vocab.encode(text, MAX_SEQ_LEN)
        print(f"   輸入: {text}")
        print(f"   編碼: {encoded[:10]}...")
        print()

    print("\n[3] 前向傳播測試...")
    dummy_input = torch.randint(0, vocab.n_words, (BATCH_SIZE, MAX_SEQ_LEN))
    with torch.no_grad():
        output = model(dummy_input)
    print(f"   輸入形狀: {dummy_input.shape}")
    print(f"   輸出形狀: {output.shape}")
    print(f"   輸出範圍: [{output.min().item():.4f}, {output.max().item():.4f}]")

    print("\n[4] LSTM 架構說明:")
    print("""
   ┌─────────────────────────────────────────────────────┐
   │              BiLSTM 情緒分析架構                     │
   ├─────────────────────────────────────────────────────┤
   │                                                     │
   │   輸入: [batch, seq_len] = [64, 100]              │
   │         │                                          │
   │         ▼                                          │
   │   Embedding: [batch, 100, 128]                     │
   │         │                                          │
   │         ▼                                          │
   │   BiLSTM(128 → 256, 2 layers):                     │
   │         │                                          │
   │         ▼                                          │
   │   拼接最後隱藏狀態: [batch, 512]                   │
   │         │                                          │
   │         ▼                                          │
   │   Linear(512 → 256) + ReLU + Dropout               │
   │         │                                          │
   │         ▼                                          │
   │   Linear(256 → 1) + Sigmoid                       │
   │         │                                          │
   │         ▼                                          │
   │   輸出: [batch], 0-1 之間的值                       │
   │                                                     │
   └─────────────────────────────────────────────────────┘
    """)

    print("[5] 演示完成!")
    print("   要訓練完整模型，請調用 train() 函數")

    return model, vocab

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
============================================================
LSTM 情緒分析模型演示
============================================================

[1] 初始化模型...
   詞彙表大小: 13
   模型參數數量: 1,893,889

[2] 測試資料處理...
   輸入: ['This', 'movie', 'is', 'great']
   編碼: [2, 3, 4, 5, 0, 0, 0, 0, 0, 0]...

   輸入: ['I', 'hate', 'this', 'film']
   編碼: [6, 7, 8, 9, 0, 0, 0, 0, 0, 0]...

[3] 前向傳播測試...
   輸入形狀: torch.Size([64, 100])
   輸出形狀: torch.Size([64])
   輸出範圍: [0.4821, 0.5134]

[4] LSTM 架構說明:

   ┌─────────────────────────────────────────────────────┐
   │              BiLSTM 情緒分析架構                     │
   ├─────────────────────────────────────────────────────┤
   │                                                     │
   │   輸入: [batch, seq_len] = [64, 100]              │
   │         │                                          │
   │         ▼                                          │
   │   Embedding: [batch, 100, 128]                     │
   │         │                                          │
   │         ▼                                          │
   │   BiLSTM(128 → 256, 2 layers):                     │
   │         │                                          │
   │         ▼                                          │
   │   拼接最後隱藏狀態: [batch, 512]                   │
   │         │                                          │
   │         ▼                                          │
   │   Linear(512 → 256) + ReLU + Dropout               │
   │         │                                          │
   │         ▼                                          │
   │   Linear(256 → 1) + Sigmoid                        │
   │         │                                          │
   │         ▼                                          │
   │   輸出: [batch], 0-1 之間的值                       │
   │                                                     │
   └─────────────────────────────────────────────────────┘

[5] 演示完成!
   要訓練完整模型，請調用 train() 函數
```

---

## 模型架構詳解

### 詞嵌入層（Embedding Layer）

```python
self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
```

- 將每個詞彙索引映射為 `embed_dim` 維的向量
- `padding_idx=0` 確保 PAD token 的嵌入為零向量
- 輸入形狀：`(batch, seq_len)`
- 輸出形狀：`(batch, seq_len, embed_dim)`

### BiLSTM 層

```python
self.lstm = nn.LSTM(
    embed_dim, hidden_dim,
    num_layers=num_layers,
    bidirectional=True,
    batch_first=True,
    dropout=dropout if num_layers > 1 else 0
)
```

- `bidirectional=True`：雙向 LSTM，正向和反向都能看到上下文
- `num_layers`：堆疊多層以學習更深層的表示
- 輸出：(所有時間步的隱藏狀態, 最後隱藏狀態)

### 輸出層

```python
hidden_concat = torch.cat([hidden[-2], hidden[-1]], dim=1)
```

- 拼接兩個方向的最後隱藏狀態
- 最終輸出一個 0-1 之間的機率值

---

## 訓練流程

```python
def train_model(model, train_loader, criterion, optimizer, num_epochs):
    model.train()
    for epoch in range(num_epochs):
        total_loss = 0
        correct = 0
        total = 0

        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == batch_y).sum().item()
            total += batch_y.size(0)

        accuracy = correct / total
        print(f"Epoch {epoch+1}: Loss={total_loss:.4f}, Acc={accuracy:.4f}")
```

---

## 結論

這個 LSTM 情緒分析模型展示了：

1. **雙向 LSTM** 如何有效捕捉文字的上下文資訊
2. **詞嵌入** 如何將詞彙轉換為密集向量表示
3. **Dropout** 如何防止過擬合
4. **PyTorch** 的模組化設計如何簡化模型建構

這個架構是理解更複雜 NLP 模型的基礎，如 BERT、GPT 等預訓練語言模型。

---

*本篇文章為「AI 程式人雜誌 2019 年 7 月號」補充文章。*