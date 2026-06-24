# 函式設計

## 簡介

函式是組織程式碼的基本單位，可以提高程式碼的重用性和可讀性。

## 定義與呼叫

```python
def greet():
    print("Hello!")

greet()  # 呼叫函式
```

### 帶參數

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Hello, Alice!
```

### 帶回傳值

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
print(f"商: {q}, 餘: {r}")  # 商: 3, 餘: 1
```

## 參數類型

### 預設參數值

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Bob", "Hi"))          # Hi, Bob!
```

### 關鍵字參數

```python
def power(base, exponent):
    return base ** exponent

power(base=2, exponent=3)  # 8
power(exponent=3, base=2)  # 8
```

### 可變參數 *args

```python
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3))        # 6
print(sum_all(1, 2, 3, 4, 5))  # 15

# 搭配一般參數
def greet(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet("Hello", "Alice", "Bob", "Charlie")
```

### 可變參數 **kwargs

```python
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="Taipei")
```

### 參數順序

```python
def func(required, *args, **kwargs):
    # required: 必要參數
    # args: 可變位置參數
    # kwargs: 可變關鍵字參數
    pass
```

## 匿名函式 (Lambda)

```python
# 基本語法
square = lambda x: x ** 2
print(square(5))  # 25

# 多參數
add = lambda a, b: a + b
print(add(3, 4))  # 7

# 搭配內建函式
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_nums = sorted(numbers)
print(sorted_nums)  # [1, 1, 2, 3, 4, 5, 6, 9]

# 自訂排序
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
print(sorted_students)  # [('Bob', 92), ('Alice', 85), ('Charlie', 78)]
```

## 作用域

### 區域變數

```python
def func():
    x = 10  # 區域變數
    print(x)

func()
# print(x)  # 錯誤！x 是區域變數
```

### 全域變數

```python
x = 10  # 全域變數

def func():
    print(x)  # 可以存取

func()
print(x)  # 10
```

### 修改全域變數

```python
x = 10

def func():
    global x
    x = 20

func()
print(x)  # 20
```

### nonlocal

```python
def outer():
    x = 10

    def inner():
        nonlocal x
        x = 20

    inner()
    print(x)  # 20

outer()
```

## 巢狀函式

```python
def outer():
    def inner():
        print("inner")
    inner()
    inner()

outer()
```

## 裝飾器

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@decorator
def say_hello():
    print("Hello!")

say_hello()
```

## 遞迴

### 基本遞迴

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120
```

### 費氏數列

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(10):
    print(fibonacci(i), end=" ")
```

## 文件字串 (Docstring)

```python
def add(a, b):
    """將兩個數字相加並回傳結果

    Args:
        a: 第一個數字
        b: 第二個數字

    Returns:
        兩個數字的和
    """
    return a + b
```

## 練習題

1. 寫一個計算機函式，支援加、減、乘、除
2. 寫一個判斷是否為質數的函式
3. 寫一個計算最大公因數的函式（使用歐幾里得演算法）
4. 寫一個裝飾器，計算函式執行時間