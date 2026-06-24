# 4. scikit-learn 入門

## scikit-learn 概述

scikit-learn 是 Python 生態系中最受歡迎的機器學習庫，提供了豐富的監督式與非監督式學習演算法，以及統一的 API 設計。

## 安裝 scikit-learn

```bash
pip install scikit-learn numpy scipy matplotlib pandas
```

## scikit-learn API 設計

scikit-learn 的 API 遵循一致的設計模式：

1. **實例化模型**：建立模型物件
2. **fit()**：訓練模型
3. **predict()**：預測新資料
4. **score()**：評估模型效能

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

clf = LogisticRegression(max_iter=200)
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print(f"準確率: {accuracy:.2%}")
```

## 估計器（Estimator）

估計器是 scikit-learn 的核心概念，所有學習演算法都實現 Estimator 介面。

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

estimators = {
    'RandomForest': RandomForestClassifier(n_estimators=100),
    'SVM': SVC(kernel='rbf'),
    'KNN': KNeighborsClassifier(n_neighbors=5)
}

for name, clf in estimators.items():
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    print(f"{name}: {acc:.2%}")
```

## 轉換器（Transformer）

轉換器用於資料預處理，實現 fit_transform() 方法。

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

minmax = MinMaxScaler()
X_train_normalized = minmax.fit_transform(X_train)
```

## Pipeline

Pipeline 將多個步驟串聯在一起，確保訓練與預測使用相同的預處理流程。

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf'))
])

pipeline.fit(X_train, y_train)
accuracy = pipeline.score(X_test, y_test)
print(f"Pipeline 準確率: {accuracy:.2%}")
```

## 交叉驗證

使用 cross_val_score 進行交叉驗證。

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(pipeline, iris.data, iris.target, cv=5)
print(f"交叉驗證分數: {scores}")
print(f"平均分數: {scores.mean():.2%}")
print(f"標準差: {scores.std():.2%}")
```

## 超參數調優

### GridSearchCV

```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

param_grid = {
    'svm__C': [0.1, 1, 10],
    'svm__kernel': ['linear', 'rbf']
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5)
grid_search.fit(iris.data, iris.target)

print(f"最佳參數: {grid_search.best_params_}")
print(f"最佳分數: {grid_search.best_score_:.2%}")
```

### RandomizedSearchCV

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform

param_dist = {
    'svm__C': uniform(0.1, 10),
    'svm__kernel': ['linear', 'rbf']
}

random_search = RandomizedSearchCV(
    pipeline, param_dist, n_iter=10, cv=5, random_state=42
)
random_search.fit(iris.data, iris.target)
print(f"最佳參數: {random_search.best_params_}")
```

## 模型儲存與載入

```python
import joblib

joblib.dump(pipeline, 'model.pkl')
loaded_model = joblib.load('model.pkl')

accuracy = loaded_model.score(X_test, y_test)
print(f"載入模型準確率: {accuracy:.2%}")
```

## 資料集工具

scikit-learn 提供了多種內建資料集：

```python
from sklearn.datasets import load_iris, load_digits, make_classification

iris = load_iris()
digits = load_digits()
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
```

## 參考資源

- https://www.google.com/search?q=scikit-learn+tutorial+API+estimator+transformer+2019
- https://www.google.com/search?q=scikit-learn+pipeline+cross+validation+grid+search+2019
- https://www.google.com/search?q=scikit-learn+datasets+load+iris+digits+make+classification+2019