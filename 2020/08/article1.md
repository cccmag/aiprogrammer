# 用 Python 實作 Transformer

## 前言

本文將從零實作一個完整的 Transformer 架構，幫助讀者深入理解其工作原理。

---

## 一、總體架構

```
輸入序列
  -> 詞嵌入
  -> 位置編碼
  -> N × Encoder 區塊
      ├─ Multi-Head Self-Attention
      └─ Feed-Forward Network
  -> N × Decoder 區塊
      ├─ Masked Self-Attention
      ├─ Cross-Attention
      └─ Feed-Forward Network
  -> 線性層 + Softmax
  -> 輸出機率
```

---

## 二、位置編碼

```python
import math
import numpy as np

class PositionalEncoding:
    def __init__(self, d_model, max_len=5000):
        self.d_model = d_model
        pe = np.zeros((max_len, d_model))
        
        for pos in range(max_len):
            for i in range(0, d_model, 2):
                denominator = 10000 ** (i / d_model)
                pe[pos, i] = math.sin(pos / denominator)
                if i + 1 < d_model:
                    pe[pos, i + 1] = math.cos(pos / denominator)
        
        self.pe = pe
    
    def forward(self, seq_len):
        return self.pe[:seq_len]
```

---

## 三、縮放點積注意力

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    
    # 計算注意力分數
    scores = np.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    # 應用遮罩
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    
    # Softmax
    exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
    
    # 輸出
    output = np.matmul(attn_weights, V)
    
    return output, attn_weights
```

---

## 四、多頭注意力

```python
class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 權重矩陣
        self.W_Q = np.random.randn(d_model, d_model) * 0.1
        self.W_K = np.random.randn(d_model, d_model) * 0.1
        self.W_V = np.random.randn(d_model, d_model) * 0.1
        self.W_O = np.random.randn(d_model, d_model) * 0.1
    
    def split_heads(self, x, batch_size):
        x = x.reshape(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(0, 2, 1, 3)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.shape[0]
        
        # 線性投影
        Q = np.dot(Q, self.W_Q)
        K = np.dot(K, self.W_K)
        V = np.dot(V, self.W_V)
        
        # 分頭
        Q = self.split_heads(Q, batch_size)
        K = self.split_heads(K, batch_size)
        V = self.split_heads(V, batch_size)
        
        # 注意力
        attn_output, attn_weights = scaled_dot_product_attention(Q, K, V, mask)
        
        # 合併多頭
        attn_output = attn_output.transpose(0, 2, 1, 3).reshape(batch_size, -1, self.d_model)
        
        # 輸出投影
        output = np.dot(attn_output, self.W_O)
        
        return output, attn_weights
```

---

## 五、前饋網路

```python
class FeedForward:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.1
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * 0.1
        self.b2 = np.zeros(d_model)
    
    def forward(self, x):
        x = np.dot(x, self.W1) + self.b1
        x = np.maximum(0, x)  # ReLU
        x = np.dot(x, self.W2) + self.b2
        return x
```

---

## 六、Transformer 區塊

```python
class EncoderBlock:
    def __init__(self, d_model, num_heads, d_ff):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = FeedForward(d_model, d_ff)
        self.norm1 = d_model
        self.norm2 = d_model
    
    def forward(self, x, mask=None):
        # 自注意力
        attn_output, _ = self.attention.forward(x, x, x, mask)
        x = x + attn_output  # 殘差連接
        x = x / np.sqrt(2)  # LayerNorm 近似
        
        # 前饋
        ff_output = self.feed_forward.forward(x)
        x = x + ff_output
        x = x / np.sqrt(2)
        
        return x

class DecoderBlock:
    def __init__(self, d_model, num_heads, d_ff):
        self.masked_attention = MultiHeadAttention(d_model, num_heads)
        self.cross_attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = FeedForward(d_model, d_ff)
    
    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        # Masked 自注意力
        mask_attn_output, _ = self.masked_attention.forward(x, x, x, tgt_mask)
        x = x + mask_attn_output
        x = x / np.sqrt(2)
        
        # Cross 注意力
        cross_output, _ = self.cross_attention.forward(x, encoder_output, encoder_output, src_mask)
        x = x + cross_output
        x = x / np.sqrt(2)
        
        # 前饋
        ff_output = self.feed_forward.forward(x)
        x = x + ff_output
        x = x / np.sqrt(2)
        
        return x
```

---

## 七、完整 Transformer

```python
class Transformer:
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff):
        self.embeddings = np.random.randn(vocab_size, d_model) * 0.1
        self.pos_encoding = PositionalEncoding(d_model)
        self.encoder_blocks = [EncoderBlock(d_model, num_heads, d_ff) for _ in range(num_layers)]
        self.decoder_blocks = [DecoderBlock(d_model, num_heads, d_ff) for _ in range(num_layers)]
        self.final_fc = np.random.randn(d_model, vocab_size) * 0.1
    
    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        # 編碼器
        src_emb = self.embeddings[src]
        src_pos = self.pos_encoding.forward(src.shape[1])
        src_emb = src_emb + src_pos
        
        for block in self.encoder_blocks:
            src_emb = block.forward(src_emb, src_mask)
        
        # 解碼器
        tgt_emb = self.embeddings[tgt]
        tgt_pos = self.pos_encoding.forward(tgt.shape[1])
        tgt_emb = tgt_emb + tgt_pos
        
        for block in self.decoder_blocks:
            tgt_emb = block.forward(tgt_emb, src_emb, src_mask, tgt_mask)
        
        # 輸出
        output = np.dot(tgt_emb, self.final_fc)
        
        return output
```

---

## 八、演示

```python
def demo():
    print("=" * 50)
    print("Transformer Implementation Demo")
    print("=" * 50)
    
    vocab_size = 1000
    d_model = 128
    num_heads = 4
    num_layers = 2
    d_ff = 512
    seq_len = 10
    
    transformer = Transformer(vocab_size, d_model, num_heads, num_layers, d_ff)
    
    src = np.random.randint(0, vocab_size, size=(2, seq_len))
    tgt = np.random.randint(0, vocab_size, size=(2, seq_len))
    
    print(f"\nInput shape: src={src.shape}, tgt={tgt.shape}")
    
    output = transformer.forward(src, tgt)
    print(f"Output shape: {output.shape}")
    
    pos_enc = PositionalEncoding(d_model)
    print(f"Positional encoding shape: {pos_enc.pe.shape}")
    
    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

---

## 結語

本文從零實作了 Transformer 的核心元件，包括位置編碼、多頭注意力、前饋網路和完整的編碼器-解碼器架構。理解這些基礎元件對於深入掌握現代大型語言模型至關重要。

---

*延伸閱讀：[Transformer+implementation+tutorial+2020](https://www.google.com/search?q=Transformer+implementation+tutorial+Python+2020)*