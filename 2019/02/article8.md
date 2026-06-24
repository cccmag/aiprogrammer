# K-means 聚類

## K-means 演算法原理

K-means 是一種無監督學習演算法，將資料劃分為 K 個集群，每個集群由其中心點（質心）代表。

## 演算法步驟

1. 隨機選擇 K 個質心
2. 將每個資料點分配給最近的質心
3. 更新質心為該集群所有點的平均值
4. 重複步驟 2-3 直到收斂

## 從零實作 K-means

```python
import numpy as np

class KMeans:
    def __init__(self, n_clusters=3, max_iter=300):
        self.k = n_clusters
        self.max_iter = max_iter
        self.centroids = None
        self.labels = None

    def fit(self, X):
        np.random.seed(42)
        idx = np.random.choice(len(X), self.k, replace=False)
        self.centroids = X[idx]

        for _ in range(self.max_iter):
            distances = self._compute_distances(X)
            self.labels = np.argmin(distances, axis=1)

            new_centroids = np.array([
                X[self.labels == i].mean(axis=0) for i in range(self.k)
            ])

            if np.allclose(self.centroids, new_centroids):
                break
            self.centroids = new_centroids

    def _compute_distances(self, X):
        distances = np.zeros((len(X), self.k))
        for i, centroid in enumerate(self.centroids):
            distances[:, i] = np.sqrt(np.sum((X - centroid)**2, axis=1))
        return distances

    def predict(self, X):
        distances = self._compute_distances(X)
        return np.argmin(distances, axis=1)
```

## 使用實作

```python
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.6, random_state=42)

kmeans = KMeans(n_clusters=4, max_iter=300)
kmeans.fit(X)

plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels, alpha=0.6)
plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1],
           c='red', marker='X', s=200, label='Centroids')
plt.title('K-means Clustering')
plt.legend()
plt.show()

print(f"集群中心:\n{kmeans.centroids}")
```

## 使用 scikit-learn

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.6, random_state=42)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)

print(f"集群標籤: {np.unique(labels)}")
print(f"集群中心:\n{kmeans.cluster_centers_}")
print(f"Inertia (集群內總距離): {kmeans.inertia_:.2f}")
```

## 選擇最佳 K 值

### 肘部法則（Elbow Method）

```python
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.grid(True)
plt.show()

print(f"Inertias: {[f'{i:.1f}' for i in inertias]}")
```

### 輪廓係數（Silhouette Score）

```python
from sklearn.metrics import silhouette_score

silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)
    print(f"K={k}: 輪廓係數={score:.3f}")

best_k = K_range[np.argmax(silhouette_scores)]
print(f"\n最佳 K 值: {best_k}")
```

## 初始質心敏感度

K-means 對初始質心選擇敏感，可能收斂到局部最佳解。

```python
for i in range(3):
    kmeans = KMeans(n_clusters=4, n_init=1, init='random', random_state=i*10)
    kmeans.fit(X)
    print(f"Run {i+1}: Inertia={kmeans.inertia_:.2f}")

kmeans_best = KMeans(n_clusters=4, n_init=10, random_state=42)
kmeans_best.fit(X)
print(f"\nBest (n_init=10): Inertia={kmeans_best.inertia_:.2f}")
```

## K-means++ 初始化

K-means++ 使用更聰明的初始化策略，提高收斂到全局最佳解的機率。

```python
kmeans_pp = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
kmeans_pp.fit(X)
print(f"K-means++ Inertia: {kmeans_pp.inertia_:.2f}")
```

## K-means 限制

- 需要預先指定 K 值
- 假設集群為球形且大小相似
- 對異常值敏感
- 可能收斂到局部最佳

## 參考資源

- https://www.google.com/search?q=K-means+clustering+Python+implementation+2019
- https://www.google.com/search?q=scikit-learn+KMeans+elbow+method+silhouette+2019
- https://www.google.com/search?q=K-means+initialization+random+k-means++2019