# 深度學習架構演進

## 早期架構：MLP 與 CNN

### 多層感知器（MLP）
最早的深度學習架構：
- 多層全連接網路
- 適用於表格資料
- 不適合序列與影像

### 卷積神經網路（CNN）
1989 年發明，2012 年 AlexNet 使其普及：
- 局部感受野與權值共用
- 擅長影像處理
- 層級化特徵學習

## 序列處理：RNN 家族

### 標準 RNN
處理序列資料的經典方法：
- Hidden state 在序列中傳遞
- 理論上可處理任意長度
- 實際受梯度消失限制

### LSTM（1997）
長短期記憶網路：
- 門控機制控制資訊流動
- 解決長期依賴問題
- 成為序列建模標準

### GRU（2014）
門控迴圈單元：
- LSTM 的簡化版本
- 訓練更快，效果相近
- 兩者都是 RNN 的重要變體

## 注意力機制的引入

### Seq2Seq + Attention（2015）
注意力應用於機器翻譯：
- 動態選擇 Encoder 輸出
- 解決長序列問題
- 大幅提升翻譯品質

### Self-Attention（2016）
注意力應用於同一序列：
- 每個位置關注所有其他位置
- 為 Transformer 奠定基礎

## Transformer 革命

### Attention is All You Need（2017）
完全基於注意力的架構：
- Self-Attention + Multi-Head
- 位置編碼
- Encoder-Decoder 結構

### Transformer 的優勢
- 完全平行計算
- 直接建模長距離依賴
- 易於擴展

## 2018 年架構發展

### BERT：雙向 Transformer Encoder
- 預訓練 + 微調範式
- 11 項任務刷新紀錄

### GPT：單向 Transformer Decoder
- 強大的生成能力

## 架構比較

| 架構 | 優點 | 缺點 | 適用場景 |
|------|------|------|----------|
| MLP | 簡單 | 難處理高維輸入 | 表格資料 |
| CNN | 局部特徵 | 固定感受野 | 影像 |
| RNN/LSTM | 序列建模 | 難並行 | 時序資料 |
| Transformer | 平行、長依賴 | O(n²) 記憶體 | NLP、生成 |

## 未來趨勢

- 更多混合架構
- 稀疏注意力
- 高效 Transformer 變體

## 參考資源

- https://www.google.com/search?q=深度學習架構+演進+MLP+CNN+RNN+Transformer+2018
- https://www.google.com/search?q=CNN+RNN+LSTM+Transformer+比較+優缺點+適用場景
- https://www.google.com/search?q=2018+深度學習架構+年度回顧+Transformer+NLP