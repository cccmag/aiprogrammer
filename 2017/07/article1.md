# Python 字串處理基礎

## 字串基本操作

Python 的字串是不可變（immutable）的序列類型。

```python
# 創建字串
s1 = "Hello"
s2 = 'World'
s3 = """多行
字串"""

# 連接
s = s1 + " " + s2
print(s)  # Hello World

# 重複
print("Ha" * 3)  # HaHaHa

# 索引
print(s[0])  # H
print(s[-1])  # d

# 切片
print(s[0:5])  # Hello
print(s[6:])   # World
```

## 字串格式化

### f-string（Python 3.6+）

```python
name = "Alice"
age = 30
print(f"My name is {name}, I'm {age} years old")
print(f"Pi: {3.14159:.2f}")
print(f"Hex: {255:08x}")
```

### format 方法

```python
"{0} {1} {0}".format("Hello", "World")
"{name} is {age}".format(name="Bob", age=25)
"{:>10}".format("right")
"{:^10}".format("center")
```

### % 格式化

```python
"%s is %d years old" % ("Charlie", 35)
```

## 常用字串方法

```python
s = "  Hello, World!  "

# 大小寫
s.upper()      # "  HELLO, WORLD!  "
s.lower()      # "  hello, world!  "
s.title()      # "  Hello, World!  "

# 去除空白
s.strip()      # "Hello, World!"
s.lstrip()     # "Hello, World!  "
s.rstrip()     # "  Hello, World!"

# 分割與合併
s.split(",")   # ["  Hello", " World!  "]
"-".join(["a", "b", "c"])  # "a-b-c"

# 替換
s.replace("World", "Python")

# 搜尋
s.find("World")   # 9（找到）
s.find("Java")    # -1（未找到）
s.count("l")      # 3
s.startswith("  H")  # True
s.endswith("!  ")    # True
```

## 字串與編碼

```python
# UTF-8 編碼
s = "中文測試"
encoded = s.encode('utf-8')
print(encoded)  # b'\xe4\xb8\xad\xe6\x96\x87\xe6\xb8\xac\xe8\xa9\xa6'

# 解碼
decoded = encoded.decode('utf-8')
print(decoded)  # 中文測試
```

## 字串與數值轉換

```python
# 轉數值
int("42")       # 42
float("3.14")   # 3.14

# 轉字串
str(42)         # "42"
str(3.14)       # "3.14"

# 其他進位
int("1010", 2)  # 10（二進位）
hex(255)        # "0xff"
```

## 正規化與清理

```python
import unicodedata

s = "café"

# Unicode 正規化
normalized = unicodedata.normalize('NFKD', s)

# 移除重音
def remove_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

print(remove_accents("café"))  # cafe
```

## 總結

Python 提供豐富的字串操作功能。f-string 是現代 Python 首選的格式化方式。處理中文需注意編碼（UTF-8）。