# RNN 與 LSTM 基礎

## 為什麼需要 RNN？

傳統神經網路無法處理序列資料，因為它們沒有「記憶」。RNN（循環神經網路）通過將前一時刻的輸出傳回當前時刻，解決了序列依賴問題。

## RNN 的基本結構

```
輸入 x_t → Hidden h_t → 輸出 o_t
          ↑            |
          └────────────┘（時間循環）
```

在時間步 t：
- h_t = f(W·x_t + U·h_{t-1} + b)
- o_t = g(V·h_t + c)

## 簡單 RNN 的問題：梯度消失

當序列很長時，反向傳播的梯度會逐漸縮小，導致早期時刻的資訊無法有效學習。

```
序列: the cat sat on the mat ... (很長) ... was tired
梯度傳播時，long-distance dependencies 很難學習
```

## LSTM（長短期記憶網路）

LSTM 由 Sepp Hochreiter 與 Jürgen Schmidhuber 在 1997 年提出，是 RNN 的變體，專門解決長期依賴問題。

### LSTM 的核心：記憶單元

LSTM 使用三個門（gate）控制資訊流動：
1. **遺忘門（Forget Gate）** - 決定丟棄什麼資訊
2. **輸入門（Input Gate）** - 決定儲存什麼新資訊
3. **輸出門（Output Gate）** - 決定輸出什麼

### 公式

```
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)      # 遺忘門
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)      # 輸入門
C_t = f_t * C_{t-1} + i_t * tanh(W_C · [h_{t-1}, x_t] + b_C)  # 記憶單元
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)      # 輸出門
h_t = o_t * tanh(C_t)                     # 隱藏狀態
```

## PyTorch 實作 LSTM

```python
import torch
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # x: (batch_size, sequence_length)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        output, (hidden, cell) = self.lstm(embedded)
        # 取最後時刻的隱藏狀態
        return self.fc(hidden[-1])

# 使用範例
model = LSTMClassifier(vocab_size=10000, embedding_dim=100, hidden_dim=128, output_dim=2)
```

## Keras 實作 LSTM

```python
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

model = Sequential([
    Embedding(input_dim=10000, output_dim=100, input_length=200),
    LSTM(128, return_sequences=False),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()
```

## 文字分類的完整流程

```python
import numpy as np
from collections import Counter

# 1. 建立詞彙表
def build_vocab(texts, min_freq=2):
    word_counts = Counter()
    for text in texts:
        word_counts.update(text.lower().split())
    vocab = {word: idx+2 for idx, (word, count) in enumerate(word_counts.items()) if count >= min_freq}
    vocab['<PAD>'] = 0
    vocab['<UNK>'] = 1
    return vocab

# 2. 文字轉索引
def text_to_indices(text, vocab, max_len=200):
    words = text.lower().split()
    indices = [vocab.get(w, vocab['<UNK>']) for w in words]
    if len(indices) < max_len:
        indices += [vocab['<PAD>']] * (max_len - len(indices))
    return indices[:max_len]

# 3. 準備資料（示意）
texts = ["I love this movie", "This is terrible", "Great film", "Boring"]
labels = [1, 0, 1, 0]

vocab = build_vocab(texts)
X = np.array([text_to_indices(t, vocab) for t in texts])
y = np.array(labels)

print("Vocab:", vocab)
print("X:", X)
print("y:", y)
```

## LSTM 的應用場景

| 任務 | 應用 |
|------|------|
| 文字分類 | 新聞分類、垃圾郵件偵測 |
| 序列標注 | 命名實體識別、詞性標注 |
| 語言模型 | 文字生成、機器翻譯 |
| 問答系統 | 答案抽取 |

## 總結

RNN 透過循環連接處理序列資料，但有梯度消失問題。LSTM 的門機制有效解決長期依賴，成為 NLP 深度學習的基石。下一期我們將介紹 NLP 工具生態系。