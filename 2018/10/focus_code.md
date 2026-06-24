# 程式碼說明 — BERT 概念示範

## 功能概述

`_code/bert_demo.py` 是一個展示 BERT 核心概念的簡化類比腳本。程式中使用簡化的 Transformer Encoder 層與注意力機制，類比 BERT 的雙向預訓練過程中對輸入序列的處理。

## demo() 函數說明

### 1. 文本向量化
將輸入文字轉換為詞索引向量，每個詞對應一個唯一 ID。特殊 token 包括 [CLS]（分類）、[SEP]（句子分隔）、[MASK]（遮蓋）。

### 2. 位置編碼
使用正弦/餘弦函數生成位置編碼向量，每個位置有獨特的編碼。位置編碼與詞嵌入相加，給予模型序列順序資訊。

### 3. 簡化 Transformer 層
類比 BERT 的 Transformer Encoder 層：
- 多頭注意力：將輸入分割為多個頭，平行計算注意力
- 前饋網路：兩層全連接網路，中間使用 ReLU
- 残差連接與 Layer Normalization

### 4. MLM 損失計算
隨機遮蓋部分輸入 token，訓練模型預測被遮蓋的詞。計算交叉熵損失，展示 BERT 的預訓練目標。

## 執行方式

```bash
cd _code
python3 bert_demo.py
```

## 輸出範例

```
====================================================
BERT 概念示範
====================================================

[1] 輸入文本
原始文字: "[CLS] BERT 是強大的語言模型 [SEP]"
詞索引: [101, 2361, ...]
詞嵌入維度: 768

[2] 位置編碼
位置編碼形狀: (序列長度, 768)
位置編碼範圍: [-0.05, 0.05]

[3] Transformer 層輸出
輸出形狀: (序列長度, 768)
每層維度不變，透過殘差連接傳遞資訊

[4] MLM 預訓練
遮蓋位置: [3, 7]
預測機率分佈形狀: (batch, vocab_size)
損失值: 2.34

====================================================
示範完成
====================================================
```

## 參考資源

- https://www.google.com/search?q=BERT+implementation+Transformer+Encoder+简化+demo+Python+code
- https://www.google.com/search?q=Transformer+positional+encoding+sinusoidal+implementation+Python
- https://www.google.com/search?q=BERT+MLM+Masked+Language+Model+loss+calculation+Python+example