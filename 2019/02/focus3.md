# 3. 非監督式學習

## 非監督式學習概念

非監督式學習使用沒有標籤的資料，目標是發現資料中的模式與結構。系統需要自行找出資料的內在規律。

## 聚類（Clustering）

聚類將相似的資料點分組到同一集群。

### K-means 聚類

K-means 是最廣泛使用的聚類演算法，將資料劃分為 K 個集群。

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

X, true_labels = make_blobs(n_samples=300, centers=4,
                            cluster_std=0.6, random_state=42)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)

print(f"集群中心:\n{kmeans.cluster_centers_}")
print(f"前10個標籤: {labels[:10]}")
```

### 層級聚類（Hierarchical Clustering）

```python
from sklearn.cluster import AgglomerativeClustering

hierarchical = AgglomerativeClustering(n_clusters=4)
labels = hierarchical.fit_predict(X)

print(f"層級聚類結果: {np.unique(labels)}")
```

### DBSCAN

DBSCAN 基於密度進行聚類，能發現任意形狀的集群。

```python
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X)

print(f"DBSCAN 標籤: {np.unique(labels)}")
print(f"噪聲點數量: {np.sum(labels == -1)}")
```

## 降維（Dimensionality Reduction）

降維減少特徵數量，同時保留重要資訊。

### PCA（Principal Component Analysis）

PCA 將高維資料投影到低維空間，保留最大變異。

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print(f"原始維度: {X.shape}")
print(f"降維後: {X_reduced.shape}")
print(f"解釋變異比例: {pca.explained_variance_ratio_}")
print(f"累計解釋變異: {sum(pca.explained_variance_ratio_):.2%}")
```

### t-SNE

t-SNE 專注於保持局部結構，適合視覺化。

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42)
X_embedded = tsne.fit_transform(X)

print(f"t-SNE 嵌入維度: {X_embedded.shape}")
```

## 異常偵測（Anomaly Detection）

使用孤立森林（Isolation Forest）偵測異常點。

```python
from sklearn.ensemble import IsolationForest

X_outliers = np.random.randn(20, 2) + np.array([10, 10])
X_normal = np.random.randn(100, 2)
X = np.vstack([X_normal, X_outliers])

iso_forest = IsolationForest(contamination=0.1, random_state=42)
predictions = iso_forest.fit_predict(X)

print(f"異常點數量: {np.sum(predictions == -1)}")
```

## 關聯規則學習

發現資料中的關聯模式。

```python
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

transactions = [
    ['牛奶', '麵包', '雞蛋'],
    ['麵包', '奶油'],
    ['牛奶', '麵包', '奶油', '雞蛋'],
    ['麵包', '雞蛋']
]

te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_array, columns=te.columns_)

frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True)
print(frequent_itemsets)
```

## 選擇聚類數量的方法

### 肘部法則（Elbow Method）

```python
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

print(f"Inertias: {inertias}")
```

## 參考資源

- https://www.google.com/search?q=unsupervised+learning+clustering+K-means+Python+2019
- https://www.google.com/search?q=PCA+t-SNE+dimensionality+reduction+Python+scikit-learn+2019
- https://www.google.com/search?q=anomaly+detection+isolation+forest+Python+2019