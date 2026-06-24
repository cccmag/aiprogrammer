# RNN 家族的演變

## 標準 RNN

循環神經網路是處理序列資料的經典架構：
```
h_t = f(W · x_t + U · h_{t-1} + b)
```

問題：梯度消失與梯度爆炸，難以學習長距離依賴。

## LSTM（Long Short-Term Memory）

Hochreiter 和 Schmidhuber 在 1997 年提出 LSTM，透過門控機制解決長期依賴問題。

### 三個門

**遺忘門（Forget Gate）**
```
f = σ(W_f · [h_{t-1}, x_t] + b_f)
```
決定從細胞狀態中遺忘多少資訊。

**輸入門（Input Gate）**
```
i = σ(W_i · [h_{t-1}, x_t] + b_i)
C~ = tanh(W_C · [h_{t-1}, x_t] + b_C)
```
決定加入多少新資訊。

**輸出門（Output Gate）**
```
o = σ(W_o · [h_{t-1}, x_t] + b_o)
h_t = o * tanh(C_t)
```
決定輸出什麼資訊。

## GRU（Gated Recurrent Unit）

Cho 等人在 2014 年提出 GRU，是 LSTM 的簡化版本：
- 合併遺忘門與輸入門為更新門
- 移除輸出門
- 參數更少，訓練更快

```
z = σ(W_z · [h_{t-1}, x_t])  # 更新門
r = σ(W_r · [h_{t-1}, x_t])  # 重置門
h~ = tanh(W · [r * h_{t-1}, x_t])
h = (1 - z) * h_{t-1} + z * h~
```

## 雙向 RNN

很多任務需要同時考慮過去與未來的上下文：
- 英語音轉文字（需要知道下一個詞才能確定發音）
- 語法分析（需要知道完整句子結構）

雙向 RNN 包含前向與後向兩個 hidden state，拼接作為輸出。

## 深層 RNN

多層 RNN 堆疊可以增加模型的表達能力：
- 每層處理不同層級的特徵
- 通常 2-4 層就足夠
- 配合殘差連接可以訓練更深

## RNN 的應用場景

- **機器翻譯**：Seq2Seq 模型的 Encoder
- **語音識別**：時序建模
- **文本生成**：逐詞生成
- **時間序列預測**：預測未來值

## 為何 Transformer 取代了 RNN？

Transformer 的 Self-Attention：
- 完全平行計算，訓練速度快
- 任意距離依賴直接建模
- 更容易擴展到大規模模型

在 2018 年，Transformer 已成為 NLP 的主流架構。

## 參考資源

- https://www.google.com/search?q=RNN+LSTM+GRU+循環神經網路+演變+原理+比較
- https://www.google.com/search?q=雙向RNN+深層RNN+多層+RNN+架構+說明
- https://www.google.com/search?q=LSTM+GRU+何時使用+優缺點+比較+RNN+選擇