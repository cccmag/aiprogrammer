# 拓撲排序

## 什麼是拓撲排序？

拓撲排序（Topological Sort）是對有向無環圖（DAG, Directed Acyclic Graph）的頂點進行線性排序，使得對於每一條有向邊 u→v，頂點 u 都排在 v 之前。簡單來說，就是將圖中的頂點按照依賴關係排列。如果圖中存在環，則無法進行拓撲排序，因此拓撲排序也可以用來檢測圖是否為 DAG。

## Kahn 演算法

Kahn 演算法基於 BFS 思想，利用入度（indegree）來實作。入度是指向該頂點的邊的數量。入度為 0 的頂點表示沒有依賴的先行任務。

**步驟**：
1. 計算每個頂點的入度。
2. 將所有入度為 0 的頂點加入佇列。
3. 從佇列取出一個頂點，加入結果列表。
4. 將該頂點的所有鄰居入度減 1（因為依賴已滿足）。
5. 若鄰居入度變為 0，則加入佇列。
6. 重複直到佇列為空。

若結果中頂點數量少於總數，表示圖中有環：

```python
def topological_sort_kahn(graph):
    indegree = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1
    queue = [v for v in graph if indegree[v] == 0]
    result = []
    while queue:
        u = queue.pop(0)
        result.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return result if len(result) == len(graph) else None
```

## DFS 實作法

也可以使用 DFS 搭配後序走訪來實作：對每個未訪問的節點執行 DFS，在遞迴返回時將節點加入結果，最後反轉結果即可。這種方法也需要能夠檢測環。

## 應用場景

1. **課程安排**：根據先修課程關係排定修課順序。
2. **編譯器**：決定原始碼檔案的編譯依賴順序。
3. **工作排程**：根據任務依賴關係決定執行順序。
4. **套件管理**：決定套件的安裝與更新順序。

## 延伸閱讀

- https://www.google.com/search?q=topological+sort+Kahn+algorithm+BFS+indegree+loop+detection
- https://www.google.com/search?q=topological+sort+DFS+postorder+approach+reverse+order
- https://www.google.com/search?q=拓撲排序+DAG+檢測+Kahn+DFS+應用場景+範例
