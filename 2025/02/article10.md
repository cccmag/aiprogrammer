# 動態規劃：費氏數列與背包問題

## 動態規劃的核心思想

動態規劃（Dynamic Programming, DP）包含兩個關鍵概念：

1. **最優子結構（Optimal Substructure）**：大問題的最優解包含子問題的最優解
2. **重疊子問題（Overlapping Subproblems）**：子問題會被重複計算，需要記錄結果

## 範例一：費氏數列

### 遞迴版本（O(2ⁿ)）

```python
def fib_rec(n):
    if n <= 1:
        return n
    return fib_rec(n - 1) + fib_rec(n - 2)
```

### 記憶化版本（Top-down DP, O(n)）

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

### 表格化版本（Bottom-up DP, O(n)）

```python
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

### 空間優化版本（O(1)）

```python
def fib_optimized(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

## 範例二：0/1 背包問題

有 n 個物品，每個物品有重量 wᵢ 和價值 vᵢ。在總重量不超過 W 的情況下，如何選擇物品使總價值最大？

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]

weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5
print(knapsack(weights, values, capacity))  # 7
```

### 空間優化版（1D DP）

```python
def knapsack_1d(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[capacity]
```

## 參考資源

- https://www.google.com/search?q=dynamic+programming+fibonacci+knapsack
- https://www.google.com/search?q=0/1+knapsack+problem+dynamic+programming

## 小結

動態規劃從費氏數列到背包問題，展現了「記錄子問題解避免重複計算」的強大威力。學會 DP 將大幅提升你解決複雜問題的能力。
