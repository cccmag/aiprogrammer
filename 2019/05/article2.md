# NumPy 強化：廣播機制詳解

## 前言

NumPy 的廣播機制使得不同形狀的陣列之間可以進行運算，大幅簡化程式碼。

## 廣播規則

```python
import numpy as np

# 基本例子
a = np.array([1, 2, 3])
b = 2
print(a * b)  # [2, 4, 6]
# b 被廣播為 [2, 2, 2]
```

## 二維廣播

```python
# 3x3 矩陣加上 1x3 向量
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
b = np.array([1, 2, 3])

print(A + b)
# [[2, 4, 6],
#  [5, 7, 9],
#  [8, 10, 12]]
```

## 高維廣播

```python
# (3, 3, 3) + (3,) → (3, 3, 3)
# 向量被廣播到所有切片
```

## 實際應用

```python
# 影像正規化
image = np.random.rand(100, 100, 3)
image = (image - image.mean(axis=(0, 1))) / image.std(axis=(0, 1))
```

## 延伸閱讀

- [NumPy 廣播文檔](https://www.google.com/search?q=numpy+broadcasting)