# 隨機化快速排序

## 為什麼快速排序需要隨機化？

快速排序的平均時間複雜度是 Θ(n log n)，但最壞情況可以退化到 O(n²)——當每次都選擇到最小或最大的元素作為樞紐時。

更糟的是，如果我們固定選擇第一個元素作為樞紐，攻擊者可以故意構造一個已排序的陣列來觸發最壞情況。隨機化正是為了解決這個問題。

## 隨機化快速排序

### 核心思想

在每次遞迴時，從陣列中**隨機選擇**一個元素作為樞紐。這樣，任何特定的輸入都無法保證觸發最壞情況。

```python
import random

def randomized_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return (randomized_quick_sort(left) + mid
            + randomized_quick_sort(right))
```

### 期望時間分析

隨機選擇樞紐後，最壞情況發生的機率極低。可以證明期望時間複雜度為 O(n log n)。

**直覺理解**：隨機選擇的樞紐期望落在陣列的中間 50% 範圍內（即第 25% 到第 75% 百分位數之間），這保證了子問題的規模至少有 25% 的縮減。

## 隨機化的威力

### 對抗惡意輸入

假設你在寫一個網路服務，使用者可以上傳資料進行排序。如果使用固定樞紐的快速排序，攻擊者可以上傳精心構造的資料讓你的伺服器耗盡 CPU 時間。

使用隨機化版本後，攻擊者無法預測哪個元素會被選為樞紐，因此無法構造針對性的最壞情況輸入。

### 分析結果

| 版本 | 平均時間 | 最壞時間 | 對抗輸入 |
|------|---------|---------|---------|
| 固定樞紐（首元素） | Θ(n log n) | O(n²) | 容易 |
| 隨機樞紐 | Θ(n log n) | O(n²) 機率極低 | 困難 |
| 中位數樞紐 | Θ(n log n) | Θ(n log n) | 困難但代價高 |

### 中位數法

理論上，選擇中位數作為樞紐可以保證 Θ(n log n)，但尋找中位數的時間成本很高（雖然可以在 O(n) 時間內找到，但常數因子大）。隨機化用更小的成本達到了幾乎相同的效果。

## 期望分析

### 指標變數法

令 X 為快速排序的總比較次數。定義指標變數 I_{ij}：如果第 i 小的元素和第 j 小的元素進行了比較，則 I_{ij} = 1。

總比較次數：E[X] = Σᵢ Σⱼ Pr[第 i 和 j 小的元素進行了比較]

可以證明 Pr[兩元素比較] = 2/(j - i + 1)，因此：

E[X] = Σᵢ Σ_{j>i} 2/(j - i + 1) = O(n log n)

這個推導過程是隨機化演算法分析的經典範例。

## 就地（In-Place）版本

上述實作使用 list comprehension 建立新列表，需要 O(n) 額外空間。下面是在地的 Lomuto 分割版本：

```python
def randomized_quick_sort_inplace(arr, low, high):
    if low < high:
        pi = randomized_partition(arr, low, high)
        randomized_quick_sort_inplace(arr, low, pi - 1)
        randomized_quick_sort_inplace(arr, pi + 1, high)

def randomized_partition(arr, low, high):
    rand_idx = random.randint(low, high)
    arr[high], arr[rand_idx] = arr[rand_idx], arr[high]
    return partition(arr, low, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

這個版本不需要額外陣列，空間複雜度僅 O(log n)。

## 隨機化的其他應用

- **隨機化二元搜尋樹**：隨機插入順序避免樹退化成鏈表
- **隨機化雜湊**：選擇隨機雜湊函式來避免碰撞攻擊
- **隨機化圖論演算法**：隨機抽樣來估計大圖的特性

## 關於隨機性

Python 的 random.choice 使用的是 Mersenne Twister 偽亂數產生器，對非密碼學應用已足夠。真正的隨機化演算法分析假設完美的隨機性來源。

## 總結

隨機化快速排序是「以極小的代價大幅提升演算法穩定性」的典範。它告訴我們：有時候引入一點不確定性，反而能得到更可靠的結果。

## 延伸閱讀

- [Randomized Quick Sort Analysis](https://www.google.com/search?q=randomized+quick+sort+analysis)
- [Las Vegas vs Monte Carlo](https://www.google.com/search?q=Las+Vegas+Monte+Carlo+algorithms)
- [Randomized Algorithms in CS](https://www.google.com/search?q=randomized+algorithms+computer+science)
