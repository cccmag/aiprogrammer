# 文章 5：資料結構與演算法

## 前言

良好的資料結構與演算法知識是高效程式設計的基礎。本章節介紹幾種重要的資料結構。

## 陣列（Array）

```python
# Python list 可作為簡單陣列
arr = [1, 2, 3, 4, 5]
print(arr[0])     # 讀取：O(1)
arr[2] = 10       # 寫入：O(1)
arr.append(6)     # 新增：O(1) 均攤
```

## 堆疊（Stack）

```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

stack = Stack()
stack.push(1)
stack.push(2)
print(stack.pop())  # 2
```

## 佇列（Queue）

```python
from collections import deque

queue = deque()
queue.append(1)
queue.append(2)
print(queue.popleft())  # 1
```

## 鏈表（Linked List）

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def find(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
```

## 雜湊表（Hash Table）

```python
# Python dict 是雜湊表實現
hash_table = {}

hash_table['name'] = 'Alice'
hash_table['age'] = 25

print(hash_table['name'])  # Alice
print('name' in hash_table)  # True
```

## 二元樹（Binary Tree）

```python
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

# 中序走訪
def inorder(node):
    if node:
        inorder(node.left)
        print(node.data)
        inorder(node.right)
```

## 圖（Graph）

```python
class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_edge(self, u, v):
        if u not in self.adjacency:
            self.adjacency[u] = []
        self.adjacency[u].append(v)

    def bfs(self, start):
        visited = set()
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node not in visited:
                print(node)
                visited.add(node)
                queue.extend(self.adjacency.get(node, []))
```

## 總結

不同的資料結構適用於不同的場景。選擇適當的資料結構能大幅提升程式效率。

## 延伸閱讀

- https://www.google.com/search?q=data+structures+algorithms+Python
- https://www.google.com/search?q=stack+queue+linked+list+python