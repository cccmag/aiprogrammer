# Python 基礎語法入門

## 簡介

Python 是一種高階、解釋型、互動式的程式語言，由 Guido van Rossum 於 1991 年建立。Python 強調程式碼的可讀性，採用縮排語法，是目前最受歡迎的程式語言之一。

## 第一支 Python 程式

```python
print("Hello, World!")
```

## 變數與資料型態

### 基本資料型態

```python
# 整數
age = 25
count = -10

# 浮點數
price = 19.99
pi = 3.14159

# 字串
name = "Alice"
message = 'Hello, Python!'

# 布林值
is_student = True
is_active = False

# 無值
result = None
```

### 型別檢查

```python
print(type(age))      # <class 'int'>
print(type(price))     # <class 'float'>
print(type(name))      # <class 'str'>
print(type(is_student)) # <class 'bool'>
```

## 運算子

### 算術運算子

```python
a, b = 10, 3

print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.333...
print(a // b)  # 3 (整數除法)
print(a % b)   # 1 (餘數)
print(a ** b)  # 1000 (次方)
```

### 比較運算子

```python
print(a == b)  # False
print(a != b)  # True
print(a > b)   # True
print(a < b)   # False
print(a >= b)  # True
```

### 邏輯運算子

```python
x, y = True, False

print(x and y)  # False
print(x or y)   # True
print(not x)    # False
```

## 控制流程

### 條件判斷

```python
age = 18

if age >= 18:
    print("成年人")
elif age >= 13:
    print("青少年")
else:
    print("兒童")
```

### 迴圈

```python
# for 迴圈
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# while 迴圈
count = 0
while count < 5:
    print(count)
    count += 1
```

### break 與 continue

```python
for i in range(10):
    if i == 5:
        break    # 立即結束迴圈
    if i % 2 == 0:
        continue # 跳過本次迭代
    print(i)  # 輸出: 1, 3, 7, 9
```

## 資料結構

### 列表（List）

```python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)
print(numbers[0])     # 1
print(numbers[-1])    # 5
print(numbers[1:3])   # [2, 3]
```

### 字典（Dictionary）

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "Taipei"
}
print(person["name"])
person["email"] = "alice@example.com"
```

### 元組（Tuple）

```python
point = (10, 20)
x, y = point
print(x, y)
```

### 集合（Set）

```python
s = {1, 2, 3, 2, 1}
print(s)  # {1, 2, 3}
```

## 函式

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Bob", "Hi"))          # Hi, Bob!

# 可變參數
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3, 4, 5))  # 15
```

## 練習題

1. 寫一個程式計算 1+2+...+100
2. 判斷一個數是否為質數
3. 將列表中的數字由小到大排序