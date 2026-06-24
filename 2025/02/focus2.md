# 陣列與串列：順序儲存

## 陣列（Array）

陣列是最基礎的資料結構，它在記憶體中佔用一塊連續的空間。每個元素透過索引（Index）存取，時間複雜度為 O(1)。Python 的 `list` 底層就是動態陣列實作。

```python
arr = [10, 20, 30, 40, 50]
print(arr[0])   # 10
print(arr[2])   # 30
arr.append(60)  # 在尾部新增
```

陣列的優點是隨機存取快速，缺點是插入和刪除需要搬動元素。

## Python 串列（List）

Python 的 list 是動態陣列，會自動擴展容量。底層使用 `PyObject*` 陣列儲存，每個元素都是指向物件的指標。

```python
lst = []
lst.append(1)
lst.insert(0, 0)  # 頭部插入 O(n)
lst.pop()         # 尾部刪除 O(1)
lst.pop(0)        # 頭部刪除 O(n)
```

## 時間複雜度對比

| 操作 | 陣列 | Python List |
|------|------|-------------|
| 索引存取 | O(1) | O(1) |
| 尾部插入 | O(1) | O(1)* |
| 頭部插入 | O(n) | O(n) |
| 中間插入 | O(n) | O(n) |
| 尾部刪除 | O(1) | O(1) |
| 頭部刪除 | O(n) | O(n) |

*Python list 在容量不足時會重新分配約 1.125 倍的新空間。

## 實戰建議

若你經常需要從頭部插入或刪除元素，應考慮使用 `collections.deque`，它在兩端操作都是 O(1)。

```python
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)   # O(1)
dq.popleft()       # O(1)
```

## 參考資源

- https://www.google.com/search?q=Python+list+dynamic+array+implementation
- https://www.google.com/search?q=array+vs+linked+list+complexity

## 小結

陣列與串列是最基礎的順序儲存結構，掌握它們的優缺點是學習進階資料結構的第一步。
