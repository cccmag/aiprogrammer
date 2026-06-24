# 動態規劃入門

## 什麼是動態規劃？

動態規劃（Dynamic Programming, DP）將複雜問題分解為子問題，儲存子問題結果以避免重複計算。

適用條件：
1. **最優子結構**：最優解包含子問題的最優解
2. **重疊子問題**：子問題會重複出現

## 費波那契數列

```python
# 暴力（指數級）
def fib_brutal(n):
    if n <= 1:
        return n
    return fib_brutal(n-1) + fib_brutal(n-2)

# DP（線性）
def fib_dp(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]

# 空間優化
def fib_optimized(n):
    if n <= 1:
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr
```

## 背包問題

### 0/1 背包

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w - weights[i-1]] + values[i-1]
                )
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]

weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5
print(knapsack(weights, values, capacity))  # 7
```

### 空間優化

```python
def knapsack_optimized(weights, values, capacity):
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]
```

## 最長公共子序列（LCS）

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

print(lcs("ABCD", "ACBD"))  # 3 (ABC 或 ABD)
```

## 最短路徑

```python
# Floyd-Warshall（所有點對最短路徑）
def floyd_warshall(dist):
    n = len(dist)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# 初始化
INF = float('inf')
dist = [
    [0, 4, INF, 2],
    [4, 0, 1, 5],
    [INF, 1, 0, 1],
    [2, 5, 1, 0]
]

floyd_warshall(dist)
```

## DP 與強化學習

Q-learning 本質上是一種 DP 方法，解決 MDP。

```python
def value_iteration(P, R, n_states, n_actions, gamma=0.9, theta=1e-6):
    V = np.zeros(n_states)

    while True:
        V_old = V.copy()

        for s in range(n_states):
            q_values = [
                sum(P[s, sp, a] * (R[s, a, sp] + gamma * V_old[sp])
                   for sp in range(n_states))
                for a in range(n_actions)
            ]
            V[s] = max(q_values)

        if np.max(np.abs(V - V_old)) < theta:
            break

    return V
```

## 總結

動態規劃是強大的解決問題的方法：
- 識別問題的 DP 特性
- 定義狀態和轉移
- 設計 DP 表
- 空間或時間優化