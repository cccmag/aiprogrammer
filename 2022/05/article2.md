# Word2vec Skip-gram 實作

## Skip-gram 架構

Skip-gram 是 Word2vec 的兩種架構之一，使用目標詞來預測上下文詞。相較於 CBOW，Skip-gram 在稀有詞上的表現更好。

## 從零實作

```python
import numpy as np
from collections import Counter
import random

class SkipGram:
    def __init__(self, vocab_size, embed_dim=100):
        self.W = np.random.randn(vocab_size, embed_dim) * 0.01
        self.C = np.random.randn(embed_dim, vocab_size) * 0.01

    def forward(self, target_idx):
        h = self.W[target_idx]            # 目標詞向量
        scores = h @ self.C               # 與所有詞的相似度
        probs = self._softmax(scores)
        return h, probs

    def _softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
```

## 負採樣

完整的 softmax 計算成本與詞彙量成正比（可能數十萬）。負採樣將任務轉換為二分類：

```python
class SkipGramWithNegSampling:
    def __init__(self, vocab_size, embed_dim=100):
        self.W = np.random.randn(vocab_size, embed_dim) * 0.01
        self.C = np.random.randn(vocab_size, embed_dim) * 0.01

    def train_pair(self, target, context, neg_samples=5, lr=0.01):
        # 正樣本：提高 (target, context) 的相似度
        score_pos = np.dot(self.W[target], self.C[context])
        loss_pos = -np.log(self._sigmoid(score_pos))

        # 負樣本：降低 (target, noise) 的相似度
        noise_words = self._sample_negative(context, neg_samples)
        loss_neg = 0
        for noise in noise_words:
            score_neg = np.dot(self.W[target], self.C[noise])
            loss_neg -= np.log(self._sigmoid(-score_neg))

        # 梯度更新
        grad_pos = self._sigmoid(score_pos) - 1
        self.W[target] -= lr * grad_pos * self.C[context]
        self.C[context] -= lr * grad_pos * self.W[target]

        for noise in noise_words:
            grad_neg = self._sigmoid(np.dot(self.W[target], self.C[noise]))
            self.W[target] -= lr * grad_neg * self.C[noise]
            self.C[noise] -= lr * grad_neg * self.W[target]

        return loss_pos + loss_neg

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -10, 10)))

    def _sample_negative(self, exclude_idx, k=5):
        # 根據詞頻採樣，P(w) ∝ count(w)^0.75
        candidates = [i for i in range(len(self.W)) if i != exclude_idx]
        return random.sample(candidates, min(k, len(candidates)))
```

## 訓練流程

```python
# 準備訓練資料
corpus = "the cat sat on the mat the dog sat on the log"
words = corpus.split()
vocab = list(set(words))
w2i = {w: i for i, w in enumerate(vocab)}

# 生成訓練對 (target, context)
pairs = []
window_size = 2
for i, target in enumerate(words):
    context_range = range(max(0, i-window_size), min(len(words), i+window_size+1))
    for j in context_range:
        if i != j:
            pairs.append((w2i[target], w2i[words[j]]))

# 訓練
model = SkipGramWithNegSampling(len(vocab), embed_dim=50)
for epoch in range(100):
    random.shuffle(pairs)
    total_loss = 0
    for target, context in pairs:
        total_loss += model.train_pair(target, context)
    if epoch % 20 == 0:
        print(f"Epoch {epoch}: loss={total_loss:.4f}")
```

## 可視化

訓練完成後，可以使用 t-SNE 將詞向量降維到 2D 進行可視化。語義相近的詞在圖中會聚集成群。

## 延伸閱讀

- [Word2Vec 原始論文](https://www.google.com/search?q=Distributed+Representations+of+Words+and+Phrases+and+their+Compositionality)
- [word2vec Parameter Learning Explained](https://www.google.com/search?q=word2vec+parameter+learning+explained)
- [Gensim Word2Vec 教學](https://www.google.com/search?q=gensim+word2vec+tutorial)
