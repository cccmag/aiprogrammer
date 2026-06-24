# 時間複雜度與漸進符號

## 為什麼需要分析演算法？

當我們寫程式解決問題時，經常面臨一個關鍵問題：這個演算法夠快嗎？但「快」是一個相對的概念——對 10 筆資料很快的演算法，處理 100 萬筆資料時可能慢如蝸牛。

**時間複雜度分析**提供了一種與機器無關的語言來描述演算法的效率。透過漸進符號，我們可以精確地說出當輸入規模趨近於無限大時，演算法的執行時間會如何增長。

## 三種漸進符號

### Big O — 上界

Big O 記號描述的是演算法在最壞情況下的時間增長率。如果我們說一個演算法是 O(f(n))，意味著存在正常數 c 和 n₀，使得對於所有 n ≥ n₀，執行時間 T(n) ≤ c·f(n)。

**常見的 Big O 類別：**

- **O(1)**：常數時間。無論輸入多大，執行時間恆定。例如：陣列隨機存取。
- **O(log n)**：對數時間。每次操作都將問題規模減半。例如：二元搜尋。
- **O(n)**：線性時間。執行時間與輸入規模成正比。例如：線性搜尋。
- **O(n log n)**：線性對數時間。許多高效排序演算法的時間。例如：合併排序。
- **O(n²)**：平方時間。雙層巢狀迴圈。例如：氣泡排序。
- **O(2ⁿ)**：指數時間。暴力解 NP 問題。

### Big Ω — 下界

Big Ω 描述的是演算法在最佳情況下的時間增長率。T(n) = Ω(g(n)) 意味著存在正常數 c 和 n₀，使得 T(n) ≥ c·g(n) 對所有 n ≥ n₀ 成立。

### Big Θ — 緊界

當一個演算法同時是 O(f(n)) 和 Ω(f(n)) 時，我們說它是 Θ(f(n))。這是最精確的描述——演算法的時間增長率被「夾在」上下界之間。

**實例分析：**

```python
# 氣泡排序 — O(n²), Ω(n), Θ(n²)（一般實作）
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

- 最壞情況（O）：陣列反向排序 → 執行 n(n-1)/2 次比較 → O(n²)
- 最佳情況（Ω）：陣列已排序（未優化時仍需比較）→ Ω(n)
- 優化版可在已排序時提前終止

## 如何分析演算法

### 基本規則

1. **單一操作**：賦值、算術、比較 → O(1)
2. **順序結構**：T₁ + T₂ → 取主導項 max(T₁, T₂)
3. **迴圈**：迴圈次數 × 迴圈體時間
4. **巢狀迴圈**：各層次相乘
5. **遞迴**：建立遞迴關係式，用主定理求解

### 範例：分析二元搜尋

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

每次迭代將搜尋範圍減半。經過 k 次迭代後範圍大小為 n/2ᵏ。當 n/2ᵏ = 1 時演算法終止，解得 k = log₂(n)。因此時間複雜度為 O(log n)。

## 常見誤解

- **O(2n) = O(n)**？Yes！常數係數被省略。
- **O(n² + n) = O(n²)**？Yes！只取最高階項。
- **O(100) = O(1)**？Yes！常數時間都是 O(1)。
- **O(n) 一定比 O(n²) 快**？不一定！對於小輸入 n < 10，O(n²) 可能更快。

## 總結

漸進符號是演算法分析的基石。掌握 Big O、Big Ω、Big Θ 的定義和用法，你就能夠精確地描述任何演算法的效率，並在不同演算法之間做出明智的選擇。

## 延伸閱讀

- [Big O 表示法介紹](https://www.google.com/search?q=Big+O+notation+explained)
- [演算法時間複雜度分析](https://www.google.com/search?q=algorithm+time+complexity+analysis)
- [Master Theorem for Recurrences](https://www.google.com/search?q=master+theorem+recurrences)
