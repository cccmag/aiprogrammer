# 自然語言處理的進步：詞嵌入技術

## 前言

2009 年，詞嵌入（Word Embedding）技術開始受到關注。這種將詞語表示為密集向量的方法，為自然語言處理帶來了革命性的變化。

## 詞嵌入的概念

### 詞向量的興起

```python
# 詞嵌入示意

# 傳統：稀疏表示（One-hot Encoding）
# "cat" = [1, 0, 0, 0, ...]
# "dog" = [0, 1, 0, 0, ...]

# 詞嵌入：密集表示
# "cat" = [0.2, -0.5, 0.8, ...]
# "dog" = [0.25, -0.4, 0.75, ...]

# 相似詞在向量空間中接近
import numpy as np

# 假設的詞向量
cat = np.array([0.2, -0.5, 0.8])
dog = np.array([0.25, -0.4, 0.75])
car = np.array([-0.8, 0.3, 0.1])

# 計算相似度（餘弦相似度）
def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(cosine(cat, dog))  # 高相似度
print(cosine(cat, car))  # 低相似度
```

### 為什麼需要詞嵌入？

```markdown
詞嵌入的優勢：

1. 語義表示
   - 語義相似的詞在向量空間中接近
   - 可以進行類比推理

2. 維度降低
   - 傳統 one-hot 需要數萬維
   - 詞嵌入通常 50-300 維

3. 可學習
   - 從大量文字中自動學習
   - 捕捉語義和語法關係

4. 遷移學習
   - 預訓練的詞向量可以用於多種任務
```

## 早期神經網路語言模型

### Bengio 的神經網路語言模型

```python
# 簡化的神經網路語言模型

class NeuralLanguageModel:
    def __init__(self, vocab_size, embedding_dim):
        self.embedding = np.random.randn(vocab_size, embedding_dim)
        self.hidden_weights = np.random.randn(embedding_dim * context_size, hidden_size)
        self.output_weights = np.random.randn(hidden_size, vocab_size)

    def forward(self, context_words):
        # 取得詞向量
        embeddings = [self.embedding[word] for word in context_words]
        # 拼接
        x = np.concatenate(embeddings)
        # 隱藏層
        h = np.tanh(np.dot(x, self.hidden_weights))
        # 輸出層
        y = np.dot(h, self.output_weights)
        return y
```

## 應用場景

### 文件分類

```python
# 詞嵌入用於文字分類

def text_classification(text, model):
    words = tokenize(text)
    embeddings = [word_embeddings[word] for word in words]
    # 平均池化
    doc_vector = np.mean(embeddings, axis=0)
    # 分類
    return classifier.predict(doc_vector)
```

### 語義相似度

```python
# 計算句子相似度

def sentence_similarity(s1, s2, embeddings):
    v1 = sentence_vector(s1, embeddings)
    v2 = sentence_vector(s2, embeddings)
    return cosine_similarity(v1, v2)
```

## 結語

詞嵌入技術是現代 NLP 的基礎。雖然 2009 年還處於早期階段，但這項技術的潛力已經顯現。

## 延伸閱讀

- [詞嵌入技術介紹](https://www.google.com/search?q=word+embedding+introduction+2009)
- [自然語言處理回顧](https://www.google.com/search?q=NLP+2009+review)
- [詞向量表示](https://www.google.com/search?q=dense+word+representations)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*