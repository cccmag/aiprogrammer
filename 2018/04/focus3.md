# 非監督式學習：分群與降維的經典演算法

## 前言

非監督式學習是機器學習的另一個重要分支。與監督式學習不同，非監督式學習處理的資料沒有標籤，演算法需要自己從資料中發現結構和模式。

## 非監督式學習的兩大類型

### 1. 分群（Clustering）

將相似的資料點歸為同一群（cluster），不同群之間的差異越大越好。

### 2. 降維（Dimensionality Reduction）

將高維度資料映射到低維度空間，同時保留重要的結構資訊。

```
┌─────────────────────────────────────────────────────┐
│                 非監督式學習的兩大類型                │
├─────────────────────────────────────────────────────┤
│                                                     │
│   分群：將資料點分組                                  │
│   ┌─────────────────────────────────┐             │
│   │  ● ● ●    ○ ○ ○                 │             │
│   │  ● ● ●    ○ ○ ○                 │             │
│   │      ▲ 不同群組                  │             │
│   └─────────────────────────────────┘             │
│                                                     │
│   降維：減少特徵維度                                  │
│   ┌─────────────────────────────────┐             │
│   │  3D ──────► 2D                  │             │
│   │  (x,y,z)    (x,y)              │             │
│   └─────────────────────────────────┘             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## K-means 分群

### 演算法步驟

1. 隨機選擇 K 個初始質心（Centroids）
2. 將每個資料點分配給最近的質心
3. 根據分配結果重新計算質心
4. 重複步驟 2-3 直到收斂

### Python 實作

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# 生成範例資料
X, _ = make_blobs(n_samples=300, centers=4,
                  cluster_std=0.6, random_state=42)

# K-means 分群
kmeans = KMeans(n_clusters=4, random_state=42)
labels = kmeans.fit_predict(X)

# 視覺化
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            c='red', marker='X', s=200)
plt.show()
```

### K-means 的挑戰

- 需要預先指定 K 值
- 對初始質心敏感
- 適合球狀分群，對非凸形分群效果不佳

## 階層分群（Hierarchical Clustering）

### 自下而上（Agglomerative）

1. 將每個點視為一個集群
2. 貪心地合併最相似的兩個集群
3. 重複直到只剩一個集群

### 距離度量

- 單一連結（Single Linkage）：集群間最近點的距離
- 完全連結（Complete Linkage）：集群間最遠點的距離
- 平均連結（Average Linkage）：集群間所有點對的平均距離

### 樹狀圖（Dendrogram）

階層分群的結果可以用樹狀圖表示，幫助選擇適當的集群數量。

## DBSCAN

DBSCAN（Density-Based Spatial Clustering of Applications with Noise）是一種基於密度的分群演算法。

### 特點

- 不需要預先指定集群數量
- 能識別異常點（噪聲）
- 能處理任意形狀的集群

### 參數

- ε（eps）：鄰域半徑
- MinPts：核心點所需的最小鄰域點數

```
┌─────────────────────────────────────────────────────┐
│                   DBSCAN 示意                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ● ● ●                                             │
│   ● ● ● ● ●   ← 核心點                              │
│     ● ● ● ● ● ●                                     │
│         ● ● ● ● ← 邊界點                            │
│                       ◆ ← 異常點                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 主成分分析（PCA）

PCA 是最常用的降維技術之一。它找到資料變異最大的方向，將資料投影到這些方向上。

### 數學原理

1. 計算資料的共變異數矩陣
2. 計算共變異數矩陣的特徵值和特徵向量
3. 選擇前 K 個最大的特徵值對應的特徵向量
4. 將資料投影到這些特徵向量構成的空間

### Python 實作

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# 載入資料
iris = load_iris()
X = iris.data

# PCA 降維到 2D
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print(f'解釋的變異量比例: {pca.explained_variance_ratio_}')
# 輸出大約是 [0.92, 0.05]，表示前兩個主成分
# 解釋了 97% 的變異量
```

## t-SNE

t-SNE（t-Distributed Stochastic Neighbor Embedding）是一種非線性降維技術，特別適合於視覺化高維度資料。

### 特點

- 保留局部結構
- 適合將高維度資料降到 2-3 維進行視覺化
- 計算代價較高

### 與 PCA 的比較

| 特性 | PCA | t-SNE |
|------|-----|-------|
| 線性/非線性 | 線性 | 非線性 |
| 速度 | 快 | 慢 |
| 保留結構 | 全域 | 局部 |
| 用途 | 壓縮、降維 | 視覺化 |

## 分群演算法的選擇

| 演算法 | 優點 | 缺點 | 適用場景 |
|--------|------|------|----------|
| K-means | 簡單、快速 | 需要指定 K、對初始值敏感 | 球狀分群、大資料集 |
| 階層分群 | 不需指定 K、可視化 | 計算複雜度 O(n²) | 小資料集、需要層次結構 |
| DBSCAN | 不需指定 K、能處理噪聲 | 對參數敏感 | 任意形狀、異常偵測 |
| PCA | 快速、可解釋 | 只能做線性降維 | 資料壓縮、特徵選擇 |

## 實作：客戶分群

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 假設這是客戶資料
data = pd.read_csv('customer_data.csv')
features = ['年齡', '年收入', '消費頻率', '平均消費金額']

X = data[features].values

# 標準化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 使用肘部法則找最佳 K 值
inertias = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# 繪製肘部圖
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of clusters (K)')
plt.ylabel('Inertia')
plt.show()
```

## 結語

非監督式學習讓我們能夠在沒有標籤的情況下探索資料的結構。分群幫助我們發現資料中的自然分組，降維幫助我們在保留重要資訊的前提下簡化資料。

下一篇文章將介紹機器學習中非常重要的概念——訓練與測試，包括過擬合、正則化和交叉驗證等技術。

---

## 延伸閱讀

- [K-means 分群演算法](https://www.google.com/search?q=K-means+clustering+algorithm)
- [PCA 主成分分析詳解](https://www.google.com/search?q=PCA+principal+component+analysis)
- [t-SNE 視覺化技術](https://www.google.com/search?q=t-SNE+visualization+tutorial)

---

*本篇文章為「AI 程式人雜誌 2018 年 4 月號」機器學習基礎系列之一。*