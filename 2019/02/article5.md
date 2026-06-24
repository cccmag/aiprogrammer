# 邏輯斯迴歸

## 邏輯斯迴歸概念

邏輯斯迴歸雖然名稱有「迴歸」，但實際上是用於分類問題的演算法，特別是二分類問題。

## Sigmoid 函數

```python
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

z = np.linspace(-10, 10, 100)
s = sigmoid(z)

plt.figure(figsize=(10, 6))
plt.plot(z, s)
plt.title('Sigmoid Function')
plt.xlabel('z')
plt.ylabel('sigmoid(z)')
plt.grid(True)
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5)
plt.axvline(x=0, color='r', linestyle='--', alpha=0.5)
plt.show()
```

## 從零實作邏輯斯迴歸

```python
class LogisticRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iterations):
            linear = np.dot(X, self.weights) + self.bias
            h = self.sigmoid(linear)

            dw = (1/n_samples) * np.dot(X.T, (h - y))
            db = (1/n_samples) * np.sum(h - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        linear = np.dot(X, self.weights) + self.bias
        return self.sigmoid(linear)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)
```

## 使用實作

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=100, n_features=2, n_redundant=0,
                           n_informative=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression(learning_rate=0.1, n_iterations=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = (y_pred == y_test).mean()
print(f"準確率: {accuracy:.2%}")
```

## 使用 scikit-learn

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

iris = load_iris()
X = iris.data[:, :2]
y = (iris.target != 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = LogisticRegression(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"準確率: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred, target_names=['class 0', 'class 1']))
```

## 多分類問題

### One-vs-Rest (OvR)

```python
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target

clf = LogisticRegression(max_iter=200, multi_class='ovr')
clf.fit(X, y)
print(f"訓練集分數: {clf.score(X, y):.2%}")
```

### Multinomial

```python
clf_multi = LogisticRegression(max_iter=200, multi_class='multinomial')
clf_multi.fit(X, y)
print(f"訓練集分數 (multinomial): {clf_multi.score(X, y):.2%}")
```

## 正規化

```python
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

for C in [0.01, 0.1, 1, 10]:
    clf = LogisticRegression(C=C, max_iter=200)
    clf.fit(X_train, y_train)
    print(f"C={C}: 訓練分數={clf.score(X_train, y_train):.2%}, 測試分數={clf.score(X_test, y_test):.2%}")
```

## 決策邊界視覺化

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_decision_boundary(X, y, model):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))

    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(10, 6))
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Decision Boundary')
    plt.show()

X, y = make_classification(n_samples=200, n_features=2, n_redundant=0,
                           n_informative=2, random_state=42)
clf = LogisticRegression()
clf.fit(X, y)
plot_decision_boundary(X, y, clf)
```

## 參考資源

- https://www.google.com/search?q=logistic+regression+Python+implementation+sigmoid+2019
- https://www.google.com/search?q=scikit-learn+logistic+regression+multiclass+2019
- https://www.google.com/search?q=logistic+regression+decision+boundary+visualization+Python+2019