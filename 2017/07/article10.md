# Gensim 詞向量實作

## Gensim 简介

Gensim 是 Python 的主題建模與詞向量庫，專注於文件相似性分析與詞嵌入。

## 安裝與基本設定

```bash
pip install gensim
```

```python
import gensim
print(gensim.__version__)
```

## 訓練 Word2Vec 模型

### 基本用法

```python
from gensim.models import Word2Vec

sentences = [
    ['machine', 'learning', 'is', 'a', 'powerful', 'technique'],
    ['deep', 'learning', 'uses', 'neural', 'networks'],
    ['natural', 'language', 'processing', 'enables', 'computers', 'to', 'understand', 'text'],
    ['word', 'embeddings', 'represent', 'words', 'as', 'vectors'],
]

model = Word2Vec(sentences, vector_size=50, window=3, min_count=1)

# 儲存模型
model.save("word2vec.model")

# 載入模型
model = Word2Vec.load("word2vec.model")
```

### 關鍵參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| vector_size | 詞向量維度 | 100 |
| window | 上下文窗口大小 | 5 |
| min_count | 最小詞頻 | 5 |
| workers | 訓練執行緒數 | 3 |
| sg | 0=CBOW, 1=Skip-gram | 0 |
| epochs | 訓練輪數 | 5 |

## 使用預訓練詞向量

```python
import gensim.downloader as api

# 下載預訓練 GloVe 向量（第一次會下載）
print("Available models:", list(api.info()['models'].keys()))

# 載入小型模型
model = api.load('glove-wiki-gigaword-50')

# 查詢相似詞
print(model.most_similar('computer'))
print(model.most_similar('machine'))
```

## 相似度計算

```python
# 詞彙相似度
similarity = model.wv.similarity('man', 'woman')
print(f"man-woman similarity: {similarity:.3f}")

# 異常詞檢測
words = ['breakfast', 'dinner', 'computer', 'lunch']
odd = model.wv.doesnt_match(words)
print(f"Doesn't fit: {odd}")
```

## 類比推理

```python
# king - man + woman ≈ queen
result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'])
print(f"king - man + woman = {result[0][0]}")

# 首都類比：Paris - France + Italy ≈ Rome
result = model.wv.most_similar(positive=['paris', 'italy'], negative=['france'])
print(f"Paris - France + Italy = {result[0][0]}")
```

## 處理中文

```python
import jieba

# 中文分詞
sentences = [
    list(jieba.cut("機器學習是人工智慧的核心技術")),
    list(jieba.cut("深度學習使用神經網路進行訓練")),
    list(jieba.cut("自然語言處理讓電腦理解人類語言")),
]

# 訓練中文詞向量
model = Word2Vec(sentences, vector_size=50, window=3, min_count=1)

# 查詢相似詞
if '學習' in model.wv:
    similar = model.wv.most_similar('學習')
    print(f"與 '學習' 相似的詞: {similar}")
```

## 文件相似性

```python
from gensim import corpora
from gensim.similarities import MatrixSimilarity

# 文件集合
documents = [
    "Machine learning is a method of data analysis",
    "Deep learning uses neural networks",
    "Natural language processing deals with text",
    "Computer vision enables machines to see",
]

# 分詞
texts = [doc.lower().split() for doc in documents]

# 建立字典
dictionary = corpora.Dictionary(texts)
print(f"Vocabulary size: {len(dictionary)}")

# 建立語料庫
corpus = [dictionary.doc2bow(text) for text in texts]

# 建立相似度索引
index = MatrixSimilarity(corpus)

# 查詢
query = "neural networks and deep learning"
query_bow = dictionary.doc2bow(query.lower().split())
similarities = index[query_bow]

print("Similarities:", list(enumerate(similarities)))
```

## 詞向量視覺化

```python
import numpy as np

# 取得詞向量
words = ['king', 'queen', 'man', 'woman', 'dog', 'cat']
vectors = np.array([model.wv[w] for w in words])

print(f"Shape: {vectors.shape}")  # (6, vector_size)
```

## 增量訓練

```python
# 新增句子，無需重新訓練整個模型
new_sentences = [
    ['machine', 'learning', 'models', 'can', 'predict'],
]

model.build_vocab(new_sentences, update=True)
model.train(new_sentences, epochs=model.epochs, total_examples=model.corpus_count)
```

## 常見問題

### 記憶體不足

```python
# 限制記憶體使用
model = Word2Vec(sentences, vector_size=100, min_count=10, max_final_vocab=30000)
```

### 未知詞彙

```python
# 檢查詞彙是否存在
if 'unknown_word' in model.wv:
    print(model.wv['unknown_word'])
else:
    print("Word not in vocabulary")
```

## 總結

Gensim 是詞向量訓練的利器：
- Word2Vec 實作簡單易用
- 支援預訓練模型載入
- 類比推理、相似度計算功能完整
- 文件相似性分析也支援

結合分詞工具（jieba），可用於處理中文。