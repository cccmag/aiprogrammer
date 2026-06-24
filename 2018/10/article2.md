# LSTM 與序列模型

## 序列資料處理的挑戰

自然語言、語音、時間序列等資料都有順序依賴性。前一個輸入會影響後續的輸出，傳統的全連接網路難以有效處理這類結構。

循環神經網路（RNN）透過引入hidden state 在序列間傳遞資訊，理論上可以處理任意長度的序列。但標準 RNN 存在梯度消失與梯度爆炸問題，難以學習長距離依賴。

## LSTM 結構

長短期記憶網路（Long Short-Term Memory, LSTM）由 Hochreiter 和 Schmidhuber 在 1997 年提出，透過門控機制解決長期依賴問題。

LSTM 的核心組件：
1. **遺忘門（Forget Gate）**：決定哪些資訊應該被丟棄
2. **輸入門（Input Gate）**：決定哪些新資訊應該被儲存
3. **輸出門（Output Gate）**：決定輸出什麼資訊

### 遺忘門
```
f = σ(W_f · [h_{t-1}, x_t] + b_f)
```
遺忘門輸出 0~1 之間的值，0 表示完全遺忘，1 表示完全保留。

### 輸入門
```
i = σ(W_i · [h_{t-1}, x_t] + b_i)
C~ = tanh(W_C · [h_{t-1}, x_t] + b_C)
C_t = f * C_{t-1} + i * C~
```
新的候選記憶單元與遺忘門結合更新細胞狀態。

### 輸出門
```
o = σ(W_o · [h_{t-1}, x_t] + b_o)
h_t = o * tanh(C_t)
```
輸出門決定從細胞狀態中提取什麼資訊作為 hidden state。

## 雙向 LSTM

雙向 LSTM（BiLSTM）結合前向與後向兩個 LSTM：
- 前向 LSTM 從左到右處理序列
- 後向 LSTM 從右到左處理序列
- 兩個方向的 hidden state 拼接作為輸出

雙向 LSTM 能夠同時利用左右上下文，適合需要完整序列資訊的任務。

## LSTM 的應用

LSTM 廣泛應用於：
- 機器翻譯
- 語音識別
- 文本生成
- 時間序列預測

## LSTM 與 BERT 的關係

LSTM 是 BERT 出現前 NLP 領域的主流模型。ELMo 使用雙向 LSTM 學習上下文詞向量，奠定了預訓練的基礎。然而 LSTM 的表達能力有限，難以建模很長的依賴關係。BERT 採用 Transformer 架構，有效解決了這個問題。

## 參考資源

- https://www.google.com/search?q=LSTM+長短期記憶+原理+門控+機制+詳解
- https://www.google.com/search?q=LSTM+bidirectional+sequence+model+NLP+application+2018
- https://www.google.com/search?q=LSTM+vs+RNN+gradient+vanishing+long+dependency+解決方案