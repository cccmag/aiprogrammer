# ML Theory：機器學習理論 Python 實作

## 概述

`ml_theory.py` 是一個展示機器學習理論四大核心概念的 Python 套件：

1. **VC 維度計算**——區間的分類器和感知機的 VC 維度
2. **偏差-變異分解**——多項式回歸中的偏差與變異權衡
3. **核函數計算**——RBF、多項式、線性核的實作與核矩陣
4. **貝氏更新**——Beta-Binomial 共軛先驗的後驗計算

## 核心概念

### 1. VC 維度

```python
def vc_dimension_intervals():
    return 2  # 實數線上的區間 VC 維度為 2

def vc_dimension_perceptron():
    return lambda d: d + 1  # d 維感知機 VC 維度為 d+1
```

VC 維度是假說空間打散（shatter）樣本點的最大數量。區間分類器的 VC 維度為 2，因為最多只能將 2 個點的所有 4 種標記方式都完美分類。

### 2. 偏差-變異分解

```python
bv = bias_variance_decomposition(degree=3)
# => {bias_sq: 0.0035, variance: 0.0074, ...}
```

透過多項式回歸模擬真實函數 sin(x)，用蒙特卡羅方法估計偏差平方和變異。檢查 `bias_sq + variance ≈ expected_error` 即可驗證分解的正確性。

### 3. 核函數

```python
kernel_functions([1,2], [3,4], 'rbf', 0.5)  # => 0.0183
kernel_functions([1,2], [3,4], 'polynomial', 3)  # => 1728.0
kernel_matrix(X, 'rbf', 0.5)  # => 4x4 核矩陣
```

實作了三種常見核函數：RBF（徑向基函數）、多項式核、線性核。核矩陣滿足 Mercer 條件，是 RKHS 的核心工具。

### 4. 貝氏更新

```python
bayesian_update(prior_alpha=2, prior_beta=2, heads=7, tails=3)
# => posterior: Beta(9, 5), posterior_mean: 0.6429
```

使用 Beta 分佈作為 Bernoulli 試驗的共軛先驗。先驗 Beta(2,2) 表示均勻的先驗信念，經過 10 次試驗（7 正 3 反）後更新為 Beta(9,5)。

## 執行結果

```
=== Machine Learning Theory Demo ===

--- VC Dimension ---
VC dimension of intervals on real line: 2
VC dimension of d-dim perceptron: d+1

--- Bias-Variance Decomposition ---
  bias_sq: 0.0035
  variance: 0.0074
  bias_sq + variance: 0.0108

--- Kernel Functions ---
  RBF kernel (gamma=0.5): 0.0183
  Polynomial kernel (d=3): 1728.0000
  Linear kernel: 11.0000

--- Bayesian Update ---
  prior: Beta(2,2)
  posterior: Beta(9,5)
  posterior_mean: 0.6429
```

## 學習理論的四個面向

| 概念 | 對應程式 | 核心公式 |
|------|---------|---------|
| 假說空間複雜度 | VC 維度函數 | VC(H) |
| 錯誤分解 | 偏差-變異函數 | Err = Bias² + Var + σ² |
| 特徵映射 | 核函數矩陣 | K(x,y) = ⟨φ(x), φ(y)⟩ |
| 不確定性量化 | 貝氏更新 | P(θ|D) ∝ P(D|θ) P(θ) |

## 延伸閱讀

- [完整程式碼](_code/ml_theory.py)
- [scikit-learn VC dimension tools](https://www.google.com/search?q=scikit+learn+VC+dimension)
- [Bias-Variance Decomposition](https://www.google.com/search?q=bias+variance+decomposition+explained)
- [Kernel Methods](https://www.google.com/search?q=kernel+method+machine+learning)
- [Conjugate Prior](https://www.google.com/search?q=conjugate+prior+Beta+distribution)
