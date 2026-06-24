# 情感分析應用

## 什麼是情感分析？

情感分析（Sentiment Analysis）是判斷文字表達情感傾向的技術，常用於：
- 產品評論分析
- 社群媒體監控
- 客戶回饋處理
- 輿情分析

## 情感分析的層次

### 文件層級（Document-level）
判斷整篇文件的情感：
```
「這家餐廳的環境很好，但食物普通。」→ 中性或負向
```

### 句子層級（Sentence-level）
分析每個句子的情感：
```
「服務態度極差！」→ 負向
「價格實惠」→ 正向
```

### 方面層級（Aspect-level）
識別不同面向的情感：
```
「手機相機很好，但電池續航力很差。」→ 相機:正向, 電池:負向
```

## 簡單方法：基於詞典

```python
from textblob import TextBlob

text = "I love this product, it's amazing!"
blob = TextBlob(text)

print(f"Polarity: {blob.sentiment.polarity}")   # -1 到 1
print(f"Subjectivity: {blob.sentiment.subjectivity}")  # 0 到 1

# 簡單分類
def classify_sentiment(polarity):
    if polarity > 0.1:
        return "正向"
    elif polarity < -0.1:
        return "負向"
    else:
        return "中性"

print(classify_sentiment(blob.sentiment.polarity))
```

## 使用 NLTK 的 VADER

專為社群媒體設計的情感分析器：

```python
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
text = "I just got the new iPhone and I'm loving it! Best purchase ever! 😊"
scores = sia.polarity_scores(text)
print(scores)
# {'neg': 0.0, 'neu': 0.37, 'pos': 0.63, 'compound': 0.85}
```

## 機器學習方法

### 訓練資料準備

```python
from sklearn.datasets import load_files

# 假設資料夾結構：train/pos/, train/neg/
train_data = load_files('path/to/train', categories=['pos', 'neg'])
X_train, y_train = train_data.data, train_data.target
```

### 特徵工程

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),  # 使用 unigram + bigram
    stop_words='english'
)

X_train_tfidf = vectorizer.fit_transform(X_train)
```

### 模型訓練

```python
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

# Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_tfidf, y_train)

# SVM
svm_model = LinearSVC()
svm_model.fit(X_train_tfidf, y_train)
```

### 預測與評估

```python
from sklearn.metrics import accuracy_score, classification_report

X_test_tfidf = vectorizer.transform(X_test)
predictions = lr_model.predict(X_test_tfidf)

print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
print(classification_report(y_test, predictions, target_names=['neg', 'pos']))
```

## 深度學習方法

### 使用預訓練詞向量

```python
import gensim
from gensim.models import KeyedVectors

# 載入預訓練詞向量
model = gensim.downloader.load('glove-wiki-gigaword-100')

def text_to_vector(text, model, dim=100):
    words = text.lower().split()
    vectors = []
    for word in words:
        if word in model:
            vectors.append(model[word])
    if vectors:
        return np.mean(vectors, axis=0)
    return np.zeros(dim)

# 轉換文字
X_train_vec = np.array([text_to_vector(t, model) for t in X_train])
```

## 實際案例：餐廳評論分析

```python
reviews = [
    "這家餐廳的氣氛很棒，服務員態度很好",
    "等了 40 分鐘才上菜，不推薦",
    "食物美味，價格合理，會再訪",
    "環境髒亂，味道一般",
]

# 使用 TextBlob
for review in reviews:
    blob = TextBlob(review)
    sentiment = "正向" if blob.sentiment.polarity > 0 else "負向"
    print(f"{review} → {sentiment} ({blob.sentiment.polarity:.2f})")
```

## 總結

情感分析是 NLP 的經典應用。從簡單的詞典方法到複雜的深度學習模型，有多種技術可選。詞向量與預訓練模型大幅提升了分析準確度。下期我們將介紹 RNN 與 LSTM 的基礎概念。