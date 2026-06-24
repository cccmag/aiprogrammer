# 最短路徑：Dijkstra 與 Bellman-Ford

## 最短路徑問題

最短路徑問題是在加權圖中尋找兩個頂點之間權重總和最小的路徑。根據圖的性質（是否有負權重邊、是否需要所有點對等）不同，適合使用的演算法也不同。這是最經典的圖論問題之一，應用範圍從 GPS 導航到網路路由無所不包。

## Dijkstra 演算法

Dijkstra 演算法解決單源最短路徑問題（Single-Source Shortest Path），適用於邊權重為非負數的圖。由 Edsger Dijkstra 在 1956 年提出。

**步驟**：
1. 初始化：起點距離為 0，其他頂點距離為無限大。
2. 使用最小堆積維護待處理頂點，以距離為優先權。
3. 每次取出距離最小的頂點 u，對每個鄰居 v 進行鬆弛操作。
4. 若新距離小於當前距離，則更新並加入堆積。
5. 重複直到堆積為空。

**時間複雜度**：O((V+E) log V)（使用最小堆積）。

**限制**：無法處理負權重邊。若圖中存在負權重，Dijkstra 會給出錯誤結果。

```python
def dijkstra(graph, start):
    dist = {v: float('inf') for v in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

## Bellman-Ford 演算法

Bellman-Ford 同樣解決單源最短路徑，由 Richard Bellman 與 Lester Ford 分別提出。它可以處理負權重邊，且能偵測負權重環。

**步驟**：
1. 初始化距離（起點 0，其他無限大）。
2. 對所有邊進行 V-1 次鬆弛操作。
3. 再進行一次鬆弛：若距離還能縮短，表示存在負權重環。

**時間複雜度**：O(VE)，比 Dijkstra 慢但功能更強大。

## 比較總結

| 特性 | Dijkstra | Bellman-Ford |
|------|----------|--------------|
| 負權重邊 | 不支援 | 支援 |
| 負環偵測 | 不支援 | 支援 |
| 時間複雜度 | O((V+E) log V) | O(VE) |
| 實作難度 | 較低 | 中等 |
| 適用場景 | 地理導航、網路路由 | 貨幣套利、通用情境 |

## 延伸閱讀

- https://www.google.com/search?q=Dijkstra+algorithm+shortest+path+heap+實作+Python
- https://www.google.com/search?q=Bellman+Ford+algorithm+negative+weight+cycle+detection
- https://www.google.com/search?q=最短路徑+Dijkstra+Bellman-Ford+SPFA+差異+應用場景
