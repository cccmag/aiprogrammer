# 遞迴與動態規劃入門

## 遞迴（Recursion）

遞迴是函數呼叫自身的程式設計技巧。一個完整的遞迴函數需要兩個要素：

1. **終止條件（Base Case）**：避免無限迴圈
2. **遞迴步驟（Recursive Step）**：逐步縮小問題規模

```python
def factorial(n):
    if n <= 1:      # base case
        return 1
    return n * factorial(n - 1)  # recursive step
```

### 遞迴的優缺點

- 優點：程式碼簡潔優雅，適合處理分治、樹狀結構
- 缺點：函數呼叫有額外開銷，過深可能導致 Stack Overflow

## 動態規劃（Dynamic Programming）

動態規劃的核心思想是：將大問題分解為重疊的子問題，並記錄子問題的答案以避免重複計算。

### 費氏數列 — 三種實作對比

```python
# 純遞迴 O(2ⁿ)
def fib_rec(n):
    if n <= 1:
        return n
    return fib_rec(n-1) + fib_rec(n-2)

# 記憶化遞迴 O(n)
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# 動態規劃 O(n)
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

### 背包問題（0/1 Knapsack）

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w - weights[i-1]],
                    dp[i-1][w]
                )
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]
```

## 參考資源

- https://www.google.com/search?q=recursion+programming+explained
- https://www.google.com/search?q=dynamic+programming+fibonacci+knapsack

## 小結

遞迴是解決分治問題的利器，動態規劃則透過記錄子問題解來大幅提升效率。兩者都是進階演算法的核心技術。
