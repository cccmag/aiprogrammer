# 詞向量可視化：t-SNE 實戰

## 前言

t-SNE 是一種降維技術，常用於高維資料視覺化。

## 使用 sklearn

```python
from sklearn.manifold import TSNE
import numpy as np

# 假設有 1000 個詞，每個 300 維
word_vectors = np.random.randn(1000, 300)

# t-SNE 降維到 2D
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
vectors_2d = tsne.fit_transform(word_vectors)

# 視覺化
import matplotlib.pyplot as plt
plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1])
plt.show()
```

## 結合 Word2Vec

```python
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 訓練模型
model = Word2Vec(sentences, vector_size=100, window=5)

# 取得詞向量
words = list(model.wv.key_toindex.keys())[:100]
vectors = [model.wv[w] for w in words]

# t-SNE
tsne = TSNE(n_components=2, random_state=42)
vectors_2d = tsne.fit_transform(vectors)

# 繪圖
for i, word in enumerate(words):
    plt.scatter(vectors_2d[i, 0], vectors_2d[i, 1])
    plt.annotate(word, (vectors_2d[i, 0], vectors_2d[i, 1]))
plt.show()
```

## 延伸閱讀

- [t-SNE 可視化指南](https://www.google.com/search?q=t-SNE+visualization+tutorial)