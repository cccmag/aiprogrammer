# 動態規劃原理

## 從遞迴到動態規劃

動態規劃（Dynamic Programming, DP）是解決**最優化問題**的強大工具。它的核心思想是：將一個複雜問題分解為重疊的子問題，並透過**記錄子問題的解**來避免重複計算。

與分治法不同，動態規劃適用於子問題重疊的場景——相同的子問題會在不同分支中被多次遇到。

## 兩個關鍵性質

### 最優子結構（Optimal Substructure）

一個問題具有最優子結構，意思是問題的最優解包含其子問題的最優解。換句話說，我們可以透過組合子問題的最優解來建構原始問題的最優解。

### 重疊子問題（Overlapping Subproblems）

當遞迴演算法重複求解相同的子問題時，該問題具有重疊子問題的特性。動態規劃透過**記憶化**或**底向上計算**來避免這種浪費。

## 兩種 DP 實作方式

### 1. 頂向下（Top-Down）— 記憶化

保持遞迴結構，但添加查表機制：

```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
```

### 2. 底向上（Bottom-Up）— 表格法

從最小子問題開始，逐步建構到原問題：

```python
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

## 經典案例：最長共同子序列（LCS）

LCS 是 DP 的經典問題。給定兩個字串 X 和 Y，找出同時出現在兩者中的最長子序列（不需要連續）。

**遞迴式**：
- 如果 X[i] == Y[j]：dp[i][j] = dp[i-1][j-1] + 1
- 否則：dp[i][j] = max(dp[i-1][j], dp[i][j-1])

```python
def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

## 經典案例：0/1 背包問題

背包問題描述：給定一組物品（每個有重量和價值），在容量限制內最大化總價值。

**遞迴式**：
- 如果 wt[i-1] ≤ w：dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]], dp[i-1][w])
- 否則：dp[i][w] = dp[i-1][w]

```python
def knapSack(W, wt, val, n):
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if wt[i-1] <= w:
                dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]
```

## DP 解題框架

1. **定義狀態**：清楚描述 dp[i][j] 代表的意義
2. **找出遞迴關係**：如何從較小問題構建出當前問題的解
3. **設定初始條件**：邊界值（base case）
4. **計算順序**：確保計算 dp[i][j] 時所需的子問題已經算好
5. **回傳答案**：通常是最後一個表格項

## 什麼時候該用 DP？

- 問題要求**最優值**（最大值、最小值、最多、最少）
- 問題可以分解為**子問題**
- 子問題會**重複出現**
- 存在**最優子結構**

## 總結

動態規劃是演算法設計中的核心技能。雖然 DP 問題有時看起來困難，但只要掌握「定義狀態 → 找出遞迴式 → 填表」這三步驟，並多做練習，就能逐漸熟悉這種思維方式。

## 延伸閱讀

- [Dynamic Programming Introduction](https://www.google.com/search?q=dynamic+programming+introduction)
- [Longest Common Subsequence](https://www.google.com/search?q=longest+common+subsequence)
- [Knapsack Problem](https://www.google.com/search?q=knapsack+problem+dp)
