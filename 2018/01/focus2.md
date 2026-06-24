# f-string 格式化字符串

## 簡介

f-string（格式化字串字面量）是 Python 3.6 引入的字串格式化語法，使用 `f` 或 `F` 前綴標記，可在字串內直接嵌入表達式。

## 基本語法

```python
name = "Python"
version = 3.6

print(f"Welcome to {name} {version}!")
# 輸出: Welcome to Python 3.6!
```

## 格式化選項

### 數值格式化

```python
import math

pi = math.pi
print(f"Pi: {pi:.2f}")      # Pi: 3.14
print(f"Pi: {pi:10.2f}")    # Pi:       3.14

number = 1234
print(f"Hex: {number:#x}")  # Hex: 0x4d2
print(f"Bin: {number:b}")   # Bin: 10011010010
```

### 對齊與填充

```python
text = "center"
print(f"[{text:^20}]")      # [      center       ]
print(f"[{text:<20}]")      # [center              ]
print(f"[{text:>20}]")      # [              center]
print(f"[{text:*>20}]")     # [*************center]
```

### 格式化表達式

```python
a = 10
b = 3
print(f"{a} / {b} = {a / b:.2f}")
print(f"{a} ** 2 = {a ** 2}")
```

## 巢狀格式化

```python
data = [
    {"name": "Alice", "score": 90},
    {"name": "Bob", "score": 85},
]

for item in data:
    print(f"{item['name']}: {item['score']}")
```

## 呼叫函式

```python
def greet(name):
    return f"Hello, {name}!"

name = "Python"
print(f"{greet(name)}")
```

## 使用物件屬性

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(f"Name: {p.name}, Age: {p.age}")
```

## 格式化日期時間

```python
from datetime import datetime

now = datetime.now()
print(f"Date: {now:%Y-%m-%d}")
print(f"Time: {now:%H:%M:%S}")
```

## 除錯專用

```python
x = 10
print(f"{x=}")
# 輸出: x=10
```

## 效能優於舊語法

```python
name = "test"

# 舊式 - 較慢
"{}".format(name)
"%s" % name

# f-string - 較快
f"{name}"
```

## 注意事項

1. f-string 內部不支援反斜杠
2. 不支援多行 f-string（在 Python 3.12+ 改善）
3. 避免過度使用巢狀表達式，影響可讀性