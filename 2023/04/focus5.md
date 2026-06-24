# 圖論演算法

## 圖的基本概念

圖（Graph）是一種抽象的資料結構，由**頂點（Vertex）**和**邊（Edge）**組成。圖論演算法是電腦科學中應用最廣泛的領域之一——從社交網路分析到導航系統，從網路路由到供應鏈優化，處處可見圖論的身影。

## 圖的表示方式

### 1. 鄰接矩陣（Adjacency Matrix）

使用 n×n 矩陣表示圖，matrix[i][j] = 1 表示存在從 i 到 j 的邊。

### 2. 鄰接串列（Adjacency List）

對每個頂點儲存一個相鄰頂點的列表，節省空間。

## 圖的遍歷

### 廣度優先搜尋（BFS）

BFS 使用佇列，從起點開始，逐層探索所有鄰居。用於最短路徑（權重相同時）、連通分量檢測等。

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                queue.append(neighbor)
    return visited
```

### 深度優先搜尋（DFS）

DFS 使用堆疊（或遞迴），深入探索一條路徑直到不能再走才回溯。

```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

## 最短路徑演算法

### Dijkstra 演算法

用於非負權重圖的單源最短路徑。使用優先佇列，每次選擇距離最近的未處理節點。

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distances[node]:
            continue
        for neighbor, weight in graph[node]:
            nd = dist + weight
            if nd < distances[neighbor]:
                distances[neighbor] = nd
                heapq.heappush(pq, (nd, neighbor))
    return distances
```

時間複雜度：O((V + E) log V) 使用二元堆積。

### Bellman-Ford 演算法

可以處理負權重邊，並檢測負環。時間複雜度 O(VE)。

## 最小生成樹

### Kruskal 演算法

基於邊的貪婪演算法，使用並查集檢測環。

### Prim 演算法

基於頂點的貪婪演算法，類似 Dijkstra。

## 最大流量：Ford-Fulkerson

### 問題定義

給定一個有向帶權圖，找到從源點（source）到匯點（sink）的最大流量，其中每條邊有容量限制。

### Ford-Fulkerson 核心思想

使用 BFS（稱為 Edmonds-Karp 演算法）在剩餘網路中找到增廣路徑，沿著路徑增加流量，直到無法再找到增廣路徑。

```python
def ford_fulkerson(graph, source, sink):
    n = len(graph)
    flow = [[0] * n for _ in range(n)]
    max_flow = 0
    while True:
        # BFS 找增廣路徑
        parent = [-1] * n
        queue = [source]
        parent[source] = source
        while queue and parent[sink] == -1:
            u = queue.pop(0)
            for v in range(n):
                if parent[v] == -1 and graph[u][v] - flow[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1:
            break
        # 計算路徑上的最小剩餘容量
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v] - flow[u][v])
            v = u
        # 更新流量
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
        max_flow += path_flow
    return max_flow
```

### 最小割定理

最大流量等於最小割容量。這是網路流理論中最漂亮的結果之一。

## 總結

圖論演算法是工程實踐中應用最廣泛的演算法類別之一。無論是最短路徑、最小生成樹還是最大流量，這些演算法都在現實系統中有著直接應用。

## 延伸閱讀

- [Graph Algorithms Overview](https://www.google.com/search?q=graph+algorithms+overview)
- [Dijkstra Algorithm](https://www.google.com/search?q=Dijkstra+algorithm)
- [Ford-Fulkerson Algorithm](https://www.google.com/search?q=Ford-Fulkerson+algorithm)
