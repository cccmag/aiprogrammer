# GloVe 與 fastText

## GloVe：全域向量表示

GloVe（Global Vectors）由 Stanford NLP 團隊於 2014 年提出，結合了共現矩陣的全域統計資訊和 Word2Vec 的局部上下文學習。

---

## GloVe 的核心思想

### 為什麼需要 GloVe？

Word2Vec 只考慮局部上下文，忽略了全域統計資訊：

```
Word2Vec：只看滑動視窗內的共現
GloVe：看整個語料庫的共現統計
```

### GloVe 的目標函數

```python
import numpy as np

def glove_loss(weights, cooc_matrix, x_max=100, alpha=0.75):
    """
    GloVe 損失函數

    權重函數：
    f(x) = (x/x_max)^alpha if x < x_max
           1 otherwise
    """
    weight = np.where(cooc_matrix < x_max,
                       (cooc_matrix / x_max) ** alpha,
                       1.0)

    # 損失 = weight * (W_i · W_j + b_i + b_j - log(X_ij))^2
    loss = weight * (np.dot(weights[0], weights[1].T) -
                     np.log(cooc_matrix + 1)) ** 2
    return np.sum(loss)
```

---

## GloVe 的訓練流程

### 步驟 1：建立共現矩陣

```python
from collections import Counter

def build_cooccurrence_matrix(corpus, window_size=10):
    """建立共現矩陣"""
    vocab = {}
    for sentence in corpus:
        for word in sentence:
            if word not in vocab:
                vocab[word] = len(vocab)

    vocab_size = len(vocab)
    cooc = np.zeros((vocab_size, vocab_size))

    for sentence in corpus:
        for i, word in enumerate(sentence):
            word_idx = vocab[word]
            start = max(0, i - window_size)
            end = min(len(sentence), i + window_size + 1)

            for j in range(start, end):
                if i != j:
                    context_word = sentence[j]
                    context_idx = vocab[context_word]
                    distance = abs(i - j)
                    cooc[word_idx][context_idx] += 1.0 / distance

    return cooc, vocab
```

### 步驟 2：加權最小平方法

```python
def train_glove(cooc_matrix, dim=100, epochs=50, learning_rate=0.05):
    """訓練 GloVe"""
    vocab_size = cooc_matrix.shape[0]

    # 初始化
    W = np.random.randn(vocab_size, dim) * 0.1
    W_tilde = np.random.randn(vocab_size, dim) * 0.1
    b = np.zeros(vocab_size)
    b_tilde = np.zeros(vocab_size)

    x_max = 100
    alpha = 0.75

    for epoch in range(epochs):
        for i in range(vocab_size):
            for j in range(vocab_size):
                if cooc_matrix[i, j] > 0:
                    x = cooc_matrix[i, j]

                    # 權重
                    if x < x_max:
                        weight = (x / x_max) ** alpha
                    else:
                        weight = 1.0

                    # 預測值
                    pred = np.dot(W[i], W_tilde[j]) + b[i] + b_tilde[j]

                    # 梯度
                    diff = pred - np.log(x + 1)
                    loss = weight * diff ** 2

                    grad = 2 * weight * diff

                    W[i] -= learning_rate * grad * W_tilde[j]
                    W_tilde[j] -= learning_rate * grad * W[i]
                    b[i] -= learning_rate * grad
                    b_tilde[j] -= learning_rate * grad

    return (W + W_tilde) / 2  # 返回兩個矩陣的平均
```

---

## fastText：子詞嵌入

fastText 由 Facebook AI Research 於 2016 年提出，核心思想是將每個詞表示為子詞（subword）的集合。

### 子詞思想

```
"apple" 的子詞：
- <ap, ple, app, ppl, ple> (字元 n-gram)
- <apple> (完整詞)

向量 = sum(所有子詞的向量)
```

### 處理未登錄詞

```python
def get_subwords(word, n_min=3, n_max=6):
    """取得詞的所有子詞"""
    word = f"<{word}>"  # 添加邊界標記
    subwords = []
    for n in range(n_min, n_max + 1):
        for i in range(len(word) - n + 1):
            subwords.append(word[i:i+n])
    return subwords

# "apple" -> ['<ap', 'app', 'ppl', 'ple', '<app', 'appl', 'pple', 'ple>']
```

---

## fastText 實作

```python
from gensim.models import FastText

sentences = [
    ['natural', 'language', 'processing'],
    ['deep', 'learning', 'revolution'],
    ['machine', 'learning', 'algorithms'],
]

model = FastText(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    epochs=100,
    min_n=3,      # 最小子詞長度
    max_n=6,      # 最大子詞長度
)

# 即使是未登錄詞也可以獲得向量
vector = model.wv['learning']
```

---

## 比較與應用場景

### GloVe vs Word2Vec

| 特性 | GloVe | Word2Vec |
|-----|-------|----------|
| 訓練目標 | 全域優化 | 局部預測 |
| 訓練速度 | 較慢 | 較快 |
| 類比任務 | 較好 | 較好 |
| 記憶體 | 較高 | 較低 |

### fastText 的優勢

1. **處理未登錄詞**：可以對任何字元組合生成向量
2. **形態學資訊**：捕捉詞的內部結構
3. **多語言支持**：適用於豐富形態的語言

### 應用場景

```python
# GloVe 適用場景
# - 需要預訓練的高質量詞向量
# - 類比推理任務
# - 大規模語料庫

# fastText 適用場景
# - 處理未登錄詞
# - 形態豐富的語言（德語、芬蘭語等）
# - 稀有詞和專有名詞
```

---

## 預訓練模型使用

```python
import gensim.downloader as api

# GloVe
glove_model = api.load("glove-wiki-gigaword-50")
print(glove_model['computer'])

# fastText (Wikipedia)
fasttext_model = api.load("fasttext-wiki-news-subwords-300")
print(fasttext_model['computer'])
```

---

## 延伸閱讀

- [GloVe 原始論文](https://www.google.com/search?q=GloVe+Pennington+2014+paper)
- [fastText 原始論文](https://www.google.com/search?q=fastText+Bojanowski+2016)
- [GloVe vs Word2Vec](https://www.google.com/search?q=GloVe+vs+Word2Vec+comparison)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」系列文章之一。*