# 主題五：詞向量與嵌入技術

## Word2Vec、ELMo、BERT 嵌入

### 1. 詞向量的起源

語言學中的「分佈假說」指出：一個詞的意義由其上下文決定。詞向量（Word Embedding）正是這一思想的數學體現——將詞映射到連續的向量空間。

**傳統方法**：
- One-hot 編碼：高維度、稀疏、無法表達語義關係
- 詞袋模型：忽略詞序、無法處理歧義

### 2. Word2Vec

2013 年，Tomas Mikolov 等人在 Google 發表了 Word2Vec，開啟了現代詞向量時代：

```python
class Word2Vec(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        self.target_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.context_embeddings = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, target, context, labels):
        target_emb = self.target_embeddings(target)
        context_emb = self.context_embeddings(context)

        scores = torch.sum(target_emb * context_emb, dim=1)
        loss = F.binary_cross_entropy_with_logits(scores, labels.float())
        return loss
```

**兩種訓練方式**：
- **CBOW**：用上下文預測中心詞
- **Skip-gram**：用中心詞預測上下文

**Word2Vec 的特性**：
- 相似的詞在向量空間中距離較近
- 詞之間的語義關係可以透過向量運算表達
- 經典案例：king - man + woman ≈ queen

### 3. GloVe

GloVe（Global Vectors）於 2014 年提出，結合了全局矩陣分解和局部上下文方法的優點：

```python
def glove_loss(weights, cooccurrence, target_emb, context_emb, biases):
    """GloVe 損失函數"""
    predictions = torch.sum(target_emb * context_emb, dim=1) + biases

    # 加權均方誤差
    weight = torch.where(cooccurrence > 0,
                        torch.pow(cooccurrence, 0.75),
                        torch.zeros_like(cooccurrence))

    loss = weight * (predictions - torch.log(cooccurrence + 1)) ** 2
    return torch.sum(loss)
```

**GloVe 的優勢**：
- 利用全局共現統計資訊
- 訓練效率高
- 產生的詞向量在類比任務上表現優秀

### 4. ELMo

2018 年，Allen AI 發表 ELMo（Embeddings from Language Models），首次引入「動態詞向量」概念：

```python
class ELMo(nn.Module):
    def __init__(self, num_layers, hidden_size, vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_size)
        self.lstm = nn.LSTM(embedding_size, hidden_size, num_layers, bidirectional=True)

    def forward(self, input_ids):
        embeddings = self.embedding(input_ids)
        lstm_output, _ = self.lstm(embeddings)

        # 組合多層 LSTM 輸出
        output = torch.cat([lstm_output[:, -1, :hidden_size],
                           lstm_output[:, 0, hidden_size:]], dim=-1)

        # 加權組合
        weights = F.softmax(self.attention_weights, dim=0)
        final_embedding = torch.sum(weights.unsqueeze(-1) * output, dim=0)

        return final_embedding
```

**ELMo 的創新**：
- 基於雙向 LSTM
- 每個詞的表示是所有層的加權平均
- 同一個詞在不同上下文中有不同表示

### 5. BERT 嵌入

BERT 的嵌入是當前最強大的詞表示方法之一：

```python
class BertEmbedding(nn.Module):
    def __init__(self, vocab_size, hidden_size, max_position, type_vocab_size):
        super().__init__()
        self.word_embedding = nn.Embedding(vocab_size, hidden_size)
        self.position_embedding = nn.Embedding(max_position, hidden_size)
        self.token_type_embedding = nn.Embedding(type_vocab_size, hidden_size)
        self.norm = nn.LayerNorm(hidden_size)
        self.dropout = nn.Dropout(0.1)

    def forward(self, input_ids, token_type_ids=None):
        seq_length = input_ids.size(1)
        position_ids = torch.arange(seq_length, dtype=torch.long, device=input_ids.device)
        position_ids = position_ids.unsqueeze(0).expand_as(input_ids)

        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)

        words = self.word_embedding(input_ids)
        positions = self.position_embedding(position_ids)
        token_types = self.token_type_embedding(token_type_ids)

        embeddings = words + positions + token_types
        embeddings = self.norm(embeddings)
        embeddings = self.dropout(embeddings)

        return embeddings
```

### 6. 嵌入空間的幾何特性

詞嵌入具有一些有趣的幾何特性：

**語義相似性**：
- 最近鄰搜尋可以找到語義相關的詞
- 餘弦相似度是最常用的度量

**語義運算**：
- 類比推理：v(king) - v(man) + v(woman) ≈ v(queen)
- 語義遷移

**語義向量的層次結構**：
- 抽象詞和具體詞在空間中分佈不同
- 名詞、動詞、形容詞有不同的分佈模式

### 7. 從靜態到動態

詞向量技術經歷了從靜態到動態的演進：

| 模型 | 上下文感知 | 代表 |
|------|-----------|------|
| Word2Vec | 否 | 靜態詞向量 |
| GloVe | 否 | 靜態詞向量 |
| ELMo | 是 | 淺層動態 |
| BERT | 是 | 深層動態 |
| GPT | 是 | 深層動態 |

動態詞向量能夠根據上下文調整表示，解決了一詞多義等問題。

---

## 延伸閱讀

- [Word2Vec 原始論文](https://www.google.com/search?q=Word2Vec+distributed+representations+vectors)
- [ELMo 論文](https://www.google.com/search?q=ELMo+deep+contextualized+word+representations)
- [BERT 嵌入详解](https://www.google.com/search?q=BERT+embeddings+word+representations)