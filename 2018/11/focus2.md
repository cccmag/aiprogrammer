# 2. Word Embeddings 的進化

## 從 One-Hot 到 Dense Embeddings

傳統文本表示使用 One-Hot 編碼：每個詞是詞彙表大小的向量，只有該詞位置為 1。這種表示維度極高且稀疏，無法表達詞之間的語義關係。

詞嵌入（Word Embeddings）將詞映射到低維連續向量空間：
- **維度降低**：從數萬維降到數百維
- **稠密表示**：每個維度都是實數值
- **語義表達**：相似詞在空間中接近

## Word2Vec 的貢獻

2013 年 Google 發表 Word2Vec，包含兩種訓練演算法：
- **Skip-gram**：輸入中心詞預測上下文
- **CBOW**：輸入上下文預測中心詞

Word2Vec 的訓練結果展示了驚人的語義性質：
```
king - man + woman ≈ queen
Paris - France + Italy ≈ Rome
```

## GloVe 的全局視角

GloVe（Global Vectors）結合了全局矩陣分解與局部上下文方法的優點：
- 統計語料庫中詞共現機率
- 奇異值分解降維
- 在類比推理任務上表現優異

## 動態 vs 靜態表示

傳統詞嵌入是靜態的：每個詞只有一個向量，無法處理一詞多義。動態表示則根據上下文調整詞義：
- **ELMo**：雙向 LSTM 動態表示
- **BERT**：基於 Transformer 的動態表示

## 上下文詞表示的意義

「bank」在以下句子中有不同含義：
- "I deposited money at the **bank**"
- "The river **bank** was muddy"

靜態詞嵌入只有一個表示，動態表示則能區分這兩種語義。這是 NLP 現代化的關鍵進步。

## 參考資源

- https://www.google.com/search?q=word+embeddings+詞嵌入+進化+從one-hot到dense+2018
- https://www.google.com/search?q=Word2Vec+GloVe+詞向量+比較+原理+区别
- https://www.google.com/search?q=靜態詞嵌入+動態詞嵌入+上下文+一詞多義+BERT+区别