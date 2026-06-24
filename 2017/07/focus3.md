# 詞嵌入與 Word2Vec

## 詞向量的革命

2013 年，Tomas Mikolov 等人在 Google 發表 Word2Vec，引發NLP領域的革命。首次展示可用稠密向量捕捉詞彙的語意關係。

## 為什麼不用 One-Hot？

傳統使用 one-hot 編碼：
- 維度等於詞彙量（數萬維）
- 所有向量正交，無法表達語意相似度

詞嵌入的優點：
- 維度低（通常 100-300 維）
- 相似的詞向量相近
- 可做代數運算：`king - man + woman ≈ queen`

## Word2Vec 兩種模型

### 1. CBOW（Continuous Bag of Words）

用上下文預測中心詞：

```
the cat sits on the [mat]
 ↓ ↓   ↓  ↓   ↓  ↓
  預測 → mat
```

### 2. Skip-gram

用中心詞預測上下文：

```
  mat
 ↓
  預測 → the, cat, sits, on, the
```

## Gensim 實作 Word2Vec

```python
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

# 訓練語料（已分詞的句子列表）
sentences = [
    ['machine', 'learning', 'is', 'powerful'],
    ['deep', 'learning', 'achieves', 'great', 'results'],
    ['natural', 'language', 'processing', 'is', 'interesting'],
    ['word', 'embeddings', 'capture', 'semantic', 'meaning'],
]

# 訓練模型
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# 查詢相似詞
similar = model.wv.most_similar('learning')
print(similar)
# [('machine', 0.15), ('deep', 0.12), ('natural', 0.10), ...]

# 語意運算
result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'])
print(result[0][0])  # queen
```

## 預訓練詞向量

可以使用大規模語料預訓練的向量：

```python
import gensim.downloader as api
model = api.load('glove-wiki-gigaword-100')  # 100維 GloVe

# 查詢
print(model.most_similar('computer'))
```

## 詞向量的特性

### 語意相似度

```python
model = Word2Vec.load('my_model.bin')
# 找出最相似的詞
print(model.wv.most_similar('machine'))
```

### 類比推理

```python
# king - man + woman ≈ queen
result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'])
print(result[0])  # ('queen', similarity_score)
```

### 異常詞檢測

```python
# 找出不合群的詞
print(model.wv.doesnt_match(['breakfast', 'dinner', 'computer', 'lunch']))
# computer
```

## Word2Vec 參數說明

| 參數 | 說明 | 常用值 |
|------|------|--------|
| vector_size | 詞向量維度 | 100-300 |
| window | 上下文窗口大小 | 5-10 |
| min_count | 最小詞頻閾值 | 1-10 |
| workers | 訓練執行緒數 | 4 |
| sg | 0=CBOW, 1=Skip-gram | 通常選 1 |

## 訓練資料準備

```python
import nltk
from nltk.tokenize import word_tokenize

# 下載文字資料
nltk.download('gutenberg')
corpus = nltk.corpus.gutenberg.raw('austen-emma.txt')

# 分詞
tokens = word_tokenize(corpus.lower())
# 過濾
tokens = [w for w in tokens if w.isalpha()]

# 轉成句子（每 N 個詞為一句）
N = 20
sentences = [tokens[i:i+N] for i in range(0, len(tokens), N)]

# 訓練
model = Word2Vec(sentences, vector_size=100, window=5, min_count=5)
```

## 儲存與載入

```python
from gensim.models import Word2Vec

# 儲存
model.save('word2vec.model')

# 載入
model = Word2Vec.load('word2vec.model')

# 只儲存詞向量（較小）
model.wv.save('word2vec.kv')
```

## 總結

Word2Vec 開創了詞嵌入時代。通過神經網路學習詞的低維表示，捕捉語意相似性與類比關係。Gensim 提供了方便的實作介面。下期我們將討論如何用這些向量進行文字分類。