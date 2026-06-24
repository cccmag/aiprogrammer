# 正規表達式入門

## 什麼是正規表達式？

正規表達式（Regular Expression, regex）是用於 pattern matching 的強大工具。可用於驗證、提取、替換文字。

## 基本語法

```python
import re

# match() - 從開頭匹配
pattern = r"\d+"  # 一或多個數字
text = "123 abc"
result = re.match(pattern, text)
print(result.group())  # 123

# search() - 找第一個匹配
text = "abc 123 def 456"
result = re.search(pattern, text)
print(result.group())  # 123

# findall() - 找所有匹配
print(re.findall(pattern, text))  # ['123', '456']

# finditer() - 找所有匹配（迭代器）
for match in re.finditer(pattern, text):
    print(match.group())
```

## 字元類別

```python
# 常用 shorthand
\d  # 數字 [0-9]
\D  # 非數字 [^0-9]
\w  # 字母數字 [a-zA-Z0-9_]
\W  # 非字母數字
\s  # 空白字元 [ \t\n\r\f\v]
\S  # 非空白

# 自訂範圍
[a-z]    # 小寫字母
[A-Z]    # 大寫字母
[0-9]    # 數字
[aeiou]  # 母音
[^aeiou] # 非母音
```

## 量詞

```python
# * - 零或多個
re.findall(r"ab*c", "ac abc abbc")  # ['ac', 'abc', 'abbc']

# + - 一或多個
re.findall(r"ab+c", "ac abc abbc")  # ['abc', 'abbc']

# ? - 零或一個
re.findall(r"colou?r", "color colour")  # ['color', 'colour']

# {n} - 剛好 n 個
re.findall(r"\d{4}", "1234 12 123456")  # ['1234', '1234']

# {n,m} - n 到 m 個
re.findall(r"\d{2,4}", "1 12 123 1234 12345")  # ['12', '123', '1234', '12345']
```

## 特殊字元

```python
.   # 任意字元（換行除外）
^   # 字串開頭
$   # 字串結尾
\   # 轉義
|   # 或
()  # 群組
(?:...) # 非 capture 群組
```

## 群組與命名群組

```python
text = "John has 5 apples"

# 群組
pattern = r"(\w+) has (\d+) (\w+)"
match = re.search(pattern, text)
print(match.group(1))  # John
print(match.group(2))  # 5
print(match.group(3))  # apples

# 命名群組
pattern = r"(?P<name>\w+) has (?P<count>\d+) (?P<fruit>\w+)"
match = re.search(pattern, text)
print(match.group('name'))   # John
print(match.group('count'))  # 5
print(match.group('fruit'))   # apples
```

## 斷言（Lookahead/Lookbehind）

```python
# 正向先行斷言 (?=...)
re.findall(r"\d+(?= dollars)", "100 dollars 50 euros")  # ['100']

# 負向先行斷言 (?!...)
re.findall(r"\d+(?! dollars)", "100 dollars 50 euros")  # ['50']

# 正向後行斷言 (?<=...)
re.findall(r"(?<=\$)\d+", "$100 50 dollars")  # ['100']

# 負向後行斷言 (?<!...)
re.findall(r"(?<!\$)\d+", "$100 50 dollars")  # ['50', 'dollars']
```

## 替換

```python
text = "Hello, World!"

# 簡單替換
print(re.sub(r"World", "Python", text))  # Hello, Python!

# 使用群組替換
print(re.sub(r"(\w+), (\w+)", r"\2, \1", text))  # World, Hello!

# 函式替換
def convert(match):
    return str(int(match.group()) * 2)

print(re.sub(r"\d+", convert, "10 apples 20 oranges"))  # 20 apples 40 oranges
```

## 編譯與旗標

```python
# 編譯 pattern（效能更好）
pattern = re.compile(r"\d+", re.IGNORECASE)

# 旗標
re.I  # IGNORECASE
re.M  # MULTILINE
re.S  # DOTALL（. 匹配換行）
re.X  # VERBOSE（可添加註解）
```

## 實用範例

```python
# 驗證 email
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
print(bool(re.match(email_pattern, "test@example.com")))  # True

# 提取 URL
text = "Visit https://example.com or http://test.org"
urls = re.findall(r"https?://[\w\.-]+", text)
print(urls)  # ['https://example.com', 'http://test.org']

# 清理 HTML
text = "<p>Hello, <b>World</b>!</p>"
clean = re.sub(r"<[^>]+>", "", text)
print(clean)  # Hello, World!
```

## 總結

正規表達式是文字處理的利器。掌握基本語法（字元類、量詞、群組）可解決大部分需求。注意效能，複雜 pattern 可先編譯。