# Python 函式式程式設計技巧

## Python 的函式式支援

Python 從誕生之初就支援多種函式式特性：

- Lambda 表達式
- map、filter、reduce
- 生成器和產生器表達式
- 閉包和高階函式
- 列表/字典/集合推导式

## 函式式工具模組

`functools` 和 `itertools` 提供了豐富的函式式工具：

```python
from functools import reduce, lru_cache, partial
from itertools import takewhile, dropwhile, groupby, compress

# reduce：聚合運算
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
print(f"Product: {product}")  # 120

# lru_cache：記憶化
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# partial：部分應用
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# itertools
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# takewhile：滿足條件時繼續取值
list(takewhile(lambda x: x < 5, data))  # [1, 2, 3, 4]

# dropwhile：跳過滿足條件的元素直到條件不滿足
list(dropwhile(lambda x: x < 5, data))  # [5, 6, 7, 8, 9, 10]
```

## 管道式程式設計

使用 Python 的管道運算子模式：

```python
from dataclasses import dataclass
from typing import TypeVar, Callable

T = TypeVar('T')
U = TypeVar('U')

@dataclass
class Pipeline:
    value: any

    def pipe(self, f: Callable) -> 'Pipeline':
        """將函式應用於當前值"""
        return Pipeline(f(self.value))

    def __rshift__(self, f: Callable) -> 'Pipeline':
        """使用 >> 作為 pipe 的運算子"""
        return self.pipe(f)

# 範例
result = (
    Pipeline([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    >> (lambda x: filter(lambda v: v % 2 == 0, x))
    >> (lambda x: map(lambda v: v ** 2, x))
    >> list
)
print(result)  # [4, 16, 36, 64, 100]
```

## 函數裝飾器

裝飾器是 Python 中函式式編程的經典應用：

```python
from functools import wraps
import time

def timing(f):
    """測量函式執行時間"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(f"{f.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper

def memoize(f):
    """記憶化裝飾器"""
    cache = {}
    @wraps(f)
    def wrapper(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return wrapper

@memoize
def expensive_computation(n):
    """昂貴的計算"""
    return sum(i**2 for i in range(n))
```

## 生成器與惰性求值

生成器實現惰性求值，適合處理大型資料：

```python
# 無限序列
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 取前 N 個
fibs = fibonacci()
first_10 = [next(fibs) for _ in range(10)]

# 生成器管道
def filter_gen(pred, gen):
    for x in gen:
        if pred(x):
            yield x

def map_gen(f, gen):
    for x in gen:
        yield f(x)

# 使用
result = list(map_gen(lambda x: x*2,
                      filter_gen(lambda x: x % 2 == 0,
                                fibonacci())))
```

## 運算子模組

`operator` 模組提供函式形式的基本運算子：

```python
from operator import add, mul, itemgetter, attrgetter

# 替代 lambda
numbers = [(1, 5), (3, 2), (1, 3), (2, 8)]
sorted(numbers, key=lambda x: x[1])  # 使用 lambda
sorted(numbers, key=itemgetter(1))   # 使用 itemgetter

# 組合
result = reduce(mul, map(add, [1, 2, 3], [4, 5, 6]))
# = reduce(mul, [5, 7, 9])
# = 315
```

## 小結

Python 的函式式特性讓你能以多種風格編寫程式。善用這些工具可以讓程式碼更簡潔、更表達力更強。

延伸閱讀：
- [Google 搜尋：Python functional programming](https://www.google.com/search?q=Python+functional+programming)
- [Google 搜尋：Python functools itertools](https://www.google.com/search?q=Python+functools+itertools)