# 線性代數複習

## 向量

```python
import numpy as np

# 向量創建
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 向量加法
c = a + b  # [5, 7, 9]

# 向量減法
d = a - b  # [-3, -3, -3]

# 純量乘法
e = 2 * a  # [2, 4, 6]

# 點積 (Dot Product)
dot = np.dot(a, b)  # 1*4 + 2*5 + 3*6 = 32

# 向量大小
norm = np.linalg.norm(a)  # sqrt(1+4+9) = sqrt(14)

# 夾角
cos_angle = dot / (np.linalg.norm(a) * np.linalg.norm(b))
```

## 矩陣

```python
# 矩陣創建
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 矩陣加法
C = A + B

# 矩陣乘法
D = np.matmul(A, B)
E = A @ B  # Python 3.5+

# 純量乘法
F = 3 * A

# 轉置
AT = A.T

# 逆矩陣
A_inv = np.linalg.inv(A)
```

## 矩陣運算性質

```python
# 結合律
(A @ B) @ C == A @ (B @ C)

# 分配律
A @ (B + C) == A @ B + A @ C

# 轉置性質
(A @ B).T == B.T @ A.T

# 逆性質
(A @ B).I == B.I @ A.I  # 假設皆可逆
```

## 特殊矩陣

```python
# 單位矩陣
I = np.eye(3)

# 對角矩陣
D = np.diag([1, 2, 3])

# 零矩陣
Z = np.zeros((3, 3))

# 對稱矩陣
S = np.array([[1, 2], [2, 1]])
```

## 行列式

```python
A = np.array([[1, 2], [3, 4]])
det = np.linalg.det(A)  # -2

# 特性
# det(AB) = det(A) * det(B)
# det(A^T) = det(A)
# det(A^-1) = 1 / det(A)
```

## 特徵值與特徵向量

```python
A = np.array([[2, 1], [1, 2]])

eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"特徵值: {eigenvalues}")
print(f"特徵向量:\n{eigenvectors}")

# 驗證：Av = λv
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    print(f"A @ v{i} = {A @ v}")
    print(f"λ{i} * v{i} = {lam * v}")
```

## 奇異值分解（SVD）

```python
A = np.array([[1, 2], [3, 4], [5, 6]])

U, S, VT = np.linalg.svd(A)

print(f"U shape: {U.shape}")
print(f"S: {S}")
print(f"VT shape: {VT.shape}")
```

## 線性系統求解

```python
# Ax = b，求 x
A = np.array([[1, 2], [3, 4]])
b = np.array([5, 11])

# 方法 1：使用 linalg.solve
x = np.linalg.solve(A, b)

# 方法 2：使用逆矩陣
x = np.linalg.inv(A) @ b

# 方法 3：使用 lstsq（適用於超定系統）
x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
```

## 在機器學習中的應用

```python
# 線性迴歸：y = Xw，求 w
# w = (X^T X)^-1 X^T y

X = np.array([[1, 1], [1, 2], [1, 3]])
y = np.array([1, 2, 3])

w = np.linalg.inv(X.T @ X) @ X.T @ y
print(f"線性迴歸係數: {w}")

# 主成分分析（PCA）
# 使用 SVD 分解
```

## 總結

線性代數是機器學習與深度學習的數學基礎。掌握向量、矩陣運算、特徵值分解等概念，對理解神經網路的原理至關重要。