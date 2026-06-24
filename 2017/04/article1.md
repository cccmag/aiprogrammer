# 文章 1：Python 基礎語法回顧

## 前言

Python 是資料科學與機器學習領域最流行的語言。本章節回顧 Python 的基礎語法，幫助讀者快速進入狀態。

## 變數與資料型態

Python 是動態型別語言，不需要聲明變數型別：

```python
x = 5           # 整數
y = 3.14        # 浮點數
name = "Python" # 字串
is_valid = True # 布林值
```

## 資料結構

### 列表（List）

```python
fruits = ["apple", "banana", "orange"]
fruits.append("grape")
print(fruits[0])  # apple
```

### 字典（Dictionary）

```python
person = {"name": "Alice", "age": 25}
print(person["name"])  # Alice
```

### 元組（Tuple）

```python
point = (3, 4)
x, y = point
```

## 控制流程

### 條件判斷

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

### 迴圈

```python
for i in range(10):
    print(i)

while condition:
    do_something()
```

## 函式定義

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

message = greet("World")
```

## 類別與物件

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} says woof!"

my_dog = Dog("Buddy", 3)
print(my_dog.bark())
```

## 列表推導式

```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

## 錯誤處理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("Done")
```

## 總結

Python 語法簡潔優美，非常適合快速開發。本章回顧的基礎知識將貫穿後續的機器學習內容。

## 延伸閱讀

- https://www.google.com/search?q=Python+3+tutorial+basics
- https://www.google.com/search?q=Python+data+structures+list+dictionary