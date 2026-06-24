# Seq2Seq 與注意力起源

## 編碼器-解碼器架構的誕生

2014 年是神經機器翻譯（NMT）的轉捩點。在此之前，機器翻譯主要基於短語統計方法（PBMT），需要大量的人工特徵工程和語言學知識。

Sutskever 等人（2014）提出的 Seq2Seq 模型改變了這一切。他們使用兩個 LSTM 網路作為編碼器和解碼器，首次展示了端到端神經翻譯的可能性。

### 編碼器的工作

編碼器按順序讀取輸入序列的每個詞，並更新其隱藏狀態。讀取完所有詞後，最後的隱藏狀態成為「上下文向量」——它是整個輸入序列的壓縮表示。

```
編碼器讀取 "I love coding"：
h₁ = LSTM("I", h₀)
h₂ = LSTM("love", h₁)
h₃ = LSTM("coding", h₂)
c = h₃  ← 上下文向量
```

### 解碼器的工作

解碼器基於上下文向量生成輸出序列。在每個時間步，它根據當前隱藏狀態和上一個輸出詞來預測下一個詞。

## 注意力機制的誕生

### 固定上下文向量的侷限

Seq2Seq 的核心問題在於上下文向量的固定大小。無論輸入序列長度是多少，編碼器都必須將所有資訊壓縮成一個向量。

這導致了兩個問題：
1. **長序列遺忘**：編碼器難以在長序列中保留所有資訊
2. **資訊瓶頸**：解碼器無法獲取輸入序列中的局部細節

### Bahdanau 的關鍵突破

Bahdanau 等人（2014）提出了一個優雅的解決方案：不再依賴單一的上下文向量，而是在每個解碼步驟建立一個新的上下文向量。

這個上下文向量是編碼器所有隱藏狀態的加權和，權重由注意力機制計算：

```
c_t = Σ α_{t,s} h_s

其中 α_{t,s} 是解碼器在時間步 t 對編碼器位置 s 的注意力權重
```

這使得解碼器能夠「關注」輸入序列的不同部分，就像人類翻譯者在閱讀原文時會來回瀏覽一樣。

## 注意力機制的數學框架

從 Seq2Seq 的注意力機制中，我們可以提煉出一個通用的注意力框架：

```
1. 計算分數：   score(q, k_i) = f(q, k_i)
2. 計算權重：   α_i = softmax(score_i)
3. 計算輸出：   output = Σ α_i v_i
```

這個框架後來被廣泛應用於各種注意力變體中。

## 影響與意義

### 對 NLP 的影響

注意力機制的引入使 NMT 的 BLEU 分數在短時間內提升了 5-10 個百分點。更重要的是，它證明了「軟性對齊」（soft alignment）比「硬性對齊」更有效。

### 可解釋性的開端

注意力權重的可視化是 NLP 模型可解釋性的起點。研究人員第一次能夠直觀地看到模型內部的運作——雖然只是部分理解，但這為後續的 AI 可解釋性研究打開了大門。

### 為 Transformer 鋪路

Seq2Seq 的注意力機制雖然是基於 RNN 的，但它為 Transformer 的 Self-Attention 奠定了概念基礎。如果有幾個關鍵詞定義了 2015-2020 年的深度學習，其中一個一定是「注意力」。

## 結論

Seq2Seq 到注意力的演進是深度學習史上最優美的「技術進化」故事之一。它不是憑空出現的，而是直接回應了一個實際問題（長序列翻譯）。這個故事告訴我們：最好的研究往往是從解決具體問題開始的，而不是追求華麗的理論。

---

**延伸閱讀**
- [Sutskever 2014: Sequence to Sequence Learning with Neural Networks](https://www.google.com/search?q=Seq2Seq+Sutskever+2014)
- [Bahdanau 2014: Neural Machine Translation by Jointly Learning to Align](https://www.google.com/search?q=Bahdanau+attention+2014)
- [Cho 2014: Learning Phrase Representations using RNN Encoder-Decoder](https://www.google.com/search?q=Cho+Seq2Seq+2014)
