# 變數與資料型態

## 簡介

在程式中，變數用於儲存資料，而資料有不同的型態。本篇介紹 Python 中的變數與基本資料型態。

## 變數

### 什麼是變數

變數是儲存資料的容器，就像一個有名字的盒子：

```python
# 建立變數
age = 25
name = "Alice"

print(f"姓名: {name}, 年齡: {age}")
```

### 命名規則

1. 只能使用字母、數字、底線
2. 不能以數字開頭
3. 不能使用保留字
4. 大小寫有區分

```python
# 有效命名
my_variable = 1
_variable2 = 2
var3 = 3

# 無效命名
# 2many = 4      # 不能以數字開頭
# my-var = 5     # 不能使用減號
# class = 6      # 不能使用保留字
```

### 最佳實踐

```python
# 小駝峰
userName = "Alice"

# 大駝峰
UserName = "Bob"

# 底線命名（Python 慣例）
user_name = "Charlie"

# 常數（全大寫）
MAX_SIZE = 100
PI = 3.14159
```

## 基本資料型態

### 整數 (int)

```python
age = 25
count = -10
binary = 0b1010  # 二進位：10
hex_val = 0xFF   # 十六進位：255

print(type(age))  # <class 'int'>
```

### 浮點數 (float)

```python
price = 19.99
pi = 3.14159
scientific = 1.5e10  # 科學記號：15000000000.0

print(type(price))  # <class 'float'>
```

### 字串 (str)

```python
name = "Alice"
message = 'Hello'
multi = """這是
多行
字串"""

print(type(name))  # <class 'str'>
```

### 布林值 (bool)

```python
is_student = True
is_active = False

print(type(is_student))  # <class 'bool'>
```

### 無值 (NoneType)

```python
result = None
print(type(result))  # <class 'NoneType'>
```

## 容器型別

### 列表 (list)

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, None]

print(fruits[0])     # apple
print(fruits[-1])    # cherry
```

### 元組 (tuple)

```python
point = (10, 20)
rgb = (255, 128, 0)

print(point[0])    # 10
# point[0] = 20  # 錯誤！元組不可變
```

### 集合 (set)

```python
s = {1, 2, 3, 2, 1}
print(s)  # {1, 2, 3}  重複被移除

# 集合運算
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)  # 聯集：{1, 2, 3, 4}
print(a & b)  # 交集：{2, 3}
print(a - b)  # 差集：{1}
```

### 字典 (dict)

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "Taipei"
}

print(person["name"])       # Alice
print(person.get("email", ""))  # ""（預設值）
```

## 型別轉換

### 常見轉換

```python
# 轉換為整數
int("123")      # "123" -> 123
int(3.14)       # 3.14 -> 3
int(True)       # True -> 1

# 轉換為浮點數
float("3.14")   # "3.14" -> 3.14
float(10)       # 10 -> 10.0

# 轉換為字串
str(123)        # 123 -> "123"
str(3.14)       # 3.14 -> "3.14"

# 轉換為布林
bool(1)         # 1 -> True
bool(0)         # 0 -> False
bool("")        # "" -> False
bool("hello")   # "hello" -> True
```

### 轉換範例

```python
# 使用者輸入轉換
user_input = input("請輸入數字: ")  # 輸入 "42"
number = int(user_input)  # 轉換為整數
result = number * 2  # 84
print(f"結果: {result}")
```

## 型別檢查

```python
x = 10
print(isinstance(x, int))      # True
print(isinstance(x, (int, float)))  # True

y = "hello"
print(type(y) == str)          # True
```

## 型別提示 (Python 3.6+)

```python
name: str = "Alice"
age: int = 30
height: float = 165.5
is_student: bool = False
scores: list = [90, 85, 88]
info: dict = {"name": "Bob", "age": 25}
```

## 練習題

1. 建立一個字典儲存學生資訊（姓名、年齡、成績）
2. 將攝氏溫度轉換為華氏（C = (F - 32) * 5/9）
3. 計算列表 [1, 2, 3, 4, 5] 的總和、平均值、最大值、最小值
4. 去除列表中的重複元素