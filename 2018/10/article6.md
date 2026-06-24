# 雙向 Transformer 實作

## Transformer Encoder 結構

BERT 的核心是 Transformer Encoder 層，每層包含：
1. Multi-Head Self-Attention
2. Add & Layer Normalization
3. Feed-Forward Network
4. Add & Layer Normalization

以下是一個簡化的 Python 實現：

## 位置編碼

```python
import numpy as np
import math

def get_positional_encoding(max_seq_len, d_model):
    pe = np.zeros((max_seq_len, d_model))
    for pos in range(max_seq_len):
        for i in range(0, d_model, 2):
            pe[pos, i] = math.sin(pos / (10000 ** (i / d_model)))
            pe[pos, i + 1] = math.cos(pos / (10000 ** (i / d_model)))
    return pe
```

## Scaled Dot-Product Attention

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = np.dot(Q, K.T) / math.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    attention_weights = softmax(scores, axis=-1)
    output = np.dot(attention_weights, V)
    return output, attention_weights

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
```

## Multi-Head Attention

```python
class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
    def split_heads(self, x):
        batch_size = x.shape[0]
        x = x.reshape(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(0, 2, 1, 3)
    
    def forward(self, Q, K, V, mask=None):
        Q = self.split_heads(Q)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        output, attention_weights = scaled_dot_product_attention(Q, K, V, mask)
        output = output.transpose(0, 2, 1, 3).reshape(output.shape[0], -1, self.d_model)
        return output
```

## Feed-Forward Network

```python
class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.02
        self.W2 = np.random.randn(d_ff, d_model) * 0.02
        
    def forward(self, x):
        return np.maximum(0, np.dot(x, self.W1.T)) @ self.W2.T  # ReLU
```

## 完整的 Encoder 層

```python
class TransformerEncoderLayer:
    def __init__(self, d_model, num_heads, d_ff):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = LayerNorm(d_model)
        self.ff = FeedForward(d_model, d_ff)
        self.norm2 = LayerNorm(d_model)
        
    def forward(self, x, mask=None):
        # Self-attention with residual
        attn_output = self.attention.forward(x, x, x, mask)
        x = self.norm1.forward(x + attn_output)
        
        # Feed-forward with residual
        ff_output = self.ff.forward(x)
        x = self.norm2.forward(x + ff_output)
        return x
```

## 參考資源

- https://www.google.com/search?q=Transformer+Encoder+实现+Python+NumPy+多头注意力+详细
- https://www.google.com/search?q=positional+encoding+Transformer+Python+实现+详解
- https://www.google.com/search?q=BERT+简化版+从零实现+Python+NLP+教程+2018