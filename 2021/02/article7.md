# 循環神經網路與 LSTM

## RNN 的問題

標準 RNN 存在梯度消失問題，難以學習長期依賴：

```python
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.W = nn.Linear(input_size + hidden_size, hidden_size)

    def forward(self, x, h):
        combined = torch.cat([x, h], dim=1)
        h = torch.tanh(self.W(combined))
        return h
```

## LSTM 結構

長短期記憶網路透過門控機制解決梯度消失：

```
LSTM 單元：
┌──────────────────────────────────────┐
│  forget gate    → 決定丟棄什麼資訊   │
│  input gate     → 決定儲存什麼新資訊 │
│  output gate    → 決定輸出什麼      │
└──────────────────────────────────────┘
```

```python
class LSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        # 四個門
        self.W = nn.Linear(input_size + hidden_size, 4 * hidden_size)

    def forward(self, x, state):
        h, c = state
        combined = torch.cat([x, h], dim=1)
        gates = self.W(combined)

        # 分割為四個門
        f, i, o, g = gates.chunk(4, dim=1)

        f = torch.sigmoid(f)  # forget
        i = torch.sigmoid(i)  # input
        o = torch.sigmoid(o)  # output
        g = torch.tanh(g)     # candidate

        c = f * c + i * g     # cell state
        h = o * torch.tanh(c) # hidden state

        return h, (h, c)
```

## PyTorch LSTM API

```python
lstm = nn.LSTM(
    input_size=256,
    hidden_size=512,
    num_layers=2,
    batch_first=True,
    dropout=0.1,
    bidirectional=True
)

output, (h_n, c_n) = lstm(input)
```

---

## 延伸閱讀

- [LSTM 原理詳解](https://www.google.com/search?q=LSTM+long+short+term+memory)
- [PyTorch+LSTM+API](https://www.google.com/search?q=PyTorch+LSTM+example)
- [GRU+vs+LSTM](https://www.google.com/search?q=GRU+vs+LSTM+comparison)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*