# Attention 機制詳解

## 為何需要 Attention？

Seq2Seq 模型中， Encoder 必須將整個輸入序列的資訊壓縮成單一 context 向量。對於長序列，這種方法不可避免地丢失重要資訊。

Attention 的核心思想是：在解碼時，讓模型「注意」到輸入序列中與當前輸出最相關的部分，而不是僅依賴單一的 context 向量。

## Attention 的計算步驟

假設 Encoder 輸出 hs（hidden states sequence），解碼器在時間步 t 的 hidden state 為 h_t，Attention 計算：

### 1. 計算注意力分數
```
score(h_t, hs_i) = h_t · hs_i  (dot-product attention)
```
或使用其他評分函數如：
- concat attention：v · tanh(W · [h_t; hs_i])
- general attention：h_t · W · hs_i

### 2. 計算注意力權重
```
attention_weights = softmax(scores)
```
透過 Softmax 正規化，將分數轉換為機率分佈，所有權重之和為 1。

### 3. 加權求和
```
context = Σ(attention_weights_i * hs_i)
```
每個 hidden state 根據其權重貢獻到 context 向量。

### 4. 結合輸出
```
output = concat(h_t, context)
```
或直接用 context 作為下一層的輸入。

## Self-Attention

Self-Attention（自注意力）是 Attention 的特例，Query、Key、Value 都來自同一序列。這使得序列內部的每個位置都能「注意」到其他所有位置。

Transformer 完全基於 Self-Attention，沒有使用 RNN 或 CNN。Self-Attention 的優勢：
- 任意距離的依賴都可以直接建模
- 高度可並行的計算
- 更容易學習長距離關係

## Multi-Head Attention

多頭注意力將注意力計算拆分為多個獨立的「頭」：
1. 將 Q、K、V 投影到 h 個不同的表示空間
2. 每個頭獨立地計算注意力
3. 拼接所有頭的輸出並線性變換

多頭注意力讓模型能夠同時關注不同類型的關係：
- 頭 1：語法結構
- 頭 2：語義相關
- 頭 3：共參照關係

## Attention 的意義

Attention 機制的發明是深度學習的重要里程碑。它不僅提升了 Seq2Seq 模型的效能，更重要的是揭示了「動態選擇性」在神經網路中的重要性。

Transformer 完全採用 Attention 機制，摒棄了 RNN 的循環結構，成為現代 NLP 模型的基礎架構。

## 參考資源

- https://www.google.com/search?q=Attention+机制+原理+计算+步骤+Seq2Seq+详解
- https://www.google.com/search?q=self-attention+自注意力+Transformer+原理+详解
- https://www.google.com/search?q=multi-head+attention+多头+原理+Transformer+作用