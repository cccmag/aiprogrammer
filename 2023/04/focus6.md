# 隨機化演算法

## 為什麼需要隨機性？

傳統演算法是確定性的——給定相同的輸入，永遠產生相同的輸出和相同的執行過程。但隨機化演算法引入了選擇的隨機性，使得同一輸入的不同執行可能產生不同結果。

引入隨機性有什麼好處？主要體現在三個方面：

1. **簡化分析**：隨機化演算法的期望時間複雜度往往更容易分析
2. **避免最壞情況**：隨機化可以讓對手無法構造針對性的最壞情況輸入
3. **更好的平均效能**：在許多問題中，隨機化演算法在平均情況下表現更出色

## 兩種主要的隨機化演算法

### Las Vegas 演算法

這類演算法**總是給出正確答案**，但執行時間是隨機變數。萬一執行時間過長，我們可以重新執行。

**範例：隨機化快速排序**

```python
import random

def randomized_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return randomized_quick_sort(left) + mid + randomized_quick_sort(right)
```

傳統快速排序選擇第一個元素作為樞紐時，已排序陣列會導致 O(n²) 的最壞情況。隨機選擇樞紐後，任何輸入的期望時間複雜度都是 O(n log n)。

### Monte Carlo 演算法

這類演算法**執行時間確定**，但可能以很小的機率給出錯誤答案。如果錯誤率足夠小，我們可以接受這種代價。

**範例：質數檢測（Miller-Rabin）**

Miller-Rabin 演算法以高機率判斷一個大數是否為質數。雖然有小機率將合數誤判為質數，但我們可以透過增加迭代次數將錯誤率降到任意低。

## 隨機化演算法的應用

### 負載平衡

在分散式系統中，將任務隨機分配給伺服器可以有效避免某些伺服器過載。

### 密碼學

隨機數是密碼學的基石——密鑰生成、加密鹽值、初始化向量等都依賴高品質的隨機性。

### 近似演算法

對某些 NP-hard 問題，隨機化演算法可以在較短時間內得到「足夠好」的近似解。

### 跳表（Skip List）

跳表是一種隨機化的資料結構，它使用隨機層數來實現在 O(log n) 期望時間內完成搜尋、插入和刪除操作。

## 隨機化 vs 確定性演算法

| 面向 | 確定性演算法 | 隨機化演算法 |
|------|-----------|-----------|
| 最壞情況時間 | 確定 | 可能很長（機率極低） |
| 期望時間 | 等同最壞情況 | 通常更好 |
| 正確性 | 100% | Las Vegas：100%；Monte Carlo：高機率 |
| 對抗性輸入 | 可能被利用 | 無法被針對 |
| 分析難度 | 相對簡單 | 需要機率論工具 |

## 隨機化演算法的限制

### 隨機數品質

真實計算機無法產生真正的亂數——我們使用的是偽亂數產生器。在密碼學應用中，必須使用密碼學安全的偽亂數產生器（CSPRNG）。

### 除錯困難

隨機化演算法的不確定性使得除錯變得困難——同一個 bug 可能只在某些執行中出現。

## 總結

隨機化演算法是演算法設計中的重要工具。透過巧妙引入隨機性，我們可以在相當寬鬆的假設下獲得優異的期望效能。在實際應用中，隨機化快速排序、隨機化二元搜尋樹等資料結構已被廣泛使用，證明了隨機化策略的實用價值。

## 延伸閱讀

- [Randomized Algorithms](https://www.google.com/search?q=randomized+algorithms+introduction)
- [Las Vegas vs Monte Carlo](https://www.google.com/search?q=Las+Vegas+vs+Monte+Carlo+algorithms)
- [Randomized Quick Sort](https://www.google.com/search?q=randomized+quick+sort)
