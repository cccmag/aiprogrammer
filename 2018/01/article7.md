# 線性代數基礎

## 簡介

線性代數是機器學習與深度學習的數學基礎。本篇介紹向量、矩陣運算及其在 Python 中的實現。

## 向量

### 什麼是向量

向量是有大小和方向的量，在機器學習中通常表示為一維陣列。

```python
import numpy as np

# 建立向量
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

print(f"v1 = {v1}")
print(f"v2 = {v2}")
```

### 向量基本運算

```python
# 加法
v_sum = v1 + v2
print(f"v1 + v2 = {v_sum}")  # [5, 7, 9]

# 純量乘法
v_scaled = 2 * v1
print(f"2 * v1 = {v_scaled}")  # [2, 4, 6]

# 減法
v_diff = v2 - v1
print(f"v2 - v1 = {v_diff}")  # [3, 3, 3]
```

### 向量內積（點積）

```python
# 內積
dot_product = np.dot(v1, v2)
print(f"v1 · v2 = {dot_product}")  # 1*4 + 2*5 + 3*6 = 32

# 也可用 @
print(f"v1 @ v2 = {v1 @ v2}")  # 32
```

### 向量大小（範數）

```python
# L2 範數（歐氏距離）
v = np.array([3, 4])
norm = np.linalg.norm(v)
print(f"||v|| = {norm}")  # 5.0

# 手動計算
manual_norm = np.sqrt(np.sum(v ** 2))
print(f"手動計算: {manual_norm}")  # 5.0
```

## 矩陣

### 建立矩陣

```python
import numpy as np

# 2x3 矩陣
A = np.array([[1, 2, 3],
              [4, 5, 6]])
print("矩陣 A:")
print(A)

# 單位矩陣
I = np.eye(3)
print("\n單位矩陣 I:")
print(I)

# 零矩陣
Z = np.zeros((2, 3))
print("\n零矩陣:")
print(Z)
```

### 矩陣基本運算

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 加法
C = A + B
print("A + B:")
print(C)

# 純量乘法
D = 2 * A
print("\n2 * A:")
print(D)

# 矩陣乘法
E = np.dot(A, B)
print("\nA @ B:")
print(E)
```

### 矩陣轉置

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])

A_T = A.T
print("轉置後:")
print(A_T)
```

### 矩陣的逆

```python
A = np.array([[1, 2], [3, 4]])
A_inv = np.linalg.inv(A)
print("A 的逆矩陣:")
print(A_inv)

# 驗證
identity = np.dot(A, A_inv)
print("\nA @ A^(-1) = I:")
print(identity)
```

## NumPy 函式

### 矩陣生成

```python
# 亂數矩陣
np.random.seed(42)
rand_matrix = np.random.rand(3, 3)
print("隨機矩陣:")
print(rand_matrix)

# 範圍陣列
arr = np.arange(0, 10, 2)  # 0, 2, 4, 6, 8
print(f"\narange: {arr}")

# 重塑矩陣
arr = np.arange(12)
matrix = arr.reshape(3, 4)
print("\n重塑後 (3x4):")
print(matrix)
```

### 統計函式

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])

print(f"總和: {np.sum(A)}")
print(f"每列總和: {np.sum(A, axis=1)}")
print(f"每行總和: {np.sum(A, axis=0)}")
print(f"平均值: {np.mean(A)}")
print(f"標準差: {np.std(A)}")
```

## 矩陣在機器學習中的應用

### 線性迴歸矩陣形式

```python
# y = Xw + b
# 使用矩陣運算快速計算

X = np.array([[1, 1], [1, 2], [1, 3]])  # 特徵矩陣（加一列1）
y = np.array([2, 4, 6])  # 目標值

# 最小二乘法：w = (X^T X)^(-1) X^T y
XtX = np.dot(X.T, X)
XtX_inv = np.linalg.inv(XtX)
Xty = np.dot(X.T, y)
w = np.dot(XtX_inv, Xty)

print(f"係數: {w}")  # [0, 2] 表示 y = 0 + 2x
```

### 多層神經網路前向傳播

```python
# 輸入層到隱藏層
X = np.array([[1, 0, 1]])  # 輸入
W1 = np.random.rand(3, 4)  # 權重
b1 = np.zeros((1, 4))     # 偏差

Z1 = np.dot(X, W1) + b1   # 線性組合
A1 = 1 / (1 + np.exp(-Z1))  # Sigmoid 激活

print("隱藏層輸出:")
print(A1)
```

## 練習題

1. 計算向量 v = [1, 2, 3] 和 w = [4, 5, 6] 的內積與夾角
2. 建立一個 3x3 單位矩陣並計算其逆矩陣
3. 實現兩個矩陣的乘法函式（不使用 np.dot）
4. 將以下線性方程組用矩陣形式表示並求解：
   - 2x + y = 5
   - x + 3y = 6