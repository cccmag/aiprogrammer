# 類神經網路語言模型：RNN 與 LSTM 的應用

## 前言

類神經網路為語言模型帶來了革命性變化。它們能夠學習更複雜的語言模式，並处理长期依赖問題。

## RNN 語言模型

### 結構

```
┌─────────────────────────────────────────────────────┐
│              RNN 語言模型結構                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   w_t ──►嵌入──► h_t ──► h_{t+1}                   │
│           │        │        │                        │
│           ▼        ▼        ▼                       │
│         權重共享   隱藏層    輸出                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 前向傳播

```python
class RNNLM:
    def __init__(self, vocab_size, embed_size, hidden_size):
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.RNN(embed_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, h):
        x = self.embed(x)
        out, h = self.rnn(x, h)
        logits = self.fc(out)
        return logits, h
```

## LSTM 語言模型

LSTM 的門控機制更好地处理长期依赖：

```python
class LSTM_LM(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size,
                           num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embedding(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out)
        return out, hidden
```

## 類神經網路語言模型的優勢

1. **泛化能力**：學習類似的上下文模式
2. **長期依賴**：LSTM/GRU 能記憶長期資訊
3. **詞嵌入**：學習詞的語意向量表示

## 訓練技巧

### 梯度裁剪

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5)
```

### 計劃採樣

```python
if np.random.random() < teacher_forcing_ratio:
    next_input = target[:, t]
else:
    next_input = predicted[:, t-1]
```

## 結語

類神經網路語言模型解決了 N-gram 的多个問題。基於 RNN/LSTM 的語言模型为后来的 Transformer 架構奠定了基礎。

---

**延伸閱讀**

- [RNN 語言模型](https://www.google.com/search?q=RNN+language+model+pytorch)
- [LSTM 語言模型詳解](https://www.google.com/search?q=LSTM+language+model+tutorial)

---

*本篇文章為「AI 程式人雜誌 2018 年 6 月號」GPT 與生成式 AI 系列之一。*