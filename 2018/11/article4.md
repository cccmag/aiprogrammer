# Seq2Seq 與注意力

## Seq2Seq 架構

序列到序列（Sequence-to-Sequence）模型用於將一個序列轉換為另一個序列：
- **Encoder**：輸入序列 → 語境向量
- **Decoder**：語境向量 → 輸出序列

經典應用：
- 機器翻譯（英翻中）
- 文本摘要（長文 → 短文）
- 對話系統（問句 → 回覆）

## Encoder-Decoder 結構

### Encoder
通常使用 LSTM 或 GRU：
```
h_1, h_2, ..., h_n = Encoder(x_1, x_2, ..., x_n)
c = h_n  # 最終 hidden state 作為 context
```

### Decoder
```
s_t = Decoder(s_{t-1}, y_{t-1}, c)
P(y_t) = softmax(W · s_t)
```

## 固定 Context 的瓶頸

所有資訊必須壓縮到單一 context 向量：
- 短序列尚可，長序列必然丢失資訊
- 這是傳統 Seq2Seq 的主要限制

## Bahdanau Attention（加性注意力）

2015 年提出的注意力機制解決了這個問題：
```
e_{ti} = v · tanh(W · s_{t-1} + U · h_i)  # 能量分數
α_{ti} = softmax(e_{ti})  # 注意力權重
c_t = Σ α_{ti} · h_i  # context 向量
```

Decoder 每個時間步都會重新計算與所有 Encoder hidden states 的相關性。

## Luong Attention（乘法注意力）

2015 年提出的另一種注意力：
```
e_{ti} = s_t · h_i  # 簡化的能量分數
```
計算更高效，效果也很好。

## Attention 的優勢

1. **動態上下文**：每個輸出詞有不的 context
2. **長序列支援**：不再依賴單一固定向量
3. **可解釋性**：可視化注意力權重
4. **對齊能力**：隱式學習輸入輸出對齊

## Attention 視覺化

機器翻譯中，注意力權重可以顯示詞之間的對應關係：
- 「I love you」 → 「我愛你」
- 「I」-「我」、「love」-「愛」、「you」-「你」的注意力權重應該較高

## 實作範例

```python
# 簡化的注意力計算
def attention(query, keys, values):
    scores = torch.matmul(query, keys.transpose(-2, -1))
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, values)
```

## 參考資源

- https://www.google.com/search?q=Seq2Seq+Encoder+Decoder+注意力機制+原理+詳解
- https://www.google.com/search?q=Bahdanau+Luong+注意力+機器翻譯+原理+区别
- https://www.google.com/search?q=attention+mechanism+seq2seq+NLP+visualization+example