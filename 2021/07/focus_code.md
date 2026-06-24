# 程式：Transformer 與 BERT 實作

## 詞向量與注意力機制的 Python 實現

### 1. 注意力機制實現

以下是 Transformer 中 Scaled Dot-Product Attention 的實現：

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

def scaled_dot_product_attention(query, key, value, mask=None, dropout=0.1):
    """縮放點積注意力機制"""
    d_k = query.size(-1)

    scores = torch.matmul(query, key.transpose(-2, -1))
    scores = scores / math.sqrt(d_k)

    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)

    attention_weights = F.softmax(scores, dim=-1)

    if dropout > 0:
        attention_weights = F.dropout(attention_weights, p=dropout)

    return torch.matmul(attention_weights, value), attention_weights
```

### 2. Multi-Head Attention

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.wq = nn.Linear(d_model, d_model)
        self.wk = nn.Linear(d_model, d_model)
        self.wv = nn.Linear(d_model, d_model)
        self.dense = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def split_heads(self, x, batch_size):
        x = x.view(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(1, 2)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        q = self.split_heads(self.wq(query), batch_size)
        k = self.split_heads(self.wk(key), batch_size)
        v = self.split_heads(self.wv(value), batch_size)

        if mask is not None:
            mask = mask.unsqueeze(1)

        attn_output, attn_weights = scaled_dot_product_attention(
            q, k, v, mask, self.dropout.p
        )

        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, -1, self.d_model)

        return self.dense(attn_output), attn_weights
```

### 3. 位置編碼

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)

        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)
```

### 4. BERT 詞嵌入

```python
class BertEmbeddings(nn.Module):
    def __init__(self, vocab_size, hidden_size, max_position, type_vocab_size, dropout=0.1):
        super().__init__()
        self.word_embedding = nn.Embedding(vocab_size, hidden_size)
        self.position_embedding = nn.Embedding(max_position, hidden_size)
        self.token_type_embedding = nn.Embedding(type_vocab_size, hidden_size)
        self.LayerNorm = nn.LayerNorm(hidden_size)
        self.dropout = nn.Dropout(dropout)

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
        embeddings = self.LayerNorm(embeddings)
        embeddings = self.dropout(embeddings)

        return embeddings
```

### 5. Masked Language Model

```python
class MaskedLanguageModel(nn.Module):
    def __init__(self, hidden_size, vocab_size):
        super().__init__()
        self.dense = nn.Linear(hidden_size, hidden_size)
        self.activation = nn.Tanh()
        self.layer_norm = nn.LayerNorm(hidden_size)
        self.decoder = nn.Linear(hidden_size, vocab_size)

    def forward(self, hidden_states, masked_tokens):
        masked_hidden = hidden_states[masked_tokens]
        masked_hidden = self.dense(masked_hidden)
        masked_hidden = self.activation(masked_hidden)
        masked_hidden = self.layer_norm(masked_hidden)
        logits = self.decoder(masked_hidden)
        return logits
```

### 6. 簡單 Transformer Encoder

```python
class TransformerEncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, dff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, dff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(dff, d_model)
        )

        self.layernorm1 = nn.LayerNorm(d_model)
        self.layernorm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        attn_output, _ = self.self_attn(x, x, x, mask)
        x = self.layernorm1(x + self.dropout1(attn_output))

        ffn_output = self.ffn(x)
        x = self.layernorm2(x + self.dropout2(ffn_output))

        return x

class TransformerEncoder(nn.Module):
    def __init__(self, num_layers, d_model, num_heads, dff, vocab_size, dropout=0.1):
        super().__init__()
        self.embedding = BertEmbeddings(vocab_size, d_model, 512, 2, dropout)
        self.pos_encoding = PositionalEncoding(d_model, dropout=dropout)
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, dff, dropout)
            for _ in range(num_layers)
        ])

    def forward(self, x, mask=None):
        x = self.embedding(x)
        x = self.pos_encoding(x)

        for layer in self.layers:
            x = layer(x, mask)

        return x
```

### 7. 測試函數

```python
def demo():
    print("=== Transformer 與 BERT 實作演示 ===\n")

    d_model = 128
    num_heads = 4
    dff = 512
    vocab_size = 1000
    batch_size = 2
    seq_length = 10

    encoder = TransformerEncoder(
        num_layers=2,
        d_model=d_model,
        num_heads=num_heads,
        dff=dff,
        vocab_size=vocab_size
    )

    x = torch.randint(0, vocab_size, (batch_size, seq_length))

    encoder.eval()
    with torch.no_grad():
        output = encoder(x)

    print(f"輸入形狀: {x.shape}")
    print(f"輸出形狀: {output.shape}")
    print(f"模型總參數量: {sum(p.numel() for p in encoder.parameters()):,}")

    print("\n--- 注意力權重示例 ---")
    attn_layer = encoder.layers[0].self_attn
    q = torch.randn(batch_size, seq_length, d_model)
    k = torch.randn(batch_size, seq_length, d_model)
    v = torch.randn(batch_size, seq_length, d_model)

    attn_output, attn_weights = scaled_dot_product_attention(q, k, v)
    print(f"注意力輸出形狀: {attn_output.shape}")
    print(f"注意力權重形狀: {attn_weights.shape}")
    print(f"注意力權重總和（每行）: {attn_weights[0].sum(dim=-1)}")

if __name__ == "__main__":
    demo()
```

---

## 延伸閱讀

- [PyTorch Transformer 官方教程](https://www.google.com/search?q=PyTorch+nn+Transformer+tutorial)
- [BERT 官方實現](https://www.google.com/search?q=BERT+TensorFlow+official+implementation)
- [注意力機制視覺化](https://www.google.com/search?q=attention+visualization+transformer)