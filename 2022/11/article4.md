# 序列到序列對話生成

## 從機器翻譯到對話生成

序列到序列（Seq2Seq）學習最初在機器翻譯領域取得了巨大成功。2015 年，Google 研究人員首次將 Seq2Seq 應用於對話生成，發表了《A Neural Conversational Model》——即著名的「Google 聊天機器人」論文。

## Seq2Seq 架構

### 編碼器

編碼器是一個 RNN（通常使用 LSTM 或 GRU），逐步讀取輸入序列的每個詞，產生隱藏狀態序列：

```
h_t = RNN_encoder(x_t, h_{t-1})
```

最終的隱藏狀態 h_n（或所有隱藏狀態的加權和）作為輸入的「摘要」傳遞給解碼器。

### 解碼器

解碼器也是一個 RNN，根據編碼器的輸出和已生成的詞逐步產生輸出序列：

```
s_t = RNN_decoder(y_{t-1}, s_{t-1}, c)
P(y_t | y_{<t}, x) = softmax(W * s_t + b)
```

其中 c 是來自編碼器的上下文向量。

## Attention 機制

Bahdanau Attention 的引入解決了 Seq2Seq 的資訊瓶頸問題。解碼器在生成每個詞時，會動態地關注輸入序列的不同部分：

```
e_{tj} = score(s_{t-1}, h_j)
a_{tj} = softmax(e_{tj})
c_t = Σ a_{tj} * h_j
```

## 損失函數與訓練

Seq2Seq 模型使用交叉熵損失（Cross-Entropy Loss）：

```
L = -Σ log P(y_t | y_{<t}, x)
```

訓練時使用 Teacher Forcing，即解碼器在每一步都使用真實的上一個詞作為輸入。

## 對話特有的挑戰

### 安全回應問題

Seq2Seq 對話模型傾向於生成「I don't know」、「OK」等安全但無資訊量的回應。這是因為這些回應在訓練資料中出現頻率極高。

### 多樣性缺乏

Beam Search 解碼雖然能產生更高質量的輸出，但會進一步降低多樣性。解決方案包括使用隨機解碼、Top-k 採樣、Top-p（Nucleus）採樣等。

### 長序列處理

對話通常是多輪的，長序列的建模對 RNN 來說具有挑戰性。Transformer 的出現大大緩解了這個問題。

## 延伸閱讀

- [A Neural Conversational Model](https://www.google.com/search?q=Vinyals+Le+neural+conversational+model)
- [Seq2Seq 學習論文](https://www.google.com/search?q=Sutskever+sequence+to+sequence+learning)
- [注意力機制詳解](https://www.google.com/search?q=Bahdanau+attention+mechanism)
