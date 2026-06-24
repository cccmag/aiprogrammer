# RNN/LSTM 文字分類

## 1. 文字資料處理

### Tokenization 與 Embedding

```python
from torchtext.data import Field, TabularDataset, Iterator

TEXT = Field(sequential=True, tokenize='spacy', lower=True)
LABEL = Field(sequential=False, is_target=True)

# 定義資料集
train_data, test_data = TabularDataset.splits(
    path='.',
    train='train.csv',
    test='test.csv',
    format='csv',
    fields=[('text', TEXT), ('label', LABEL)]
)

# 建立詞彙表
TEXT.build_vocab(train_data, max_size=25000)
LABEL.build_vocab(train_data)

# DataLoader
train_iter = Iterator(train_data, batch_size=32, sort_key=lambda x: len(x.text))
```

## 2. LSTM 模型

```python
class TextLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, text):
        # text: (batch_size, seq_len)
        embedded = self.embedding(text)  # (batch_size, seq_len, embed_dim)

        lstm_out, (hidden, cell) = self.lstm(embedded)
        # hidden: (1, batch_size, hidden_dim)

        return self.fc(hidden.squeeze(0))
```

## 3. 雙向 LSTM

```python
class TextBiLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim,
                           batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)  # 乘以 2 因為雙向

    def forward(self, text):
        embedded = self.embedding(text)
        lstm_out, (hidden, cell) = self.lstm(embedded)

        # 合併前向和後向 hidden state
        hidden_concat = torch.cat([hidden[-2], hidden[-1]], dim=1)

        return self.fc(hidden_concat)
```

## 4. 訓練與評估

```python
def train_epoch(model, iterator, optimizer, criterion):
    model.train()
    total_loss = 0
    for batch in iterator:
        optimizer.zero_grad()
        predictions = model(batch.text)
        loss = criterion(predictions, batch.label)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(iterator)

def evaluate(model, iterator, criterion):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in iterator:
            predictions = model(batch.text).argmax(1)
            correct += (predictions == batch.label).sum().item()
            total += len(batch.label)
    return correct / total
```

## 5. 小結

LSTM 是處理序列資料的經典架構，文字分類是其典型應用場景。

---

**參考資料**
- [LSTM Text Classification](https://www.google.com/search?q=LSTM+text+classification+PyTorch+tutorial)
- [NLP with PyTorch](https://www.google.com/search?q=PyTorch+NLP+tutorial+text+classification)