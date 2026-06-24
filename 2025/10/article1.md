# 裝飾器實作與應用

## 1. 引言

裝飾器是 Python 中最優雅也最具威力的語言特性之一。它讓開發者可以在不修改函式原始碼的情況下，為函式添加額外的行為。從 Web 框架的路由系統到 pytest 的 fixture，從快取機制到權限驗證，裝飾器無處不在。

## 2. 裝飾器的實作原理

裝飾器的本質是高階函式——接受一個函式作為參數，返回一個新的函式。Python 的 `@` 語法只是語法糖：

```python
# 這兩種寫法完全等價
@decorator
def func(): ...

func = decorator(func)
```

## 3. 實作一個完整的計時裝飾器

一個實用的計時裝飾器需要考慮多種邊界情況：

```python
import time
from functools import wraps

def timer(print_args=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            info = f"{func.__name__}"
            if print_args:
                info += f"({args}, {kwargs})"
            print(f"[timer] {info}: {elapsed:.4f}s")
            return result
        return wrapper
    return decorator

@timer(print_args=True)
def slow_add(a, b):
    time.sleep(0.1)
    return a + b

print(slow_add(3, 5))
```

## 4. 記憶化裝飾器

記憶化（memoization）是裝飾器的經典應用——快取函式的計算結果：

```python
from functools import wraps

def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 快！每個值只計算一次
print(fibonacci(100))
```

Python 3.9 以後有 `functools.cache` 可以直接使用。

## 5. 類別裝飾器

裝飾器也可以用類別實作，適合需要維護狀態的場景：

```python
class Retry:
    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_attempts - 1:
                        raise
                    print(f"重試 {attempt + 1}/{self.max_attempts}")
        return wrapper

@Retry(max_attempts=3)
def unstable_api():
    import random
    if random.random() < 0.7:
        raise ConnectionError("連線失敗")
    return "成功!"
```

## 6. 裝飾器的疊加與順序

多個裝飾器疊加時，應用順序從內到外：

```python
@timer
@memoize
def expensive(n):
    # memoize 先應用，timer 在外層
    total = 0
    for i in range(n):
        total += i
    return total
```

## 7. 實戰案例

**Flask 風格的路由裝飾器**：

```python
class Router:
    def __init__(self):
        self.routes = {}
    
    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

router = Router()

@router.route("/hello")
def hello():
    return "Hello, World!"

@router.route("/bye")
def bye():
    return "Goodbye!"
```

## 8. 總結

裝飾器是 Python 函數式程式設計的基石。掌握裝飾器的實作原理，不僅可以寫出更乾淨、更可重用的程式碼，還能深入理解 Python 物件模型的底層機制。

## 延伸閱讀

- [Python functools 官方文件](https://www.google.com/search?q=Python+functools+module+documentation)
- [Real Python: Python Decorators 101](https://www.google.com/search?q=Real+Python+decorators+101)
