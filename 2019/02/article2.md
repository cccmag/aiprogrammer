# NumPy 矩陣運算

## NumPy 簡介

NumPy 是 Python 數值計算的基礎庫，提供高效的多維陣列物件與矩陣運算功能。

## 建立陣列

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.zeros((3, 4))
c = np.ones((2, 3))
d = np.arange(0, 10, 2)
e = np.linspace(0, 1, 5)
f = np.random.rand(3, 3)

print(f"一維陣列: {a}")
print(f"零矩陣: {b.shape}")
print(f"單位陣列: {c.shape}")
print(f"等差陣列: {d}")
print(f"等分陣列: {e}")
```

## 基本運算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(f"加法: {a + b}")
print(f"減法: {a - b}")
print(f"乘法: {a * b}")
print(f"除法: {a / b}")
print(f"點積: {np.dot(a, b)}")
print(f"總和: {a.sum()}")
print(f"均值: {a.mean()}")
print(f"標準差: {a.std()}")
```

## 矩陣運算

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"矩陣乘法: \n{np.matmul(A, B)}")
print(f"矩陣轉置: \n{A.T}")
print(f"矩陣逆: \n{np.linalg.inv(A)}")
print(f"行列式: {np.linalg.det(A)}")
print(f"特徵值: {np.linalg.eigvals(A)}")
```

## 切片與索引

```python
a = np.arange(12).reshape(3, 4)
print(f"原始矩陣:\n{a}")
print(f"第一列: {a[0]}")
print(f"最後一列: {a[-1]}")
print(f"第一、二列: \n{a[:2]}")
print(f"第二、三列: \n{a[1:3]}")
print(f"特定元素: {a[1, 2]}")
print(f"列切片: {a[:, 0]}")
print(f"奇數行: \n{a[::2]}")
```

## 布林索引

```python
a = np.array([1, 2, 3, 4, 5, 6])
mask = a > 3
print(f"遮罩: {mask}")
print(f"過濾結果: {a[mask]}")

a[a > 3] = 0
print(f"條件賦值: {a}")
```

## 廣播（Broadcasting）

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([10, 20, 30])

print(f"矩陣 + 向量: \n{a + b}")

c = np.array([[10], [20]])
print(f"矩陣 + 向量(列): \n{a + c}")
```

## 統計函數

```python
a = np.arange(12).reshape(3, 4)

print(f"總和: {a.sum()}")
print(f"每列總和: {a.sum(axis=1)}")
print(f"每行總和: {a.sum(axis=0)}")
print(f"最大值: {a.max()}")
print(f"每行最大: {a.max(axis=1)}")
print(f"最大索引: {a.argmax()}")
print(f"累計和: {a.cumsum()}")
```

## 線性代數

```python
A = np.array([[1, 2], [3, 4]])
b = np.array([5, 6])

x = np.linalg.solve(A, b)
print(f"解向量: {x}")

A_inv = np.linalg.inv(A)
print(f"逆矩陣: \n{A_inv}")

eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"特徵值: {eigenvalues}")
print(f"特徵向量: \n{eigenvectors}")

U, s, Vt = np.linalg.svd(A)
print(f"SVD 奇異值: {s}")
```

## 亂數生成

```python
np.random.seed(42)

print(f"常態分佈: {np.random.randn(5)}")
print(f"均勻分佈: {np.random.rand(5)}")
print(f"整數亂數: {np.random.randint(1, 10, 5)}")
print(f"常態分佈(指定均值標準差): {np.random.normal(100, 15, 5)}")
print(f"排列: {np.random.permutation(10)}")
```

## 參考資源

- https://www.google.com/search?q=NumPy+tutorial+array+operations+Python+2019
- https://www.google.com/search?q=NumPy+matrix+multiplication+linear+algebra+scipy+2019
- https://www.google.com/search?q=NumPy+broadcasting+slicing+indexing+Python+2019