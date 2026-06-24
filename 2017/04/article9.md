# 文章 9：非監督式學習

## 前言

非監督式學習從無標籤數據中發現結構。本章節介紹聚類與降維兩大核心任務。

## 聚類（Clustering）

將相似樣本分組的任務。

### K-Means

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# 查看聚類中心
centers = kmeans.cluster_centers_
```

演算法步驟：
1. 隨機選擇 K 個中心
2. 將每個樣本分配到最近的中心
3. 更新中心為該簇的平均值
4. 重複直到收斂

### 階層式聚類（Hierarchical Clustering）

```python
from sklearn.cluster import AgglomerativeClustering

hc = AgglomerativeClustering(n_clusters=3)
clusters = hc.fit_predict(X)
```

### DBSCAN

基於密度的聚類，能發現任意形狀的簇：

```python
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X)
```

## 降維（Dimensionality Reduction）

減少特徵維度，同時保留重要資訊。

### PCA（主成分分析）

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# 查看解釋的變異量
print(pca.explained_variance_ratio_)
```

原理：找到方差最大的正交軸（主成分）。

### t-SNE

非線性降維，擅長視覺化：

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30)
X_embedded = tsne.fit_transform(X)
```

## 異常偵測（Anomaly Detection）

識別偏離正常模式的樣本：

```python
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(contamination=0.1)
anomalies = iso_forest.fit_predict(X)
```

## 應用場景

- **市場細分**：根據購買行為對客戶分群
- **文件分類**：將相似文件聚類
- **影像壓縮**：使用 PCA 降維
- **異常偵測**：詐騙偵測、設備故障預測

## 總結

非監督式學習在沒有標籤的情況下發現數據結構。聚類與降維是探索性資料分析的重要工具。

## 延伸閱讀

- https://www.google.com/search?q=unsupervised+learning+clustering+降維
- https://www.google.com/search?q=K-means+PCA+t-SNE+explained