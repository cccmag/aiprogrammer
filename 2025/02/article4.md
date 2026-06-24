# 佇列實作與 BFS

## 佇列的定義

佇列（Queue）是一種遵循先進先出（FIFO）原則的線性資料結構。元素從後端（rear）加入，從前端（front）移除。

## Python 實作佇列

### 使用 list 實作（不推薦）

```python
class QueueList:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.pop(0)  # O(n)
```

`pop(0)` 的時間複雜度是 O(n)，不適合大量資料。

### 使用 collections.deque 實作（推薦）

```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.popleft()  # O(1)

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
```

## BFS — 廣度優先搜尋

BFS（Breadth-First Search）是圖論中最基本的搜尋演算法之一，使用佇列來實現。

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            result.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return result

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
print(bfs(graph, 'A'))  # ['A', 'B', 'C', 'D', 'E', 'F']
```

## 佇列的實際應用

- 工作排程：作業系統的行程排程
- 訊息佇列：RabbitMQ、Redis 佇列
- 網路請求：Web 伺服器請求佇列
- 快取淘汰：FIFO 淘汰策略

## 參考資源

- https://www.google.com/search?q=BFS+breadth+first+search+Python
- https://www.google.com/search?q=Python+deque+queue+implementation

## 小結

佇列是 BFS 的核心資料結構，理解佇列的運作原理是學習圖論演算法的重要基石。使用 `deque` 能確保兩端操作皆為 O(1)。
