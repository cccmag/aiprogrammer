# 二分搜尋與搜尋樹

## 二分搜尋（Binary Search）

二分搜尋是解決「在有序陣列中尋找目標值」問題的最高效方法。每次比較都能排除一半的資料。

### 迭代實作

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### 遞迴實作

```python
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

## 二分搜尋的變體

### 找左邊界（First Occurrence）

```python
def first_occurrence(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # 繼續往左找
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

### 找右邊界（Last Occurrence）

```python
def last_occurrence(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1  # 繼續往右找
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

## 二元搜尋樹（Binary Search Tree）

BST 是一種將二分搜尋概念延伸到樹狀結構的資料結構。

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST:
    def insert(self, root, val):
        if not root:
            return TreeNode(val)
        if val < root.val:
            root.left = self.insert(root.left, val)
        else:
            root.right = self.insert(root.right, val)
        return root

    def search(self, root, val):
        if not root or root.val == val:
            return root
        if val < root.val:
            return self.search(root.left, val)
        return self.search(root.right, val)
```

## 時間複雜度

| 操作 | 陣列二分搜 | BST |
|------|-----------|-----|
| 搜尋 | O(log n) | O(log n) 平均 |
| 插入 | O(n) | O(log n) 平均 |
| 刪除 | O(n) | O(log n) 平均 |

## 參考資源

- https://www.google.com/search?q=binary+search+algorithm+Python
- https://www.google.com/search?q=binary+search+tree+data+structure

## 小結

二分搜尋是 O(log n) 演算法的經典代表，BST 則將其延伸為動態資料結構。掌握這兩者對於理解資料庫索引等進階主題很有幫助。
