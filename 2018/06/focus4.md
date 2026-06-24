# 注意力機制：Attention 的原理

## 前言

注意力機制（Attention Mechanism）是深度學習的重要突破，2015 年提出後徹底改變了 NLP 領域。

## Seq2seq 模型的問題

傳統的 Encoder-Decoder 模型有一個瓶頸：
- Encoder 必须將所有資訊压缩到一個固定長度的向量
- 對於長序列，效果不佳

## Attention 的解決方案

讓 Decoder 在每個時間步都能看到整個輸入序列，並根據當前輸出動態選擇關注的輸入部分。

### Attention 公式

```python
# 計算 attention 分數
scores = torch.matmul(query, key.transpose(-2, -1))
scores = scores / math.sqrt(key_dim)

# softmax 獲得權重
attention_weights = F.softmax(scores, dim=-1)

# 加權求和
context = torch.matmul(attention_weights, value)
```

## Attention 的類型

### 1. Additive Attention

```python
score = v.tanh(W1 * query + W2 * key)
```

### 2. Dot-Product Attention

```python
score = (query * key).sum(dim=-1)
```

### 3. Multi-Head Attention

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.fc = nn.Linear(d_model, d_model)

    def forward(self, query, key, value):
        batch_size = query.size(0)

        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        attention_weights = F.softmax(scores, dim=-1)
        context = torch.matmul(attention_weights, V)

        return self.fc(context.transpose(1, 2).contiguous().view(batch_size, -1, d_model))
```

## Self-Attention

Self-Attention 是輸入序列內部的元素之間的注意力計算：

```
┌─────────────────────────────────────────────────────┐
│                  Self-Attention                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│   "The cat sat on the mat"                          │
│                                                     │
│   Attention weights:                                │
│   "cat" ───► 對 "The", "cat", "sat" 等的注意力      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

Self-Attention 是 Transformer 的核心組件。

## 結論

注意力機制解決了 Seq2seq 的瓶頸問題，為 Transformer 的發明奠定了基礎。GPT 使用的就是 Transformer 的解碼器部分。

---

**延伸閱讀**

- [Attention 機制詳解](https://www.google.com/search?q=attention+mechanism+deep+learning)
- [注意力機制論文](https://www.google.com/search?q=neural+machine+translation+by+jointly+learning+2015)

---

*本篇文章為「AI 程式人雜誌 2018 年 6 月號」GPT 與生成式 AI 系列之一。*