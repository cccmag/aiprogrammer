# 文章 3：線性代數進階

## 前言

深度學習依賴大量的線性代數運算。本章節介紹更深層的線性代數概念，包括特徵值分解與奇異值分解。

## 特徵值與特徵向量

對於方陣 A，若存在向量 v 與純量 λ：

```
Av = λv
```

則 v 為特徵向量，λ 為特徵值。

```python
import numpy as np

A = np.array([[4, 2], [1, 3]])

eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"Eigenvalues: {eigenvalues}")
print(f"Eigenvectors:\n{eigenvectors}")
```

## 奇異值分解（SVD）

對於任意矩陣 A：

```
A = U × Σ × Vᵀ
```

- U: 左奇異向量矩陣
- Σ: 奇異值對角矩陣
- Vᵀ: 右奇異向量矩陣的轉置

```python
A = np.array([[1, 2], [3, 4], [5, 6]])

U, S, Vt = np.linalg.svd(A)

print(f"U shape: {U.shape}")
print(f"S shape: {S.shape}")
print(f"Vt shape: {Vt.shape}")
```

## SVD 的應用

### 影像壓縮

```python
from PIL import Image

img = np.array(Image.open('image.jpg').convert('L'))

U, S, Vt = np.linalg.svd(img)

# 只保留前 k 個奇異值
k = 50
compressed = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

Image.fromarray(compressed.astype('uint8')).save('compressed.jpg')
```

### 降維

```python
def svd_reduction(X, n_components):
    U, S, Vt = np.linalg.svd(X - np.mean(X, axis=0))
    return U[:, :n_components] * S[:n_components]
```

## 行列式

行列式表示線性變換的面積（2D）或體積（3D）縮放因子：

```python
A = np.array([[4, 2], [1, 3]])
det_A = np.linalg.det(A)  # 10
```

## 矩陣範數

### Frobenius 範數

```python
norm_F = np.linalg.norm(A, 'fro')
```

### 譜範數

```python
norm_spec = np.linalg.norm(A, 2)
```

## 總結

特徵值分解與奇異值分解是機器學習與深度學習的數學基礎，從降維到神經網路權重分析都有應用。

## 延伸閱讀

- https://www.google.com/search?q=eigenvalue+eigenvector+SVD+deep+learning
- https://www.google.com/search?q=singular+value+decomposition+image+compression