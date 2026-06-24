# scikit-learn 文字分類

## scikit-learn NLP 流程

```
文字 → 預處理 → 特徵提取 → 模型訓練 → 預測
```

## TF-IDF 特徵提取

```python
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    "This is a positive review",
    "This is a negative review",
    "Great product, highly recommend",
    "Terrible experience, avoid",
]

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(corpus)

print(f"Feature matrix shape: {X.shape}")
print(f"Feature names: {vectorizer.get_feature_names_out()[:10]}")
```

## 文字分類器

### 線性 SVM

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

train_texts = [
    "I love this product, it's amazing",
    "This is the worst purchase ever",
    "Great quality and fast shipping",
    "Very disappointed with the quality",
    "Excellent product, would buy again",
    "Terrible, waste of money",
]
train_labels = [1, 0, 1, 0, 1, 0]

# 建立 pipeline
clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('svm', LinearSVC())
])

clf.fit(train_texts, train_labels)

# 預測
test_text = "I really love this item"
prediction = clf.predict([test_text])[0]
print(f"Prediction: {'Positive' if prediction == 1 else 'Negative'}")
```

### 樸素貝葉斯

```python
from sklearn.naive_bayes import MultinomialNB

clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('nb', MultinomialNB())
])

clf.fit(train_texts, train_labels)
prediction = clf.predict(["Best product ever!"])[0]
print(f"Prediction: {'Positive' if prediction == 1 else 'Negative'}")
```

### Logistic Regression

```python
from sklearn.linear_model import LogisticRegression

clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('lr', LogisticRegression(max_iter=1000))
])

clf.fit(train_texts, train_labels)
```

## 新聞分類實例

```python
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

# 載入資料
categories = ['rec.sport.baseball', 'sci.med']
train_data = fetch_20newsgroups(subset='train', categories=categories)
test_data = fetch_20newsgroups(subset='test', categories=categories)

# 特徵提取
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_data.data)
X_test = vectorizer.transform(test_data.data)

# 訓練
clf = LinearSVC()
clf.fit(X_train, train_data.target)

# 評估
predictions = clf.predict(X_test)
print(classification_report(test_data.target, predictions, target_names=categories))
```

## 交叉驗證

```python
from sklearn.model_selection import cross_val_score

clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('svm', LinearSVC())
])

scores = cross_val_score(clf, train_texts, train_labels, cv=5)
print(f"CV scores: {scores}")
print(f"Mean: {scores.mean():.3f}, Std: {scores.std():.3f}")
```

## Grid Search 超參數調優

```python
from sklearn.model_selection import GridSearchCV

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('svm', LinearSVC())
])

param_grid = {
    'tfidf__max_features': [1000, 5000, None],
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'svm__C': [0.1, 1, 10],
}

grid = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1)
grid.fit(train_texts, train_labels)

print(f"Best params: {grid.best_params_}")
print(f"Best score: {grid.best_score_:.3f}")
```

## 多類別分類

```python
from sklearn.datasets import load_digits
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# 載入數字資料（作為範例）
digits = load_digits()
X, y = digits.data, digits.target

clf = Pipeline([
    ('tfidf', TfidfVectorizer()),  # 這裡用於非文字資料教學
    ('lr', LogisticRegression(max_iter=2000, multi_class='multinomial'))
])

# 這只是一個概念範例
# 實際上不應該對數字影像使用 TF-IDF
```

## 儲存與載入模型

```python
import joblib

# 儲存
joblib.dump(clf, 'text_classifier.pkl')

# 載入
clf_loaded = joblib.load('text_classifier.pkl')
predictions = clf_loaded.predict(test_texts)
```

## 常見問題與解決

### 類別不平衡

```python
from sklearn.utils.class_weight import compute_class_weight

weights = compute_class_weight('balanced', classes=np.unique(train_labels), y=train_labels)
class_weight = dict(zip(np.unique(train_labels), weights))

clf = LinearSVC(class_weight=class_weight)
```

### 處理未登錄詞

```python
vectorizer = TfidfVectorizer(vocabulary=known_words)
```

## 總結

scikit-learn 提供完整的文字分類工具鏈：
- TfidfVectorizer 特徵提取
- LinearSVC、MultinomialNB、LogisticRegression 等分類器
- Pipeline 組合多個步驟
- 交叉驗證與 Grid Search 調參

這個流程足以應對大多數文字分類需求。