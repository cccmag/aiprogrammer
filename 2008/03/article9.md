# 集群分析

## 前言

集群分析（Clustering）是將資料分組的過程，使得同一組內的資料點相似，而不同組之間差異較大。這是無監督學習的主要任務之一。

## 集群的基礎概念

### 什麼是集群？

```python
clustering_definition = {
    "定義": "將資料集划分为多个群组（clusters）",
    "同一群組": "資料點彼此相似",
    "不同群組": "資料點彼此不相似",
    "無標籤": "不需要訓練資料的標籤"
}
```

### 與分類的對比

```python
# 分類（監督式學習）
classification = {
    "輸入": "特徵 + 標籤（訓練資料）",
    "輸出": "類別預測",
    "學習": "找到特徵到標籤的映射"
}

# 集群（無監督式學習）
clustering = {
    "輸入": "只有特徵，無標籤",
    "輸出": "每個資料點的群組歸屬",
    "學習": "發現資料的內在結構"
}
```

## 相似度度量

### 常用距離

```python
# 歐氏距離
def euclidean_distance(x, y):
    return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))

# 曼哈頓距離
def manhattan_distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))

# 餘弦相似度
from math import sqrt

def cosine_similarity(x, y):
    dot_product = sum(a * b for a, b in zip(x, y))
    norm_x = sqrt(sum(a ** 2 for a in x))
    norm_y = sqrt(sum(b ** 2 for b in y))
    return dot_product / (norm_x * norm_y)
```

## K-Means 集群

### 演算法

```python
kmeans_algorithm = {
    "步驟1": "隨機選擇 K 個中心點",
    "步驟2": "將每個資料點分配到最近的中心",
    "步驟3": "重新計算每個群組的中心",
    "步驟4": "重複步驟 2-3 直到收斂"
}
```

### 實現

```python
def kmeans(X, K, max_iterations=100):
    # 步驟 1：隨機選擇 K 個中心
    centroids = X[:K]

    for _ in range(max_iterations):
        # 步驟 2：分配每個點到最近的中心
        clusters = [[] for _ in range(K)]
        for x in X:
            distances = [euclidean_distance(x, c) for c in centroids]
            nearest = distances.index(min(distances))
            clusters[nearest].append(x)

        # 步驟 3：重新計算中心
        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_centroid = [sum(feature) / len(feature)
                               for feature in zip(*cluster)]
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(centroids[len(new_centroids)])

        # 檢查收斂
        if new_centroids == centroids:
            break

        centroids = new_centroids

    return clusters, centroids
```

### 選擇 K 值

```python
# 手肘法（Elbow Method）

def elbow_method(X, max_k=10):
    """評估不同 K 值的集群品質"""
    results = []

    for k in range(1, max_k + 1):
        clusters, centroids = kmeans(X, k)
        # 計算總群內平方和
        wcss = sum(
            euclidean_distance(x, c) ** 2
            for cluster, c in zip(clusters, centroids)
            for x in cluster
        )
        results.append((k, wcss))

    return results
```

## 階層式集群

### 兩種方法

```python
hierarchical_methods = {
    "凝聚式（Agglomerative）": "由下而上，先每點為一群，逐漸合併",
    "分裂式（Divisive）": "由上而下，先全部為一群，逐漸分裂"
}
```

### 凝聚式集群

```python
def agglomerative_clustering(X, k):
    """凝聚式階層集群"""
    # 初始：每個點都是一個群
    clusters = [[i] for i in range(len(X))]

    while len(clusters) > k:
        # 找到最相似的兩個群
        min_dist = float('inf')
        to_merge = (0, 1)

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = average_linkage(X, clusters[i], clusters[j])
                if dist < min_dist:
                    min_dist = dist
                    to_merge = (i, j)

        # 合併
        i, j = to_merge
        clusters[i].extend(clusters[j])
        del clusters[j]

    return clusters

def average_linkage(X, cluster1, cluster2):
    """平均連接法：兩個群之間的平均距離"""
    distances = []
    for i in cluster1:
        for j in cluster2:
            distances.append(euclidean_distance(X[i], X[j]))
    return sum(distances) / len(distances)
```

## DBSCAN

### 密度基礎集群

```python
dbscan_algorithm = {
    "概念": "基於密度的集群",
    "優點": "可以發現任意形狀的群",
    "優點": "可以識別雜訊點",
    "缺點": "對參數敏感"
}
```

### DBSCAN 實現

```python
def dbscan(X, eps, min_samples):
    """DBSCAN 演算法"""
    labels = [-1] * len(X)  # -1 表示未分類
    cluster_id = 0

    for i in range(len(X)):
        if labels[i] != -1:
            continue

        # 找到 eps 範圍內的所有點
        neighbors = region_query(X, i, eps)

        if len(neighbors) < min_samples:
            labels[i] = -1  # 標記為雜訊
        else:
            # 擴展群
            labels[i] = cluster_id
            grow_cluster(X, labels, i, neighbors, eps, min_samples, cluster_id)
            cluster_id += 1

    return labels

def region_query(X, i, eps):
    """找到點 i eps 範圍內的所有點"""
    return [j for j in range(len(X))
            if euclidean_distance(X[i], X[j]) <= eps]

def grow_cluster(X, labels, i, neighbors, eps, min_samples, cluster_id):
    """遞迴擴展群"""
    for j in neighbors:
        if labels[j] == -1:
            labels[j] = cluster_id
            new_neighbors = region_query(X, j, eps)
            if len(new_neighbors) >= min_samples:
                neighbors.extend(new_neighbors)
        elif labels[j] == -1:
            labels[j] = cluster_id
```

## 集群評估

### 內部指標

```python
# 群內距離（越小越好）
def intra_cluster_distance(X, labels, centroids):
    total = 0
    for i, label in enumerate(labels):
        total += euclidean_distance(X[i], centroids[label])
    return total / len(X)

# 群間距離（越大越好）
def inter_cluster_distance(centroids):
    total = 0
    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            total += euclidean_distance(centroids[i], centroids[j])
    return total / (len(centroids) * (len(centroids) - 1) / 2)
```

### 輪廓係數

```python
def silhouette_score(X, labels):
    """輪廓係數：-1 到 1 之間，越高越好"""
    from math import sqrt

    scores = []
    for i, label in enumerate(labels):
        # a: 同群其他點的平均距離
        same_cluster = [j for j, l in enumerate(labels) if l == label and j != i]
        if not same_cluster:
            a = 0
        else:
            a = sum(euclidean_distance(X[i], X[j]) for j in same_cluster) / len(same_cluster)

        # b: 最近的其他群的平均距離
        other_labels = set(labels) - {label}
        b = float('inf')
        for other_label in other_labels:
            other_points = [j for j, l in enumerate(labels) if l == other_label]
            if other_points:
                dist = sum(euclidean_distance(X[i], X[j]) for j in other_points) / len(other_points)
                b = min(b, dist)

        if max(a, b) > 0:
            scores.append((b - a) / max(a, b))

    return sum(scores) / len(scores) if scores else 0
```

## 應用場景

```python
clustering_applications = {
    "客戶分群": "根據購買行為分群",
    "影像壓縮": "色彩量化",
    "文件分類": "主題分組",
    "異常偵測": "識別與主流不同的點",
    "推薦系統": "協同過濾"
}
```

---

**延伸閱讀**

- [Clustering+algorithms+machine+learning](https://www.google.com/search?q=clustering+algorithms+machine+learning)
- [K-means+clustering+tutorial](https://www.google.com/search?q=K-means+clustering+tutorial)
- [Hierarchical+clustering+python](https://www.google.com/search?q=hierarchical+clustering+python)