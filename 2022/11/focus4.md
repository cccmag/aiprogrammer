# 生成式對話模型

## 從統計到神經網路

生成式對話模型直接產生回覆文本，而非從候選庫中選擇。這使得生成式系統能夠產生全新的、創造性的回覆，但同時也帶來了控制性較差的問題。

## Seq2Seq 架構

2014 年，Sutskever、Vinyals 和 Le 發表了 sequence-to-sequence（Seq2Seq）學習框架，最初用於機器翻譯。這個框架包含兩個主要組件：

1. **編碼器（Encoder）**：將輸入序列編碼為固定大小的上下文向量
2. **解碼器（Decoder）**：根據上下文向量逐步生成輸出序列

```
輸入： "你好嗎？"
編碼器 → 上下文向量 → 解碼器 → "我很好，謝謝！"
```

### Attention 機制

Bahdanau 等人於 2015 年提出的注意力機制解決了 Seq2Seq 的資訊瓶頸問題。Attention 讓解碼器在每一步都能動態關注輸入序列的不同部分：

```
解碼器在生成第 t 個詞時：
  1. 計算與編碼器所有隱藏狀態的相似度
  2. 加權求和得到上下文向量
  3. 結合當前隱藏狀態生成輸出
```

## Transformer 革命

2017 年，Vaswani 等人發表了 Transformer 架構，完全基於注意力機制，拋棄了遞迴網路。Transformer 的核心創新包括：

- **多頭注意力**：從不同維度關注輸入
- **位置編碼**：為序列提供位置資訊
- **層歸一化與殘差連接**：穩定訓練

## 預訓練語言模型

GPT（2018）和 BERT（2019）展示了預訓練+微調範式的巨大潛力。對話系統開始使用這些大規模預訓練模型作為基礎，在對話資料上進行微調。

## 對話生成的挑戰

生成式對話系統面臨的主要挑戰：

- **安全性**：模型可能產生有害或不當內容
- **事實性**：模型可能產生幻覺（hallucination）
- **一致性**：多輪對話中可能前後矛盾
- **多樣性**：傾向於生成安全但無聊的回覆

## 延伸閱讀

- [Seq2Seq 對話生成論文](https://www.google.com/search?q=Seq2Seq+neural+dialogue+generation)
- [Transformer 架構](https://www.google.com/search?q=Attention+is+all+you+need+transformer)
- [GPT 對話模型](https://www.google.com/search?q=GPT+dialogue+generation)
