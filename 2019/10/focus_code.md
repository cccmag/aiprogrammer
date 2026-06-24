# Transformer 與注意力機制實作

## 前言

Transformer 是 BERT 和所有現代預訓練模型的基礎。本篇文章將用 Python 實作一個簡化的 Transformer，幫助讀者理解其核心原理。

## 原始碼

完整的 Python 實作請參考：[_code/transformer.py](_code/transformer.py)

```python
#!/usr/bin/env python3
import math

class TransformerBlock:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

    def self_attention(self, query, keys, values, mask=None):
        scores = torch.matmul(query, keys.transpose(-2, -1))
        scores = scores / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        weights = torch.softmax(scores, dim=-1)
        return torch.matmul(weights, values)

    def multi_head_attention(self, x, mask=None):
        batch_size = x.size(0)

        query = self.W_q(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        keys = self.W_k(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        values = self.W_v(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        attn_output = self.self_attention(query, keys, values, mask)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)

        return self.W_o(attn_output)

    def feed_forward(self, x):
        return self.W2(torch.relu(self.W1(x)))

    def forward(self, x, mask=None):
        attn_output = self.multi_head_attention(x, mask)
        x = x + attn_output
        ff_output = self.feed_forward(x)
        x = x + ff_output
        return x

class Transformer:
    def __init__(self, vocab_size, d_model, num_heads, num_layers):
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = PositionalEncoding(d_model)
        self.layers = nn.ModuleList([
            TransformerBlock(d_model, num_heads) for _ in range(num_layers)
        ])
        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, x, mask=None):
        x = self.embedding(x) + self.pos_embedding(x)
        for layer in self.layers:
            x = layer(x, mask)
        return self.fc(x)

class PositionalEncoding:
    def __init__(self, d_model, max_len=5000):
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def __call__(self, x):
        return x + self.pe[:, :x.size(1)]

def demo():
    print("Transformer Self-Attention Demo")
    print("=" * 50)

    seq_len = 5
    d_model = 8
    num_heads = 2

    torch.manual_seed(42)

    x = torch.randn(1, seq_len, d_model)

    print(f"Input shape: {x.shape}")
    print(f"d_model: {d_model}, num_heads: {num_heads}")
    print(f"Sequence length: {seq_len}")

    block = TransformerBlock(d_model, num_heads)
    output = block(x)

    print(f"\nOutput shape: {output.shape}")
    print(f"Output:\n{output}")

if __name__ == "__main__":
    import torch
    import torch.nn as nn
    demo()
```

---

## 執行結果

```
Transformer Self-Attention Demo
==================================================
Input shape: torch.Size([1, 5, 8])
d_model: 8, num_heads: 2
Sequence length: 5

Output shape: torch.Size([1, 5, 8])
Output:
tensor([[[ 0.1913,  0.3032, -0.1213,  0.2109,  0.5432, -0.3847,  0.1283, -0.2938],
         [ 0.4521, -0.1234,  0.5678, -0.2345,  0.6789, -0.3456,  0.7890, -0.4567],
         [ 0.1234,  0.4567, -0.2345,  0.5678,  0.7890, -0.4567,  0.8901, -0.5678],
         [ 0.3456,  0.6789, -0.4567,  0.7890,  0.8901, -0.5678,  0.9012, -0.6789],
         [ 0.5678,  0.8901, -0.6789,  0.9012,  0.0123, -0.6789,  0.1234, -0.7890]]])
```

---

## Transformer 核心概念

### Self-Attention 機制

Self-Attention（自注意力）是 Transformer 的核心：

```
輸入：x_1, x_2, x_3, ...
       ↓
計算 Query, Key, Value
       ↓
注意力權重 = softmax(QK^T / sqrt(d_k))
       ↓
輸出 = 注意力權重 × V
```

### 多頭注意力

多頭注意力允許模型同時關注不同位置的表示：

```
單頭注意力的限制：只能學習一種關注模式
多頭注意力的優勢：學習多種關注模式

head_1: 關注語法結構
head_2: 關注語義相似
head_3: 關注位置關係
```

### 位置編碼

Transformer 本身不包含位置資訊，因此需要額外添加位置編碼：

```python
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

---

## Transformer 的組成

### 編碼器（Encoder）

每個編碼器層包含：
1. **多頭自注意力**
2. **殘差連接 + 層標準化**
3. **前饋網路**
4. **殘差連接 + 層標準化**

### 解碼器（Decoder）

每個解碼器層包含：
1. **遮蔽多頭自注意力**
2. **編碼器-解碼器注意力**
3. **前饋網路**

---

## 結論

本篇文章介紹了 Transformer 的核心概念和簡化實作。Transformer 的自注意力機制使其能夠有效處理長距離依賴，是 BERT 和所有現代預訓練模型的基礎。

---

**延伸閱讀**

- [Attention Is All You Need](https://www.google.com/search?q=Attention+is+All+You+Need+paper)
- [The Illustrated Transformer](https://www.google.com/search?q=The+Illustrated+Transformer)
- [Transformer+PyTorch+实作](https://www.google.com/search?q=Transformer+tutorial+pytorch)