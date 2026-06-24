# PCA 降維

## PCA 概念

主成分分析（Principal Component Analysis, PCA）是一種常用的降維技術，透過線性變換將資料轉換到新的座標系統。

## PCA 原理

PCA 找到資料變異最大的方向（主成分），並將資料投影到這些主成分構成的子空間。

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print(f"原始維度: {X.shape}")
print(f"降維後: {X_reduced.shape}")
print(f"解釋變異比例: {pca.explained_variance_ratio_}")
print(f"累計解釋變異: {sum(pca.explained_variance_ratio_):.2%}")
```

## 可視化降維結果

```python
plt.figure(figsize=(10, 6))
colors = ['red', 'green', 'blue']
for i, color, label in zip(range(3), colors, iris.target_names):
    plt.scatter(X_reduced[y == i, 0], X_reduced[y == i, 1],
               c=color, label=label, alpha=0.6)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('PCA - Iris Dataset')
plt.legend()
plt.show()
```

## 完整 PCA 實作

```python
class PCA_from_scratch:
    def __init__(self, n_components=2):
        self.n_components = n_components
        self.components = None
        self.mean = None

    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

        cov = np.cov(X_centered, rowvar=False)

        eigenvalues, eigenvectors = np.linalg.eig(cov)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        self.components = eigenvectors[:self.n_components]

    def transform(self, X):
        X_centered = X - self.mean
        return np.dot(X_centered, self.components.T)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
```

## 使用自訂實作

```python
pca_custom = PCA_from_scratch(n_components=2)
X_custom = pca_custom.fit_transform(X)

print(f"自訂 PCA 結果形狀: {X_custom.shape}")
print(f"主成分方向:\n{pca_custom.components}")
```

## 維度數量選擇

### 解釋變異圖

```python
pca_full = PCA()
pca_full.fit(X)

cumulative_variance = np.cumsum(pca_full.explained_variance_ratio_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, 'bo-')
plt.axhline(y=0.95, color='r', linestyle='--', label='95% 變異')
plt.axhline(y=0.99, color='g', linestyle='--', label='99% 變異')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA - Explained Variance')
plt.legend()
plt.grid(True)
plt.show()

n_95 = np.argmax(cumulative_variance >= 0.95) + 1
n_99 = np.argmax(cumulative_variance >= 0.99) + 1
print(f"達到 95% 變異所需維度: {n_95}")
print(f"達到 99% 變異所需維度: {n_99}")
```

### 使用 n_components

```python
pca_95 = PCA(n_components=0.95)
X_95 = pca_95.fit_transform(X)
print(f"n_components=0.95: 維度={X_95.shape[1]}")

pca_99 = PCA(n_components=0.99)
X_99 = pca_99.fit_transform(X)
print(f"n_components=0.99: 維度={X_99.shape[1]}")
```

## PCA 在機器學習中的應用

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

clf = LogisticRegression(max_iter=200)
clf.fit(X_train_pca, y_train)
accuracy = clf.score(X_test_pca, y_test)

print(f"PCA + Logistic Regression 準確率: {accuracy:.2%}")
print(f"原始維度: {X_train.shape[1]}, 降維後: {X_train_pca.shape[1]}")
```

## 比較原始與降維效能

```python
clf_full = LogisticRegression(max_iter=200)
clf_full.fit(X_train, y_train)
accuracy_full = clf_full.score(X_test, y_test)

clf_pca = LogisticRegression(max_iter=200)
clf_pca.fit(X_train_pca, y_train)
accuracy_pca = clf_pca.score(X_test_pca, y_test)

print(f"原始資料準確率: {accuracy_full:.2%}")
print(f"PCA 降維後準確率: {accuracy_pca:.2%}")
```

## SVD 與 PCA 的關係

```python
from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=2)
X_svd = svd.fit_transform(X)

print(f"SVD 解釋變異比例: {svd.explained_variance_ratio_}")
print(f"SVD 與 PCA 結果相似: {np.allclose(X_reduced, X_svd, atol=1e-10)}")
```

## 參考資源

- https://www.google.com/search?q=PCA+principal+component+analysis+Python+tutorial+2019
- https://www.google.com/search?q=PCA+dimensionality+reduction+scikit-learn+2019
- https://www.google.com/search?q=PCA+explained+variance+selection+components+Python+2019