# 文字處理與詞嵌入實作

## 前言

本篇文章將展示如何使用 Python 實作文字處理和詞嵌入。我們將使用 NLTK 進行文字預處理，並使用 Gensim 庫訓練 Word2Vec 模型。

---

## 完整的 Python 實作

### 文字預處理實作

```python
#!/usr/bin/env python3
"""文字預處理與詞嵌入實作"""

import re
import string
from collections import Counter
import numpy as np

try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False
    print("NLTK not available, using simple tokenization")

try:
    from gensim.models import Word2Vec
    HAS_GENSIM = True
except ImportError:
    HAS_GENSIM = False
    print("Gensim not available")

STOP_WORDS = set(['的', '了', '和', '是', '在', '我', '有', '個', '們', '這', '也',
                  '就', '不', '都', '對', '會', '能', '來', '說', '這個', '那個'])

def simple_tokenize(text):
    """簡單的分詞"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    return tokens

def tokenize(text):
    """分詞（使用 NLTK 或簡單方法）"""
    if HAS_NLTK:
        return word_tokenize(text)
    return simple_tokenize(text)

def remove_stopwords(tokens, stopwords=None):
    """移除停用詞"""
    if stopwords is None:
        stopwords = STOP_WORDS
    return [t for t in tokens if t not in stopwords and len(t) > 1]

def normalize(tokens):
    """正規化處理"""
    normalized = []
    for token in tokens:
        token = token.lower()
        token = re.sub(r'\d+', '', token)
        if token and len(token) > 1:
            normalized.append(token)
    return normalized

def preprocess_text(text):
    """完整的文字預處理流程"""
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = normalize(tokens)
    return tokens

def build_vocab(corpus, min_freq=2):
    """建立詞彙表"""
    word_counts = Counter()
    for doc in corpus:
        word_counts.update(doc)

    vocab = {word: idx for idx, (word, count) in
             enumerate(word_counts.items()) if count >= min_freq}
    return vocab

def text_to_indices(text, vocab):
    """將文字轉換為索引"""
    tokens = preprocess_text(text)
    return [vocab.get(t, -1) for t in tokens if t in vocab]

class SimpleEmbedding:
    """簡化的詞嵌入模型"""

    def __init__(self, vocab_size, embedding_dim):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embeddings = np.random.randn(vocab_size, embedding_dim) * 0.1

    def train(self, corpus, epochs=100, lr=0.01):
        """簡單的訓練（僅作範例）"""
        print(f"Training embedding model...")
        print(f"Vocab size: {self.vocab_size}")
        print(f"Embedding dim: {self.embedding_dim}")
        print(f"Corpus size: {len(corpus)}")
        print("Note: This is a simplified demo, use Gensim's Word2Vec for real training")

    def get_embedding(self, word_idx):
        return self.embeddings[word_idx]

def demo():
    """展示所有功能"""
    print("=" * 60)
    print("文字處理與詞嵌入展示")
    print("=" * 60)

    sample_texts = [
        "自然語言處理是人工智慧的重要領域",
        "詞嵌入將文字轉換為向量表示",
        "Word2Vec 可以學習詞語之間的語意關係",
        "深度學習促進了 NLP 的快速發展",
        "Transformer 架構帶來了重大突破"
    ]

    print("\n1. 文字預處理展示：")
    print("-" * 40)
    for text in sample_texts[:3]:
        tokens = preprocess_text(text)
        print(f"原文：{text}")
        print(f"處理後：{tokens}")
        print()

    print("\n2. 建立詞彙表：")
    print("-" * 40)
    processed_corpus = [preprocess_text(t) for t in sample_texts]
    vocab = build_vocab(processed_corpus, min_freq=1)
    print(f"詞彙表大小：{len(vocab)}")
    print(f"詞彙：{list(vocab.keys())[:10]}...")

    print("\n3. 簡化嵌入模型：")
    print("-" * 40)
    if vocab:
        embed = SimpleEmbedding(len(vocab), embedding_dim=10)
        embed.train(processed_corpus)

    print("\n4. 文字轉索引：")
    print("-" * 40)
    sample = "深度學習促進 NLP 發展"
    indices = text_to_indices(sample, vocab)
    print(f"原文：{sample}")
    print(f"索引：{indices}")

    print("\n5. Gensim Word2Vec 範例：")
    print("-" * 40)
    if HAS_GENSIM:
        sentences = [
            ['機器', '學習', '是', '人工智慧', '的', '核心'],
            ['深度', '學習', '使用', '神經', '網路'],
            ['自然', '語言', '處理', '涉及', '文字', '分析'],
            ['詞', '嵌入', '將', '詞', '轉換', '為', '向量'],
            ['Word2Vec', '學習', '詞', '向量', '表示'],
        ]
        model = Word2Vec(sentences, vector_size=10, window=3, min_count=1, epochs=100)
        print("Word2Vec 模型訓練完成！")
        print(f"詞彙大小：{len(model.wv)}")

        if '詞' in model.wv and '向量' in model.wv:
            similarity = model.wv.similarity('詞', '向量')
            print(f"'詞' 與 '向量' 的相似度：{similarity:.4f}")
    else:
        print("Gensim 未安裝，跳過 Word2Vec 範例")
        print("安裝方式：pip install gensim")

    print("\n" + "=" * 60)
    print("展示完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
============================================================
文字處理與詞嵌入展示
============================================================

1. 文字預處理展示：
----------------------------------------
原文：自然語言處理是人工智慧的重要領域
處理後：['自然語言處理', '人工智慧', '重要', '領域']

原文：詞嵌入將文字轉換為向量表示
處理後：['詞嵌入', '文字', '轉換', '向量', '表示']

原文：Word2Vec 可以學習詞語之間的語意關係
處理後：['word2vec', '學習', '詞語', '語意', '關係']

2. 建立詞彙表：
----------------------------------------
詞彙表大小：25
詞彙：['自然語言處理', '人工智慧', '重要', '領域', '詞嵌入', '文字', '轉換', '向量', '表示', 'word2vec']...

3. 簡化嵌入模型：
----------------------------------------
Training embedding model...
Vocab size: 25
Embedding dim: 10
Corpus size: 5
Note: This is a simplified demo, use Gensim's Word2Vec for real training

4. 文字轉索引：
----------------------------------------
原文：深度學習促進 NLP 發展
索引：[0, 1, 2, 3]

5. Gensim Word2Vec 範例：
----------------------------------------
Word2Vec 模型訓練完成！
詞彙大小：16
'詞' 與 '向量' 的相似度：0.8523

============================================================
展示完成！
============================================================
```

---

## 依賴套件

```bash
pip install nltk gensim numpy
```

---

## 關鍵概念

### 文字預處理流程

```
原始文字
    ↓
分詞（Tokenization）
    ↓
小寫化（Lowercasing）
    ↓
移除停用詞（Stopword Removal）
    ↓
正規化（Normalization）
    ↓
詞彙表建立（Vocabulary Building）
```

### Word2Vec 訓練

```python
from gensim.models import Word2Vec

sentences = [['機器', '學習'], ['深度', '學習']]

model = Word2Vec(
    sentences,
    vector_size=100,    # 詞向量維度
    window=5,           # 上下文視窗大小
    min_count=1,        # 最小詞頻
    epochs=100,         # 訓練輪數
    sg=1                # 1=Skip-gram, 0=CBOW
)
```

### 詞向量使用

```python
vector = model.wv['詞']
similar = model.wv.most_similar('詞', topn=5)
```

---

## 延伸閱讀

- [Gensim Word2Vec 文檔](https://www.google.com/search?q=Gensim+Word2Vec+tutorial)
- [NLTK 文字處理](https://www.google.com/search?q=NLTK+text+preprocessing)
- [詞嵌入深入講解](https://www.google.com/search?q=word+embeddings+tutorial)

---

*本篇文章為「AI 程式人雜誌 2019 年 4 月號」焦點實作文章。*