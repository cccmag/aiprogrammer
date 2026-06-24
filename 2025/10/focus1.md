# 裝飾器：函數的函數

## 高階函式的藝術（2013-2026）

### 前言

裝飾器（decorator）是 Python 最優雅的語言特性之一。它讓開發者可以在不修改原始函式定義的情況下，為函式添加額外的功能——就像在現有函式外層包裹一層「糖衣」。

### 裝飾器的本質

裝飾器的本質是高階函式——接受一個函式作為參數，返回一個新的函式：

```python
def my_decorator(func):
    def wrapper():
        print("在函式執行前")
        func()
        print("在函式執行後")
    return wrapper

def say_hello():
    print("Hello!")

# 手動應用裝飾器
say_hello = my_decorator(say_hello)
say_hello()
```

Python 提供了 `@` 語法糖來簡化這個過程：

```python
@my_decorator
def say_hello():
    print("Hello!")
```

這兩種寫法完全等價。

### functools.wraps 的重要性

直接實作裝飾器有一個問題——裝飾後的函式失去了原始資訊：

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """向某人打招呼"""
    print(f"Hi {name}")

print(greet.__name__)  # 輸出 'wrapper'，不是 'greet'
print(greet.__doc__)   # 輸出 None
```

使用 `functools.wraps` 解決：

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """向某人打招呼"""
    print(f"Hi {name}")

print(greet.__name__)  # 輸出 'greet'
print(greet.__doc__)   # 輸出 '向某人打招呼'
```

### 帶參數的裝飾器

有時裝飾器本身需要參數，需要在外面再包一層：

```python
def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say(message):
    print(message)

say("Hello!")  # 輸出三次
```

### 類別裝飾器

裝飾器也可以用類別實作，透過 `__call__` 協定：

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"第 {self.count} 次呼叫")
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    print("Hello!")

hello()  # 第 1 次呼叫
hello()  # 第 2 次呼叫
```

### 常見應用場景

1. **計時**：測量函式執行時間
2. **日誌**：記錄函式呼叫參數和結果
3. **權限檢查**：驗證使用者是否有權限執行
4. **快取**：記憶化重複計算的結果
5. **重試**：在函式失敗時自動重試
6. **除錯**：印出函式呼叫堆疊

### 疊加裝飾器

多個裝飾器可以疊加使用，執行順序從內到外：

```python
@debug
@timer
def process(data):
    # ...
```

這相當於 `process = debug(timer(process))`。

### 小結

裝飾器是 Python 函數式程式設計的核心工具。它讓橫切關注點（cross-cutting concerns）可以在不影響原始程式碼邏輯的情況下被優雅地處理。掌握裝飾器是 Python 進階使用者的必備技能。

---

**下一步**：[生成器與迭代器](focus2.md)

## 延伸閱讀

- [Python 裝飾器官方指南](https://www.google.com/search?q=Python+decorator+official+documentation)
- [Real Python: Primer on Python Decorators](https://www.google.com/search?q=Real+Python+Python+decorators)
- [PEP 318: Decorators for Functions and Methods](https://www.google.com/search?q=PEP+318+Python+decorators)
