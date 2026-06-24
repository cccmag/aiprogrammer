# KNN 分類器

## KNN 演算法原理

K近鄰（K-Nearest Neighbors）是一種基於實例的學習演算法，分類決策基於最近的K個鄰居的投票。

## 演算法步驟

1. 選擇K值
2. 計算測試樣本與所有訓練樣本的距離
3. 找出最近的K個鄰居
4. 根據多數投票決定類別

## 從零實作 KNN

```python
import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def euclidean_distance(self, x1, x2):
        return np.sqrt(np.sum((x1 - x2)**2))

    def predict(self, X):
        predictions = [self._predict(x) for x in X]
        return np.array(predictions)

    def _predict(self, x):
        distances = [self.euclidean_distance(x, x_train) for x_train in self.X_train]
        k_indices = np.argsort(distances)[:self.k]
        k_labels = self.y_train[k_indices]
        most_common = Counter(k_labels).most_common(1)
        return most_common[0][0]
```

## 使用實作

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=100, n_features=2, n_redundant=0,
                           n_informative=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

knn = KNN(k=5)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
accuracy = (y_pred == y_test).mean()
print(f"K=5 準確率: {accuracy:.2%}")
```

## 使用 scikit-learn

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

clf = KNeighborsClassifier(n_neighbors=5)
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print(f"準確率: {accuracy:.2%}")
```

## K 值選擇

```python
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=100, n_features=2, n_redundant=0,
                           n_informative=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

k_values = range(1, 21)
accuracies = []

for k in k_values:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    accuracies.append(clf.score(X_test, y_test))

best_k = k_values[np.argmax(accuracies)]
print(f"最佳 K 值: {best_k}")
print(f"最佳準確率: {max(accuracies):.2%}")
```

## 距離度量

### Euclidean Distance（預設）

```python
clf = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
```

### Manhattan Distance

```python
clf = KNeighborsClassifier(n_neighbors=5, metric='manhattan')
```

### Minkowski Distance

```python
clf = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
```

## 權重投票

```python
clf_uniform = KNeighborsClassifier(n_neighbors=5, weights='uniform')
clf_distance = KNeighborsClassifier(n_neighbors=5, weights='distance')

clf_uniform.fit(X_train, y_train)
clf_distance.fit(X_train, y_train)

print(f"均勻權重: {clf_uniform.score(X_test, y_test):.2%}")
print(f"距離加權: {clf_distance.score(X_test, y_test):.2%}")
```

## 決策邊界視覺化

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_knn_boundary(X, y, k):
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X, y)

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
    plt.title(f'KNN Decision Boundary (K={k})')
    plt.show()

X, y = make_classification(n_samples=200, n_features=2, n_redundant=0,
                           n_informative=2, random_state=42)

for k in [1, 5, 15]:
    plot_knn_boundary(X, y, k)
```

## KNN 的優缺點

優點：
- 簡單直觀
- 無需訓練時間
- 適合多分類問題

缺點：
- 預測時間複雜度高 O(n)
- 對特徵尺度敏感
- 需要選擇合適的 K 值

## 參考資源

- https://www.google.com/search?q=KNN+K+nearest+neighbors+Python+implementation+2019
- https://www.google.com/search?q=scikit-learn+KNeighborsClassifier+tutorial+2019
- https://www.google.com/search?q=KNN+decision+boundary+visualization+Python+2019