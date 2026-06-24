# RNN 語言模型實戰

## 從理論到實作

本文使用 PyTorch 從零實作一個字元級 RNN 語言模型，並在繁體中文資料上進行訓練。

## 資料準備

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 字元級語言模型
with open("chinese_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

chars = sorted(list(set(text)))
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for i, ch in enumerate(chars)}
vocab_size = len(chars)

# 訓練序列
seq_length = 64
def get_batch(text, batch_size=32):
    starts = np.random.randint(0, len(text)-seq_length-1, batch_size)
    inputs, targets = [], []
    for start in starts:
        seq = text[start:start+seq_length+1]
        inputs.append([char_to_idx[ch] for ch in seq[:-1]])
        targets.append([char_to_idx[ch] for ch in seq[1:]])
    return (torch.tensor(inputs), torch.tensor(targets))
```

## 模型定義

```python
class CharRNN(nn.Module):
    def __init__(self, vocab_size, hidden_dim=256, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_dim)
        self.rnn = nn.RNN(hidden_dim, hidden_dim,
                          num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embedding(x)
        out, hidden = self.rnn(x, hidden)
        out = self.fc(out.reshape(-1, out.size(-1)))
        return out, hidden
```

## 訓練循環

```python
model = CharRNN(vocab_size, hidden_dim=256, num_layers=2)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    inputs, targets = get_batch(text, batch_size=64)
    optimizer.zero_grad()
    outputs, _ = model(inputs)
    loss = criterion(outputs, targets.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
    optimizer.step()
    if epoch % 10 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")
```

## 文本生成

```python
def generate(model, start_str, length=200, temperature=0.8):
    model.eval()
    chars = [char_to_idx[ch] for ch in start_str]
    hidden = None
    result = start_str

    for _ in range(length):
        x = torch.tensor([chars[-1:]]).unsqueeze(0)
        with torch.no_grad():
            output, hidden = model(x, hidden)
        probs = nn.functional.softmax(output[0, 0] / temperature, dim=0)
        next_idx = torch.multinomial(probs, 1).item()
        result += idx_to_char[next_idx]
        chars.append(next_idx)
    return result

# 溫度參數控制隨機性
# temperature=0.1 → 確定性輸出（重複常見模式）
# temperature=1.0 → 平衡創造性
# temperature=2.0 → 高隨機性（可能產生不合理文本）
```

## 實驗結果

使用 100  epochs 訓練後，模型可以生成語法基本合理的句子。增加 hidden_dim 和 num_layers 可以提高生成品質，但也增加了過擬合風險。

## 字級 vs 詞級模型

| 特性 | 字級模型 | 詞級模型 |
|------|---------|---------|
| 詞彙量 | 數千（中文字元） | 數萬到數十萬 |
| OOV 問題 | 低 | 高 |
| 生成彈性 | 高（可組合新詞） | 低（受限於詞彙表） |
| 語義理解 | 差（需要學習組詞規則） | 好（直接操作詞義） |

## 延伸閱讀

- [PyTorch RNN 教學](https://www.google.com/search?q=PyTorch+RNN+language+model+tutorial)
- [Karpathy RNN 有效性](https://www.google.com/search?q=the+unreasonable+effectiveness+of+recurrent+neural+networks)
