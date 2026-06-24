# 文章 2：NumPy 與矩陣運算

## 前言

NumPy 是 Python 數值計算的基礎，本章節介紹在影像處理中常用的矩陣運算。

## 影像作為矩陣

```python
import numpy as np
from PIL import Image

img = Image.open('image.jpg')
arr = np.array(img)

print(f"Shape: {arr.shape}")  # (H, W, C)
print(f"Dimensions: {arr.ndim}")  # 3
```

## 矩陣基本運算

### 元素級運算

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A + B)  # [[6, 8], [10, 12]]
print(A * B)  # [[5, 12], [21, 32]] 元素對應相乘
print(A @ B)  # 矩陣乘法
```

### 標量運算

```python
print(A * 2)  # 所有元素乘 2
print(A + 1)  # 所有元素加 1
```

## 矩陣切片

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print(arr[0, :])     # 第一行
print(arr[:, 0])     # 第一列
print(arr[1:3, 1:3]) # 子矩陣
```

## 矩陣轉置

```python
print(arr.T)  # 轉置矩陣
```

## 廣播機制

NumPy 自動擴展小型矩陣：

```python
# 影像亮度調整
brightness = 50
adjusted = img_array + brightness

# 對比度調整
contrast = 1.5
adjusted = (img_array - 128) * contrast + 128
```

## 線性代數函數

```python
A = np.array([[1, 2], [3, 4]])

# 行列式
det = np.linalg.det(A)

# 逆矩陣
A_inv = np.linalg.inv(A)

# 特徵值與特徵向量
eigenvalues, eigenvectors = np.linalg.eig(A)

# 奇異值分解
U, S, Vt = np.linalg.svd(A)
```

## 總結

NumPy 提供了豐富的矩陣運算功能，對影像處理與神經網路實現都至關重要。

## 延伸閱讀

- https://www.google.com/search?q=NumPy+matrix+operations+tutorial
- https://www.google.com/search?q=numpy+linear+algebra+linalg