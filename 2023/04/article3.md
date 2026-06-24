# 合併排序與快速排序

## 排序問題的重要性

排序是電腦科學中最基本的問題之一。高效的排序演算法是許多複雜系統的基礎——資料庫索引、搜尋引擎、數據分析等領域都離不開排序。

本文將深入比較兩種經典的分治排序演算法：**合併排序**與**快速排序**。

## 合併排序（Merge Sort）

### 演算法原理

合併排序採用經典的分治策略：
1. **分解**：將陣列分成兩個相等的一半
2. **解決**：遞迴排序兩個子陣列
3. **合併**：將兩個已排序子陣列合併為一個

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### 時間與空間分析

- **時間複雜度**：Θ(n log n) 在所有情況下
- **空間複雜度**：O(n) 需要額外陣列進行合併
- **穩定排序**：是（相等元素的相對順序不變）

### 優缺點

**優點**：
- 保證 O(n log n) 時間
- 穩定排序
- 適合外部排序（處理無法放入記憶體的資料）

**缺點**：
- 需要 O(n) 額外空間
- 對於小陣列，常數因子較大

## 快速排序（Quick Sort）

### 演算法原理

快速排序也使用分治法，但策略不同：
1. **選擇樞紐**：從陣列中選擇一個元素作為樞紐（pivot）
2. **分割**：將陣列分為小於樞紐、等於樞紐、大於樞紐三部分
3. **遞迴**：遞迴排序小於和大於樞紐的部分

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)
```

### 時間與空間分析

- **平均時間複雜度**：Θ(n log n)
- **最壞時間複雜度**：O(n²)（每次選擇最小或最大元素作為樞紐）
- **空間複雜度**：O(log n)（遞迴堆疊，原地分割版本）
- **穩定排序**：不穩定（標準實作）

### 優缺點

**優點**：
- 平均情況非常快（常數因子小）
- 可以原地排序（in-place），空間效率高
- 廣泛用於實際系統（C 的 qsort、Java 的 Arrays.sort）

**缺點**：
- 最壞情況 O(n²)
- 不穩定
- 對已排序陣列的效能取決於樞紐選擇策略

## 深度比較

| 特性 | 合併排序 | 快速排序 |
|------|---------|---------|
| 時間（平均） | Θ(n log n) | Θ(n log n) |
| 時間（最壞） | Θ(n log n) | O(n²) |
| 空間 | O(n) | O(log n) |
| 穩定 | 是 | 否 |
| 常數因子 | 較大 | 較小 |
| 樞紐選擇 | 無需 | 需要策略 |
| 外部排序 | 適合 | 不適合 |

## 混合策略：TimSort

Python 和 Java 實際使用 TimSort——一種結合合併排序和插入排序的混合演算法。

```python
# Python 的內建排序就是 TimSort
arr = [38, 27, 43, 3, 9, 82, 10]
arr.sort()
```

TimSort 的策略：
- 對於小陣列（< 64 元素），使用插入排序
- 對於大陣列，使用改良的合併排序
- 利用已排序的「run」來加速

## 實戰建議

1. **需要穩定排序** → 使用合併排序或 TimSort
2. **記憶體受限** → 使用快速排序（原地）
3. **不確定輸入特性** → 使用隨機化快速排序或 TimSort
4. **處理超大型資料** → 使用外部合併排序

## 總結

合併排序和快速排序各有優缺點。理解兩者的原理和特性，可以幫助你在不同的應用場景中做出最佳的排序選擇。

## 延伸閱讀

- [Merge Sort Visualization](https://www.google.com/search?q=merge+sort+visualization)
- [Quick Sort Explained](https://www.google.com/search?q=quick+sort+explained)
- [TimSort Algorithm](https://www.google.com/search?q=TimSort+algorithm)
