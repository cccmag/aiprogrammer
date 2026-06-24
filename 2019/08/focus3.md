# 自注意力機制

## 序列內部的 Attention

自注意力（Self-Attention）是注意力機制的一種重要變體，它允許序列中的每個位置關注同一序列中的所有其他位置。這個概念是 Transformer 架構的核心。

---

## 自注意力的定義

### 與傳統注意力的區別

```
傳統注意力（用於翻譯）：
- Query 來自解碼器
- Keys/Values 來自編碼器
- 跨序列的交互

自注意力：
- Query, Keys, Values 都來自同一序列
- 序列內部的交互
- 捕捉內部結構
```

### 視覺化

```
┌─────────────────────────────────────────────────────┐
│                  自注意力圖示                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   輸入序列: [x1, x2, x3, x4, x5]                  │
│                                                     │
│   自注意力：每個位置與所有位置計算相關性            │
│                                                     │
│   x1 ←── α_{1,1} ──→ x1                            │
│    │  ↖       ↗   ↖       ↗                        │
│    │ α_{2,1}  α_{1,2} α_{1,3} α_{1,5}             │
│    ↓       ↑   ↓       ↑                           │
│   x2 ←── α_{2,2} ──→ x2                            │
│    │  ↖       ↗   ↖       ↗                        │
│    │ α_{3,2}  α_{2,3} α_{2,4} α_{2,5}             │
│    ↓       ↑   ↓       ↑                           │
│   x3 ←── α_{3,3} ──→ x3                            │
│                                                     │
│   每個位置的輸出是所有位置的加權和                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 自注意力的數學表示

### 基本公式

```python
# 自注意力的核心計算
class SelfAttention(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        self.embed_dim = embed_dim

    def forward(self, x):
        # x: [batch, seq_len, embed_dim]

        # 計算 Q, K, V
        Q = x  # 查詢
        K = x  # 鍵
        V = x  # 值

        # 計算注意力分數
        scores = torch.matmul(Q, K.transpose(-2, -1))
        # scores: [batch, seq_len, seq_len]

        # 縮放
        scores = scores / (self.embed_dim ** 0.5)

        # Softmax
        weights = F.softmax(scores, dim=-1)

        # 加權求和
        output = torch.matmul(weights, V)
        # output: [batch, seq_len, embed_dim]

        return output
```

---

## Non-Local Neural Networks

### 2018 年的重要論文

Non-Local Neural Networks（Wang et al., 2018）將自注意力引入 CNN：

```python
# Non-Local Block 的實現
class NonLocalBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.inter_channel = channels // 2
        self.query_conv = nn.Conv2d(channels, self.inter_channel, 1)
        self.key_conv = nn.Conv2d(channels, self.inter_channel, 1)
        self.value_conv = nn.Conv2d(channels, channels, 1)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        batch, channels, height, width = x.size()

        # Q, K, V
        query = self.query_conv(x).view(batch, -1, height * width).permute(0, 2, 1)
        key = self.key_conv(x).view(batch, -1, height * width)
        value = self.value_conv(x).view(batch, -1, height * width)

        # 注意力
        energy = torch.bmm(query, key)
        attention = self.softmax(energy / (channels ** 0.5))

        # 輸出
        out = torch.bmm(value, attention.permute(0, 2, 1))
        out = out.view(batch, channels, height, width)

        return x + out  # 殘差連接
```

---

## 自注意力的優勢

### 1. 直接捕捉長距離依賴

```
RNN 的問題：
- 需要通過多個時間步傳遞資訊
- 梯度路徑長，容易衰減

自注意力的優勢：
- 任意兩個位置之間的直接連接
- 路徑長度 O(1)
```

### 2. 可並行計算

```
RNN：必須順序計算
h1 → h2 → h3 → h4 → h5

自注意力：可以並行
所有位置可以同時計算 Q, K, V
```

### 3. 可解釋性

注意力權重可以直觀顯示詞與詞之間的關係：

```
"The cat sat on the mat because it was tired"

注意力權重（"it" 對其他詞的注意力）：
- "The": 0.05
- "cat": 0.85  ← 高注意力
- "sat": 0.02
- "on": 0.01
- "the": 0.02
- "mat": 0.02
- "because": 0.01
- "was": 0.01
- "tired": 0.01

"it" 正確地指向前面的 "cat"
```

---

## 應用場景

### 1. 文字分類

```python
# 自注意力用於文字分類
class AttentionClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_classes):
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.attention = SelfAttention(embed_dim)
        self.classifier = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)
        attended = self.attention(embedded)
        pooled = attended.mean(dim=1)  # 全域池化
        return self.classifier(pooled)
```

### 2. 語言模型

自注意力允許語言模型在生成每個詞時看到序列中的任意位置。

### 3. 問答系統

```python
# 問答中的自注意力
class QAWithAttention(nn.Module):
    def __init__(self, embed_dim, hidden_dim):
        self.self_attention = SelfAttention(embed_dim)
        self.bi_attention = BiAttention(hidden_dim)

    def forward(self, context, question):
        # 自注意力：用於編碼上下文
        context = self.self_attention(context)

        # 雙向注意力：用於上下文-問題交互
        output = self.bi_attention(context, question)

        return output
```

---

## 多頭注意力

### 思想

使用多個注意力頭，每個頭學習不同的注意力模式：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.W_q = nn.Linear(embed_dim, embed_dim)
        self.W_k = nn.Linear(embed_dim, embed_dim)
        self.W_v = nn.Linear(embed_dim, embed_dim)
        self.W_o = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        batch, seq_len, embed_dim = x.size()

        # 線性變換
        Q = self.W_q(x).view(batch, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.W_k(x).view(batch, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.W_v(x).view(batch, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # 注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        weights = F.softmax(scores, dim=-1)
        attended = torch.matmul(weights, V)

        # 拼接並輸出
        attended = attended.transpose(1, 2).contiguous().view(batch, seq_len, embed_dim)
        return self.W_o(attended)
```

### 多頭注意力的直覺

每個頭可以專注於不同的關係：

```
句子: "The dog chased the cat because it was hungry"

頭 1（主語-動詞關係）：
- "chased" 關注 "dog"

頭 2（共參照關係）：
- "it" 關注 "cat"

頭 3（因果關係）：
- "because" 關注 "hungry"
```

---

## 總結

自注意力的關鍵創新：

1. **序列內部交互**：捕捉序列的內部結構
2. **並行計算**：提高計算效率
3. **直接依賴**：任意位置之間的直接連接
4. **多頭擴展**：學習多樣的注意力模式

自注意力是 Transformer 的核心，下一章我們將看到它如何與其他元件結合，形成完整的 Transformer 架構。

---

## 延伸閱讀

- [Self Attention Paper](https://www.google.com/search?q=self+attention+机制+self-attention+paper)
- [Non-Local Neural Networks](https://www.google.com/search?q=non-local+neural+networks+self+attention)
- [Multi-Head Attention Explained](https://www.google.com/search?q=multi-head+attention+explained)

---

*本篇文章為「AI 程式人雜誌 2019 年 8 月號」注意力機制系列之三。*