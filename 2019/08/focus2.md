# Seq2Seq 與注意力

## 突破編碼器瓶頸

2015 年，Bahdanau、Cho 和 Bengio 發表了論文《Neural Machine Translation by Jointly Learning to Align and Translate》，提出了用於機器翻譯的注意力機制。這是注意力在 NLP 領域的首次重大應用，解決了傳統 Seq2Seq 模型的嚴重瓶頸。

---

## 傳統 Seq2Seq 的問題

### 編碼器-解碼器架構

2014 年的 Seq2Seq 模型將輸入序列編碼為一個固定維度的向量：

```
┌─────────────────────────────────────────────────────┐
│         傳統 Seq2Seq 模型                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│   "The cat sat on the mat"                         │
│   │   │   │   │   │   │                            │
│   ▼   ▼   ▼   ▼   ▼   ▼                            │
│   Encoder (BiRNN/LSTM)                            │
│   │                                           │
│   ▼                                           │
│ ┌──────────────────────┐                        │
│ │   固定維度向量 c       │ ← 所有資訊的壓縮     │
│ │   (bottleneck)       │                        │
│ └──────────┬───────────┘                        │
│             │                                    │
│             ▼                                    │
│   Decoder (RNN)                                  │
│             │                                    │
│             ▼                                    │
│   "Le chat s'est assis sur le tapis"             │
│                                                     │
│ 問題：輸入越長，壓縮流失越嚴重                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 實驗數據：翻譯品質 vs 句子長度

| 句子長度 | BLEU 分數（無注意力）| BLEU 分數（有注意力）|
|----------|---------------------|---------------------|
| 0-10 詞 | 30.2 | 31.5 |
| 11-20 詞 | 26.8 | 29.8 |
| 21-30 詞 | 22.5 | 29.1 |
| 31-40 詞 | 18.3 | 27.9 |
| 41+ 詞 | 15.1 | 26.8 |

注意力機制在長句子上效果顯著。

---

## Bahdanau 注意力

### 核心思想

Bahdanau 注意力的創新在於：**讓解碼器的每個時間步都能「關注」輸入序列的不同部分**。

```
┌─────────────────────────────────────────────────────┐
│            Bahdanau 注意力                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   解碼器時間步 t:                                   │
│                                                     │
│   h_{t-1} (解碼器隱藏狀態)                         │
│        │                                            │
│        ▼                                            │
│   ┌─────────────────────┐                        │
│   │   注意力計算         │                        │
│   │   α_{t,s} = softmax │                        │
│   │   (e_{t,s})         │                        │
│   └──────────┬──────────┘                        │
│              │                                   │
│      ┌───────┴───────┐                          │
│      │               │                          │
│      ▼               ▼                          │
│   α_{t,1}         α_{t,n}                        │
│      │               │                          │
│      └───────┬───────┘                          │
│              │                                   │
│              ▼                                   │
│   c_t = Σ α_{t,s} * h_s  (上下文向量)            │
│              │                                   │
│              ▼                                   │
│   h_t = RNN(h_{t-1}, y_{t-1}, c_t)              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 數學公式

**1. 注意力分數**

```python
# 計算每個輸入位置的注意力分數
# e_{t,s} = v^T * tanh(W * h_{t-1} + U * h_s)

class BahdanauAttention(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.W = nn.Linear(hidden_dim, hidden_dim)
        self.U = nn.Linear(hidden_dim, hidden_dim)
        self.v = nn.Linear(hidden_dim, 1)

    def forward(self, query, keys):
        # query: [batch, hidden_dim] - 解碼器隱藏狀態
        # keys: [batch, seq_len, hidden_dim] - 編碼器隱藏狀態

        scores = self.v(torch.tanh(
            self.W(query.unsqueeze(1)) + self.U(keys)
        ))  # [batch, seq_len, 1]

        weights = F.softmax(scores, dim=1)  # [batch, seq_len, 1]
        context = torch.sum(weights * keys, dim=1)  # [batch, hidden_dim]

        return context, weights
```

**2. 解碼器更新**

```python
# 使用上下文向量更新解碼器
# h_t = tanh(W_h * [h_{t-1}; c_t] + b_h)

# 輸出
# y_t = softmax(V * h_t)
```

---

## 注意力視覺化

### 機器翻譯的注意力圖

注意力機制的一個重要優勢是**可解釋性**：

```
英文 → 法文翻譯的注意力權重：

英文:  The    cat    sat    on    the    mat
       ─────────────────────────────────────
法文 "Le"    ███░░░░░░░░░░░░░░░░░░░
法文 "chat"  ░░░░████████████░░░░░░
法文 "s'est"░░░░░░░░░░░████████████
法文 "assis"░░░░░░░░░░░░░░░░████░░░
法文 "sur"   ░░░░░░░░░░░░░░░░░░░██
法文 "le"    ░░░░░░░░░░░░░░░░░░░██
法文 "tapis" ░░░░░░░░░░░░░░░░░░░██

每個法語單詞主要「關注」對應的英語單詞
```

---

## 對比：全局注意力 vs 局部注意力

### 全局注意力

每次考慮所有輸入位置：

```python
# 全局注意力的計算代價
# O(seq_len * hidden_dim) per step
# 序列越長，計算量越大
```

### 局部注意力

只考慮輸入的一個窗口：

```python
# 局部注意力的設計
# p_t = seq_len * sigmoid(W * h_{t-1})
# 只在 [p_t - D, p_t + D] 範圍內計算
```

---

## 實作：帶注意力的機器翻譯

### 模型架構

```python
class AttentionSeq2Seq(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, embed_dim, hidden_dim):
        self.encoder = Encoder(src_vocab, embed_dim, hidden_dim)
        self.decoder = Decoder(tgt_vocab, embed_dim, hidden_dim)
        self.attention = BahdanauAttention(hidden_dim)

    def forward(self, src, tgt):
        # 編碼
        encoder_outputs, hidden = self.encoder(src)

        # 解碼
        outputs = []
        decoder_input = tgt[:, 0]  # <START>
        decoder_hidden = hidden

        for t in range(1, tgt.size(1)):
            context, _ = self.attention(decoder_hidden, encoder_outputs)
            output, decoder_hidden = self.decoder(
                decoder_input, decoder_hidden, context
            )
            outputs.append(output)
            decoder_input = tgt[:, t]

        return torch.stack(outputs)
```

### 訓練技巧

1. **教師強迫（Teacher Forcing）**：加速收斂
2. **梯度裁剪**：防止梯度爆炸
3. **注意力權重的 L2 正則化**：鼓勵清晰的對齊

---

## 注意力機制的影響

### 解決了什麼問題

1. **長序列翻譯**：BLEU 分數提升 5-10 分
2. **對齊學習**：自動學習單詞對應關係
3. **可解釋性**：可以視覺化翻譯過程

### 開啟的新方向

1. **更通用的注意力定義**：從翻譯推廣到其他任務
2. **自注意力的誕生**：序列內部的 attention
3. **Transformer 的誕生**：純注意力架構

---

## 總結

Bahdanau 注意力的貢獻：

1. **實用性**：首次在大規模機器翻譯任務上展示效果
2. **通用性**：注意力機制成為 NLP 的標準元件
3. **理論創新**：為 Transformer 的誕生奠定基礎

下一章我們將看到自注意力如何進一步簡化並強化這個概念。

---

## 延伸閱讀

- [Bahdanau Attention Paper](https://www.google.com/search?q=Bahdanau+neural+machine+translation+attention+2015)
- [Neural Machine Translation by Jointly Learning to Align and Translate](https://www.google.com/search?q=Neural+Machine+Translation+by+Jointly+Learning+to+Align+and+Translate)
- [Sequence to sequence attention](https://www.google.com/search?q=sequence+to+sequence+attention+mechanism)

---

*本篇文章為「AI 程式人雜誌 2019 年 8 月號」注意力機制系列之二。*