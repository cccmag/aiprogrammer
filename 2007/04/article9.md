# 自然語言處理的詞向量時代

## 前言

2007 年，Bengio 等人提出的神經網路語言模型開始受到關注。這是詞向量（Word Embedding）研究的早期階段。

## 語言模型的問題

### 維度災難

傳統的 n-gram 語言模型面臨嚴重的維度問題：

```python
# n-gram 模型
# 「天氣很好」可能產生的組合：
# 天氣: vocab_size
# 天氣 -> 很好: vocab_size^2
# 天氣 -> 很好 -> : vocab_size^3

# 10000 詞彙的情況
# 3-gram: 10^12 種可能組合
# 大部分從未在訓練資料中出現
```

### 稀疏性問題

```python
# 稀疏性問題
def ngram_probability(corpus, n):
    ngrams = {}
    total = 0

    for sentence in corpus:
        tokens = tokenize(sentence)
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams[ngram] = ngrams.get(ngram, 0) + 1
            total += 1

    # 大部分 ngram 的計數為 0 或 1
    return {k: v / total for k, v in ngrams.items()}
```

## 神經網路語言模型

### 基本架構

Bengio 2003 年的神經網路語言模型：

```python
# 簡化的神經網路語言模型
class NeuralLM:
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        self.embedding = numpy.random.randn(vocab_size, embedding_dim) * 0.01
        self.W1 = numpy.random.randn(embedding_dim, hidden_dim) * 0.01
        self.W2 = numpy.random.randn(hidden_dim, vocab_size) * 0.01

    def forward(self, context_words):
        # 查詢詞向量
        embeddings = [self.embedding[w] for w in context_words]
        # 平均
        x = numpy.mean(embeddings, axis=0)
        # 隱藏層
        h = numpy.tanh(numpy.dot(x, self.W1))
        # 輸出層
        y = numpy.dot(h, self.W2)
        return y

    def softmax(self, y):
        exp_y = numpy.exp(y - numpy.max(y))
        return exp_y / exp_y.sum()
```

### 詞向量的學習

```python
# 詞向量會自動學習語意關係
# 訓練完成後：
# vec("king") - vec("man") + vec("woman") ≈ vec("queen")
```

## 結語

雖然 2007 年詞向量還不是主流，但這條研究線索最終在 2013 年催生了 Word2Vec。從神經網路語言模型到詞向量，NLP 經歷了漫長的探索過程。

---

## 延伸閱讀

- [Neural+network+language+model+Bengio](https://www.google.com/search?q=Neural+network+language+model+Bengio+2003)
- [Word+embedding+history+2007](https://www.google.com/search?q=Word+embedding+history+2007)

---