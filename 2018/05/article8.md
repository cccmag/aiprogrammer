# word2vec 與詞嵌入的應用

## 前言

詞嵌入（Word Embedding）是 NLP 的基礎技術。word2vec（2013）開創了這一領域。

## word2vec 原理

word2vec 使用淺層神經網路學習詞的向量表示。

### 兩種架構

- **Skip-gram**：用中心詞預測上下文
- **CBOW**：用上下文預測中心詞

## 詞嵌入的特性

```python
# 語意相似性
king - man + woman ≈ queen

# 類比關係
Paris : France : : Rome : Italy
```

## 應用場景

1. **文字分類**：輸入表示
2. **機器翻譯**：跨語言嵌入
3. **推薦系統**：物品表示
4. **問答系統**：語意匹配

## 其他詞嵌入技術

- GloVe（2014）
- FastText（2016）
- ELMo（2018）

## 結論

詞嵌入是現代 NLP 的基礎，GPT 等模型的湧現並未取代它們的重要性。

---

**延伸閱讀**

- [word2vec 原始論文](https://www.google.com/search?q=word2vec+Mikolov+2013)
- [詞嵌入教程](https://www.google.com/search?q=word+embedding+tutorial)