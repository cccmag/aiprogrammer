# 堆疊與佇列：先進後出 vs 先進先出

## 堆疊（Stack）— LIFO

堆疊就像一疊盤子，你只能從頂端放盤子或拿盤子。最後放進去的東西會最先被取出，這就是「後進先出」（Last In, First Out, LIFO）。

生活中處處可見堆疊的應用：
- 瀏覽器的「上一頁」功能
- 編輯器的 Undo（復原）操作
- 函數呼叫的 Call Stack

```python
stack = []
stack.append('A')  # push
stack.append('B')
stack.append('C')
print(stack.pop())  # C
print(stack.pop())  # B
print(stack.pop())  # A
```

## 佇列（Queue）— FIFO

佇列就像排隊買票，先來的人先服務，這就是「先進先出」（First In, First Out, FIFO）。

佇列的常見應用：
- 印表機工作佇列
- 作業系統的行程排程
- BFS（廣度優先搜尋）

```python
from collections import deque
queue = deque()
queue.append('A')   # enqueue
queue.append('B')
queue.append('C')
print(queue.popleft())  # A
print(queue.popleft())  # B
print(queue.popleft())  # C
```

## 堆疊 vs 佇列

| 特性 | Stack | Queue |
|------|-------|-------|
| 原則 | LIFO | FIFO |
| 插入 | push (top) | enqueue (rear) |
| 刪除 | pop (top) | dequeue (front) |
| 底層 | list / deque | deque |
| 應用 | DFS, Undo | BFS, 排程 |

## Python 實作選擇

- 堆疊可直接用 `list`（`append` / `pop` O(1)）
- 佇列建議用 `collections.deque`（`append` / `popleft` O(1)）

## 參考資源

- https://www.google.com/search?q=stack+data+structure+LIFO
- https://www.google.com/search?q=queue+data+structure+FIFO
- https://www.google.com/search?q=Python+collections+deque

## 小結

堆疊與佇列是兩種最基本的受限線性結構，理解它們的運作原理是學習進階搜尋演算法的重要基礎。
