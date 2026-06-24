# 自然語言處理：Word2Vec, Attention, Neural Machine Translation

## 前言

2017 年自然語言處理領域經歷了重要轉變。注意力機制（Attention）的成功為日後 Transformer 架構的誕生奠定了基礎。

## Word2Vec 的成功

### Word2Vec 簡介

2013 年提出的 Word2Vec 仍然是 2017 年 NLP 的重要基礎：

```python
# Gensim 中的 Word2Vec
from gensim.models import Word2Vec

sentences = [["word", "embedding", "example"],
             ["natural", "language", "processing"]]

model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

# 獲取詞向量
vector = model.wv["word"]
print(f"Embedding dim: {vector.shape}")

# 詞類比
result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'])
print(result)
```

### 詞嵌入的應用

```python
# 詞嵌入用於文本分類
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)  # (batch, seq_len, embedding_dim)
        output, (hidden, cell) = self.lstm(embedded)
        final_hidden = hidden[-1]  # 最後一層的最後隱藏狀態
        return self.fc(final_hidden)
```

## 注意力機制的興起

### Sequence-to-Sequence with Attention

```python
class Attention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim):
        super().__init__()
        self.encoder_dim = encoder_dim
        self.decoder_dim = decoder_dim

        # 計算 attention 權重
        self.attn = nn.Linear(encoder_dim + decoder_dim, decoder_dim)
        self.v = nn.Parameter(torch.rand(decoder_dim))

    def forward(self, encoder_outputs, decoder_hidden):
        """
        encoder_outputs: (batch, seq_len, encoder_dim)
        decoder_hidden: (batch, decoder_dim)
        """
        seq_len = encoder_outputs.size(1)

        # 擴展 decoder hidden
        decoder_hidden = decoder_hidden.unsqueeze(1).repeat(1, seq_len, 1)

        # 計算 energy
        energy = torch.tanh(self.attn(torch.cat([encoder_outputs, decoder_hidden], dim=2)))
        energy = energy.sum(-1)  # (batch, seq_len)

        # Softmax 得到權重
        attention_weights = F.softmax(energy, dim=1)  # (batch, seq_len)

        # 加權求和
        context = attention_weights.unsqueeze(1).bmm(encoder_outputs)  # (batch, 1, encoder_dim)

        return context.squeeze(1), attention_weights
```

### Attention 的視覺化

```
┌─────────────────────────────────────────────────────────┐
│              Attention 權重視覺化                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  輸入句子: "The cat sat on the mat"                     │
│                                                         │
│  Attention 熱力圖:                                     │
│                        the    cat    sat    on    mat  │
│               the    [0.1]  [0.2]  [0.05] [0.3] [0.35] │
│               cat    [0.15] [0.5]  [0.1]  [0.05] [0.2]  │
│               sat    [0.05] [0.15] [0.6]  [0.1]  [0.1]  │
│               on     [0.2]  [0.05] [0.1]  [0.5]  [0.15] │
│               mat    [0.15] [0.1]  [0.05] [0.2]  [0.5]  │
│                                                         │
│  目標單詞: sat                                         │
│  注意到 "cat" 是主詞，"on" 是位置                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Neural Machine Translation

### Transformer 之前的 NMT

2017 年的主流 NMT 架構：

```python
class Seq2Seq(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.encoder = Encoder(src_vocab_size, embed_dim, hidden_dim)
        self.decoder = Decoder(tgt_vocab_size, embed_dim, hidden_dim)

    def forward(self, src, tgt):
        # 編碼
        encoder_outputs, encoder_hidden = self.encoder(src)

        # 解碼（帶 Attention）
        decoder_outputs, _ = self.decoder(tgt, encoder_outputs, encoder_hidden)

        return decoder_outputs
```

### 《Attention Is All You Need》

2017 年 12 月，Google Brain 發表了 Transformer 論文：

```python
# Transformer 的核心思想（2017 年論文）
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_model = d_model
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        # 線性變換
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)

        # 分頭
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        # Scaled Dot-Product Attention
        scores = Q @ K.transpose(-2, -1) / (self.d_k ** 0.5)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = F.softmax(scores, dim=-1)
        context = attention_weights @ V

        # 合併頭
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)

        return self.W_o(context)
```

## 2017 年 NLP 重要發展

```
┌─────────────────────────────────────────────────────────┐
│              2017 年 NLP 重要發展                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Word Embeddings:                                      │
│  - Word2Vec 仍是主流                                   │
│  - FastText 獲得更多應用                               │
│  - 上下文相關嵌入開始興起                               │
│                                                         │
│  Sequence Modeling:                                    │
│  - LSTM/GRU 仍是標準                                   │
│  - Attention 機制成為標配                             │
│  - Transformer 論文發表                                │
│                                                         │
│  翻譯:                                               │
│  - Google Neural Machine Translation 投入使用          │
│  - Attention Is All You Need (12月)                   │
│                                                         │
│  預訓練模型:                                           │
│  - ELMo (2018年初) - 預訓練 LM                         │
│  - 為日後 BERT 奠定基礎                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 對話系統進展

```python
# 簡單的對話生成模型
class DialogueModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.encoder = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.decoder = nn.LSTM(embed_dim, hidden_dim, batch_first=True)

        # Attention
        self.attention = Attention(hidden_dim, hidden_dim)

        self.output = nn.Linear(hidden_dim, vocab_size)

    def forward(self, input_text, target_text):
        # 編碼輸入
        encoder_outputs, encoder_hidden = self.encoder(self.embedding(input_text))

        # 解碼輸出
        decoder_hidden = encoder_hidden
        outputs = []

        for t in range(target_text.size(1)):
            # Attention 加權
            context, _ = self.attention(encoder_outputs, decoder_hidden[0])

            # 一步解碼
            decoder_input = self.embedding(target_text[:, t:t+1]).squeeze(1)
            decoder_output, decoder_hidden = self.decoder(
                decoder_input.unsqueeze(1),
                decoder_hidden
            )

            output = self.output(decoder_output.squeeze(1))
            outputs.append(output)

        return torch.stack(outputs, dim=1)
```

## 總結

2017 年是 NLP 的轉折點：

1. **Word2Vec 仍是基礎**：但上下文相關嵌入開始顯現
2. **Attention 成為標配**：幾乎所有序列模型都使用注意力
3. **Transformer 誕生**：為日後大型語言模型奠定基礎
4. **NMT 實用化**：Google 將 NMT 投入實際服務

---

**延伸閱讀**

- [Word2Vec (Mikolov et al., 2013)](https://www.google.com/search?q=word2vec+mikolov+2013)
- [Attention Is All You Need (Vaswani et al., 2017)](https://www.google.com/search?q=Attention+Is+All+You+Need+2017)
- [Neural Machine Translation (Sutskever et al., 2014)](https://www.google.com/search?q=seq2seq+neural+machine+translation)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*