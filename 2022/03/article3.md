# 線性代數與矩陣分解

## 線性代數在資料科學的角色

線性代數是資料科學的數學基石。從主成分分析（PCA）到奇異值分解（SVD），從線性迴歸到神經網路，幾乎所有機器學習演算法都離不開矩陣運算。

## NumPy 與 SciPy 的線性代數工具

NumPy 提供了基本的線性代數功能，而 SciPy 則提供了更完整的 LAPACK 介面。

```python
import numpy as np
from scipy import linalg

A = np.array([[3, 1, 1],
              [1, 3, 1],
              [1, 1, 3]])
```

## LU 分解

將矩陣分解為下三角（L）和上三角（U）矩陣的乘積：

```python
P, L, U = linalg.lu(A)
# A = P @ L @ U
```

## QR 分解

正交-三角分解，常用於求解最小平方法問題：

```python
Q, R = linalg.qr(A)
# A = Q @ R，其中 Q 是正交矩陣
```

## 特徵分解

對稱矩陣的特徵分解是 PCA 的核心：

```python
eigvals, eigvecs = linalg.eigh(A)  # 對稱矩陣專用
# A = V @ diag(λ) @ V^T
print(f"Eigenvalues: {eigvals}")
```

```python
# 實作 PCA
def pca(X, n_components):
    X_centered = X - X.mean(axis=0)
    cov = X_centered.T @ X_centered / (X.shape[0] - 1)
    eigvals, eigvecs = linalg.eigh(cov)
    idx = np.argsort(eigvals)[::-1][:n_components]
    return eigvecs[:, idx]
```

## SVD 分解

奇異值分解是最通用的矩陣分解方法，適用於任意矩陣：

```python
U, s, Vt = linalg.svd(A)
# A = U @ diag(s) @ Vt

# SVD 的應用：矩陣近似
k = 2
A_approx = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
```

SVD 的應用範圍極廣：
- **降維**：截斷 SVD 即為 PCA
- **推薦系統**：協同過濾的基礎
- **壓縮**：保留最大的奇異值
- **去噪**：捨棄小的奇異值

## Cholesky 分解

對正定矩陣進行三角分解，比 LU 快兩倍：

```python
L = linalg.cholesky(A, lower=True)
# A = L @ L^T
```

Cholesky 分解在蒙地卡羅模擬中尤為重要——從多變量常態分佈取樣：

```python
def multivariate_normal_sample(mean, cov, n=1):
    L = linalg.cholesky(cov, lower=True)
    z = np.random.randn(n, len(mean))
    return mean + z @ L.T
```

## 線性方程組求解

```python
b = np.array([5, 5, 5])
x = linalg.solve(A, b)  # 比 A^{-1} @ b 更快更穩定
```

## 延伸閱讀

- [線性代數與機器學習](https://www.google.com/search?q=linear+algebra+for+machine+learning)
- [SVD 視覺化解釋](https://www.google.com/search?q=SVD+visual+explanation)
- [SciPy 線性代數文件](https://www.google.com/search?q=SciPy+linear+algebra+documentation)
