# 3. 雙向預訓練原理

## 為何需要雙向性？

傳統的語言模型受限於「單向性」。從左到右的語言模型只能使用左側上下文預測當前詞；從右到左的語言模型則只能使用右側上下文。這種限制在某些任務中可以接受（如語音識別），但對於需要完整語境理解的 NLP 任務則遠遠不夠。

考慮句子「這個蘋果很好吃，我想買一些**果汁**」：要正確預測「果汁」，模型需要同時理解左側（蘋果、好吃）和右側（我想買）的語義。這只有雙向模型才能做到。

## BERT 的雙向實現

BERT 使用「遮蓋語言模型」（Masked Language Model, MLM）來實現雙向預訓練。具體做法：
1. 隨機遮蓋輸入中約 15% 的 token
2. 僅根據被遮蓋位置的上下文（左右兩側）預測原始詞
3. 模型必須同時利用雙向資訊才能準確預測

這種訓練方式與傳統語言模型截然不同：傳統語言模型是生成式的（預測下一個詞），而 BERT 是填空式的（預測被遮蓋的詞）。

## 雙向 Transformer Encoder

BERT 使用多層雙向 Transformer Encoder。每層的自注意力機制讓每個位置的表示都能參照所有其他位置。通過層層堆疊，模型逐漸構建出更抽象、更豐富的語言表示。

在第 N 層，每個 token 的表示包含了：
- 原始詞彙資訊
- 淺層語法特徵
- 深層語義關係
- 跨句依賴

## 與 ELMo 的區別

ELMo 雖然號稱「雙向」，但實際上是兩個分開的語言模型的拼接：從左到右的 LSTM 與從右到左的 LSTM 分別訓練，最後簡單拼接。這種方式是「淺層雙向」，無法真正交互左右上下文資訊。

BERT 是「深層雙向」，透過 MLM 目標函數，讓模型在每層都真正融合雙向資訊。這是 BERT 性能大幅領先 ELMo 的關鍵原因。

## 預訓練的數學形式

BERT 的預訓練目標是最小化遮蓋詞的負對數似然：

```
L_MLM = - E_{(w) ~ D} [log P(w | context)]
```

其中 `context` 包含被遮蓋詞的左右上下文。這種目標函數直接優化雙向語言理解能力。

## 參考資源

- https://www.google.com/search?q=BERT+bidirectional+pre-training+MLM+Masked+Language+Model+原理
- https://www.google.com/search?q=BERT+deep+bidirectional+vs+ELMo+shallow+bidirectional+区别
- https://www.google.com/search?q=masked+language+model+pretraining+objective+BERT+explained