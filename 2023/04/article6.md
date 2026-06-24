# 背包問題完整分析

## 問題家族

背包問題（Knapsack Problem）是最經典的組合優化問題之一。它有多種變體，本文將涵蓋三種主要類型。

## 1. 0/1 背包問題

### 問題定義

給定 n 個物品，每個物品有重量 wᵢ 和價值 vᵢ。背包容量為 W。每個物品要嘛全部取走，要嘛不取（不能取一部分）。目標是在容量限制下最大化總價值。

### DP 解法

```python
def knapSack_01(W, wt, val, n):
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if wt[i-1] <= w:
                dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]
```

### 空間優化

使用一維陣列：

```python
def knapSack_01_opt(W, wt, val, n):
    dp = [0] * (W + 1)
    for i in range(n):
        for w in range(W, wt[i] - 1, -1):
            dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]
```

注意內層迴圈必須從右向左，確保每個物品只被使用一次。

### 範例

物品：{(重量, 價值)} = {(10, 60), (20, 100), (30, 120)}
容量：50

最優解：選擇物品 2（20, 100）和物品 3（30, 120），總價值 220。

## 2. 完全背包問題

### 問題定義

與 0/1 背包相同，但每個物品可以取無限多次。

### DP 解法

```python
def knapSack_unbounded(W, wt, val, n):
    dp = [0] * (W + 1)
    for w in range(1, W + 1):
        for i in range(n):
            if wt[i] <= w:
                dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
    return dp[W]
```

注意內層迴圈從左向右，允許同一物品被多次選取。

### 0/1 與完全背包的關鍵差異

| 面向 | 0/1 背包 | 完全背包 |
|------|---------|---------|
| 物品使用次數 | 最多一次 | 無限次 |
| 內層迴圈方向 | 從右向左 | 從左向右 |
| 空間優化後 | dp[w] = max(dp[w], val[i] + dp[w - wt[i]]) | dp[w] = max(dp[w], val[i] + dp[w - wt[i]]) |
| 時間複雜度 | O(nW) | O(nW) |

## 3. 多重背包問題

### 問題定義

每個物品 i 有數量限制 cᵢ——最多可以取 cᵢ 次。

### 解法

可以將 cᵢ 個相同物品視為 cᵢ 個獨立的 0/1 物品。但更好的方法是使用**二進制拆分**：

```python
def knapSack_bounded(W, wt, val, cnt, n):
    items = []
    for i in range(n):
        k = 1
        while k <= cnt[i]:
            items.append((k * wt[i], k * val[i]))
            cnt[i] -= k
            k *= 2
        if cnt[i] > 0:
            items.append((cnt[i] * wt[i], cnt[i] * val[i]))
    dp = [0] * (W + 1)
    for w, v in items:
        for cap in range(W, w - 1, -1):
            dp[cap] = max(dp[cap], v + dp[cap - w])
    return dp[W]
```

### 追蹤選擇的物品

```python
def knapSack_with_items(W, wt, val, n):
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if wt[i-1] <= w:
                dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    # 回溯
    w = W
    items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            items.append(i-1)
            w -= wt[i-1]
    return dp[n][W], list(reversed(items))
```

## 常見面試題

### 分割等和子集

判斷能否將陣列分割為兩個和相等的子集 → 0/1 背包（target = sum/2）。

### 零錢兌換

給定硬幣面額和目標金額，求最少硬幣數 → 完全背包。

### 目標和

在數字之間插入 + 或 -，使表達式等於目標值 → 轉化為子集和問題。

## 總結

背包問題家族展示了 DP 的豐富性和靈活性。從 0/1 背包到完全背包再到多重背包，雖然問題相似，但解法有微妙差異。理解這些差異背後的邏輯（物品是否可重複使用），比死記硬背程式碼更重要。

## 延伸閱讀

- [Knapsack Problem Explained](https://www.google.com/search?q=knapsack+problem+explained)
- [0/1 Knapsack DP](https://www.google.com/search?q=0+1+knapsack+dynamic+programming)
- [Unbounded Knapsack](https://www.google.com/search?q=unbounded+knapsack+problem)
