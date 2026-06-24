# Attention Is All You Need

## Transformer 誕生

2017 年 6 月，Google Brain 發表了論文《Attention Is All You Need》，提出了 Transformer 架構。這篇論文徹底改變了深度學習的格局，被引用超過數萬次，開啟了 NLP 領域的新時代。

---

## 論文概述

### 核心主張

論文標題《Attention Is All You Need》揭示了其核心主張：**僅使用注意力機制就可以完成序列到序列的任務，不需要循環結構**。

### 作者陣容

Vaswani et al.，包括：
- Ashish Vaswani
- Noam Shazeer
- Niki Parmar
- Jakob Uszkoreit
- Llion Jones
- Aidan N. Gomez
- Lukasz Kaiser
- Illia Polosukhin

---

## Transformer 架構

### 整體結構

```
┌─────────────────────────────────────────────────────┐
│              Transformer 架構                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   輸入: "The cat sat"                              │
│         │                                           │
│         ▼                                           │
│   ┌─────────────────────────┐                      │
│   │  Input Embedding        │                      │
│   │  + Positional Encoding  │                      │
│   └───────────┬─────────────┘                      │
│               │                                    │
│   ┌───────────┴─────────────┐                      │
│   │  Encoder Stack (N=6)   │                      │
│   │                         │                      │
│   │  ┌─────────────────┐  │                      │
│   │  │ Multi-Head      │  │                      │
│   │  │ Self-Attention  │  │                      │
│   │  └────────┬────────┘  │                      │
│   │           │           │                      │
│   │  ┌────────┴────────┐  │                      │
│   │  │ Feed-Forward     │  │                      │
│   │  │ Network          │  │                      │
│   │  └─────────────────┘  │                      │
│   │                         │                      │
│   │  (重複 6 層)            │                      │
│   └───────────┬─────────────┘                      │
│               │                                    │
│               ▼                                    │
│   ┌─────────────────────────┐                      │
│   │  Decoder Stack (N=6)   │                      │
│   │                         │                      │
│   │  ┌─────────────────┐  │                      │
│   │  │ Masked Multi-Head│  │                      │
│   │  │ Self-Attention  │  │                      │
│   │  └────────┬────────┘  │                      │
│   │           │           │                      │
│   │  ┌────────┴────────┐  │                      │
│   │  │ Encoder-Decoder │  │                      │
│   │  │ Attention       │  │                      │
│   │  └────────┬────────┘  │                      │
│   │           │           │                      │
│   │  ┌────────┴────────┐  │                      │
│   │  │ Feed-Forward     │  │                      │
│   │  │ Network          │  │                      │
│   │  └─────────────────┘  │                      │
│   │                         │                      │
│   └───────────┬─────────────┘                      │
│               │                                    │
│               ▼                                    │
│   ┌─────────────────────────┐                      │
│   │  Linear + Softmax       │                      │
│   └───────────┬─────────────┘                      │
│               │                                    │
│               ▼                                    │
│   輸出: "Le chat s'est assis"                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 編碼器結構

### 編碼器層

每個編碼器層包含兩個子層：

```python
class EncoderLayer(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_dim):
        super().__init__()
        self.self_attention = MultiHeadAttention(embed_dim, num_heads)
        self.feed_forward = FeedForward(embed_dim, ff_dim)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        # 自注意力子層
        attn_output = self.self_attention(x)
        x = self.norm1(x + self.dropout(attn_output))

        # 前饋網路子層
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))

        return x
```

### 殘差連接和層歸一化

每個子層的輸出：
```
LayerNorm(x + Sublayer(x))
```

這種設計：
1. 緩解梯度傳播問題
2. 穩定訓練
3. 允許更深層的網路

---

## 解碼器結構

### 解碼器層

解碼器增加了一個第三子層：

```python
class DecoderLayer(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_dim):
        super().__init__()
        self.self_attention = MultiHeadAttention(embed_dim, num_heads)
        self.encoder_attention = MultiHeadAttention(embed_dim, num_heads)
        self.feed_forward = FeedForward(embed_dim, ff_dim)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.norm3 = nn.LayerNorm(embed_dim)

    def forward(self, x, encoder_output):
        # 遮罩自注意力（不能看到未來的 token）
        attn_output = self.self_attention(x)
        x = self.norm1(x + attn_output)

        # 編碼器-解碼器注意力
        attn_output = self.encoder_attention(x, encoder_output)
        x = self.norm2(x + attn_output)

        # 前饋網路
        ff_output = self.feed_forward(x)
        x = self.norm3(x + ff_output)

        return x
```

### 遮罩（Masking）

```python
def subsequent_mask(size):
    """防止看到未來位置的遮罩"""
    mask = torch.triu(torch.ones(size, size), diagonal=1).bool()
    return mask.unsqueeze(0)
```

---

## 前饋網路

### Position-wise 前饋網路

```python
class FeedForward(nn.Module):
    def __init__(self, embed_dim, ff_dim):
        super().__init__()
        self.linear1 = nn.Linear(embed_dim, ff_dim)
        self.linear2 = nn.Linear(ff_dim, embed_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.linear2(self.relu(self.linear1(x)))
```

---

## 關鍵設計决策

### 1. 縮放點積注意力

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)

    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)

    p_attn = F.softmax(scores, dim=-1)
    return torch.matmul(p_attn, V)
```

為什麼要縮放？防止點積過大導致 softmax 進入低梯度區域。

### 2. 多頭注意力

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        assert embed_dim % num_heads == 0

        self.d_k = embed_dim // num_heads
        self.num_heads = num_heads

        self.w_q = nn.Linear(embed_dim, embed_dim)
        self.w_k = nn.Linear(embed_dim, embed_dim)
        self.w_v = nn.Linear(embed_dim, embed_dim)
        self.w_o = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, mask=None):
        batch_size = x.size(0)

        Q = self.w_q(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.w_k(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.w_v(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        if mask is not None:
            mask = mask.unsqueeze(1)

        attn_output = scaled_dot_product_attention(Q, K, V, mask)

        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)

        return self.w_o(attn_output)
```

---

## Transformer 的優勢

### 1. 並行化

```
RNN：
- 必須順序計算
- O(n) 時間步
- 難以并行

Transformer：
- 所有位置可以并行計算 Q, K, V
- O(1) 步（注意力計算本身是 O(n²) 但可高度并行）
- 顯著加速訓練
```

### 2. 路徑長度

```
從位置 i 到位置 j 的路徑長度：
- RNN: O(n)
- Self-Attention: O(1)

這使得長距離依賴更容易學習。
```

### 3. 可解釋性

注意力權重可以直觀顯示翻譯對齊。

---

## 實驗結果

### 機器翻譯

| 模型 | WMT 英德 BLEU | 參數量 |
|------|---------------|--------|
| ByteNet | 23.75 | - |
| ConvS2S | 25.16 | - |
| MoE | 26.03 | - |
| Deep-Attention | 26.40 | - |
| Transformer (base) | 25.8 | 65M |
| Transformer (big) | 26.9 | 213M |

### 訓練成本

Transformer (big) 的訓練時間：
- 8 個 P100 GPU
- 3.5 天
- 顯著低於之前的模型

---

## 影響與意義

### 開啟的新時代

1. **NLP 的 Transformer 時代**：幾乎所有 SOTA 模型都基於 Transformer
2. **預訓練的普及**：BERT、GPT 等预训练模型
3. **跨模態應用**：Vision Transformer (ViT)

### 後續發展

- 2018: BERT, GPT
- 2019: GPT-2, RoBERTa, XLNet
- 2020: GPT-3, T5, CLIP
- 2021: ViT, DeiT
- 2022: ChatGPT, LLaMA
- 2023+: GPT-4, Claude, Gemini

---

## 總結

Transformer 的貢獻：

1. **純注意力架構**：首次完全拋棄 RNN
2. **高效并行**：極大加速訓練
3. **可擴展性**：容易擴展到更大模型
4. **通用性**：適用於多個領域

「Attention Is All You Need」不僅是論文標題，更是深度學習的重要里程碑。

---

## 延伸閱讀

- [Attention Is All You Need Paper](https://www.google.com/search?q=Attention+Is+All+You+Need+paper+2017)
- [Transformer architecture](https://www.google.com/search?q=Transformer+architecture+attention)
- [Google+BERT+2018](https://www.google.com/search?q=Google+BERT+2018+transformer)

---

*本篇文章為「AI 程式人雜誌 2019 年 8 月號」注意力機制系列之四。*