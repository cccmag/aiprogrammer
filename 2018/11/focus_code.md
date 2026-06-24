# 程式碼說明 — NLP 概念示範

## 功能概述

`_code/nlp_demo.py` 展示 NLP 現代化的關鍵概念，包括詞嵌入、注意力計算、序列編碼等基本操作。這些概念是理解 BERT 與預訓練模型的基礎。

## demo() 函數說明

### 1. 簡化詞嵌入
展示如何將詞彙轉換為向量表示，並計算詞之間的相似度。

### 2. Self-Attention 計算
演示 Transformer 中注意力機制的計算過程：
- Q、K、V 的生成
- 注意力分數的計算
- Softmax 正規化
- 加權求和

### 3. 位置編碼
展示 Transformer 如何加入序列位置資訊。

### 4. 序列編碼
展示完整的前向傳播過程，從詞嵌入到 Transformer 層輸出。

## 執行方式

```bash
cd _code
python3 nlp_demo.py
```

## 輸出範例

```
====================================================
NLP 概念示範
====================================================

[1] 詞嵌入與相似度
詞向量維度: 64
詞彙表大小: 10
「機器學習」與「深度學習」相似度: 0.87
「機器學習」與「蘋果」相似度: 0.12

[2] Self-Attention
查詢向量維度: (1, 3, 64)
鍵向量維度: (1, 3, 64)
注意力權重形狀: (1, 3, 3)

[3] 位置編碼
位置編碼形狀: (10, 64)
位置編碼範圍: [-0.1, 0.1]

[4] 序列編碼
最終輸出維度: (1, 3, 64)

====================================================
示範完成
====================================================
```

## 參考資源

- https://www.google.com/search?q=NLP+概念+示範+詞嵌入+注意力機制+代碼+Python
- https://www.google.com/search?q=word+embedding+similarity+calculation+Python+NumPy+example
- https://www.google.com/search?q=transformer+positional+encoding+self-attention+demo+Python+2018