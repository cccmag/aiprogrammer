# 文字分類實務

## 文字分類的應用場景

- 垃圾郵件偵測
- 新聞分類（體育、財經、娛樂等）
- 情感分析（正向、負向、中立）
- 意圖識別（客服機器人）

## 兩種主要方法

### 1. 傳統機器學習：TF-IDF + 分類器

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# 訓練資料
train_texts = [
    "I love this movie, it's fantastic!",
    "This film is terrible, waste of time",
    "Great acting and wonderful story",
    "Boring and predictable plot",
]
train_labels = [1, 0, 1, 0]  # 1=正向, 0=負向

# 建立 pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

# 訓練
pipeline.fit(train_texts, train_labels)

# 預測
test_text = "Amazing director, brilliant performance!"
prediction = pipeline.predict([test_text])
print(prediction)  # [1]
```

### 2. 深度學習：詞嵌入 + CNN/RNN

```python
import numpy as np

# 假設已有詞向量矩陣
# vocab_size = 10000, embedding_dim = 100
embedding_matrix = np.random.randn(10000, 100)

# 簡化的分類模型
def classify_text(text_indices, embedding_matrix):
    # 取得詞向量
    embeddings = embedding_matrix[text_indices]
    # 平均池化
    avg_embedding = np.mean(embeddings, axis=0)
    # 簡單線性分類
    scores = np.dot(avg_embedding, np.random.randn(100, 2))
    return np.argmax(scores)
```

## TF-IDF 详解

TF-IDF = 詞頻（TF）× 逆文檔頻率（IDF）

```python
from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "machine learning is powerful",
    "deep learning uses neural networks",
    "machine learning and deep learning are related",
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

print(tfidf_matrix.toarray())
print(vectorizer.get_feature_names_out())
```

## 使用 scikit-learn 的完整範例

```python
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# 載入資料
newsgroups_train = fetch_20newsgroups(subset='train')
newsgroups_test = fetch_20newsgroups(subset='test')

# 建立分類器
clf = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=10000, stop_words='english')),
    ('svm', LinearSVC(C=1.0, max_iter=10000))
])

# 訓練
clf.fit(newsgroups_train.data, newsgroups_train.target)

# 預測
predictions = clf.predict(newsgroups_test.data)

# 評估
print(classification_report(newsgroups_test.target, predictions))
```

## 交叉驗證

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf, newsgroups_train.data, newsgroups_train.target, cv=5)
print(f"Cross-validation scores: {scores}")
print(f"Mean: {scores.mean():.3f}, Std: {scores.std():.3f}")
```

## 類別不平衡處理

```python
from sklearn.utils.class_weight import compute_class_weight

# 計算類別權重
weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights = dict(zip(np.unique(y_train), weights))

# SVM with class weights
clf = LinearSVC(class_weight=class_weights)
```

## 多類別分類

```python
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', OneVsRestClassifier(LogisticRegression(max_iter=1000)))
])

clf.fit(train_texts, train_labels_multi)
```

## 總結

文字分類是 NLP 基礎任務之一。TF-IDF + 線性分類器速度快、效果好，適合入門。深度學習方法則可捕捉更複雜的語意模式。下期我們將討論情感分析的具體應用。