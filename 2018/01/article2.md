# 函式與模組設計

## 簡介

良好的函式與模組設計是寫出可維護程式碼的關鍵。本篇介紹 Python 中函式的各種用法以及如何組織模組。

## 函式基礎

### 定義與呼叫

```python
def say_hello():
    print("Hello!")

say_hello()
```

### 參數與回傳值

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)  # 7
```

### 多個回傳值

```python
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder

q, r = divide(10, 3)
print(f"商: {q}, 餘: {r}")
```

## 參數類型

### 預設參數值

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# 使用預設值
print(greet("Alice"))           # Hello, Alice!

# 覆寫預設值
print(greet("Bob", "Hi"))       # Hi, Bob!
```

### 關鍵字參數

```python
def power(base, exponent):
    return base ** exponent

print(power(base=2, exponent=3))  # 8
print(power(exponent=2, base=5))  # 25
```

### 可變參數

```python
# *args - 接收不定數量的位置參數
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3))       # 6
print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs - 接收不定數量的關鍵字參數
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="Taipei")
```

### 組合使用

```python
def func(required, *args, **kwargs):
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

func("test", 1, 2, 3, name="Alice", age=30)
```

## 匿名函式（Lambda）

```python
# 語法
square = lambda x: x ** 2
print(square(5))  # 25

# 搭配內建函式
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

filtered = list(filter(lambda x: x > 2, numbers))
print(filtered)  # [3, 4, 5]

sorted_list = sorted(numbers, key=lambda x: -x)
print(sorted_list)  # [5, 4, 3, 2, 1]
```

## 模組

### 建立模組

```python
# mymodule.py
def hello():
    return "Hello from mymodule!"

class Calculator:
    def add(self, a, b):
        return a + b
```

### 導入模組

```python
# 方式1
import mymodule
print(mymodule.hello())
calc = mymodule.Calculator()

# 方式2
from mymodule import hello, Calculator
print(hello())

# 方式3 - 導入全部
from mymodule import *

# 方式4 - 別名
import mymodule as mm
from mymodule import Calculator as Calc
```

### 標準庫常用模組

```python
import math
print(math.pi)           # 3.141592653589793
print(math.sqrt(16))    # 4.0
print(math.sin(math.pi/2))  # 1.0

import random
print(random.randint(1, 10))      # 1-10 隨機整數
print(random.choice(['a', 'b', 'c']))  # 隨機選擇

import datetime
now = datetime.datetime.now()
print(now.year, now.month, now.day)
```

### if __name__ == "__main__"

```python
# mymodule.py
def main():
    print("Running as script")

if __name__ == "__main__":
    main()
```

## 練習題

1. 寫一個計算機模組，包含加、減、乘、除、平方功能
2. 寫一個日期工具模組，計算兩個日期之間的天數差
3. 使用 lambda 函式對列表進行多鍵排序