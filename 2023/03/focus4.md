# 堆積與優先佇列

## 什麼是堆積？

堆積（Heap）是一種特殊的完全二元樹（Complete Binary Tree）。最大堆積（Max Heap）滿足每個節點的值都大於或等於其子節點的值；最小堆積（Min Heap）則相反。堆積通常用陣列實作，不需要額外的指標，記憶體效率極高。

使用 0-indexed 陣列時的位置關係：
- 節點 i 的左子節點：2i + 1
- 節點 i 的右子節點：2i + 2
- 節點 i 的父節點：(i - 1) / 2

## 堆積的基本操作

**插入（push）**：將新元素放在陣列末尾，向上調整（sift up），不斷與父節點比較交換直到滿足堆積性質。O(log n)。

**取出最大值/最小值（pop）**：根節點與最後元素交換，刪除最後元素，從根向下調整（sift down），與較大（最大堆積）或較小（最小堆積）的子節點交換。O(log n)。

**建立堆積（heapify）**：從最後一個非葉節點開始向下調整。時間 O(n)，比逐個插入的 O(n log n) 快。

## 優先佇列

優先佇列（Priority Queue）是一種 ADT，每個元素有優先權，高優先權者先取出。堆積是實作優先佇列最常用的方式。

Python 的 heapq 模組提供最小堆積實作：

```python
import heapq
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
print(heapq.heappop(heap))  # 1
arr = [5, 2, 8, 1, 9]
heapq.heapify(arr)
```

## 應用場景

1. **Dijkstra 最短路徑**：最小堆積取出距離最小節點。
2. **合併 k 個有序串列**：各串列首元素入堆，不斷取最小。
3. **Top K 問題**：大小 k 的最小堆積保留前 k 大元素。
4. **工作排程**：按優先權執行任務。
5. **中位數維護**：最大堆積 + 最小堆積動態維護中位數。

## 延伸閱讀

- https://www.google.com/search?q=heap+data+structure+array+representation+complete+binary+tree+操作
- https://www.google.com/search?q=priority+queue+heap+Python+heapq+module+tutorial+範例
- https://www.google.com/search?q=堆積+建立+heapify+時間複雜度+O+n+證明+推導
