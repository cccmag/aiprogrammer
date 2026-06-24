# 3. 從 RNN 到 Transformer

## RNN 的基本原理

循環神經網路（RNN）透過 hidden state 在序列中傳遞資訊：
- 每個時間步處理一個輸入
- Hidden state 取決於前一時間步的 hidden state 與當前輸入
- 理論上可以處理任意長度的序列

## LSTM 與 GRU

標準 RNN 存在梯度消失問題，難以學習長距離依賴。LSTM（Long Short-Term Memory）透過門控機制解決這個問題：
- **遺忘門**：決定遺忘多少過去資訊
- **輸入門**：決定加入多少新資訊
- **輸出門**：決定輸出多少資訊

GRU（Gated Recurrent Unit）是簡化版本，使用更少的門：
- **更新門**：結合遺忘門與輸入門
- **重置門**：決定忽略多少過去資訊

## RNN 的局限性

即使有 LSTM、GRU，RNN 仍有根本限制：
- **順序計算**：無法平行化處理序列
- **長距離依賴**：即使有門控，距離越遠梯度仍然衰減
- **梯度爆炸/消失**：深層網路訓練困難

## CNN for Sequence

捲積神經網路也被嘗試用於序列處理：
- 可以捕捉局部特徵
- 透過多層捲積擴大感受野
- 計算可以平行化

但 CNN 的感受野受限，難以捕捉長距離依賴。

## Transformer 的突破

2017 年 Transformer 完全基於注意力機制，徹底解決了 RNN 的問題：
- **完全平行化**：所有位置同時計算
- **直接長距離聯繫**：注意力讓任意位置直接互動
- **可擴展性**：易於擴展到更大模型

Transformer 的核心組件：
- Self-Attention
- Multi-Head Attention
- Position-wise Feed-Forward
- Positional Encoding

## 參考資源

- https://www.google.com/search?q=RNN+LSTM+GRU+循環神經網路+原理+比較+局限性
- https://www.google.com/search?q=CNN+序列處理+TextCNN+卷積神經網路+文本
- https://www.google.com/search?q=Transformer+RNN+区别+優勢+為何取代+RNN+2018