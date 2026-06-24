# 最大流量：Ford-Fulkerson

## 網路流問題

網路流問題是圖論中的經典問題。想像一個自來水網路：水從水源（source）經過管線輸送到用戶端（sink），每條管線都有其最大容量。網路流問題要回答的是：從水源到用戶端最多能輸送多少水？

## Ford-Fulkerson 方法

Ford-Fulkerson 方法是解決最大流量問題的核心演算法。其思想極為優美：**只要能找到一條從源點到匯點還剩餘容量的路徑（增廣路徑），就沿著這條路徑增加流量。**

### 關鍵概念：剩餘網路

剩餘網路記錄每條邊上還有多少容量可以傳送。對於每條邊 (u, v)：
- 如果流量 f(u,v) < 容量 c(u,v)，則有正向剩餘容量 c(u,v) - f(u,v)
- 如果有流量 f(u,v) > 0，則有反向剩餘容量 f(u,v)（允許撤銷流量）

### 演算法步驟

1. 初始化所有邊的流量為 0
2. 在剩餘網路中用 BFS 找增廣路徑（從 source 到 sink）
3. 如果找不到，結束演算法
4. 計算路徑上的最小剩餘容量
5. 沿路徑增加流量
6. 回到步驟 2

### Python 實作

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
            break  # 沒有更多增廣路徑

        # 計算增廣路徑上的最小剩餘容量
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

### Edmonds-Karp 演算法

使用 BFS 找增廣路徑的 Ford-Fulkerson 變體稱為 Edmonds-Karp 演算法。BFS 保證找到最短路徑（以邊數計算），使得時間複雜度為 O(VE²)。

## 最小割定理

### 什麼是割？

將圖的頂點分為兩部分 S 和 T（source ∈ S, sink ∈ T），割的容量是從 S 到 T 的所有邊的容量總和。

### 最大流 = 最小割

**定理**：在任何網路中，最大流量的值等於最小割的容量。

這個定理是網路流理論的核心結果。它不僅提供了驗證最大流量正確性的方法，還有實際應用——尋找「瓶頸」所在。

### 如何找到最小割？

執行完 Ford-Fulkerson 後，從 source 出發，沿著剩餘容量大於 0 的邊可以到達的頂點集合就是 S。從 S 到 T 的所有邊即為最小割。

## 應用場景

### 二分圖匹配

最大匹配問題可以轉化為最大流問題。加入源點連接到左側頂點，右側頂點連接到匯點，所有邊容量為 1。

### 頂點容量

當頂點本身也有容量限制時，可以將頂點拆為兩個（入點和出點），中間用一條容量等於頂點容量的邊連接。

### 多源多匯

增加一個超級源點連接到所有源點，增加一個超級匯點讓所有匯點連接到它。

### 實際應用

- **交通運輸**：最大化公路網的車流量
- **通訊網路**：最大化資料傳輸速率
- **專案排程**：專案選擇問題（Profit Maximization）
- **圖像分割**：最小割用於圖像前景背景分離

## 完整範例

```python
graph = [
    [0, 16, 13, 0, 0, 0],  # 0: source
    [0, 0, 10, 12, 0, 0],  # 1
    [0, 4, 0, 0, 14, 0],   # 2
    [0, 0, 9, 0, 0, 20],   # 3
    [0, 0, 0, 7, 0, 4],    # 4
    [0, 0, 0, 0, 0, 0]     # 5: sink
]
max_flow = ford_fulkerson(graph, 0, 5)
print(f"最大流量: {max_flow}")  # 輸出 23
```

## 總結

Ford-Fulkerson 方法是網路流問題的基石。其核心思想「持續找增廣路徑」不僅簡單直覺，而且連接著最大流和最小割這兩個看似不同的概念。

## 延伸閱讀

- [Ford-Fulkerson Algorithm](https://www.google.com/search?q=Ford+Fulkerson+algorithm)
- [Max Flow Min Cut Theorem](https://www.google.com/search?q=max+flow+min+cut+theorem)
- [Edmonds-Karp Algorithm](https://www.google.com/search?q=Edmonds+Karp+algorithm)
