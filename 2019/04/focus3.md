# 詞嵌入技術

## 詞向量的起源

詞嵌入（Word Embedding）是將詞映射到稠密向量空間的技術，是現代 NLP 的基石。

---

## 從 One-Hot 到詞嵌入

### One-Hot 編碼的問題

傳統的詞表示使用 one-hot 編碼：

```
詞彙表：["cat", "dog", "bird"]
cat  -> [1, 0, 0]
dog  -> [0, 1, 0]
bird -> [0, 0, 1]
```

問題：
- **維度爆炸**：詞彙表可達數十萬維
- **語意鸿溝**：相似詞的向量正交，無法捕捉語意關係

### 詞嵌入的革命

詞嵌入將詞表示為低維稠密向量：

```
cat  -> [0.2, -0.5, 0.8, ...]  (100 維)
dog  -> [0.25, -0.4, 0.75, ...]
bird -> [-0.3, 0.6, 0.1, ...]
```

優點：
- **維度可控**：通常 50-300 維
- **語意相似**：相似詞的向量接近
- **可學習**：從資料中自動學習

---

## 語意向量空間

詞嵌入將詞表示為向量，這些向量形成一個語意向量空間。

### 向量空間的特性

```
                    king
                     ↑
                     │
             man ────┼────── queen
                     │
                     │
        apple ───────┼────── fruit
                     │
                     ↓
                   orange
```

在這個空間中：
- **語意相似的詞彼此接近**
- **類比關係可以透過向量運算捕捉**

### 經典類比範例

```python
# king - man + woman ≈ queen
# king 和 queen 的關係，類似 man 和 woman 的關係
```

---

## 詞嵌入的特性

### 語法關係

```
fast -> faster -> fastest
slow -> slower -> slowest

walking -> walked
running -> ran
```

### 語意關係

```
king : queen :: man : woman
apple : fruit :: carrot : vegetable
```

### 向量運算

```python
import numpy as np

def cosine_similarity(a, b):
    """計算餘弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 範例
v_king = np.array([0.2, 0.5, 0.3, ...])
v_man = np.array([0.1, 0.4, 0.2, ...])
v_woman = np.array([0.15, 0.45, 0.25, ...])

similarity = cosine_similarity(v_king, v_man)
```

---

## 詞嵌入的訓練方法

### 基於計數的方法

**共現矩陣**

```python
from collections import Counter

def build_cooccurrence_matrix(corpus, window_size=2):
    """建立共現矩陣"""
    vocab = set()
    for sentence in corpus:
        vocab.update(sentence)

    word2idx = {w: i for i, w in enumerate(vocab)}
    idx2word = {i: w for w, i in word2idx.items()}

    cooc = np.zeros((len(vocab), len(vocab)))

    for sentence in corpus:
        for i, word in enumerate(sentence):
            start = max(0, i - window_size)
            end = min(len(sentence), i + window_size + 1)

            for j in range(start, end):
                if i != j:
                    cooc[word2idx[word]][word2idx[sentence[j]]] += 1

    return cooc, word2idx, idx2word
```

**奇異值分解（SVD）**

```python
from numpy.linalg import svd

def embed_with_svd(cooc_matrix, dim=100):
    """使用 SVD 提取詞向量"""
    U, S, V = svd(cooc_matrix, full_matrices=False)
    embeddings = U[:, :dim] * np.sqrt(S[:dim])
    return embeddings
```

### 基於預測的方法

**神經網路語言模型（2003）**

Bengio 等人於 2003 年提出神經網路語言模型（NNLM），首次使用神經網路學習詞向量：

```
輸入：前面 n-1 個詞（one-hot）
    ↓
詞嵌入層（Projection）
    ↓
隱藏層
    ↓
輸出層（Softmax）
```

**Word2Vec（2013）**

Mikolov 等人於 2013 年提出 Word2Vec，大幅簡化訓練過程：

- **CBOW**：用上下文預測中心詞
- **Skip-gram**：用中心詞預測上下文

---

## 詞嵌入的評估

### 內在評估

**類比推理**

```python
def evaluate_analogies(model, analogies):
    """評估類比任務"""
    correct = 0
    total = 0

    for a, b, c, expected in analogies:
        if a not in model.wv or b not in model.wv or c not in model.wv:
            continue

        result = model.wv.most_similar(positive=[b, c], negative=[a])[0][0]
        if result == expected:
            correct += 1
        total += 1

    return correct / total if total > 0 else 0
```

### 外在評估

在實際任務上測試，如文字分類、命名實體識別等。

---

## 常用詞嵌入模型

| 模型 | 年份 | 特點 |
|-----|------|------|
| Word2Vec | 2013 | 簡單高效，廣泛使用 |
| GloVe | 2014 | 全域統計 + 局部上下文 |
| fastText | 2016 | 子詞嵌入，處理未登錄詞 |
| ELMo | 2018 | 雙向 LSTM，上下文化 |
| BERT | 2018 | Transformer，上下文化 |

---

## 應用場景

### 文件分類

```python
# 將文件中的詞向量平均
doc_vector = np.mean([word_vectors[word] for word in tokens if word in word_vectors], axis=0)
```

### 語意搜尋

```python
def semantic_search(query, documents, model):
    query_vec = np.mean([model.wv[w] for w in query if w in model.wv], axis=0)
    scores = [cosine_similarity(query_vec, doc) for doc in documents]
    return scores
```

### 推薦系統

使用詞嵌入計算商品或內容的相似度。

---

## 延伸閱讀

- [Word2Vec 原始論文](https://www.google.com/search?q=Mikolov+Word2Vec+2013+paper)
- [GloVe 論文](https://www.google.com/search?q=GloVe+pennington+2014)
- [詞向量評估基準](https://www.google.com/search?q=word+embedding+evaluation+benchmarks)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」系列文章之一。*