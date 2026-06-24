# 文字向量化的數學原理

## 文字數值化的必要性

電腦無法直接處理文字，需要將文字轉換為數值向量。

## One-Hot 編碼

每個詞彙用一個維度表示，該詞出現為 1，否則為 0。

```python
# 詞彙表
vocab = ["cat", "dog", "bird"]

# One-Hot 編碼
def one_hot(word, vocab):
    vec = [0] * len(vocab)
    if word in vocab:
        vec[vocab.index(word)] = 1
    return vec

print(one_hot("cat", vocab))  # [1, 0, 0]
print(one_hot("dog", vocab))  # [0, 1, 0]
print(one_hot("bird", vocab))  # [0, 0, 1]
```

### 問題

- 維度等於詞彙量（可能數萬維）
- 所有向量正交，無法表示語意相似度
- 無法處理未登錄詞

## Bag of Words (BoW)

文件用詞頻向量表示。

```python
from collections import Counter

def bow(texts, vocab=None):
    if vocab is None:
        vocab = set(" ".join(texts).split())

    vocab = list(vocab)
    vectors = []
    for text in texts:
        words = text.lower().split()
        vec = [0] * len(vocab)
        for word, count in Counter(words).items():
            if word in vocab:
                vec[vocab.index(word)] = count
        vectors.append(vec)
    return vectors, vocab

texts = [
    "the cat sat",
    "the dog ran",
    "the cat and the dog"
]

vectors, vocab = bow(texts)
print(f"Vocabulary: {vocab}")
for i, v in enumerate(vectors):
    print(f"Text {i+1}: {v}")
```

## TF-IDF

詞語重要性考量文件頻率。

TF-IDF(w) = TF(w) × IDF(w)

- TF(w) = 詞 w 在文件中出現次數
- IDF(w) = log(總文件數 / 包含 w 的文件數)

```python
import math

def tf_idf(documents):
    N = len(documents)
    docs = [doc.lower().split() for doc in documents]
    vocab = list(set(word for doc in docs for word in doc))

    # 計算 IDF
    idf = {}
    for word in vocab:
        df = sum(1 for doc in docs if word in doc)
        idf[word] = math.log(N / df) + 1

    # 計算 TF-IDF
    vectors = []
    for doc in docs:
        tf = {}
        for word in doc:
            tf[word] = tf.get(word, 0) + 1

        vec = []
        for word in vocab:
            tf_val = tf.get(word, 0)
            vec.append(tf_val * idf[word])
        vectors.append(vec)

    return vectors, vocab

docs = ["the cat sat", "the dog ran", "the cat and the dog"]
vectors, vocab = tf_idf(docs)
print(f"Vocabulary: {vocab}")
for i, v in enumerate(vectors):
    print(f"Doc {i+1}: {v}")
```

## 詞嵌入（Word Embedding）

將詞彙映射到低維稠密向量空間。

### 詞嵌入的幾何性質

相似詞在向量空間中接近：

```python
# 使用 Gensim 訓練詞向量
from gensim.models import Word2Vec

sentences = [
    ['king', 'man', 'woman'],
    ['queen', 'woman', 'man'],
    ['apple', 'fruit', 'red'],
    ['banana', 'fruit', 'yellow'],
]

model = Word2Vec(sentences, vector_size=10, window=2, min_count=1)

# 類比運算：king - man + woman ≈ queen
try:
    result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'])
    print(f"king - man + woman ≈ {result[0][0]}")
except Exception as e:
    print(f"無法完成類比: {e}")
```

## Skip-gram 模型的數學原理

Word2Vec Skip-gram 模型最大化：

Σ log P(w_{t+j} | w_t) for j in context

其中：
P(w_{t+j} | w_t) = exp(v_{w_{t+j}}^T · v_{w_t}) / Σ exp(v_w^T · v_{w_t})

## 共現矩陣（Co-occurrence Matrix）

記錄詞彙在上下文中的共現頻率。

```python
from collections import Counter, defaultdict

def build_cooccurrence_matrix(sentences, window_size=2):
    vocab = set(word for sent in sentences for word in sent)
    vocab = sorted(vocab)
    word_to_idx = {w: i for i, w in enumerate(vocab)}

    cooc = defaultdict(lambda: defaultdict(int))

    for sentence in sentences:
        for i, word in enumerate(sentence):
            start = max(0, i - window_size)
            end = min(len(sentence), i + window_size + 1)

            for j in range(start, end):
                if i != j:
                    cooc[word][sentence[j]] += 1

    n = len(vocab)
    matrix = [[cooc[vocab[i]][vocab[j]] for j in range(n)] for i in range(n)]

    return matrix, vocab

sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "sat", "on", "the", "log"],
]

matrix, vocab = build_cooccurrence_matrix(sentences)
print(f"Vocabulary: {vocab}")
print(f"Co-occurrence matrix shape: {len(matrix)}x{len(matrix[0])}")
```

## SVD 降維

從共現矩陣獲取詞向量。

```python
import numpy as np

def svd_word_embeddings(cooc_matrix, k=10):
    U, S, Vt = np.linalg.svd(cooc_matrix)
    return U[:, :k] * np.sqrt(S[:k])

# 假設已有共現矩陣
cooc = np.array([[0, 2, 1], [2, 0, 1], [1, 1, 0]])
embeddings = svd_word_embeddings(cooc, k=2)
print(f"Embeddings shape: {embeddings.shape}")
```

## 總結

文字向量化經歷了從稀疏到稠密、從離散到連續的發展：
- **One-Hot**：高維稀疏，無語意
- **BoW/TF-IDF**：稀疏，基於詞頻
- **詞嵌入**：低維稠密，捕捉語意關係

詞嵌入是現代 NLP 的基石，大幅提升了文字處理的效果。