# 堆疊實作與應用

## 堆疊的定義

堆疊（Stack）是一種受限的線性資料結構，只允許在頂端進行插入（push）和刪除（pop）操作，遵循後進先出（LIFO）原則。

## Python 實作堆疊

### 使用 list 實作

```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        return None if self.is_empty() else self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
```

### 使用 collections.deque 實作

```python
from collections import deque

class StackDeque:
    def __init__(self):
        self.items = deque()

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
```

## 堆疊的應用

### 應用一：括號匹配

```python
def is_balanced(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack.pop() != pairs[ch]:
                return False
    return len(stack) == 0

print(is_balanced("()[]{}"))    # True
print(is_balanced("([)]"))      # False
```

### 應用二：逆波蘭表示法

```python
def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t in "+-*/":
            b, a = stack.pop(), stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            else: stack.append(a // b)
        else:
            stack.append(int(t))
    return stack.pop()

print(eval_rpn(["2", "1", "+", "3", "*"]))  # 9
```

### 應用三：DFS 深度優先搜尋

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)
    return visited
```

## 參考資源

- https://www.google.com/search?q=Python+stack+implementation
- https://www.google.com/search?q=stack+data+structure+applications

## 小結

堆疊結構簡單卻功能強大，從括號匹配到 DFS，到處都可見它的身影。熟練堆疊是程式設計師的基本功。
