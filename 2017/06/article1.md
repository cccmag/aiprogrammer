# 文章 1：Python 字串處理

## 前言

字串是文字處理的基本單位。本章節介紹 Python 中常用的字串操作。

## 字串創建

```python
s1 = "Hello World"
s2 = 'Python'
s3 = """多行字串"""
s4 = "Hello " + "World"
```

## 基本操作

```python
s = "Hello World"

print(len(s))       # 長度：11
print(s[0])         # H
print(s[0:5])       # Hello
print(s.upper())    # HELLO WORLD
print(s.lower())    # hello world
```

## 字串格式化

```python
name = "Alice"
age = 25

# f-string (Python 3.6+)
print(f"My name is {name}, I'm {age} years old")

# format
print("My name is {}, I'm {} years old".format(name, age))

# % 格式化
print("My name is %s, I'm %d years old" % (name, age))
```

## 常用方法

```python
s = "  Hello, World!  "

print(s.strip())       # 去除空白
print(s.replace(",", ""))  # 取代
print(s.split(","))    # 分割：['  Hello', ' World!  ']
print(s.count("l"))    # 計算出現次數：3
print(s.find("World")) # 尋找子字串：9
```

## 字串拼接與分割

```python
words = ["Hello", "World", "Python"]
sentence = " ".join(words)
print(sentence)  # Hello World Python

# 分割
text = "apple,banana,orange"
fruits = text.split(",")
print(fruits)  # ['apple', 'banana', 'orange']
```

## 判斷與搜尋

```python
s = "Hello World"

print(s.startswith("Hello"))  # True
print(s.endswith("World"))    # True
print(s.isdigit())            # False
print("Hello" in s)           # True
```

## 總結

Python 提供了豐富的字串操作功能。熟練掌握這些方法對文字處理與 NLP 任務至關重要。

## 延伸閱讀

- https://www.google.com/search?q=Python+string+methods+tutorial
- https://www.google.com/search?q=Python+string+formatting+f-string