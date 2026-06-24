# doctest 與文件測試一體化

## doctest 的核心理念

doctest 將測試直接嵌入文件字串中，實現「文件即測試、測試即文件」的理想。這種方式特別適合教學程式碼、範例程式碼、以及需要強調正確性的 API 文件。

## 基本用法

```python
def add(a, b):
    """
    兩數相加

    >>> add(1, 2)
    3
    >>> add(-1, 1)
    0
    """
    return a + b
```

文件中的 `>>>` 開頭的行是互動式 Python 會話，下一行是預期輸出。執行 `doctest.testmod()` 即可驗證。

## 測試所有情況

doctest 適合驗證函式行為的各種情況：

```python
def factorial(n):
    """
    計算階層

    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    >>> factorial(-1)
    Traceback (most recent call last):
    ...
    ValueError: n must be non-negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

`ELLIPSIS` 標記允許部分輸出匹配，`Traceback` 區塊可測試異常情況。

## 在模組級別使用

doctest 不只可以用在函式文件，整個模組也可以有頂層文件：

```python
"""
這個模組提供數學運算函式

範例用法：
>>> import math_operations
>>> math_operations.square(5)
25
"""

def square(x):
    return x * x
```

## 與 unittest 整合

doctest 可以與 unittest 框架整合：

```python
import unittest
import doctest
import my_module

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(doctest.DocTestSuite(my_module))
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
```

這樣就能在統一的測試介面中執行所有測試。

## 優點與限制

doctest 的優點是直觀、文件與測試一體、易於維護簡單函式。但它不適合複雜的測試場景，因為文件字串中的程式碼難以除錯和重構。

## 最佳實踐

對公共 API 編寫 doctest，確保範例程式碼的正確性；對複雜邏輯使用 pytest 或 unittest。同時使用兩種測試方法，可以獲得文件品質和測試覆蓋率的雙重保障。