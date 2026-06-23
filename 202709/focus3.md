# 近似最近鄰搜尋演算法（2011-2026）

## 精確 vs 近似：效能的取捨

### 暴力搜尋的問題

在高維空間中，精確最近鄰（KNN）的時間複雜度是 O(n × d)，其中 n 是向量數量，d 是維度。當 n = 1000 萬、d = 768 時，一次查詢需要數十億次浮點運算：

```python
def brute_force_knn(query, vectors, k=10):
    """暴力搜尋：精確但緩慢"""
    distances = []
    for vec in vectors:
        dist = np.linalg.norm(query - vec)
        distances.append(dist)
    indices = np.argsort(distances)[:k]
    return [(i, distances[i]) for i in indices]
```

這在大型資料集上完全不可行，因此需要 ANN（Approximate Nearest Neighbor）演算法。

### 三大主流 ANN 演算法

#### IVF（Inverted File Index）

IVF 將向量空間劃分為多個分區（Voronoi cells），查詢時只搜尋最近的分區：

```python
class IVFIndex:
    def __init__(self, nlist=100):
        self.cells = [[] for _ in range(nlist)]

    def train(self, vectors):
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=self.nlist).fit(vectors)
        self.centroids = kmeans.cluster_centers_
        for i, vec in enumerate(vectors):
            self.cells[kmeans.labels_[i]].append(vec)

    def search(self, query, nprobe=3, k=10):
        dists = np.linalg.norm(self.centroids - query, axis=1)
        nearest = np.argsort(dists)[:nprobe]
        candidates = sum((self.cells[i] for i in nearest), [])
        return brute_force_knn(query, candidates, k)
```

#### HNSW（Hierarchical Navigable Small World）

HNSW 是**多層圖**——上層快速導航，下層精細搜尋：

```python
class HNSWIndex:
    def __init__(self, M=16, ef=200):
        self.M, self.ef = M, ef
        self.graph = []

    def search(self, query, ef=50):
        entry = self._get_entry_point()
        for level in reversed(range(len(self.graph))):
            for nb in self.graph[level][entry]:
                if np.linalg.norm(self.vectors[nb] - query) < \
                   np.linalg.norm(self.vectors[entry] - query):
                    entry = nb
        return self._search_layer(query, entry, ef)
```

#### PQ（Product Quantization）

PQ 將高維向量壓縮為短碼，大幅減少記憶體用量。每個子向量用 codeword 索引代替：

```python
def product_quantize(vector, codebooks, m=8):
    dim = len(vector) // m
    return [np.argmin(np.linalg.norm(cb - vector[i*dim:(i+1)*dim], axis=1))
            for i, cb in enumerate(codebooks)]
```

### 準確率 vs 速度的權衡

| 演算法 | 準確率@10 | 查詢時間 | 記憶體 | 適合場景 |
|-------|-----------|----------|--------|----------|
| 暴力搜尋 | 100% | 1000ms | 最高 | 小資料集 |
| IVF | 85-95% | 10ms | 中 | 中型資料集 |
| HNSW | 95-99% | 1-5ms | 高 | 通用/即時 |
| PQ | 75-90% | 1ms | 極低 | 大規模/記憶體受限 |

### 2026 的趨勢

混合索引——在同一系統中同時使用 HNSW 和 PQ 的優點。HNSW 提供高召回率，PQ 壓縮降低記憶體，兩者結合可支援數十億級別的向量搜尋。

---

**下一步**：[向量資料庫架構](focus4.md)

## 延伸閱讀

- [HNSW 演算法詳細介紹](https://www.google.com/search?q=HNSW+approximate+nearest+neighbor+search)
- [IVF 與 Product Quantization](https://www.google.com/search?q=IVF+product+quantization+vector+search)
