# 詞嵌入的藝術：從 Word2Vec 到 BERT

## 前言

詞嵌入技術經歷了從靜態到動態、從局部到上下文的演進。本篇文章回顧這段發展歷程。

## 詞嵌入的演進

| 年份 | 模型 | 特點 |
|-----|------|------|
| 2003 | NNLM | 首個神經網路語言模型 |
| 2013 | Word2Vec | 簡化訓練，高質量向量 |
| 2014 | GloVe | 全域統計 + 局部上下文 |
| 2016 | fastText | 子詞嵌入，處理 OOV |
| 2018 | ELMo | 雙向 LSTM，上下文化 |
| 2018 | BERT | Transformer，上下文化 |

## Word2Vec 的局限性

```python
# 靜態向量：一個詞只有一個表示
word2vec["bank"] = [0.2, -0.5, 0.8, ...]
# 無法區分：
# - "I deposited money at the bank"
# - "The river bank was muddy"
```

## 上下文表示的解決方案

### ELMo：雙向 LSTM

```python
# ELMo 使用雙向語言模型產生上下文相關表示
elmo_embed = elmo(text)  # 每個詞有兩個方向的表示
```

### BERT：Transformer

```python
# BERT 使用注意力機制捕獲雙向上下文
bert_embed = bert(text)  # 動態、上下文相關
```

## 比較實驗

```python
# 測量詞嵌入的語意捕捉能力
def evaluate_word_similarity(model, word_pairs):
    scores = []
    for w1, w2, similarity in word_pairs:
        vec1 = model[w1]
        vec2 = model[w2]
        score = cosine_similarity(vec1, vec2)
        scores.append((score, similarity))
    return pearson_correlation(scores)
```

## 混合方法

```python
# 結合靜態和動態嵌入
combined_embedding = alpha * static_embed(word) + (1 - alpha) * contextual_embed(word)
```

## 結論

從 Word2Vec 到 BERT，詞嵌入技術經歷了革命性變化。理解這些技術的發展對於掌握現代 NLP 至關重要。

---

**延伸閱讀**

- [詞嵌入綜述](https://www.google.com/search?q=word+embeddings+survey)
- [ELMo vs BERT](https://www.google.com/search?q=ELMo+BERT+comparison)