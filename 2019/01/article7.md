# scikit-learn 入門

## scikit-learn 簡介

scikit-learn 是 Python 最流行的機器學習函式庫，提供了從資料预处理到模型訓練、評估的完整工具鏈。

## 監督式學習流程

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. 載入資料
iris = load_iris()
X, y = iris.data, iris.target

# 2. 分割資料
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 標準化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 訓練模型
model = LogisticRegression(max_iter=200)
model.fit(X_train_scaled, y_train)

# 5. 預測與評估
y_pred = model.predict(X_test_scaled)
print(f"準確率：{accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))
```

## 線性迴歸

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# 準備資料
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2.1, 4.0, 5.9, 8.1, 10.2])

# 訓練
model = LinearRegression()
model.fit(X, y)

# 預測
new_X = np.array([[6]])
print(f"預測值：{model.predict(new_X)[0]:.2f}")
print(f"係數：{model.coef_[0]:.2f}, 截距：{model.intercept_:.2f}")
```

## 決策樹

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42
)

clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

train_acc = clf.score(X_train, y_train)
test_acc = clf.score(X_test, y_test)
print(f"訓練準確率：{train_acc:.2%}")
print(f"測試準確率：{test_acc:.2%}")
```

## 隨機森林

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()
X_train, X_test, y_train, y_test = train_test_split(
    housing.data, housing.target, test_size=0.2, random_state=42
)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

print(f"訓練 R²：{rf.score(X_train, y_train):.3f}")
print(f"測試 R²：{rf.score(X_test, y_test):.3f}")
```

## 非監督式學習

### K-Means 聚類

```python
from sklearn.cluster import KMeans
import numpy as np

X = np.array([
    [1, 2], [1, 4], [1, 0],
    [10, 2], [10, 4], [10, 0]
])

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_
centers = kmeans.cluster_centers_

print(f"標籤：{labels}")
print(f"中心點：{centers}")
```

## 模型選擇

```python
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

# 交叉驗證
iris = load_iris()
svm = SVC(kernel='rbf', C=1.0)
cv_scores = cross_val_score(svm, iris.data, iris.target, cv=5)

print(f"交叉驗證分數：{cv_scores}")
print(f"平均分數：{cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")
```

## pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf'))
])

pipe.fit(X_train, y_train)
print(f"測試分數：{pipe.score(X_test, y_test):.3f}")
```

## 參考資源

- https://www.google.com/search?q=scikit-learn+tutorial+supervised+unsupervised+learning+2019
- https://www.google.com/search?q=scikit-learn+LinearRegression+DecisionTree+RandomForest+examples+2019
- https://www.google.com/search?q=scikit-learn+cross+validation+pipeline+model+selection+2019