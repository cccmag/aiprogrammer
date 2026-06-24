# LSTM 文本生成

## 超越 RNN 的長期記憶

LSTM 透過門控機制解決了 RNN 的梯度消失問題，在文本生成任務上表現更佳。本文以金庸小說為訓練資料進行實戰。

## LSTM 模型

```python
class CharLSTM(nn.Module):
    def __init__(self, vocab_size, hidden_dim=512, num_layers=3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_dim)
        self.lstm = nn.LSTM(hidden_dim, hidden_dim,
                           num_layers, batch_first=True,
                           dropout=0.3 if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, state=None):
        x = self.embedding(x)
        out, state = self.lstm(x, state)
        out = self.fc(out.reshape(-1, out.size(-1)))
        return out, state
```

## 中文文本處理

```python
# 金庸小說字元統計
# 天龍八部：約 120 萬字，12,000+ 不同字元
# 射鵰英雄傳：約 100 萬字

def load_jinyong(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # 保留中文字元和基本標點
    import re
    text = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f，。！？、]', '', text)
    return text

# 建立字元索引
text = load_jinyong("jinyong.txt")
chars = sorted(list(set(text)))
vocab_size = len(chars)
print(f"字元數: {len(text)}")
print(f"不同字元: {vocab_size}")
```

## 訓練策略

```python
def train_lstm(model, text, epochs=50, batch_size=128, seq_len=128):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

    for epoch in range(epochs):
        model.train()
        hidden = None
        total_loss = 0
        # 使用 stateful LSTM：保留跨 batch 的隱藏狀態
        for i in range(0, len(text) - seq_len - 1, seq_len):
            seq = text[i:i+seq_len+1]
            inputs = torch.tensor([char_to_idx[ch] for ch in seq[:-1]]).unsqueeze(0)
            targets = torch.tensor([char_to_idx[ch] for ch in seq[1:]])

            optimizer.zero_grad()
            outputs, hidden = model(inputs, hidden)
            hidden = tuple(h.detach() for h in hidden)
            loss = criterion(outputs, targets.view(-1))
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            optimizer.step()
            total_loss += loss.item()

        scheduler.step()
        avg_loss = total_loss / ((len(text) - seq_len) // seq_len)
        print(f"Epoch {epoch}: loss={avg_loss:.4f}")
```

## 文本生成實例

訓練數個 epoch 後，使用不同溫度參數生成：

```python
def generate_text(model, seed, length=200, temperature=0.6):
    model.eval()
    chars = list(seed)
    hidden = None

    for _ in range(length):
        x = torch.tensor([char_to_idx[ch] for ch in chars[-seq_len:]]).unsqueeze(0)
        with torch.no_grad():
            output, hidden = model(x, hidden)
        logits = output[0, -1] / temperature
        probs = F.softmax(logits, dim=0)
        next_idx = torch.multinomial(probs, 1).item()
        chars.append(idx_to_char[next_idx])

    return "".join(chars)
```

**溫度的作用**：
- **低溫度（0.2-0.5）**：輸出較確定，傾向於高頻詞，重複性高
- **中溫度（0.6-0.9）**：創造性與連貫性的平衡
- **高溫度（1.0-1.5）**：多樣性高，但可能不合理

## 生成效果

使用 LSTM（3層、512維）訓練金庸全集後：
- 能生成風格相近的武俠文句
- 能使用正確的人物名稱和武功招式
- 長程情節連貫性有限

## 延伸閱讀

- [LSTM 文本生成教學](https://www.google.com/search?q=LSTM+text+generation+tutorial+PyTorch)
- [溫度參數解釋](https://www.google.com/search?q=softmax+temperature+scaling+explained)
