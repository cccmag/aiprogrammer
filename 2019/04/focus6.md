# 類神經網路與 NLP

## RNN 序列建模

傳統的類神經網路（如 CNN）無法有效處理序列資料，因為它們沒有記憶機制。循環神經網路（RNN）透過引入 Hidden State 來處理序列依賴。

---

## RNN 的基本結構

```
輸入序列：x1, x2, x3, ..., xt
          ↓   ↓   ↓       ↓
        ┌────┬────┬──┬────┐
        │ RNN│ RNN│  │ RNN│
        │ h1 │ h2 │  │ ht │
        └────┴────┴──┴────┘
```

### 前向傳播

```python
import numpy as np

class SimpleRNN:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size

        # 權重矩陣
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.1
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.1
        self.Why = np.random.randn(input_size, hidden_size) * 0.1
        self.bh = np.zeros((hidden_size, 1))
        self.by = np.zeros((input_size, 1))

    def forward(self, x):
        """
        x: (input_size,) 輸入向量
        """
        seq_len = len(x)
        h = np.zeros((self.hidden_size, seq_len + 1))

        for t in range(seq_len):
            h[:, t] = np.tanh(
                self.Wxh @ x[t] + self.Whh @ h[:, t-1] + self.bh
            )

        return h

    def step_forward(self, x, prev_h):
        """單步前向傳播"""
        next_h = np.tanh(self.Wxh @ x + self.Whh @ prev_h + self.bh)
        return next_h
```

---

## LSTM 與 GRU

標準 RNN 存在梯度消失問題，難以學習長期依賴。LSTM（Long Short-Term Memory）和 GRU（Gated Recurrent Unit）透過門控機制解決這個問題。

### LSTM 結構

```python
class LSTM:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size

        # 輸入閘、遺忘閘、輸出閘
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * 0.1

    def step_forward(self, x, prev_h, prev_c):
        """
        LSTM 單步前向傳播

        閘機制：
        - 遺忘閘：決定丟棄什麼資訊
        - 輸入閘：決定儲存什麼新資訊
        - 輸出閘：決定輸出什麼
        """
        combined = np.concatenate([x, prev_h])

        # 遺忘閘
        f = sigmoid(self.Wf @ combined)

        # 輸入閘
        i = sigmoid(self.Wi @ combined)
        c_tilde = np.tanh(self.Wc @ combined)

        # 細胞狀態更新
        c = f * prev_c + i * c_tilde

        # 輸出閘
        o = sigmoid(self.Wo @ combined)
        h = o * np.tanh(c)

        return h, c

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
```

### LSTM 視覺化

```
                    ┌──────────────┐
         prev_h ────►│              │
                    │   遺忘閘 (f)  │────► 遺忘多少過去
         prev_c ────►│              │
                    └──────────────┘

                    ┌──────────────┐
         prev_h ────►│              │
                    │   輸入閘 (i)  │────► 加入多少新資訊
                    │  細胞候選    │────► 新細胞內容
         prev_c ────►│  (c_tilde)   │
                    └──────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │  細胞狀態更新 │
                    │  c = f*c + i*c_tilde
                    └──────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │   輸出閘 (o)  │────► 輸出多少
                    │   h = o * tanh(c)
                    └──────────────┘
```

### GRU 結構

GRU 是 LSTM 的簡化版本，合併了遺忘閘和輸入閘：

```python
class GRU:
    def step_forward(self, x, prev_h):
        combined = np.concatenate([x, prev_h])

        # 重置閘
        r = sigmoid(self.Wr @ combined)

        # 更新閘
        z = sigmoid(self.Wz @ combined)

        # 候選隱藏狀態
        h_tilde = np.tanh(self.Wh @ np.concatenate([x, r * prev_h]))

        # 隱藏狀態更新
        h = z * prev_h + (1 - z) * h_tilde

        return h
```

---

## 文字分類應用

### 使用 LSTM 进行文字分類

```python
import numpy as np

class TextClassifier:
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_classes):
        self.embedding = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.lstm = LSTM(embedding_dim, hidden_dim)
        self.output = np.random.randn(num_classes, hidden_dim) * 0.1

    def forward(self, text):
        """
        text: (seq_len,) 文字序列（詞索引）
        """
        # 嵌入
        x = self.embedding[text]

        # LSTM
        h, _ = self.lstm.forward(x)

        # 取最後隱藏狀態
        final_h = h[:, -1]

        # 輸出分類
        scores = self.output @ final_h
        probs = softmax(scores)

        return probs

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)
```

---

## 雙向 RNN

雙向 RNN 同時處理正向和反向序列：

```python
class BidirectionalLSTM:
    def __init__(self, input_size, hidden_size):
        self.forward_lstm = LSTM(input_size, hidden_size)
        self.backward_lstm = LSTM(input_size, hidden_size)

    def forward(self, x):
        # 正向
        h_forward, _ = self.forward_lstm.forward(x)

        # 反向（反轉輸入）
        x_reversed = x[::-1]
        h_backward, _ = self.backward_lstm.forward(x_reversed)
        h_backward = h_backward[:, ::-1]  # 翻轉回來

        # 拼接
        h = np.concatenate([h_forward, h_backward], axis=0)
        return h
```

---

## 文字分類的 PyTorch 實作

```python
import torch
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, text):
        # text: (seq_len, batch)
        embedded = self.embedding(text)  # (seq_len, batch, embed_dim)

        lstm_out, (hidden, cell) = self.lstm(embedded)

        # 取最後隱藏狀態（雙向需要拼接）
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)

        return self.fc(hidden)
```

---

## 注意力機制

注意力機制讓模型能夠「關注」輸入序列的不同部分：

```python
class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.attn = nn.Linear(hidden_dim * 2, hidden_dim * 2)
        self.v = nn.Parameter(torch.rand(hidden_dim * 2))

    def forward(self, hidden, encoder_outputs):
        # hidden: (hidden_dim,)
        # encoder_outputs: (seq_len, hidden_dim * 2)

        seq_len = encoder_outputs.shape[0]

        # 計算注意力分數
        hidden_repeated = hidden.unsqueeze(0).repeat(seq_len, 1)
        energy = torch.tanh(self.attn(torch.cat([hidden_repeated, encoder_outputs], dim=1)))
        energy = energy @ self.v  # (seq_len,)

        # 計算注意力權重
        attention = torch.softmax(energy, dim=0)

        # 加權平均
        context = (attention.unsqueeze(1) @ encoder_outputs.unsqueeze(0)).squeeze(1)

        return context, attention
```

---

## 延伸閱讀

- [LSTM 原始論文](https://www.google.com/search?q=LSTM+Hochreiter+1997)
- [GRU 論文](https://www.google.com/search?q=GRU+Cho+2014)
- [NLP RNN 教程](https://www.google.com/search?q=RNN+LSTM+NLP+tutorial)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」系列文章之一。*