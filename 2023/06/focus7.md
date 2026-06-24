# 空間複雜度與 PSPACE

## 空間複雜度

時間不是唯一重要的計算資源。記憶體（空間）同樣是有限的資源。空間複雜度研究的是解決一個問題所需要的記憶體空間量。

一個演算法的空間複雜度定義為它在計算過程中使用的最大記憶體單元數（以輸入規模 n 的函式表示）。

## 空間複雜度類別

最重要的空間複雜度類別：

| 類別 | 定義 | 範例問題 |
|------|------|---------|
| L（Logarithmic Space） | 使用 O(log n) 空間的確定性圖靈機 | 有向圖連通性 |
| NL（Nondeterministic Log Space） | 使用 O(log n) 空間的非確定性圖靈機 | 有向圖連通性 |
| PSPACE | 使用多項式空間的確定性圖靈機 | QSAT、廣義地理遊戲 |
| NPSPACE | 使用多項式空間的非確定性圖靈機 | 與 PSPACE 相等 |
| EXPSPACE | 使用指數空間的確定性圖靈機 | 某些數學問題 |

## PSPACE 的定義

PSPACE 是所有可以在多項式空間內解決的決策問題的集合。

形式化定義：
> PSPACE = ∪_{k≥1} SPACE(n^k)

PSPACE 包含 P 和 NP，因為如果一個問題可以在多項式時間內解決，它使用的空間不可能超過時間：

> P ⊆ NP ⊆ PSPACE

## PSPACE-Complete

一個問題是 PSPACE-Complete 的，當且僅當：

1. 它在 PSPACE 中
2. 所有 PSPACE 問題都可以在多項式時間內歸約到它

經典的 PSPACE-Complete 問題：

### QSAT（量化布林公式）

QSAT 是 SAT 的推廣，允許存在量詞（∃）和全稱量詞（∀）：

```
∀x₁ ∃x₂ ∀x₃ ... φ(x₁, x₂, x₃, ..., xₙ)
```

其中 φ 是布林公式。問題是：這個量化公式是否為真？

QSAT 可以視為一個遊戲：玩家 1（∃）和玩家 2（∀）輪流設定變數的值，玩家 1 試圖讓 φ 為真，玩家 2 試圖讓 φ 為假。QSAT 為真當且僅當玩家 1 有必勝策略。

### 廣義地理遊戲

給定一個有向圖和一個起始頂點，兩個玩家輪流沿著邊移動一個標記，不能重複使用頂點。無法移動的玩家輸。判斷先手是否有必勝策略。

### 正規語言包含性

給定兩個正規表達式，它們描述的語言是否相等？

## Savitch 定理

Savitch 定理是空間複雜度中的一個重要結果：

> NSPACE(f(n)) ⊆ SPACE(f(n)²)

也就是說，非確定性空間可以以平方的代價被確定性空間模擬。這個定理的關鍵結論是：

> PSPACE = NPSPACE

在空間的世界裡，非確定性與確定性之間的差距沒有時間世界裡那麼大（時間世界裡 P vs NP 是否相等仍然未知）。

## PSPACE 與 NP 的關係

雖然我們知道 P ⊆ NP ⊆ PSPACE，但這些包含關係是否是嚴格的（即是否不等於）仍然是開放問題：

1. P = NP？這個問題還沒解決
2. NP = PSPACE？這也不太可能，但沒有證明
3. P = PSPACE？這更不太可能

如果 P = PSPACE，那麼 P = NP 也成立，因為 P ⊆ NP ⊆ PSPACE。

## 空間與時間的權衡

在計算中，時間和空間經常可以互相交換：

- **空間換時間**：使用記憶體來快取計算結果（如動態規劃）
- **時間換空間**：需要時重新計算而非儲存（如遞迴）

經典範例：計算 Fibonacci 數列

```
# 空間 O(n)，時間 O(n)
def fib_dp(n):
    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i-1] + dp[i-2])
    return dp[n]

# 空間 O(1)，時間 O(n)
def fib_const(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

## 空間複雜度的實際應用

空間複雜度的概念在現代軟體開發中至關重要：

- **大數據處理**：如何在有限記憶體中處理 TB 級資料
- **串流演算法**：使用次線性空間處理資料串流
- **資料壓縮**：在儲存空間和計算時間之間取得平衡
- **嵌入式系統**：在記憶體受限的環境中執行程式

## 延伸閱讀

- [PSPACE Complexity Class](https://www.google.com/search?q=PSPACE+complexity+class)
- [QSAT and PSPACE-Completeness](https://www.google.com/search?q=QSAT+PSPACE+complete)
- [Savitch Theorem](https://www.google.com/search?q=Savitch+theorem+proof)
