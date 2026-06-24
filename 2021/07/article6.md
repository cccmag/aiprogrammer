# Transformer 架構詳解

Transformer 架構是現代 NLP 的基石。本文詳細解析其核心組件。

## 1. 自注意力機制

自注意力讓序列中的每個位置都能關注其他所有位置：

```python
def self_attention(query, key, value):
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, value)
```

## 2. 多頭注意力

多頭注意力讓模型能夠同時關注不同方面的關係：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.wq = nn.Linear(d_model, d_model)
        self.wk = nn.Linear(d_model, d_model)
        self.wv = nn.Linear(d_model, d_model)
        self.dense = nn.Linear(d_model, d_model)

    def split_heads(self, x):
        x = x.view(-1, self.num_heads, self.d_k)
        return x.transpose(1, 2)

    def forward(self, q, k, v):
        q = self.split_heads(self.wq(q))
        k = self.split_heads(self.wk(k))
        v = self.split_heads(self.wv(v))
        attn = self_attention(q, k, v)
        return self.dense(attn)
```

## 3. 位置編碼

Transformer 使用正弦/餘弦位置編碼來注入序列順序資訊。

## 4. 結論

Transformer 的並行計算能力和長距離依賴建模能力，使其成為 NLP 領域的核心架構。

---

## 延伸閱讀

- [《Attention Is All You Need》論文](https://www.google.com/search?q=Attention+Is+All+You+Need+paper)
- [Transformer 視覺化教程](https://www.google.com/search?q=Transformer+visualization+tutorial)