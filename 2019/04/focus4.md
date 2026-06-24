# Word2Vec 詳解

## Mikolov 與神經網路語言模型

2013 年，Tomas Mikolov 和他在 Google 的團隊發表了 Word2Vec，這是 NLP 領域的重大突破。

---

## Word2Vec 的核心思想

Word2Vec 展示了「簡單可以很強大」——用一個淺層神經網路，就可以學習高質量的詞向量。

### 關鍵創新

1. **簡化架構**：移除深度網路的複雜層
2. **高效訓練**：層次 Softmax、負採樣
3. **類比特性**：詞向量支援語意類比運算

---

## 兩個核心模型

### CBOW（Continuous Bag-of-Words）

**用上下文詞預測中心詞**

```
上下文：[the, cat, on, mat]
            ↓
         CBOW
            ↓
中心詞預測：the
```

**網路結構**：

```
輸入層（上下文 one-hot）x 2
    ↓
嵌入層（詞向量）
    ↓
平均層
    ↓
隱藏層
    ↓
輸出層（Softmax）
```

**訓練目標**：

```python
# 最大化正確中心詞的機率
max P(center_word | context_words)
```

### Skip-gram

**用中心詞預測上下文詞**

```
中心詞：cat
            ↓
        Skip-gram
            ↓
上下文預測：[the, on, mat, sat]
```

**網路結構**：

```
輸入層（中心詞 one-hot）
    ↓
嵌入層（詞向量）
    ↓
複製（多個輸出）
    ↓
多個輸出層（Softmax）
```

**訓練目標**：

```python
# 最大化上下文詞的機率
max P(context_words | center_word)
```

---

## 技術細節

### 輸入表示

```python
# 假設詞彙表大小為 V，嵌入維度為 N

# 輸入：V 維 one-hot 向量
# 嵌入矩陣：V x N
# 輸出：N 維詞向量

embedding_matrix = np.random.randn(vocab_size, embedding_dim) * 0.1
```

### 損失函數

```python
import torch
import torch.nn as nn

class Word2Vec(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        self.target_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.context_embeddings = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, target, context):
        target_emb = self.target_embeddings(target)  # batch x dim
        context_emb = self.context_embeddings(context)  # batch x dim
        score = torch.sum(target_emb * context_emb, dim=1)
        return score
```

---

## 高效訓練技巧

### 層次 Softmax

將輸出層改為霍夫曼樹，避免計算整個 Softmax：

```
輸出層：V 個節點 → log(V) 個二元决策
```

**優點**： 時間複雜度從 O(V) 降到 O(log V)

### 負採樣（Negative Sampling）

對於每個正樣本，採樣少量負樣本：

```python
def negative_sampling(target, context, k=5):
    """
    target: 正樣本對的中心詞
    context: 正樣本對的上下文詞
    k: 負採樣數量
    """
    # 正樣本：target 和 context 是鄰居
    # 負樣本：從噪音分佈採樣
    noise = np.random.choice(vocab_size, k, replace=False)
    return noise
```

**噪音分佈**：

```python
# 噪音分佈（unigram 分數的 3/4 次方）
noise_prob = (freq(word) ** 0.75) / sum(freq ** 0.75)
```

### 二次採樣

對高頻詞進行採樣：

```python
def subsample高频词(word, freq, threshold=1e-5):
    """高頻詞被保留的機率"""
    return (np.sqrt(freq / threshold) + 1) * threshold / freq
```

---

## 類比推理能力

Word2Vec 最引人注目的特性是支援類比推理：

### 經典範例

```python
# king - man + woman ≈ queen
# paris - france + italy ≈ rome

result = model.most_similar(
    positive=['king', 'woman'],
    negative=['man']
)
# [(queen, 0.92), ...]

result = model.most_similar(
    positive=['paris', 'italy'],
    negative=['france']
)
# [(rome, 0.89), ...]
```

### 視覺化

```
        queen
         |
      king+woman-man
         |
    ---------------
    |             |
   man          woman
    |             |
    +-------------+
         |
        cat
```

---

## Gensim 實作

```python
from gensim.models import Word2Vec

sentences = [
    ['natural', 'language', 'processing', 'is', 'fascinating'],
    ['deep', 'learning', 'has', 'revolutionized', 'NLP'],
    ['word', 'embeddings', 'capture', 'semantic', 'relationships'],
]

model = Word2Vec(
    sentences,
    vector_size=100,      # 詞向量維度
    window=5,             # 上下文視窗
    min_count=1,          # 最小詞頻
    workers=4,            # 訓練執行緒
    sg=1,                # 1=Skip-gram, 0=CBOW
    epochs=100,           # 訓練輪數
    negative=5,          # 負採樣數量
)

# 儲存模型
model.save("word2vec.model")

# 取得詞向量
vector = model.wv['language']

# 找相似詞
similar = model.wv.most_similar('NLP', topn=5)

# 類比推理
result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'])
```

---

## 訓練資料

### 資料量與質量

- **最少**：數百萬詞
- **推薦**：數十億詞（Wikipedia、News corpus 等）
- **高質量**：多樣性、領域覆蓋

### 預訓練模型

```python
import gensim.downloader as api

# 下載預訓練模型
model = api.load("glove-wiki-gigaword-100")

# 使用
vector = model['computer']
similar = model.most_similar('computer')
```

---

## 限制與改進

### 局限性

1. **上下文無關**：每個詞只有一個向量
2. **多義性**：無法區分不同含義
3. **未登錄詞**：OOV 問題

### 改進方向

| 問題 | 解決方案 |
|-----|---------|
| 上下文無關 | ELMo、BERT |
| 多義性 | Sense2Vec |
| 未登錄詞 | fastText 子詞嵌入 |

---

## 延伸閱讀

- [Word2Vec 原始論文](https://www.google.com/search?q=Mikolov+Efficient+Estimation+Word+Representations+2013)
- [Skip-gram 論文](https://www.google.com/search?q=Mikolov+Distributed+Representations+2013)
- [Gensim Word2Vec 文檔](https://www.google.com/search?q=gensim+word2vec+tutorial)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」系列文章之一。*