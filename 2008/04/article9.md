# 資料探勘的經典演算法

## 資料探勘概述

資料探勘是從大量資料中發現隱藏模式和知識的過程。2008 年電子商務和 Web 2.0 的蓬勃發展，使資料探勘技術日益重要。

## 分類演算法

### 決策樹

```python
from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(criterion='gini', max_depth=5)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
```

### 決策樹生成

```python
def build_tree(X, y, depth=0, max_depth=5):
    # 終止條件
    if len(set(y)) == 1:
        return Node(label=y[0])
    if depth >= max_depth:
        return Node(label=most_common(y))

    # 選擇最佳分割
    best_feature, best_threshold = find_best_split(X, y)

    # 遞迴建立子樹
    left_mask = X[:, best_feature] <= best_threshold
    right_mask = ~left_mask

    return Node(
        feature=best_feature,
        threshold=best_threshold,
        left=build_tree(X[left_mask], y[left_mask], depth+1, max_depth),
        right=build_tree(X[right_mask], y[right_mask], depth+1, max_depth)
    )
```

### 隨機森林

```python
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=100, max_depth=10)
clf.fit(X_train, y_train)
```

## 集群演算法

### K-Means

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_
centers = kmeans.cluster_centers_
```

### K-Means 實現

```python
import numpy as np

def kmeans(X, k, max_iters=100):
    # 隨機選擇初始質心
    centroids = X[np.random.choice(len(X), k, replace=False)]

    for _ in range(max_iters):
        # 分配到最近的質心
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)

        # 更新質心
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])

        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids

    return centroids, labels
```

### 階層式集群

```python
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# 計算距離矩陣
Z = linkage(X, method='ward')

# 繪製樹狀圖
dendrogram(Z)

# 分割為 k 個集群
labels = fcluster(Z, k, criterion='maxclust')
```

## 關聯規則

### Apriori 演算法

```python
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

transactions = [
    ['牛奶', '麵包', '雞蛋'],
    ['麵包', '果醬'],
    ['牛奶', '麵包', '奶油'],
    ['雞蛋', '麵包'],
]

te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_array, columns=te.columns_)

frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True)
```

### 支援度與信賴度

```python
def support(itemset, transactions):
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)

def confidence(rule, transactions):
    support_X = support(rule['X'], transactions)
    support_XY = support(rule['X'] | rule['Y'], transactions)
    return support_XY / support_X
```

## 推薦系統

### 協同過濾

```python
from sklearn.metrics.pairwise import cosine_similarity

# 計算使用者相似度
user_similarity = cosine_similarity(user_item_matrix)

# 預測評分
def predict_rating(user_id, item_id, user_similarity, user_item_matrix):
    similar_users = user_similarity[user_id]
    ratings = user_item_matrix[:, item_id]

    # 加權平均
    mask = ratings > 0
    if not mask.any():
        return 0

    weighted_sum = (similar_users[mask] * ratings[mask]).sum()
    norm = np.abs(similar_users[mask]).sum()
    return weighted_sum / norm if norm > 0 else 0
```

## 異常檢測

### 基於分佈

```python
def detect_outliers_zscore(data, threshold=3):
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold
```

### 基於距離

```python
from sklearn.ensemble import IsolationForest

clf = IsolationForest(contamination=0.1, random_state=42)
outliers = clf.fit_predict(X)
```

## 降維

### PCA

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)
```

## 結論

資料探勘演算法為從巨量資料中提取知識提供了強大工具。不同的演算法適用於不同的問題，需要根據實際情況選擇。

---

**延伸閱讀**

- [機器學習的數學基礎](article8.md)
- [Data+mining+algorithms](https://www.google.com/search?q=data+mining+algorithms)