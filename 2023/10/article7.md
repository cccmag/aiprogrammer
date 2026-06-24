# 正則化路徑：L1 vs L2

## 兩種正則化的幾何直觀

L1 和 L2 正則化是最常用的兩種正則化技術。它們的區別在本質上是**幾何的**——約束區域的形狀決定了解的性質。

### 最佳化問題的等效形式

**L2 正則化**（Ridge）：

```
min (1/n)||Xw - y||²    subject to ||w||²₂ ≤ t
```

**L1 正則化**（Lasso）：

```
min (1/n)||Xw - y||²    subject to ||w||₁ ≤ t
```

### 約束區域的形狀

```
L2: 球形 —— 邊界光滑，無角點
L1: 菱形 —— 邊界有尖角（位於坐標軸上）
```

最優解通常是等誤差輪廓線與約束區域邊界的切點。L1 的尖角使得切點往往出現在坐標軸上——對應於某些權重為零。

## L2 正則化（Ridge）

### 閉式解

```
ŵ_ridge = (X^T X + λI)^{-1} X^T y
```

當 λ > 0 時，X^T X + λI 總是可逆的（即使 X^T X 奇異）。

### 奇異值分解視角

設 X = UDV^T，則：

```
ŵ_ridge = V (D² + λI)^{-1} D U^T y
```

與 OLS 解 ŵ_ols = V D^{-1} U^T y 相比，Ridge 將奇異值從 σ_i 變為 σ_i/(σ_i² + λ)：

- 大奇異值（主成分）幾乎不受影響
- 小奇異值（雜訊成分）被強烈壓縮
- 因此 Ridge 是「均勻收縮」

### 有效自由度

```
d_eff(λ) = Σ_{i=1}^d σ_i² / (σ_i² + λ)
```

- λ = 0：d_eff = d（無正則化）
- λ → ∞：d_eff → 0（完全正則化）

## L1 正則化（Lasso）

### 沒有閉式解

Lasso 沒有簡單的閉式解，但可以透過以下方法求解：

- **坐標下降**（Coordinate Descent）：每次優化一個 w_i
- **LARS**（Least Angle Regression）：逐步增加變量

### 稀疏性的來源

Lasso 的稀疏解源自 L1 範數的幾何特性：

```
次梯度條件：∂|w_i| = sign(w_i) if w_i ≠ 0
            ∂|w_i| ∈ [-1, 1] if w_i = 0
```

當 w_i = 0 時，只要資料與殘差的相關性低於 λ，w_i 就會保持在 0。

### 正則化路徑

隨著 λ 從大到小變化，Lasso 的解路徑會逐步納入更多變量：

```
λ_max → λ_min
變量數：0 → d（滿模型）
```

對於某些設計矩陣，Lasso 路徑是**分段線性**的。

## L1 vs L2 的比較

| 特性 | L2（Ridge） | L1（Lasso） |
|------|------------|------------|
| 解性質 | 均勻收縮 | 稀疏解 |
| 變量選擇 | 否 | 是 |
| 閉式解 | 是 | 否 |
| 群組效果 | 相關變量一起保留 | 選一個 |
| 預測表現 | 通常更好 | 變量選擇時好 |
| 計算 | O(d³) | O(d·n·λ_steps) |

## Elastic Net：兩者兼顧

Elastic Net 結合了 L1 和 L2：

```
min (1/n)||Xw - y||² + λ₁||w||₁ + λ₂||w||²₂
```

當 π = λ₂/(λ₁ + λ₂) = 0 時為 Lasso，π = 1 時為 Ridge。

**Elastic Net 的優勢**：
- 像 Lasso 一樣做變量選擇
- 像 Ridge 一樣處理群組效應（相關變量不會被隨機選一個）
- 在變量數大於樣本數（p > n）時仍然穩定

## 正則化參數的選擇

```python
from sklearn.linear_model import LassoCV, RidgeCV

# Lasso: 交叉驗證選擇 λ
lasso = LassoCV(cv=5).fit(X, y)
print(f"Best λ for Lasso: {lasso.alpha_}")

# Ridge: 交叉驗證選擇 λ
ridge = RidgeCV(cv=5).fit(X, y)
print(f"Best λ for Ridge: {ridge.alpha_}")
```

## 正則化路徑視覺化

Lasso 的正則化路徑（係數隨 λ 的變化）是評估特徵重要性的有力工具。隨著 λ 減小，係數逐一非零，形成一條「路徑」。

## 小結

選擇 L1 還是 L2 取決於具體問題：

| 場景 | 建議 |
|------|------|
| 所有特徵可能都有用 | L2（Ridge） |
| 預期只有少數特徵重要 | L1（Lasso） |
| 相關特徵需要一起保留 | Elastic Net |
| p >> n 且需要變量選擇 | Lasso 或 Elastic Net |

## 延伸閱讀

- [L1 vs L2 Regularization](https://www.google.com/search?q=L1+vs+L2+regularization+detailed+comparison)
- [Lasso Regularization Path](https://www.google.com/search?q=lasso+regularization+path+visualization)
- [Elastic Net Explained](https://www.google.com/search?q=elastic+net+regularization+explained)
