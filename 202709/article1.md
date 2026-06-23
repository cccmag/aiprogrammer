# 從零實作向量索引：IVF vs HNSW

## 1. 為什麼需要近似最近鄰搜尋？

當向量資料量達到數百萬甚至數十億時，暴力搜尋（對所有向量計算相似度）變得不可行。假設你有 1000 萬個 768 維向量，每次搜尋需要計算 1000 萬次餘弦相似度——在單機上可能需要數秒，完全無法滿足即時應用的需求。

**近似最近鄰搜尋**（Approximate Nearest Neighbor, ANN）正是為解決這個問題而生。它犧牲少量準確率，換取數百倍的速度提升。本文將從零實作兩種經典的 ANN 演算法：IVF 和 HNSW。

## 2. IVF：倒排檔案索引

IVF（Inverted File Index）是最直觀的 ANN 方法。核心思想是將向量空間劃分為多個區域，搜尋時只檢查 query 附近區域的向量。

### 實作步驟

1. **訓練叢集**：用 K-means 將資料向量分為 N 個叢集
2. **建立倒排列表**：將每個向量分配到最近的叢集中心
3. **搜尋**：計算 query 與所有叢集中心的距離，選擇最近的數個叢集，只在這些叢集中搜尋

```python
import numpy as np
from sklearn.cluster import KMeans

class IVFIndex:
    def __init__(self, n_clusters=10, nprobe=3):
        self.n_clusters = n_clusters
        self.nprobe = nprobe
        self.kmeans = KMeans(n_clusters=n_clusters)
        self.inverted_lists = {i: [] for i in range(n_clusters)}

    def train(self, vectors):
        self.kmeans.fit(vectors)
        self.centroids = self.kmeans.cluster_centers_

    def add(self, vectors, ids):
        labels = self.kmeans.predict(vectors)
        for vec, label, vid in zip(vectors, labels, ids):
            self.inverted_lists[label].append((vid, vec))

    def search(self, query, k=5):
        dists = np.linalg.norm(self.centroids - query, axis=1)
        probe_ids = np.argsort(dists)[:self.nprobe]
        candidates = []
        for pid in probe_ids:
            candidates.extend(self.inverted_lists[pid])
        scores = [(vid, float(np.dot(query, vec)))
                  for vid, vec in candidates]
        scores.sort(key=lambda x: -x[1])
        return scores[:k]
```

IVF 的關鍵參數是 `nprobe`（探測叢集數）。`nprobe` 越大，召回率越高但速度越慢。Faiss 提供了高效的 GPU 加速 IVF 實作。

## 3. HNSW：分層可導航小世界圖

HNSW（Hierarchical Navigable Small World）是目前公認最佳的 ANN 演算法之一，被 Pinecone、Weaviate、Qdrant 等主流向量資料庫採用。其核心是建構多層圖結構：

- **底層**（Layer 0）：包含所有向量
- **上層**（Layer 1, 2, ...）：逐層減少節點數（通常以指數衰減）
- 搜尋時從最高層開始，利用「長跳躍」快速接近目標區域，再到底層進行精細搜尋

```python
import numpy as np
from heapq import heappush, heappop

class HNSWIndex:
    def __init__(self, m=16, ef_construction=200, ml=1.0):
        self.m = m
        self.ef_construction = ef_construction
        self.ml = ml
        self.layers = [[]]
        self.vectors = []
        self.ids = []

    def _random_level(self):
        return int(-np.log(np.random.random()) * self.ml)

    def add(self, vec, vid):
        level = self._random_level()
        while len(self.layers) <= level:
            self.layers.append([])
        self.vectors.append(vec)
        self.ids.append(vid)
        idx = len(self.vectors) - 1
        for lc in range(level, -1, -1):
            self._insert_at_layer(idx, lc)

    def _insert_at_layer(self, idx, lc):
        vec = self.vectors[idx]
        neighbors = self._search_layer(vec, self.ef_construction, lc)
        self.layers[lc].append((idx, neighbors[:self.m]))

    def _search_layer(self, query, ef, lc):
        candidates = [(np.linalg.norm(self.vectors[0] - query), 0)]
        result = []
        visited = {0}
        while candidates:
            dist, cur = heappop(candidates)
            for nb, _ in self.layers[lc]:
                if nb not in visited:
                    visited.add(nb)
                    d = np.linalg.norm(self.vectors[nb] - query)
                    heappush(candidates, (d, nb))
                    heappush(result, (-d, nb))
                    if len(result) > ef:
                        heappop(result)
        return [idx for _, idx in result]

    def search(self, query, k=10, ef=None):
        if ef is None:
            ef = k
        cur = 0
        for lc in range(len(self.layers) - 1, 0, -1):
            self._search_layer(query, 1, lc)
        result = self._search_layer(query, max(ef, k), 0)
        return [(self.ids[idx], float(np.dot(self.vectors[idx], query)))
                for _, idx in result[:k]]
```

## 4. IVF vs HNSW 比較

| 特性 | IVF | HNSW |
|------|-----|------|
| 建索引速度 | 快（O(N)） | 慢（O(N log N)） |
| 搜尋速度 | 中等 | 極快 |
| 召回率（Recall@10） | ~85-93% | ~95-99% |
| 記憶體使用 | 低 | 較高（儲存圖結構） |
| 增量插入 | 需重新訓練 | 支援增量 |
| 參數數量 | 少（nlist, nprobe） | 多（m, ef, ef_construction） |

## 5. 實戰建議

- **小於 10 萬筆**：暴力搜尋即可
- **10 萬到 1000 萬筆**：IVF 是成本和效能的平衡點
- **大於 1000 萬筆**：HNSW 或結合 PQ（乘積量化）壓縮向量

Faiss 和 hnswlib 提供了生產級實作，但理解底層原理對除錯和調參至關重要。建議先用本文的 Python 實作理解核心概念，再切換到工業級函式庫。

## 參考資料

- [Faiss 文件](https://www.google.com/search?q=faiss+ivf+index+parameters)
- [HNSW 演算法原始論文](https://www.google.com/search?q=HNSW+algorithm+paper+2016)
- [ANN 演算法基準測試](https://www.google.com/search?q=ann+benchmarks+github)
