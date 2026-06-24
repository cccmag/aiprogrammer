# LSTM 在序列處理中的應用

## 前言

長短期記憶網路（LSTM）是處理序列資料的強大工具。1997 年由 Hochreiter 和 Schmidhuber 提出。

## LSTM 的核心組件

### 門控機制

- **遺忘門**：决定丢弃什麼資訊
- **輸入門**：决定存储什麼新資訊
- **輸出門**：决定輸出什麼

### 細胞狀態

長期資訊沿著細胞狀態傳遞。

## LSTM 的 Python 實現

```python
import torch
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMClassifier, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
```

## 應用場景

1. **機器翻譯**：Seq2Seq 模型
2. **情感分析**：文字分類
3. **語音辨識**：聲學建模
4. **時間序列預測**：金融、天氣

## 結論

LSTM 開創了序列建模的新時代，現在被 Transformer 架構所補充。

---

**延伸閱讀**

- [LSTM 原始論文](https://www.google.com/search?q=LSTM+Hochreiter+1997)
- [LSTM 教程](https://www.google.com/search?q=LSTM+tutorial+pytorch)