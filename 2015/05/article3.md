# 裝飾器的藝術

## 裝飾器基礎

裝飾器是 Python 中一種強大但不容易理解的特性。它允許你在不修改原函式的情況下，動態地新增功能。

## 簡單範例

### 無引數裝飾器

```python
def my_decorator(func):
    """包裝函式的包裝器"""
    def wrapper(*args, **kwargs):
        print("在函式執行之前")
        result = func(*args, **kwargs)
        print("在函式執行之後")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# 相當於：say_hello = my_decorator(say_hello)

say_hello()
```

輸出：
```
在函式執行之前
Hello!
在函式執行之後
```

### 帶引數的裝飾器

```python
def repeat(times):
    """重複執行指定次數"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    return f"Hello, {name}!"

print(greet("小明"))
# ['Hello, 小明!', 'Hello, 小明!', 'Hello, 小明!']
```

## 常見應用

### 計時裝飾器

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)  # 保留原函式的名稱和文件字串
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 執行時間：{end - start:.4f} 秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "完成"

slow_function()
# slow_function 執行時間：1.0023 秒
```

### 日誌裝飾器

```python
import logging

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"呼叫 {func.__name__}，參數：{args}, {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} 回傳：{result}")
        return result
    return wrapper

@log
def add(a, b):
    return a + b
```

### 驗證裝飾器

```python
def validate(**validators):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for key, validator in validators.items():
                if key in kwargs:
                    value = kwargs[key]
                    if not validator(value):
                        raise ValueError(f"無效的 {key}: {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate(age=lambda x: x >= 0, name=lambda x: len(x) > 0)
def create_user(name, age):
    return {"name": name, "age": age}

create_user("小明", 25)  # OK
# create_user("", -1)  # 會引發 ValueError
```

### 快取裝飾器

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 快取結果，避免重複計算
print(fibonacci(100))  # 很快，因為有快取
```

### 單例模式的裝飾器

```python
def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("資料庫連線建立")

db1 = Database()
db2 = Database()
print(db1 is db2)  # True，應該是同一個實例
```

## 類別裝飾器

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"{self.func.__name__} 被呼叫了 {self.calls} 次")
        return self.func(*args, **kwargs)

@CountCalls
def say_something():
    print("說點什麼")

say_something()
say_something()
say_something()
```

## 堆疊多個裝飾器

```python
def decorator1(func):
    def wrapper(*args, **kwargs):
        print("裝飾器 1")
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("裝飾器 2")
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def hello():
    print("Hello!")

# 執行順序：decorator1 -> decorator2 -> hello
# 輸出：
# 裝飾器 1
# 裝飾器 2
# Hello!
```

## 使用 functools.wraps

`wraps` 是一個重要的工具，用於保留原函式的元資料：

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """這是包裝器的文件字串"""
        return func(*args, **kwargs)

# 使用 @wraps 後
# wrapper.__name__ == func.__name__
# wrapper.__doc__ == func.__doc__
# 這對於除錯和文檔生成很重要
```

## 結論

裝飾器是 Python 中一個強大且優雅的功能，正確使用可以大幅簡化程式碼並提高重用性。雖然一開始可能比較難理解，但一旦掌握，就能寫出更加優雅的程式碼。