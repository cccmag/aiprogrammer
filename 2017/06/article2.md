# 文章 2：正規表達式基礎

## 前言

正規表達式（Regular Expression）是處理文字的強大工具。本章節介紹 Python 中正規表達式的基本用法。

## 基本概念

正規表達式使用特殊字元描述字串模式：
- `.`：匹配任意單一字元
- `^`：匹配開頭
- `$`：匹配結尾
- `*`：匹配零或多個
- `+`：匹配一或多個

## Python re 模組

```python
import re
```

## 基本匹配

```python
text = "The quick brown fox"

print(re.findall(r"quick", text))     # ['quick']
print(re.search(r"brown", text))      # Match object
print(re.match(r"The", text))         # Match object
```

## 模式匹配

```python
# 匹配數字
text = "Price: $199, Year: 2023"
numbers = re.findall(r'\d+', text)
print(numbers)  # ['199', '2023']

# 匹配電子郵件
email = "Contact: user@example.com"
pattern = r'\b[\w.-]+@[\w.-]+\.\w+\b'
emails = re.findall(pattern, email)
print(emails)  # ['user@example.com']
```

## 字符類

```python
text = "abc123DEF"

print(re.findall(r'[a-z]', text))   # 小寫字母
print(re.findall(r'[A-Z]', text))   # 大寫字母
print(re.findall(r'[0-9]', text))   # 數字
print(re.findall(r'[a-zA-Z0-9]', text))  # 字母數字
```

## 量詞

```python
text = "aaab abb aabbbb"

print(re.findall(r'a*', text))   # 零或多個 a
print(re.findall(r'a+', text))   # 一或多個 a
print(re.findall(r'a?', text))   # 零或一個 a
print(re.findall(r'a{2}', text))  # 剛好兩個 a
```

## 群組

```python
text = "John: 25, Jane: 30"

pattern = r'(\w+): (\d+)'
matches = re.findall(pattern, text)
print(matches)  # [('John', '25'), ('Jane', '30')]

for name, age in matches:
    print(f"{name} is {age} years old")
```

## 替換

```python
text = "Hello World"

result = re.sub(r'World', 'Python', text)
print(result)  # Hello Python

result = re.sub(r'\d+', '#', "Price: 100, Quantity: 50")
print(result)  # Price: #, Quantity: #
```

## 總結

正規表達式是文字處理的利器。雖然語法學習曲線較陡，但掌握後能大幅提升文字處理效率。

## 延伸閱讀

- https://www.google.com/search?q=Python+regex+regular+expression+tutorial
- https://www.google.com/search?q=regex+pattern+cheat+sheet