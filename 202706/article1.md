# 從零實作 Transformer：完整的 Python 教學

## 前言

Transformer 架構自 2017 年由 Vaswani 等人提出以來，已成為現代深度學習的基石。從 BERT、GPT 到當今的 Llama、Gemini，所有大型語言模型的核心都是 Transformer。本文將帶領讀者從零開始，用 Python 與 PyTorch 實作一個完整的 Transformer，並在小型資料集上訓練與生成。

## Transformer 的設計哲學

在開始實作之前，我們需要理解 Transformer 的設計理念。不同於 RNN 的序列處理方式，Transformer 採用「並行處理 + 注意力篩選」的架構。這意味著模型在每一層都能同時「看到」整個序列，並透過注意力權重決定哪些資訊是重要的。這種設計帶來兩個重大優勢：訓練速度大幅提升（可並行計算）、長距離依賴捕捉能力顯著增強。

完整的 Transformer 包含 Encoder 與 Decoder 兩個子模型。Encoder 負責將輸入序列轉換為豐富的表示向量，Decoder 則根據這些表示逐步生成輸出序列。我們將逐一實作每個元件，從最底層的嵌入與位置編碼開始，逐步堆疊出完整的模型。

### 嵌入層與位置編碼

Transformer 沒有遞迴結構，也缺乏卷積的局部感知能力，因此必須透過位置編碼注入序列順序資訊。原始論文的設計非常巧妙：使用不同頻率的正弦與餘弦函數，讓模型可以透過線性變換輕易學會相對位置關係。這種編碼方式無需訓練參數，且能推廣到訓練時未見過的序列長度。

```python
import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() *
                             (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:x.size(1)]
```

### 多頭注意力機制

多頭注意力（Multi-Head Attention）是 Transformer 最核心的元件。它的靈感來自人類的注意力機制：當我們閱讀一句話時，並非平等對待每個詞，而是會根據當前的理解目標，將注意力集中在關鍵詞上。多頭注意力進一步將這個過程複製多次，每次使用不同的線性投影，讓模型能從不同角度觀察序列中的關聯性。例如，在處理「它」這個代名詞時，一個注意力頭可能專注於尋找最近的動物名詞，另一個頭可能關注句子的主語位置，第三個頭則可能捕捉語法結構中的長期依賴。

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, nhead):
        super().__init__()
        self.nhead = nhead
        self.d_k = d_model // nhead
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        Q = self.w_q(query).view(batch_size, -1, self.nhead, self.d_k).transpose(1, 2)
        K = self.w_k(key).view(batch_size, -1, self.nhead, self.d_k).transpose(1, 2)
        V = self.w_v(value).view(batch_size, -1, self.nhead, self.d_k).transpose(1, 2)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = torch.softmax(scores, dim=-1)
        out = torch.matmul(attn, V).transpose(1, 2).contiguous()
        out = out.view(batch_size, -1, self.nhead * self.d_k)
        return self.w_o(out)
```

### Feed-Forward 與層歸一化

每個注意力層後接一個前饋網路與 LayerNorm：

```python
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff=2048):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )

    def forward(self, x):
        return self.net(x)

class TransformerBlock(nn.Module):
    def __init__(self, d_model, nhead, d_ff):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, nhead)
        self.ff = FeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x), mask)
        x = x + self.ff(self.norm2(x))
        return x
```

### 完整 Transformer 模型

組裝 Encoder-Decoder：

```python
class Transformer(nn.Module):
    def __init__(self, vocab_size, d_model=512, nhead=8, d_ff=2048, num_layers=6):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos = PositionalEncoding(d_model)
        self.encoder = nn.ModuleList([TransformerBlock(d_model, nhead, d_ff)
                                       for _ in range(num_layers)])
        self.decoder = nn.ModuleList([TransformerBlock(d_model, nhead, d_ff)
                                       for _ in range(num_layers)])
        self.out = nn.Linear(d_model, vocab_size)

    def forward(self, src, tgt):
        src = self.pos(self.embed(src))
        tgt = self.pos(self.embed(tgt))
        for layer in self.encoder:
            src = layer(src)
        for layer in self.decoder:
            tgt = layer(tgt, None)
        return self.out(tgt)
```

## 訓練範例

使用小型加法資料集訓練模型學會數字加法：

```python
import torch.optim as optim

vocab = "0123456789+= "  # 簡單的字彙表
stoi = {c: i for i, c in enumerate(vocab)}
itos = {i: c for c, i in stoi.items()}
vocab_size = len(vocab)

def encode(s):
    return [stoi[c] for c in s]

def decode(tokens):
    return ''.join(itos[t] for t in tokens)

# 資料：12+34=46 格式
data = [f"{a}+{b}={a+b}" for a in range(100) for b in range(100)]
data = [s.ljust(7) for s in data]  # 補齊到固定長度

model = Transformer(vocab_size, d_model=64, nhead=4, d_ff=128, num_layers=2)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    total_loss = 0
    for sample in data:
        src = torch.tensor(encode(sample[:-1])).unsqueeze(0)
        tgt = torch.tensor(encode(sample[:-1])).unsqueeze(0)
        target = torch.tensor(encode(sample[1:])).unsqueeze(0)
        optimizer.zero_grad()
        out = model(src, tgt)
        loss = criterion(out.view(-1, vocab_size), target.view(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch}: loss = {total_loss/len(data):.4f}")
```

## 生成範例

訓練後進行推論：

```python
def generate(model, prompt, max_len=10):
    model.eval()
    with torch.no_grad():
        src = torch.tensor(encode(prompt)).unsqueeze(0)
        tgt = src.clone()
        for _ in range(max_len):
            out = model(src, tgt)
            next_token = out[0, -1].argmax().item()
            tgt = torch.cat([tgt, torch.tensor([[next_token]])], dim=1)
            if itos[next_token] == "=":
                break
        return decode(tgt[0].tolist())

print(generate(model, "34+56"))  # 預期輸出: 34+56=90
```

## 參考資源

- [Transformer 原始論文](https://www.google.com/search?q=Attention+is+All+You+Need+paper)
- [PyTorch Transformer 官方教學](https://www.google.com/search?q=pytorch+transformer+tutorial)
- [The Annotated Transformer](https://www.google.com/search?q=The+Annotated+Transformer+Harvard+NLP)
