# 分治法與遞迴關係

## 分治法的核心思想

分治法（Divide and Conquer）是演算法設計中最古老也最優雅的策略之一。其核心思想非常直覺：**將一個大問題分解成若干個小問題，分別解決後再將結果合併起來**。

這個策略包含三個步驟：

1. **分解（Divide）**：將原始問題分解為數個規模較小但結構相同的子問題
2. **解決（Conquer）**：遞迴地解決各個子問題。當子問題足夠小時，直接求解
3. **合併（Combine）**：將子問題的解組合成原始問題的解

## 經典案例：合併排序

合併排序是分治法的經典教材案例。

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

合併排序的時間複雜度可以寫成遞迴關係式：T(n) = 2T(n/2) + O(n)。其中 2T(n/2) 是遞迴排序兩個子陣列的時間，O(n) 是合併兩個排序陣列的時間。

## 遞迴關係式

遞迴關係式是分析分治演算法時間的關鍵工具。一般形式為：

T(n) = a·T(n/b) + f(n)

其中：
- a：子問題的數量
- b：每次分解後子問題的規模縮小倍數
- f(n)：分解和合併所需的時間

### 主定理（Master Theorem）

主定理提供了求解這類遞迴關係式的系統性方法。對於 T(n) = a·T(n/b) + f(n)：

1. 如果 f(n) = O(n^(log_b(a) - ε))，則 T(n) = Θ(n^(log_b(a)))
2. 如果 f(n) = Θ(n^(log_b(a)))，則 T(n) = Θ(n^(log_b(a)) · log n)
3. 如果 f(n) = Ω(n^(log_b(a) + ε)) 且 a·f(n/b) ≤ c·f(n)，則 T(n) = Θ(f(n))

### 主定理的應用

| 演算法 | 遞迴式 | a | b | f(n) | log_b(a) | 案例 | 結果 |
|-------|-------|---|---|------|----------|------|------|
| 合併排序 | T(n)=2T(n/2)+O(n) | 2 | 2 | O(n) | 1 | 案例 2 | Θ(n log n) |
| 二元搜尋 | T(n)=T(n/2)+O(1) | 1 | 2 | O(1) | 0 | 案例 2 | Θ(log n) |
| 快速排序(平均) | T(n)=2T(n/2)+O(n) | 2 | 2 | O(n) | 1 | 案例 2 | Θ(n log n) |
| Strassen 矩陣 | T(n)=7T(n/2)+O(n²) | 7 | 2 | O(n²) | log₂7≈2.81 | 案例 1 | Θ(n^2.81) |

### 遞迴樹法

當主定理不適用時，遞迴樹法是一個更通用的替代方案。我們將遞迴式展開為樹狀結構，每一層代表一次遞迴調用，然後加總所有層的開銷。

## 其他分治案例

### 快速排序

快速排序也使用分治法，但樞紐選擇的不同會導致不同的時間複雜度。

### 最大子陣列問題

在陣列中找到連續子陣列的最大和，可以透過分治法在 O(n log n) 時間內解決。

```python
def max_subarray(arr, low, high):
    if low == high:
        return arr[low]
    mid = (low + high) // 2
    left_sum = max_subarray(arr, low, mid)
    right_sum = max_subarray(arr, mid + 1, high)
    cross_sum = max_crossing(arr, low, mid, high)
    return max(left_sum, right_sum, cross_sum)
```

## 分治法的侷限

分治法雖然強大，但並非所有問題都適用。如果子問題之間高度相關（重疊子問題），動態規劃可能是更好的選擇。

## 總結

分治法是遞迴思維的體現。掌握分治法不僅意味著學會了幾種經典演算法，更代表你學會了「將複雜問題拆解為可管理的小塊」這種重要的思維方式。

## 延伸閱讀

- [Divide and Conquer Algorithm](https://www.google.com/search?q=divide+and+conquer+algorithm)
- [Master Theorem Explained](https://www.google.com/search?q=master+theorem+explained)
- [Recurrence Tree Method](https://www.google.com/search?q=recurrence+tree+method)
