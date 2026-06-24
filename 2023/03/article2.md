# 堆疊與佇列的實作比較

## 堆疊（Stack）

堆疊是後進先出（LIFO, Last In First Out）的資料結構。主要操作有 push（放入頂端）、pop（從頂端取出）與 peek / top（查看頂端元素而不移除）。堆疊的應用非常廣泛，從函式呼叫的執行堆疊到文字編輯器的 undo 功能，都離不開堆疊。

**陣列實作**：使用 Python list 的 append 與 pop，簡單且快取友好。Python list 會自動處理動態擴容，所以使用上非常方便。

```python
stack = []
stack.append(1)  # push
stack.append(2)
top = stack[-1]  # peek
item = stack.pop()  # pop
```

**鏈結串列實作**：在頭部進行 push 與 pop，時間複雜度均為 O(1)。適合不確定資料量或需要頻繁擴縮的場景。

## 佇列（Queue）

佇列是先進先出（FIFO, First In First Out）的資料結構。主要操作有 enqueue（從尾端放入）、dequeue（從前端取出）與 front（查看前端元素）。

**陣列實作**：使用 list 的 append（enqueue）與 pop(0)（dequeue）。但 pop(0) 需要 O(n) 時間來搬移所有元素，效率不佳，不適合大型資料。

**鏈結串列實作**：在尾部 enqueue（O(1)），頭部 dequeue（O(1)）。這是較好的實作方式，但需要自行管理節點記憶體。

**collections.deque**：Python 的 collections.deque 使用雙向鏈結串列實作，兩端操作皆為 O(1)，是佇列的最佳選擇。

```python
from collections import deque
q = deque()
q.append(1)    # enqueue
q.append(2)
front = q[0]   # front
item = q.popleft()  # dequeue
```

## 其他變體

**雙端佇列（Deque）**：允許在頭尾兩端進行插入與刪除。
**優先佇列（Priority Queue）**：元素按優先權順序取出，通常用堆積實作。
**單調堆疊/佇列**：維護元素單調性，用於解決 Next Greater Element 等經典問題。

## 實作建議

| 需求 | 建議實作 |
|------|----------|
| 一般堆疊 | Python list |
| 一般佇列 | collections.deque |
| 頻繁頭部操作 | collections.deque |
| 自訂記憶體管理 | 鏈結串列實作 |
| 優先權排序 | heapq 模組 |

## 延伸閱讀

- https://www.google.com/search?q=stack+vs+queue+implementation+Python+list+deque
- https://www.google.com/search?q=Python+deque+performance+vs+list+pop+0+效率
- https://www.google.com/search?q=堆疊+佇列+陣列+鏈結串列+實作+方式+優缺點+比較
