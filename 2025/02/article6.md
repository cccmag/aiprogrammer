# 氣泡排序與插入排序

## 氣泡排序（Bubble Sort）

氣泡排序是最直觀的排序演算法。它反覆掃描陣列，比較相鄰元素並交換，直到整個陣列有序。

### 實作

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # 已排序，提前結束
            break
    return arr
```

### 執行過程

```
初始：[5, 3, 8, 1, 2]
第1趟：[3, 5, 1, 2, 8]  # 8 浮到正確位置
第2趟：[3, 1, 2, 5, 8]  # 5 浮到正確位置
第3趟：[1, 2, 3, 5, 8]  # 3 浮到正確位置
第4趟：[1, 2, 3, 5, 8]  # 排序完成
```

### 時間複雜度

- 最佳：O(n) — 已排序，加上 swapped 優化
- 最差：O(n²) — 反向排序
- 平均：O(n²)

## 插入排序（Insertion Sort）

插入排序像整理撲克牌，將元素逐一插入到已排序部分的適當位置。

### 實作

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

### 執行過程

```
初始：[5, 3, 8, 1, 2]
i=1：[3, 5, 8, 1, 2]  # 3 插入到已排序區
i=2：[3, 5, 8, 1, 2]  # 8 保持不動
i=3：[1, 3, 5, 8, 2]  # 1 插入到最前面
i=4：[1, 2, 3, 5, 8]  # 2 插入到正確位置
```

### 時間複雜度

- 最佳：O(n) — 已排序
- 最差：O(n²) — 反向排序
- 平均：O(n²)

## 兩者對比

| 特性 | 氣泡排序 | 插入排序 |
|------|---------|---------|
| 交換次數 | 較多 | 較少 |
| 穩定 | 是 | 是 |
| 原地排序 | 是 | 是 |
| 適合場景 | 教學範例 | 小資料集、近乎排序 |

## 參考資源

- https://www.google.com/search?q=bubble+sort+algorithm+explanation
- https://www.google.com/search?q=insertion+sort+algorithm+Python

## 小結

雖然氣泡排序和插入排序在大型資料集上效率不高，但作為學習排序演算法的起點，它們能幫助你理解演算法分析的基本概念。
