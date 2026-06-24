# 矩陣鏈乘積 DP

## 問題描述

給定一個矩陣鏈 (A₁, A₂, ..., Aₙ)，其中 Aᵢ 的維度為 p_{i-1} × pᵢ，我們要找出最有效率的乘法順序。

矩陣乘法滿足結合律，所以不同的括號化方式會得到相同的結果，但計算次數可能天差地遠。

### 具體範例

考慮三個矩陣：A₁(10×100)、A₂(100×5)、A₃(5×50)：

- (A₁ × A₂) × A₃：10×100×5 + 10×5×50 = 5000 + 2500 = 7500 次乘法
- A₁ × (A₂ × A₃)：100×5×50 + 10×100×50 = 25000 + 50000 = 75000 次乘法

不同順序相差 10 倍！而矩陣規模更大時，差異可能達到數百萬倍。

## DP 解法

### 定義子問題

令 dp[i][j] 表示計算 Aᵢ × A_{i+1} × ... × Aⱼ 所需的最少乘法次數。

### 遞迴關係

對於 i < j，最後一次乘法發生在某個 k 位置（i ≤ k < j）：
dp[i][j] = min(dp[i][k] + dp[k+1][j] + p_{i-1} × p_k × p_j)

其中：
- dp[i][k]：計算 Aᵢ...Aₖ 的成本
- dp[k+1][j]：計算 A_{k+1}...Aⱼ 的成本
- p_{i-1} × p_k × p_j：合併兩個結果矩陣的乘法成本

### 初始條件

當 i = j 時，只有一個矩陣，不需要乘法：dp[i][i] = 0。

### Python 實作

```python
def matrix_chain_order(p):
    n = len(p) - 1
    dp = [[0] * n for _ in range(n)]
    # chain_len 是子鏈的長度
    for chain_len in range(2, n + 1):
        for i in range(n - chain_len + 1):
            j = i + chain_len - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = (dp[i][k] + dp[k+1][j]
                        + p[i] * p[k+1] * p[j+1])
                if cost < dp[i][j]:
                    dp[i][j] = cost
    return dp[0][n-1]
```

### 時間複雜度

三層迴圈：O(n³)。空間複雜度：O(n²)。

### 重建括號化方案

除了記錄最小成本，我們還需要記錄在哪個 k 分割：

```python
def matrix_chain_order_with_solution(p):
    n = len(p) - 1
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for chain_len in range(2, n + 1):
        for i in range(n - chain_len + 1):
            j = i + chain_len - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = (dp[i][k] + dp[k+1][j]
                        + p[i] * p[k+1] * p[j+1])
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k
    return dp[0][n-1], split

def print_parenthesis(split, i, j):
    if i == j:
        print(f"A{i+1}", end="")
    else:
        print("(", end="")
        print_parenthesis(split, i, split[i][j])
        print(" × ", end="")
        print_parenthesis(split, split[i][j]+1, j)
        print(")", end="")
```

## 完整執行

```python
p = [10, 100, 5, 50]  # A₁=10×100, A₂=100×5, A₃=5×50
min_cost, split = matrix_chain_order_with_solution(p)
print(f"最少乘法次數: {min_cost}")
print("最優括號化: ", end="")
print_parenthesis(split, 0, len(p) - 2)
```

輸出：
```
最少乘法次數: 7500
最優括號化: (A1 × (A2 × A3))
```

## DP 解題模式

矩陣鏈乘積是典型的**區間 DP** 問題。這類問題的特徵：

1. 問題涉及對一個序列的操作
2. 子問題定義為序列的連續子區間
3. 遞迴關係涉及在區間內選擇一個分割點

其他區間 DP 問題包括：最優二元搜尋樹、括號配對、戳氣球問題等。

## 總結

矩陣鏈乘積展示了 DP「透過記錄子問題解避免重複計算」的核心思想。雖然問題本身看起來抽象，但其 DP 模式在許多實際問題中都會出現。

## 延伸閱讀

- [Matrix Chain Multiplication](https://www.google.com/search?q=matrix+chain+multiplication+dp)
- [Interval DP Tutorial](https://www.google.com/search?q=interval+dp+tutorial)
- [Optimal Binary Search Tree](https://www.google.com/search?q=optimal+binary+search+tree+dp)
