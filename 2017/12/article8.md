# 自然語言處理：word2vec 到 Transformer

## 前言

2017 年是 NLP 領域的重要轉折點。Transformer 架構的提出為日後大型語言模型奠定了基礎。

## Word2Vec 的成功

```python
# Word2Vec 仍然是重要的基礎技術

from gensim.models import Word2Vec

sentences = [
    ["machine", "learning", "is", "fun"],
    ["deep", "learning", "is", "powerful"],
    ["natural", "language", "processing", "is", "cool"]
]

model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

# 詞向量
vec = model.wv["learning"]
print(f"Word embedding shape: {vec.shape}")

# 相似詞
similar = model.wv.most_similar("learning")
print(f"Similar words: {similar}")
```

## LSTM 與 GRU

```python
# LSTM (Long Short-Term Memory)
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=2,
            bidirectional=True,
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded)

        # 合併雙向 hidden states
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)

        return self.fc(hidden)
```

## Attention 機制

```python
# Bahdanau Attention
class Attention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim):
        super().__init__()
        self.attn = nn.Linear(encoder_dim + decoder_dim, decoder_dim)
        self.v = nn.Parameter(torch.rand(decoder_dim))

    def forward(self, encoder_outputs, decoder_hidden):
        seq_len = encoder_outputs.size(1)

        decoder_hidden = decoder_hidden.unsqueeze(1).repeat(1, seq_len, 1)

        energy = torch.tanh(
            self.attn(torch.cat([encoder_outputs, decoder_hidden], dim=2))
        )
        energy = energy.sum(dim=-1)

        attention_weights = F.softmax(energy, dim=1)
        context = attention_weights.unsqueeze(1).bmm(encoder_outputs)

        return context.squeeze(1), attention_weights
```

## Transformer (2017)

```python
# 《Attention Is All You Need》中的 Transformer

class TransformerEncoder(nn.Module):
    def __init__(self, d_model, num_heads, num_layers):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads)
            for _ in range(num_layers)
        ])

    def forward(self, x, mask=None):
        for layer in self.layers:
            x = layer(x, mask)
        return x

class TransformerEncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionwiseFeedForward(d_model)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)

    def forward(self, x, mask=None):
        attn_output = self.self_attn(x, x, x, mask)
        x = self.norm1(x + attn_output)
        ff_output = self.feed_forward(x)
        x = self.norm2(x + ff_output)
        return x
```

## 2017 年 NLP 成就

```
┌─────────────────────────────────────────────────────────┐
│              2017 年 NLP 重要發展                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  翻譯:                                               │
│  - Google Neural Machine Translation 投入使用          │
│  - Transformer 論文發表                                 │
│                                                         │
│  預訓練:                                               │
│  - ELMo 概念形成 (2018年發布)                           │
│                                                         │
│  框架:                                               │
│  - AllenNLP 發布                                        │
│  - spaCy 2.0                                           │
│                                                         │
│  應用:                                               │
│  - 對話系統進步                                        │
│  - 情感分析普及                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 對日後的影響

Transformer 的提出為以下技術奠定基礎：
- BERT (2018)
- GPT-2 (2019)
- GPT-3 (2020)
- 以及後續所有大型語言模型

---

**延伸閱讀**

- [Word2Vec Paper](https://www.google.com/search?q=word2vec+mikolov+2013)
- [Attention Is All You Need](https://www.google.com/search?q=attention+is+all+you+need+2017)
- [LSTM Paper](https://www.google.com/search?q=lstm+hochreiter+1997)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*