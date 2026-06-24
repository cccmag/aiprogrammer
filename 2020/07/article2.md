# 用 Python 實作簡單的 Transformer 架構

## 前言

Transformer 架構自 2017 年提出以來，已成為 NLP 領域的核心。本文中，我們將用 Python 從零實作一個簡化的 Transformer，幫助讀者理解其工作原理。

---

## 一、整體架構

```
輸入 -> 詞嵌入 + 位置編碼 -> Encoder（多層）
                                    -> 解碼器（多層）-> 輸出
```

### 主要元件

1. **詞嵌入（Word Embedding）**：將 token 轉換為向量
2. **位置編碼（Positional Encoding）**：注入序列順序資訊
3. **注意力機制（Attention）**：捕捉序列內的依賴關係
4. **前饋網路（Feed Forward）**：非線性轉換

---

## 二、詞嵌入與位置編碼

```python
import math
import numpy as np

class TokenEmbedding:
    def __init__(self, vocab_size, d_model):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.embeddings = np.random.randn(vocab_size, d_model) * 0.1

    def forward(self, token_ids):
        return self.embeddings[token_ids]

class PositionalEncoding:
    def __init__(self, d_model, max_len=5000):
        self.d_model = d_model
        self.pe = np.zeros((max_len, d_model))
        
        for pos in range(max_len):
            for i in range(0, d_model, 2):
                self.pe[pos, i] = math.sin(pos / (10000 ** (i / d_model)))
                if i + 1 < d_model:
                    self.pe[pos, i + 1] = math.cos(pos / (10000 ** ((i + 1) / d_model)))

    def forward(self, seq_len):
        return self.pe[:seq_len]
```

---

## 三、注意力機制

### Scaled Dot-Product Attention

```python
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def attention(Q, K, V, mask=None):
    """
    Q: (batch, heads, seq_len, d_k)
    K: (batch, heads, seq_len, d_k)
    V: (batch, heads, seq_len, d_v)
    """
    d_k = Q.shape[-1]
    
    # 計算注意力分數
    scores = np.matmul(Q, K.transpose(0, 1, 3, 2)) / math.sqrt(d_k)
    
    # 應用遮罩（可選）
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    
    # 計算注意力權重
    attn_weights = softmax(scores)
    
    # 計算輸出
    output = np.matmul(attn_weights, V)
    
    return output, attn_weights
```

### Multi-Head Attention

```python
class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 初始化 Q, K, V 的投影矩陣
        self.W_Q = np.random.randn(d_model, d_model) * 0.1
        self.W_K = np.random.randn(d_model, d_model) * 0.1
        self.W_V = np.random.randn(d_model, d_model) * 0.1
        self.W_O = np.random.randn(d_model, d_model) * 0.1

    def split_heads(self, x, batch_size):
        # x: (batch, seq_len, d_model)
        x = x.reshape(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(0, 2, 1, 3)  # (batch, heads, seq_len, d_k)

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.shape[0]
        
        # 線性投影
        Q = np.dot(Q, self.W_Q)
        K = np.dot(K, self.W_K)
        V = np.dot(V, self.W_V)
        
        # 分成多個頭
        Q = self.split_heads(Q, batch_size)
        K = self.split_heads(K, batch_size)
        V = self.split_heads(V, batch_size)
        
        # 計算注意力
        attn_output, _ = attention(Q, K, V, mask)
        
        # 合併多個頭
        attn_output = attn_output.transpose(0, 2, 1, 3).reshape(batch_size, -1, self.d_model)
        
        # 輸出投影
        output = np.dot(attn_output, self.W_O)
        
        return output
```

---

## 四、前饋網路

```python
class FeedForward:
    def __init__(self, d_model, d_ff):
        self.d_model = d_model
        self.d_ff = d_ff
        self.W1 = np.random.randn(d_model, d_ff) * 0.1
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * 0.1
        self.b2 = np.zeros(d_model)

    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, x):
        x = np.dot(x, self.W1) + self.b1
        x = self.relu(x)
        x = np.dot(x, self.W2) + self.b2
        return x
```

---

## 五、Transformer 區塊

```python
class TransformerBlock:
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.dropout = dropout

    def forward(self, x, mask=None):
        # Self-attention
        attn_output = self.attention.forward(x, x, x, mask)
        x = self.norm1.forward(x + attn_output)
        
        # Feed forward
        ff_output = self.feed_forward.forward(x)
        x = self.norm2.forward(x + ff_output)
        
        return x

class LayerNorm:
    def __init__(self, d_model, eps=1e-6):
        self.d_model = d_model
        self.eps = eps
        self.gamma = np.ones(d_model)
        self.beta = np.zeros(d_model)

    def forward(self, x):
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return self.gamma * (x - mean) / (std + self.eps) + self.beta
```

---

## 六、完整 Transformer

```python
class SimpleTransformer:
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff):
        self.token_embedding = TokenEmbedding(vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model)
        self.layers = [
            TransformerBlock(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ]
        self.final_norm = LayerNorm(d_model)

    def forward(self, token_ids):
        # 詞嵌入
        x = self.token_embedding.forward(token_ids)
        
        # 位置編碼
        seq_len = token_ids.shape[1]
        pos_enc = self.positional_encoding.forward(seq_len)
        x = x + pos_enc
        
        # 通過所有 Transformer 區塊
        for layer in self.layers:
            x = layer.forward(x)
        
        # 最終 LayerNorm
        x = self.final_norm.forward(x)
        
        return x
```

---

## 七、演示

```python
def demo():
    print("=" * 50)
    print("簡單 Transformer 架構演示")
    print("=" * 50)

    # 參數設定
    vocab_size = 10000
    d_model = 128
    num_heads = 8
    num_layers = 4
    d_ff = 512
    seq_len = 10

    # 建立模型
    transformer = SimpleTransformer(vocab_size, d_model, num_heads, num_layers, d_ff)

    # 測試輸入
    token_ids = np.random.randint(0, vocab_size, size=(2, seq_len))
    print(f"\n輸入形狀: {token_ids.shape}")

    # 前向傳播
    output = transformer.forward(token_ids)
    print(f"輸出形狀: {output.shape}")

    # 展示詞嵌入
    print("\n詞嵌入範例:")
    token_emb = transformer.token_embedding
    for i in range(min(5, vocab_size)):
        vec = token_emb.embeddings[i][:5]
        print(f"  Token {i}: {vec}")

    print("\n" + "=" * 50)
    print("演示完成")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

---

## 結語

本文從零實作了一個簡化的 Transformer 架構，涵蓋了核心元件：詞嵌入、位置編碼、多頭注意力機制和前饋網路。理解這些基礎元件，有助於讀者更深入掌握現代 NLP 模型的原理。

---

*延伸閱讀：[Attention is All You Need 原始論文](https://www.google.com/search?q=Attention+is+All+You+Need+Transformer+paper)*