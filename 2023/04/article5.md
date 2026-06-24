# 最長共同子序列 LCS

## 問題介紹

最長共同子序列（Longest Common Subsequence, LCS）是一個經典的 DP 問題。給定兩個字串 X 和 Y，LCS 是同時出現在兩者中的最長子序列。

**重要區別**：子序列（Subsequence）不同於子字串（Substring）。子序列不要求連續，只需保持相對順序即可。

### 範例

X = "ABCBDAB"
Y = "BDCABC"

LCS 可以是 "BCAB"（長度 4）、"BDAB"（長度 4）或 "BCBA"（長度 4）。最長長度為 4。

## 暴力法 vs DP

### 暴力法

最直接的解法是生成 X 的所有子序列（2^m 個），檢查每個是否也是 Y 的子序列。時間複雜度 O(2^m × n)，完全不可行。

### DP 的核心觀察

LCS 問題具有最優子結構：
- 如果 X[i] == Y[j]，則 LCS 包含這個字元，然後繼續在 X[i-1] 和 Y[j-1] 中尋找
- 如果 X[i] != Y[j]，則 LCS 是 max(LCS(X[i-1], Y[j]), LCS(X[i], Y[j-1]))

## DP 解法

### 定義狀態

令 dp[i][j] 表示 X[0..i-1] 和 Y[0..j-1] 的 LCS 長度。

### 遞迴關係

```
dp[i][j] = 0                             如果 i=0 或 j=0
dp[i][j] = dp[i-1][j-1] + 1             如果 X[i-1] == Y[j-1]
dp[i][j] = max(dp[i-1][j], dp[i][j-1])  如果 X[i-1] != Y[j-1]
```

### Python 實作

```python
def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 回溯找出 LCS 序列
    seq = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            seq.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], ''.join(reversed(seq))
```

### 時間與空間分析

- 時間複雜度：O(mn)——填滿 m×n 表格
- 空間複雜度：O(mn)——儲存整個 DP 表

### 空間優化

如果只需要 LCS 長度（不需要序列），可以只保留兩行：

```python
def lcs_length(X, Y):
    m, n = len(X), len(Y)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]
```

空間複雜度降至 O(min(m,n))。

## 完整 DP 分析

讓我們追蹤範例的 DP 表：

```
    Ø  B  D  C  A  B  C
Ø   0  0  0  0  0  0  0
A   0  0  0  0  1  1  1
B   0  1  1  1  1  2  2
C   0  1  1  2  2  2  3
B   0  1  1  2  2  3  3
D   0  1  2  2  2  3  3
A   0  1  2  2  3  3  3
B   0  1  2  2  3  4  4
```

右下角 dp[7][6] = 4，正是 LCS 長度。

## LCS 的變體與應用

### 應用場景

1. **版本控制（diff）**：計算兩個檔案版本的差異
2. **生物資訊學**：DNA 序列比對（Needleman-Wunsch 演算法）
3. **拼寫檢查**：計算兩個字串的相似度
4. **抄襲檢測**：比對文件間的相似內容

### 相關問題

- **最長共同子字串（LCSubStr）**：要求字元必須連續
- **編輯距離（Edit Distance）**：透過插入、刪除、替換操作的最小次數
- **最短共同超序列（SCS）**：包含兩個字串的最短字串

## 總結

LCS 問題是動態規劃的經典教材案例。它清楚地展示了 DP 的兩個核心特徵：最優子結構和重疊子問題。掌握 LCS 不僅有助於理解 DP，還有許多實際應用。

## 延伸閱讀

- [Longest Common Subsequence](https://www.google.com/search?q=longest+common+subsequence+algorithm)
- [Dynamic Programming for LCS](https://www.google.com/search?q=dynamic+programming+LCS)
- [Needleman-Wunsch Algorithm](https://www.google.com/search?q=Needleman+Wunsch+algorithm)
