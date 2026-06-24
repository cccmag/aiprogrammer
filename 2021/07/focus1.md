# 主題一：Transformer 架構解析

## 從注意力機制到大型語言模型

### 1. Transformer 的誕生背景

在 Transformer 出現之前，序列處理任務主要依賴循環神經網路（RNN），包括 LSTM 和 GRU。然而，RNN 存在幾個根本性的限制：

**梯度消失與爆炸**：長序列訓練時，梯度難以有效傳遞
**順序計算瓶頸**：無法并行處理，訓練速度受限
**長距離依賴建模困難**：雖然 LSTM/GRU 有所改善，但效果仍不理想

2017 年，Google 在論文《Attention Is All You Need》中提出了 Transformer，完全拋棄了 RNN 結構，僅使用注意力機制，實現了革命性的突破。

### 2. 注意力機制的原理

注意力機制的核心思想是：**在處理序列中的每個位置時，模型應該能夠「關注」序列中的任何其他位置**。

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(query, key, value, mask=None):
    """縮放點積注意力"""
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1))
    scores = scores / math.sqrt(d_k)

    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)

    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, value), weights
```

**為什麼叫「縮放」點積注意力？**
- 點積後除以 √d_k 可以防止梯度消失/爆炸
- 當 d_k 較大時，點積結果往往較大，會使 softmax 進入低梯度區域

### 3. Multi-Head Attention

單一注意力頭只能捕捉一種類型的關係。Multi-Head Attention 將注意力分散到多個「頭」，每個頭學習不同的注意力模式：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_model = d_model
        self.depth = d_model // num_heads

        self.wq = nn.Linear(d_model, d_model)
        self.wk = nn.Linear(d_model, d_model)
        self.wv = nn.Linear(d_model, d_model)
        self.dense = nn.Linear(d_model, d_model)

    def split_heads(self, x, batch_size):
        x = x.reshape(batch_size, -1, self.num_heads, self.depth)
        return x.transpose(1, 2)

    def forward(self, query, key, value, mask):
        batch_size = query.size(0)

        q = self.split_heads(self.wq(query), batch_size)
        k = self.split_heads(self.wk(key), batch_size)
        v = self.split_heads(self.wv(value), batch_size)

        attn_output, _ = scaled_dot_product_attention(q, k, v, mask)

        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(batch_size, -1, self.d_model)

        return self.dense(attn_output)
```

**Multi-Head Attention 的優勢**：
- 每個頭可以專注於不同的語義關係（如句法、語義、指代）
- 增加模型的表達能力
- 維持總計算量不變（與單頭注意力相比）

### 4. 位置編碼

Transformer 本身沒有循環結構，也沒有位置資訊的概念。為了讓模型理解序列順序，需要額外加入位置編碼（Positional Encoding）：

```python
import numpy as np

def get_positional_encoding(max_len, d_model):
    """正弦和餘弦位置編碼"""
    pe = np.zeros((max_len, d_model))

    position = np.arange(0, max_len).reshape(-1, 1)
    div_term = np.exp(np.arange(0, d_model, 2) * -(math.log(10000.0) / d_model))

    pe[:, 0::2] = np.sin(position * div_term)
    pe[:, 1::2] = np.cos(position * div_term)

    return torch.FloatTensor(pe)
```

為什麼使用正弦/餘弦函數？因為對於任意固定的偏移 k，PE(pos+k) 可以表示為 PE(pos) 的線性組合。

### 5. Encoder 與 Decoder 架構

**Encoder**：
- 由 N 個相同的層堆疊而成
- 每層包含：Multi-Head Self-Attention + Feed-Forward Network
- 使用殘差連接和層標準化

**Decoder**：
- 同樣由 N 個相同的層堆疊而成
- 每層包含：
  - Masked Multi-Head Self-Attention（防止看到未來位置）
  - Encoder-Decoder Attention（關注 Encoder 輸出）
  - Feed-Forward Network

### 6. Transformer 的影響

Transformer 的出現徹底改變了深度學習的格局：

**NLP 領域**：BERT、GPT、T5 等模型相繼問世
**電腦視覺**：ViT、Swin Transformer 等展示了視覺 Transformer 的潛力
**多模態學習**：CLIP、DALL-E 等利用 Transformer 統一不同模態
**語音處理**：Conformer、Wav2vec 等語音模型也採用 Transformer

### 7. 結語

Transformer 的成功源於其優雅的設計和強大的表現力。注意力機制讓模型能夠靈活地捕捉任意距離的依賴關係，而并行計算的能力使得訓練大規模模型成為可能。

然而，Transformer 也有其局限性：
- 計算複雜度 O(n²)，難以處理很長的序列
- 位置編碼是人工設計的，可能不是最優
- 對資源的需求巨大，限制了應用場景

這些問題催生了後續的研究，如 Linformer、Performer、Reformer 等高效 Transformer 變體。

---

## 延伸閱讀

- [《Attention Is All You Need》論文](https://www.google.com/search?q=Attention+Is+All+You+Need+Transformer+paper)
- [BERT 論文](https://www.google.com/search?q=BERT+pre-training+deep+bidirectional)
- [PyTorch Transformer 文档](https://www.google.com/search?q=PyTorch+nn+Transformer+tutorial)