# 程式碼範例

## 文字預處理實作

```python
#!/usr/bin/env python3
"""文字預處理示範"""

import re
import jieba

def preprocess_text(text, language='en'):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    if language == 'zh':
        words = list(jieba.cut(text))
    else:
        words = text.split()
    return words

def demo():
    texts = [
        "Hello, World! I have 3 apples.",
        "我愛機器學習！2023 年是 AI 爆發年。",
    ]

    print("=" * 50)
    print("文字預處理示範")
    print("=" * 50)

    for i, text in enumerate(texts):
        lang = 'zh' if '\u4e00' <= text[0] <= '\u9fff' else 'en'
        result = preprocess_text(text, lang)
        print(f"\n原文 {i+1}: {text}")
        print(f"處理後: {result}")
```

## Word2Vec 訓練

```python
#!/usr/bin/env python3
"""Word2Vec 訓練示範"""

from gensim.models import Word2Vec

def demo():
    sentences = [
        ['machine', 'learning', 'is', 'powerful'],
        ['deep', 'learning', 'uses', 'neural', 'networks'],
        ['natural', 'language', 'processing', 'is', 'interesting'],
        ['word', 'embeddings', 'capture', 'semantic', 'meaning'],
        ['python', 'is', 'great', 'for', 'data', 'science'],
        ['neural', 'networks', 'can', 'learn', 'complex', 'patterns'],
    ]

    print("=" * 50)
    print("Word2Vec 訓練示範")
    print("=" * 50)

    model = Word2Vec(sentences, vector_size=50, window=3, min_count=1)

    print(f"\n詞彙量: {len(model.wv)}")
    print(f"向量維度: {model.wv.vector_size}")

    # 查詢相似詞
    if 'learning' in model.wv:
        similar = model.wv.most_similar('learning', topn=3)
        print(f"\n與 'learning' 最相似的詞:")
        for word, score in similar:
            print(f"  {word}: {score:.3f}")

    # 語意運算
    try:
        result = model.wv.most_similar(positive=['machine', 'science'], negative=['python'], topn=1)
        print(f"\nmachine + science - python ≈ {result[0][0]}")
    except:
        pass
```

## TF-IDF 文字分類

```python
#!/usr/bin/env python3
"""TF-IDF 文字分類示範"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def demo():
    train_texts = [
        "I love this movie, it's fantastic!",
        "This film is terrible, waste of time",
        "Great acting and wonderful story",
        "Boring and predictable plot",
        "Best movie I have ever seen",
        "Absolutely horrible experience",
    ]
    train_labels = [1, 0, 1, 0, 1, 0]

    test_texts = [
        "I enjoyed every minute of it",
        "Very disappointed with the result",
    ]

    print("=" * 50)
    print("TF-IDF 文字分類示範")
    print("=" * 50)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

    pipeline.fit(train_texts, train_labels)

    predictions = pipeline.predict(test_texts)
    for text, pred in zip(test_texts, predictions):
        label = "正向" if pred == 1 else "負向"
        print(f"\n文字: {text}")
        print(f"分類: {label}")
```

## 情感分析

```python
#!/usr/bin/env python3
"""情感分析示範"""

from textblob import TextBlob

def demo():
    texts = [
        "I love this product, it's amazing!",
        "This is terrible, worst purchase ever",
        "It's okay, nothing special",
        "Great service and friendly staff",
        "Very disappointed with the quality",
    ]

    print("=" * 50)
    print("情感分析示範")
    print("=" * 50)

    for text in texts:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment = "正向"
        elif polarity < -0.1:
            sentiment = "負向"
        else:
            sentiment = "中性"

        print(f"\n文字: {text}")
        print(f"情感: {sentiment} (polarity: {polarity:.2f})")
```

## 完整 RNN 文字分類

```python
#!/usr/bin/env python3
"""RNN/LSTM 文字分類概念示範"""

import numpy as np

def demo():
    print("=" * 50)
    print("LSTM 文字分類概念示範")
    print("=" * 50)

    vocab_size = 100
    embedding_dim = 32
    hidden_dim = 64
    sequence_length = 10

    np.random.seed(42)

    embedding = np.random.randn(vocab_size, embedding_dim)
    lstm_weights = {
        'Wf': np.random.randn(hidden_dim, embedding_dim + hidden_dim) * 0.1,
        'Wi': np.random.randn(hidden_dim, embedding_dim + hidden_dim) * 0.1,
        'Wc': np.random.randn(hidden_dim, embedding_dim + hidden_dim) * 0.1,
        'Wo': np.random.randn(hidden_dim, embedding_dim + hidden_dim) * 0.1,
    }

    print(f"\n模型參數:")
    print(f"  詞彙大小: {vocab_size}")
    print(f"  嵌入維度: {embedding_dim}")
    print(f"  隱藏層維度: {hidden_dim}")
    print(f"  序列長度: {sequence_length}")

    sample_indices = np.random.randint(0, vocab_size, sequence_length)
    print(f"\n範例輸入索引: {sample_indices[:5]}...")

    embedded = embedding[sample_indices]
    print(f"嵌入後 shape: {embedded.shape}")

    print("\n概念性 LSTM 前向傳播完成")
    print("(實際訓練需使用 PyTorch/TensorFlow)")

if __name__ == "__main__":
    demo()
```

```python
#!/usr/bin/env python3
"""Word2Vec 訓練示範"""

from gensim.models import Word2Vec

def demo():
    sentences = [
        ['machine', 'learning', 'is', 'powerful'],
        ['deep', 'learning', 'uses', 'neural', 'networks'],
        ['natural', 'language', 'processing', 'is', 'interesting'],
        ['word', 'embeddings', 'capture', 'semantic', 'meaning'],
        ['python', 'is', 'great', 'for', 'data', 'science'],
        ['neural', 'networks', 'can', 'learn', 'complex', 'patterns'],
    ]

    print("=" * 50)
    print("Word2Vec 訓練示範")
    print("=" * 50)

    model = Word2Vec(sentences, vector_size=50, window=3, min_count=1)

    print(f"\n詞彙量: {len(model.wv)}")
    print(f"向量維度: {model.wv.vector_size}")

    if 'learning' in model.wv:
        similar = model.wv.most_similar('learning', topn=3)
        print(f"\n與 'learning' 最相似的詞:")
        for word, score in similar:
            print(f"  {word}: {score:.3f}")

    try:
        result = model.wv.most_similar(positive=['machine', 'science'], negative=['python'], topn=1)
        print(f"\nmachine + science - python ≈ {result[0][0]}")
    except:
        pass

if __name__ == "__main__":
    demo()
```