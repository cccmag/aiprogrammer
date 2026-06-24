# 文章 3：線性代數與神經網路

## 前言

線性代數是理解神經網路的數學基礎。本章節介紹神經網路中常用的線性代數概念與運算。

## 向量

向量是有大小與方向的數學物件，在神經網路中表示輸入特徵：

```python
import numpy as np

x = np.array([1, 2, 3])
w = np.array([0.1, 0.2, 0.3])
z = np.dot(w, x)  # 內積：1*0.1 + 2*0.2 + 3*0.3 = 1.4
```

## 矩陣

矩陣是二維數組，在神經網路中表示權重：

```python
W = np.array([[1, 2, 3],
              [4, 5, 6]])  # 2x3 矩陣
```

### 矩陣加法

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = A + B  # [[6, 8], [10, 12]]
```

### 矩陣乘法

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = A @ B  # [[19, 22], [43, 50]]
```

## 矩陣轉置

```python
A = np.array([[1, 2, 3], [4, 5, 6]])
A_T = A.T
# [[1, 4],
#  [2, 5],
#  [3, 6]]
```

## 單位矩陣與逆矩陣

```python
I = np.eye(3)  # 3x3 單位矩陣
A_inv = np.linalg.inv(A)  # A 的逆矩陣
```

## 元素對應運算 vs 矩陣乘法

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 元素對應相乘
A * B  # [[5, 12], [21, 32]]

# 矩陣乘法
A @ B  # [[19, 22], [43, 50]]
```

## 神經網路中的線性代數

### 前向傳播

```
z = Wx + b
```

```python
W = np.random.randn(128, 784)  # 權重矩陣
x = np.random.randn(784, 32)    # 輸入向量（批次）
b = np.zeros((128, 1))          # 偏置

z = W @ x + b                   # 加權和
a = relu(z)                     # 激活
```

### 反向傳播

梯度計算涉及矩陣轉置：

```python
dL/dW = delta @ x.T
dL/db = sum(delta, axis=1, keepdims=True)
```

## 總結

線性代數提供了描述與操作神經網路的數學語言。掌握矩陣運算對理解網路原理與除錯至關重要。

## 延伸閱讀

- https://www.google.com/search?q=linear+algebra+neural+network+basics
- https://www.google.com/search?q=matrix+operations+deep+learning