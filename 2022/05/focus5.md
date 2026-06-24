# Seq2Seq 與注意力機制

## 序列到序列模型

Seq2Seq（Sequence-to-Sequence）由 Sutskever 在 2014 年提出，使用編碼器-解碼器架構處理「序列到序列」的任務：

```
編碼器：將輸入序列編碼為固定長度的上下文向量 c
解碼器：基於上下文向量 c 產生輸出序列
```

**編碼器 RNN**：讀取整個輸入序列，最後的隱藏狀態作為序列的摘要：

```python
def encoder(input_sequence):
    h = zeros
    for x in input_sequence:
        h = rnn_step(x, h)
    return h  # 上下文向量 c
```

**解碼器 RNN**：基於上下文向量 c，逐步生成輸出序列：

```python
def decoder(context, max_len=50):
    h = context
    y_start = <SOS>
    for t in range(max_len):
        p = rnn_step(y_{t-1}, h)
        y_t = argmax(p)
        yield y_t
```

## 注意力機制的誕生

Seq2Seq 的資訊瓶頸在於：編碼器必須將整個輸入序列壓縮為一個固定長度的向量。當輸入序列很長時，這個向量無法保留所有資訊。

Bahdanau 在 2015 年提出的**注意力機制**解決了這個問題：解碼器在每一步可以「關注」輸入序列的不同位置：

```python
def attention_step(query, encoder_outputs):
    # 計算 query 與每個編碼器輸出的相似度
    scores = [score_func(query, h_j) for h_j in encoder_outputs]
    # softmax 標準化為權重
    weights = softmax(scores)
    # 加權總和作為上下文向量
    context = sum(weights[j] * h_j for j in range(len(encoder_outputs)))
    return context
```

## 三種注意力機制

**Bahdanau Attention**（加法注意力）：

```
score(h_t, h_s) = v^T * tanh(W_1 @ h_t + W_2 @ h_s)
```

**Luong Attention**（乘法注意力）：

```
score(h_t, h_s) = h_t^T @ W @ h_s          # 一般
score(h_t, h_s) = h_t^T @ h_s              # 點積
score(h_t, h_s) = h_t^T @ W_a @ h_s        # 拼接
```

**Self-Attention**（自注意力）：查詢和鍵來自同一個序列，是 Transformer 的核心。

## 注意力機制的關鍵優勢

1. **資訊瓶頸消除**：不再需要將全部資訊壓縮到一個向量
2. **可解釋性**：注意力權重直觀地顯示了模型的「注意力分布」
3. **梯度傳播**：注意力提供了短路徑，緩解了梯度消失
4. **翻譯對齊**：在機器翻譯中，注意力權重通常對應詞的對齊關係

## 影響

注意力機制是 NLP 領域最重要的概念之一。它不僅大幅提升了 Seq2Seq 模型的性能，更催生了 Transformer 架構——完全基於注意力、拋棄循環結構的模型，後者成為了 GPT 和 BERT 等預訓練模型的基礎。

---

**下一步**：[ELMo、BERT 與雙向編碼](focus6.md)

## 延伸閱讀

- [Seq2Seq 論文](https://www.google.com/search?q=Sequence+to+Sequence+Learning+with+Neural+Networks)
- [Bahdanau Attention 論文](https://www.google.com/search?q=Neural+Machine+Translation+by+Jointly+Learning+to+Align+and+Translate)
- [Visualizing A Neural Machine Translation Model](https://www.google.com/search?q=visualizing+neural+machine+translation+attention)
