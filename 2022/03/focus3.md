# SciPy 科學計算函式庫

## SciPy 的定位

SciPy（Scientific Python）是建立在 NumPy 基礎之上的科學計算函式庫。如果說 NumPy 提供了多維陣列的基礎結構，SciPy 則提供了一系列高階的科學計算演算法。它的子模組涵蓋了從線性代數到數值積分，從最佳化到訊號處理的廣泛領域。

```
scipy
├── linalg    — 線性代數（擴展 NumPy）
├── optimize  — 最佳化與求根
├── integrate — 數值積分
├── signal    — 訊號處理
├── stats     — 統計分佈與檢定
├── sparse    — 稀疏矩陣
├── fft       — 快速傅立葉轉換
├── ndimage   — 多維影像處理
├── interpolate — 內插
└── spatial   — 空間演算法
```

## 線性代數：scipy.linalg

SciPy 的線性代數模組是 LAPACK 和 BLAS 的高階封裝。

```python
import numpy as np
from scipy import linalg

A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])

# 解線性方程組
x = linalg.solve(A, b)

# 特徵值與特徵向量
eigvals, eigvecs = linalg.eig(A)

# SVD 分解
U, s, Vt = linalg.svd(A)
```

## 最佳化：scipy.optimize

提供多種最佳化演算法，從無約束最佳化到帶約束的非線性規劃：

```python
from scipy.optimize import minimize

# Rosenbrock 函式最佳化
def rosen(x):
    return sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

res = minimize(rosen, [0, 0], method="nelder-mead")
print(res.x)  # 接近 [1, 1]
```

## 數值積分：scipy.integrate

```python
from scipy.integrate import quad, solve_ivp

# 數值積分
result, error = quad(lambda x: x**2, 0, 1)

# 解常微分方程組
def ode(t, y):
    return [-y[1], y[0]]
sol = solve_ivp(ode, [0, 10], [1, 0])
```

## 統計分析：scipy.stats

提供數百種機率分佈和統計檢定：

```python
from scipy import stats

# 常態分佈
rv = stats.norm(loc=0, scale=1)
rv.pdf(0)      # 0.3989
rv.cdf(1.96)   # 0.975

# 統計檢定
t_stat, p_val = stats.ttest_ind(sample_a, sample_b)
```

## 訊號處理：scipy.signal

```python
from scipy import signal

# FIR 濾波器設計
b = signal.firwin(21, 0.3, window="hamming")
filtered = signal.lfilter(b, 1.0, noisy_signal)
```

## 稀疏矩陣：scipy.sparse

處理大規模稀疏資料時，稀疏矩陣可以大幅節省記憶體：

```python
from scipy.sparse import csr_matrix

# 建立稀疏矩陣
sparse_mat = csr_matrix((data, (rows, cols)), shape=(N, M))

# 稀疏線性代數
from scipy.sparse.linalg import spsolve
x = spsolve(sparse_mat, b)
```

## SciPy 的應用場景

- **物理模擬**：解偏微分方程、模擬動力系統
- **金融工程**：投資組合最佳化、蒙地卡羅模擬
- **生物資訊**：序列比對、訊號處理
- **影像處理**：濾波、形態學運算
- **統計建模**：假設檢定、分佈擬合

## 延伸閱讀

- [SciPy 官方教學](https://www.google.com/search?q=SciPy+tutorial)
- [SciPy 線性代數](https://www.google.com/search?q=SciPy+linear+algebra)
- [SciPy 最佳化指南](https://www.google.com/search?q=SciPy+optimization)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」歷史回顧系列之一。*
