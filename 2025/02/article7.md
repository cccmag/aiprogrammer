# 快速排序實戰

## 快速排序的歷史

快速排序（Quicksort）由 Tony Hoare 於 1959 年提出，是實際應用中最常用的排序演算法之一。多數語言的內建排序函數都使用 Quicksort 的變體。

## 核心思想：分治法

Quicksort 採用分治策略：

1. **分割（Partition）**：選一個 pivot，將陣列分為小於 pivot 和大於 pivot 的兩部分
2. **遞迴排序（Recursively Sort）**：對左右兩部分分別執行 Quicksort
3. **合併（Combine）**：左 + pivot + 右 即為排序結果

## 實作一：簡潔版（額外空間）

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

時間 O(n log n) 平均，空間 O(n)。

## 實作二：原地分割版（優化空間）

```python
def quicksort_inplace(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort_inplace(arr, low, pi - 1)
        quicksort_inplace(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]  # 選最後一個元素為 pivot
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

## 如何選擇 Pivot？

Pivot 的選擇影響 Quicksort 的效能：

| 策略 | 方法 | 優缺點 |
|------|------|--------|
| 固定位置 | 選第一個/最後一個 | 已排序資料會 O(n²) |
| 隨機選取 | `random.choice(arr)` | 避免最差情況 |
| 三數中位數 | 首、中、尾的中位數 | 實際表現好 |

```python
import random

def quicksort_random(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_random(left) + mid + quicksort_random(right)
```

## Quicksort vs Mergesort

| 特性 | Quicksort | Mergesort |
|------|-----------|-----------|
| 平均時間 | O(n log n) | O(n log n) |
| 最差時間 | O(n²) | O(n log n) |
| 空間複雜度 | O(log n) | O(n) |
| 穩定 | 否 | 是 |

## 參考資源

- https://www.google.com/search?q=quicksort+algorithm+detailed+explanation
- https://www.google.com/search?q=quicksort+vs+mergesort+comparison

## 小結

Quicksort 是實務中最受歡迎的排序演算法，理解其分治思想和 pivot 選擇策略，對掌握進階演算法至關重要。
