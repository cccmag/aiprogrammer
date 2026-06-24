# Big O、Big Θ、Big Ω 深入探討

## 從直覺到數學定義

漸進符號是演算法分析的共通語言。雖然在基礎課程中我們常說「Big O 是最壞情況、Big Ω 是最佳情況」，但這種說法其實不夠精確。本文將從數學定義出發，深入探討這三種符號的真正含義。

## Big O：上界（最壞情況）

### 正式定義

f(n) = O(g(n)) 若存在正常數 c 和 n₀，使得對所有 n ≥ n₀，0 ≤ f(n) ≤ c·g(n)。

這個定義的核心是：當 n 足夠大時，f(n) 的增長不會超過 g(n) 的某個常數倍。

### 使用方式

```python
# 思考以下程式碼的時間複雜度
def example(n):
    total = 0              # O(1)
    for i in range(n):     # 執行 n 次
        total += i         # O(1)
    for i in range(n):     # 執行 n 次
        for j in range(n): # 每次執行 n 次
            total += i * j # O(1)
    return total           # O(1)
```

第一層迴圈：O(n)，第二層巢狀迴圈：O(n²)。總時間：O(n² + n) = O(n²)。常數係數和低階項被省略。

### Big O 的嚴謹用法

嚴格來說，Big O 不是一個函式，而是一個集合。我們寫 f(n) = O(g(n)) 時，實際上是在說 f(n) ∈ O(g(n))。O(g(n)) 是所有滿足上述條件的函式的集合。

## Big Ω：下界（最佳情況）

### 正式定義

f(n) = Ω(g(n)) 若存在正常數 c 和 n₀，使得對所有 n ≥ n₀，0 ≤ c·g(n) ≤ f(n)。

### 使用方式

當我們說「插入排序在最佳情況下是 Ω(n)」，意思是已排序陣列只需 O(n) 次比較。

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:  # 已排序時此條件永遠不成立
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

- 最佳情況（已排序）：Ω(n)
- 最壞情況（反向排序）：O(n²)

## Big Θ：緊界（平均情況）

### 正式定義

f(n) = Θ(g(n)) 若存在正常數 c₁、c₂ 和 n₀，使得對所有 n ≥ n₀，0 ≤ c₁·g(n) ≤ f(n) ≤ c₂·g(n)。

換句話說，f(n) 同時是 O(g(n)) 和 Ω(g(n))。這是我們能給出的最精確的描述。

### 使用方式

合併排序對任何輸入都執行 Θ(n log n) 次比較，所以我們可以說合併排序的時間複雜度是 Θ(n log n)。相比之下，插入排序只有 Θ(n²)，因為它的上界和下界不同。

## 常見誤用與釐清

### 誤用 1：將 Big O 當作「大約」

說「這個演算法是 O(n²)」並不意味著執行時間大約是 n²，而是說它不會比 n² 增長的更快。

### 誤用 2：混淆最壞情況與 Big O

Big O 不是「最壞情況」的同意詞。我們可以分析最壞情況的 Big O、最佳情況的 Big O，甚至平均情況的 Big O。最壞情況通常用 Big O 表示，但並非必然。

### 誤用 3：Big O 隱含常數不重要

對於小輸入，常數可能比增長率更重要。一個 1000n 的演算法在 n < 100 時比一個 0.001n² 的演算法慢。

## 實戰分析

```python
def search_matrix(matrix, target):
    # matrix 是 m×n 的排序矩陣
    row, col = 0, len(matrix[0]) - 1
    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] < target:
            row += 1
        else:
            col -= 1
    return False
```

- 每次迭代減少一行或一列，最多 m + n 步
- 時間複雜度：O(m + n)
- 空間複雜度：O(1)

## 總結

漸進符號提供了描述演算法效率的精確語言。理解 Big O、Big Ω、Big Θ 的真正定義和正確使用方式，是成為優秀演算法工程師的第一步。

## 延伸閱讀

- [Big O Cheatsheet](https://www.google.com/search?q=big+o+cheatsheet)
- [Asymptotic Notation Explained](https://www.google.com/search?q=asymptotic+notation+explained)
- [Algorithm Complexity Analysis](https://www.google.com/search?q=algorithm+complexity+analysis)
