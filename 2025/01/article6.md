# 函數進階：參數與回傳值

## 函數是一等公民

在 Python 中，函數是「一等公民」（first-class citizen），這意味著函數可以像其他資料型別一樣被傳遞：

```python
def say_hello(name):
    return f"你好，{name}"

def say_bye(name):
    return f"再見，{name}"

# 函數可以賦值給變數
greeting = say_hello
print(greeting("Alice"))  # 你好，Alice

# 函數可以作為參數傳遞
def greet_person(greet_func, name):
    return greet_func(name)

print(greet_person(say_hello, "Bob"))  # 你好，Bob
print(greet_person(say_bye, "Bob"))    # 再見，Bob
```

## Lambda 函數

Lambda 是 Python 中的匿名函數，適合用於簡單的運算：

```python
# 基本語法
square = lambda x: x ** 2
print(square(5))  # 25

# 多參數
add = lambda a, b: a + b
print(add(3, 7))  # 10

# 與高階函數結合
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(doubled)  # [2, 4, 6, 8, 10]
print(evens)    # [2, 4]

# 自訂排序
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]
sorted_students = sorted(students, key=lambda s: s["grade"])
print([s["name"] for s in sorted_students])  # ['Charlie', 'Alice', 'Bob']
```

## 閉包 (Closure)

閉包是能捕捉外部環境的函數：

```python
def make_multiplier(n):
    """建立一個乘以 n 的函數"""
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

### 實用範例：計數器

```python
def make_counter():
    count = [0]  # 使用列表來繞過不可變限制

    def counter():
        count[0] += 1
        return count[0]

    return counter

my_counter = make_counter()
print(my_counter())  # 1
print(my_counter())  # 2
print(my_counter())  # 3
```

## 裝飾器 (Decorator)

裝飾器是在不修改原函數的情況下擴充功能的方式：

```python
import time

def timer(func):
    """計算函數執行時間的裝飾器"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 執行時間：{elapsed:.4f} 秒")
        return result
    return wrapper

@timer
def slow_function():
    total = sum(range(1000000))
    return total

result = slow_function()
print(f"結果：{result}")
```

### 帶參數的裝飾器

```python
def repeat(times):
    """重複執行指定次數的裝飾器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"你好，{name}")

greet("Alice")
# 你好，Alice
# 你好，Alice
# 你好，Alice
```

## Partial 函數

`functools.partial` 可以用來固定某些參數：

```python
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)

print(square(5))  # 25
print(cube(5))    # 125
```

## 回傳多個值的內部機制

```python
def analyze(numbers):
    """回傳多個統計數據"""
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

# 回傳的其實是一個元組
result = analyze([1, 2, 3, 4, 5])
print(type(result))  # <class 'tuple'>
print(result)        # (1, 5, 3.0)

# 解包
minimum, maximum, average = analyze([1, 2, 3, 4, 5])
print(f"最小={minimum}, 最大={maximum}, 平均={average}")
```

## 實戰：策略模式

```python
from typing import Callable, List

def bubble_sort(items: List[int]) -> List[int]:
    """氣泡排序"""
    items = items.copy()
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items

def quick_sort(items: List[int]) -> List[int]:
    """快速排序"""
    if len(items) <= 1:
        return items
    pivot = items[0]
    less = [x for x in items[1:] if x <= pivot]
    greater = [x for x in items[1:] if x > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)

def sort_data(data: List[int], strategy: Callable) -> List[int]:
    """根據選擇的策略排序"""
    return strategy(data)

data = [64, 34, 25, 12, 22, 11, 90]
print(f"氣泡排序：{sort_data(data, bubble_sort)}")
print(f"快速排序：{sort_data(data, quick_sort)}")
```

## 小結

Python 的函數遠比表面看起來強大。從 lambda 到裝飾器，從閉包到策略模式，函數式程式設計的技巧能讓你的程式碼更簡潔、更靈活、更容易測試。理解這些概念，是從初級開發者邁向進階開發者的重要一步。

---

**延伸閱讀**

- [Python 官方文件 — 裝飾器](https://www.google.com/search?q=Python+decorators+tutorial)
- [Python functools 模組](https://www.google.com/search?q=Python+functools+module)
