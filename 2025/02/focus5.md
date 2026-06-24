# 排序演算法：氣泡、插入、快速排序

## 為什麼要學排序？

排序是電腦科學中最基礎的問題之一。好的排序演算法能讓後續的搜尋更有效率（例如二分搜尋需要已排序的資料）。

## 氣泡排序（Bubble Sort）

氣泡排序反覆走訪陣列，兩兩比較相鄰元素，順序錯誤就交換。每回合會把最大元素「浮」到最後。

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

- 最佳：O(n)（已排序，可優化）
- 平均：O(n²)
- 最差：O(n²)

## 插入排序（Insertion Sort）

插入排序像整理撲克牌，每次將一張牌插入到已排序序列的正確位置。

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

- 最佳：O(n)
- 平均：O(n²)
- 適合少量資料或近乎排序的資料

## 快速排序（Quick Sort）

快速排序採用分治法（Divide and Conquer），選定 pivot 後將陣列分為左右兩部分，再遞迴排序。

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

- 最佳：O(n log n)
- 平均：O(n log n)
- 最差：O(n²)

## 效能對比

| 演算法 | 平均時間 | 空間 | 穩定 |
|--------|---------|------|------|
| 氣泡排序 | O(n²) | O(1) | 是 |
| 插入排序 | O(n²) | O(1) | 是 |
| 快速排序 | O(n log n) | O(log n) | 否 |

## 參考資源

- https://www.google.com/search?q=sorting+algorithms+comparison
- https://www.google.com/search?q=quicksort+algorithm+Python

## 小結

排序是學習演算法的最佳入門，不同演算法在時間、空間與穩定性之間各有取捨。
