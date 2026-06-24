# 時間複雜度與 Big O

## 什麼是時間複雜度？

時間複雜度是用來描述演算法執行時間與輸入資料量之間關係的函數。它幫助我們在不實際執行程式的情況下，預估演算法的效率。

## Big O 表示法

Big O 表示法描述的是演算法在最壞情況下的執行時間上界。常見的時間複雜度由快到慢排列：

### O(1) — 常數時間

無論輸入多大，執行時間都固定。

```python
def get_first(arr):
    return arr[0]  # 永遠只需一步
```

### O(log n) — 對數時間

每次操作將問題規模縮減一半。

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

### O(n) — 線性時間

執行時間與輸入規模成正比。

```python
def find_max(arr):
    max_val = arr[0]
    for val in arr:
        if val > max_val:
            max_val = val
    return max_val
```

### O(n log n) — 線性對數時間

常見於較好的排序演算法，如快速排序、合併排序。

### O(n²) — 平方時間

常見於雙重迴圈的演算法，如氣泡排序。

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

### O(2ⁿ) — 指數時間

常見於單純遞迴的費氏數列計算。當 n 稍微增加，執行時間就會暴增。

## 時間複雜度圖解

| n | O(1) | O(log n) | O(n) | O(n log n) | O(n²) | O(2ⁿ) |
|---|------|----------|------|------------|-------|-------|
| 10 | 1 | ~3 | 10 | ~30 | 100 | 1024 |
| 100 | 1 | ~7 | 100 | ~700 | 10000 | 巨大 |

## 參考資源

- https://www.google.com/search?q=Big+O+notation+explained+simply
- https://www.google.com/search?q=time+complexity+cheat+sheet

## 小結

掌握時間複雜度分析，才能寫出真正高效的程式。面試時幾乎必考，請務必熟練。
