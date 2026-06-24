# ELMo 與預訓練語言模型

## 語言模型的定義

語言模型（Language Model）的目標是學習詞序列的機率分佈：
```
P(w_1, w_2, ..., w_n) = Π P(w_i | w_1, ..., w_{i-1})
```
簡單來說，就是預測下一個詞的機率。 хороший

語言模型可以無監督地從大量文本中學習，無需人工標注。這種特性使語言模型成為預訓練的理想任務。

## ELMo 概述

ELMo（Embeddings from Language Models）由 Peters 等人在 2018 年 2 月發表，是首個成功的預訓練語言模型方法。ELMo 的核心創新：

1. **雙向 LSTM**：使用雙向語言模型，同時考慮左右上下文
2. **層級表示**：不同層捕捉不同類型的資訊（淺層語法、深層語義）
3. **任務無關**：學習到的表示可用於各種下游任務

## 雙向語言模型

ELMo 的雙向語言模型包含兩個方向：
- **前向 LM**：從左到右預測下一個詞
- **後向 LM**：從右到左預測下一個詞

總損失是兩個方向的負對數似然之和：
```
L = Σ [log P(w_i | w_1, ..., w_{i-1}) + log P(w_i | w_{i+1}, ..., w_n)]
```

## ELMo 的使用方法

ELMo 輸出每層的 hidden states，可依任務選擇不同層：

```python
# 使用頂層輸出
elmo_output = elmo(input_tokens, output_layer=3)

# 或加權組合所有層
elmo_output = sum(alpha_i * layer_i for i in range(1, N+1))
```

不同任務可能偏好不同層級的表示：
- 語法任務（詞性標注）偏好淺層
- 語義任務（語義角色標注）偏好深層

## ELMo 的貢獻

ELMo 驗證了預訓練語言模型的有效性：
- 只需少量標注資料即可在下游任務取得好效果
- 動態的上下文表示可以處理一詞多義
- 雙向預訓練能夠充分利用文本資訊

## ELMo 的局限

ELMo 仍有不足：
- 使用 LSTM 而非 Transformer，難以捕捉更長的依賴
- 雙向表示是淺層組合，非真正的深度雙向
- LSTM 的序列性質限制了平行計算

這些局限推動了 BERT 的誕生。

## 參考資源

- https://www.google.com/search?q=ELMo+預訓練+語言模型+雙向+LSTM+原理+詳解
- https://www.google.com/search?q=ELMo+word+embedding+contextual+representation+paper+Peters+2018
- https://www.google.com/search?q=ELMo+vs+BERT+区别+預訓練+語言模型+比較