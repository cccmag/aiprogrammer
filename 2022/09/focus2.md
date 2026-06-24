# Bahdanau Attention（加法注意力）

## Seq2Seq 的瓶頸問題

在注意力機制出現之前，序列到序列（Seq2Seq）學習使用一種簡單但有限制的架構：編碼器將整個輸入序列編碼成一個固定大小的上下文向量，解碼器基於這個向量生成輸出。

這種方法的問題在於：當輸入序列變長時，固定大小的上下文向量成為了一個嚴重的資訊瓶頸。想像一下，你必須將一篇 1000 字的文章壓縮成一個 512 維的向量，然後期望解碼器能夠從這個向量中準確地還原出翻譯結果——這在長句子上幾乎是不可能的任務。

### 瓶頸的量化影響

Cho 等人（2014）的研究發現，傳統的 Seq2Seq 模型在處理 20 個詞以上的句子時，BLEU 分數急劇下降。這是因為上下文向量無法容納足夠的資訊來指導解碼過程。

## Bahdanau 的解決方案

2014 年，Bahdanau、Cho 與 Bengio 發表了論文《Neural Machine Translation by Jointly Learning to Align and Translate》，提出了一個革命性的想法：**不要將所有資訊壓縮到一個向量中，而是在每個解碼步驟動態地選擇相關的輸入資訊**。

他們的關鍵洞見是：在每個解碼時間步，不是只依賴單一的上下文向量，而是計算一個「對齊分數」，決定輸入序列中各個位置對當前輸出詞的重要性。

## 對齊分數的計算

### 加法注意力的數學公式

Bahdanau Attention 的計算過程可以分解為三個步驟：

**步驟 1：計算對齊分數**
```
score(h_t, h_s) = v^T tanh(W_q h_t + W_k h_s)
```

其中：
- h_t 是解碼器在時間步 t 的隱藏狀態（查詢）
- h_s 是編碼器在位置 s 的隱藏狀態（鍵）
- W_q 和 W_k 是權重矩陣
- v 是權重向量

由於這個公式使用了加法和 tanh 激活函數，它被稱為「加法注意力」（Additive Attention）。

**步驟 2：計算注意力權重**
```
α_{t,s} = softmax(score(h_t, h_s))
```

通過 softmax 函數將所有位置的對齊分數歸一化為機率分佈。

**步驟 3：計算上下文向量**
```
c_t = Σ_s α_{t,s} h_s
```

將所有編碼器隱藏狀態按照注意力權重加權求和，得到當前時間步的上下文向量。

### 可視化 Bahdanau 的計算

```
        解碼器隱藏狀態 h_t
              │
              ▼
         W_q @ h_t
              │
              ├───► tanh ──► v^T ──► softmax ──► α
              │                                    │
         W_k @ H[s] ◄─────── 編碼器隱藏狀態 H     │
              │                                    │
              └────────────────────────────────────┘
                                                   │
                                                   ▼
                                            c_t = Σ α_s H[s]
```

## Bahdanau 的實現細節

在原始論文中，Bahdanau 使用了雙向 RNN 作為編碼器，這樣每個輸入位置的隱藏狀態同時包含了前文和後文的資訊。解碼器使用了一個基於前一步注意力狀態的 GRU 單元。

### 與傳統 Seq2Seq 的比較

| 特性 | 傳統 Seq2Seq | Bahdanau Attention |
|------|-------------|-------------------|
| 上下文表示 | 固定大小向量 | 動態加權求和 |
| 長序列表現 | 快速下降 | 保持穩定 |
| 計算複雜度 | O(T) | O(T²) |
| 可解釋性 | 低 | 高（可視化對齊矩陣） |

### 對齊矩陣的可解釋性

Bahdanau 注意力的一個重要副產品是對齊矩陣（alignment matrix）。這個矩陣可視化了解碼器在每個步驟關注的輸入位置。例如，在英法翻譯中，對齊矩陣通常顯示出一種對角線模式——輸出詞與對應的輸入詞大致對齊。

## 歷史影響

Bahdanau Attention 的提出是 NLP 領域的一個分水嶺。它不僅顯著改善了機器翻譯的品質（尤其是對長句子的處理），更重要的是引入了「注意力」這個概念，為後續的 Transformer 革命鋪平了道路。

雖然 Bahdanau Attention 的計算效率不如後來的 Luong Attention 和 Transformer 的縮放點積注意力，但它在歷史上的重要性不可忽視——它是第一個成功展示了「注意力」在深度學習中價值的模型。

---

**延伸閱讀**
- [Bahdanau 2014: Neural Machine Translation by Jointly Learning to Align and Translate](https://www.google.com/search?q=Bahdanau+attention+2014)
- [Cho 2014: Learning Phrase Representations using RNN Encoder-Decoder](https://www.google.com/search?q=Cho+Seq2Seq+2014)
- [對齊矩陣可視化](https://www.google.com/search?q=alignment+matrix+attention+visualization)
