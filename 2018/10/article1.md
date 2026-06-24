# Word2Vec 與詞嵌入回顧

## 詞嵌入的基本概念

詞嵌入（Word Embedding）是將詞彙映射到連續向量空間的技術。在傳統的詞袋模型中，每個詞被表示為 one-hot 向量，維度等於詞彙表大小，導致維度極高且稀疏。詞嵌入則將每個詞表示為低維稠密向量（如 300 維），大幅降低維度並捕捉語義關係。

理想的詞嵌入空間中，語義相似的詞在向量空間中彼此接近。例如「king」和「queen」的距離比「king」和「apple」更近。更進一步，詞向量運算能夠捕捉語義關係：「king - man + woman ≈ queen」。

## Word2Vec 原理

2013 年 Google 發表 Word2Vec，包含兩種訓練架構：

### Skip-gram
輸入中心詞，預測上下文詞。適用於大型語料庫，對稀有詞效果較好。

訓練目標：最大化上下文詞出現的機率
```
Objective = Σ log P(context | center_word)
```

### CBOW（Continuous Bag of Words）
輸入上下文詞，預測中心詞。訓練速度較快，對常見詞效果較好。

## Word2Vec 的創新

Word2Vec 的成功在於：
1. **高效**：使用層次 Softmax 或負採樣，大幅加速訓練
2. **小規模**：僅需單機即可訓練數十億詞語料
3. **高品質**：學習到豐富的語義與語法關係

## 預訓練詞向量

訓練好的 Word2Vec 模型可以直接用於下游任務：
- 初始化 NLP 模型的詞嵌入層
- 作為特徵輸入分類器
- 計算詞語相似度

## 詞嵌入的局限

詞嵌入的主要問題是靜態表示（static representation）：
- 每個詞只有一個向量，無法處理一詞多義
- 無法根據上下文動態調整詞義

這個局限促使了動態語境表示（如 ELMo、BERT）的發展。

## 工具與資源

- **gensim**：Python 的 Word2Vec 實現
- **Google News Vectors**：預訓練詞向量，300 維、300 萬詞彙
- **GloVe**：另一種流行的詞嵌入方法

## 參考資源

- https://www.google.com/search?q=Word2Vec+词嵌入+原理+Skip-gram+CBOW+教程+2018
- https://www.google.com/search?q=Word2Vec+word+embedding+gensim+training+Python+example
- https://www.google.com/search?q=词向量+语义+相似度+king+queen+analogy+example