# NumPy 陣列運算

## ndarray 核心結構

NumPy 最核心的資料結構是 `ndarray`（N 維陣列）。不同於 Python 原生的 list，ndarray 要求所有元素類型相同，這使得它在記憶體佈局上極為緊湊，同時讓向量化運算成為可能。

```
ndarray 的記憶體佈局：

┌──────┬──────┬──────┬──────┬──────┬──────┐
│ d0   │ d1   │ d2   │ d3   │ d4   │ d5   │
├──────┼──────┼──────┼──────┼──────┼──────┤
│float64│      │      │      │      │      │
├──────┴──────┴──────┴──────┴──────┴──────┤
│  連續記憶體區塊（C-contiguous）            │
└─────────────────────────────────────────────┘
```

ndarray 的關鍵屬性：
- `ndarray.shape` — 各維度大小
- `ndarray.dtype` — 元素資料類型
- `ndarray.strides` — 各維度步長
- `ndarray.ndim` — 維度數量

```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape)    # (2, 3)
print(a.dtype)    # int64
print(a.strides)  # (24, 8)
```

## 向量化運算

NumPy 的向量化是資料科學效能的核心。不用撰寫迴圈，而是直接對整個陣列進行操作，底層由 C 和 Fortran 進行最佳化。

```python
import numpy as np

# Python 迴圈 vs NumPy 向量化
n = 10_000_000
a = np.random.randn(n)
b = np.random.randn(n)

# Python 迴圈（慢）
# c = [a[i] + b[i] for i in range(n)]

# NumPy 向量化（快 100 倍）
c = a + b
```

常見的向量化運算：
- **算術運算**：`+`, `-`, `*`, `/`, `**`
- **比較運算**：`>`, `<`, `==`, `!=`
- **通用函數**：`np.sin()`, `np.exp()`, `np.log()`
- **聚合運算**：`a.sum()`, `a.mean()`, `a.max()`

## 陣列建立

NumPy 提供多種建立陣列的方式：

```python
np.zeros((3, 4))      # 全零陣列
np.ones((2, 3))       # 全一陣列
np.eye(4)             # 單位矩陣
np.arange(10)         # 0..9
np.linspace(0, 1, 5)  # [0.0, 0.25, 0.5, 0.75, 1.0]
np.random.randn(3, 3)  # 標準常態分佈
```

## 索引與切片

NumPy 的索引語法比 Python list 更加強大：

```python
a = np.random.randn(5, 5)

# 基本切片
a[1:4, 2:5]

# 花式索引
a[[0, 2, 4]]

# 布林索引
a[a > 0]
```

## 通用函數（ufunc）

通用函數是 NumPy 向量化的基石。它們對陣列中每個元素獨立執行相同操作，並自動處理不同形狀陣列的廣播：

```python
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)  # 對整個陣列執行 sin

# ufunc 的 reduce 操作
np.add.reduce([1, 2, 3, 4])  # 10
```

## 延伸閱讀

- [NumPy 官方快速入門](https://www.google.com/search?q=NumPy+quickstart)
- [NumPy 廣播機制詳解](https://www.google.com/search?q=NumPy+broadcasting)
- [NumPy 索引指南](https://www.google.com/search?q=NumPy+indexing)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」歷史回顧系列之一。*
