# 主題三：正規表達式

## 什麼是正規表達式？

正規表達式（Regular Expression，regex）是一種用於描述正規語言的簡潔表示法。

### 基本運算

正規表達式有三種基本運算：

1. **並集（Union）**：a | b 表示 {a, b}
2. **連接（Concatenation）**：ab 表示 {w1w2 | w1 ∈ {a}, w2 ∈ {b}}
3. **克林閉包（Kleene Star）**：a* 表示 {ε, a, aa, aaa, ...}

### 運算順序

```
克林閉包 > 連接 > 並集
```

即，* 的優先順序最高，其次是連接，最後是 |。

## 正規表達式語法

### 基本符號

```python
import re

# 精確匹配
pattern = re.compile(r"hello")  # 匹配 "hello"
pattern.match("hello world")  # 匹配
pattern.match("HELLO world")  # 不匹配（大寫）

# 任意單一字元（除換行外）
pattern = re.compile(r"h.llo")  # 匹配 "hello", "hallo", "hxllo"...
```

### 字元類

```python
# 字元類 [...]：匹配方括號中的任意一個字元
pattern = re.compile(r"[aeiou]")  # 匹配任意母音
pattern.findall("hello")  # ['e', 'o']

# 範圍 [a-z], [0-9]
pattern = re.compile(r"[a-z]+")  # 匹配小寫字母序列

# 否定 [^...]
pattern = re.compile(r"[^aeiou]+")  # 匹配非母音序列
```

### 預定義字元類

```python
# \d = [0-9]：數字
# \D = [^0-9]：非數字
# \w = [a-zA-Z0-9_]：詞字元
# \W = [^\w]：非詞字元
# \s = [ \t\n\r\f\v]：空白字元
# \S = [^\s]：非空白字元
# .  = 任意字元（除換行外）

pattern = re.compile(r"\d+")  # 匹配數字序列
pattern = re.compile(r"\w+")  # 匹配詞字元序列
```

### 量詞

```python
# * ：零或多個（等價於 {0,}）
pattern = re.compile(r"ab*")  # a, ab, abb, abbb...

# + ：一或多個（等價於 {1,}）
pattern = re.compile(r"ab+")  # ab, abb, abbb...

# ? ：零或一個（等價於 {0,1}）
pattern = re.compile(r"colou?r")  # color, colour

# {n} ：精確 n 個
pattern = re.compile(r"\d{4}")  # 4 位數字

# {n,} ：至少 n 個
pattern = re.compile(r"\d{2,}")  # 至少 2 位數字

# {n,m} ：n 到 m 個
pattern = re.compile(r"\d{2,4}")  # 2-4 位數字
```

### 錨點

```python
# ^ ：行開頭
pattern = re.compile(r"^hello")  # 行開頭的 hello

# $ ：行結尾
pattern = re.compile(r"world$")  # 行結尾的 world

# \b ：詞邊界
pattern = re.compile(r"\bword\b")  # 完整的單詞

# \B ：非詞邊界
pattern = re.compile(r"\Bword")  # word 不在詞邊界
```

### 轉義

```python
# 匹配特殊字元
pattern = re.compile(r"\$\d+\.\d{2}")  # $12.34

# 匹配 . * + ? ^ $ { } [ ] \ | ( )
pattern = re.compile(r"\.\*\+")  # .*+
```

## 進階特性

### 分組

```python
# () ：分組捕獲
pattern = re.compile(r"(\d{4})-(\d{4})-(\d{4})-(\d{4})")
match = pattern.search("Card: 1234-5678-9012-3456")
if match:
    print(match.group(1))  # 1234
    print(match.group(2))  # 5678

# 非捕獲分組 (?:...)
pattern = re.compile(r"(?:Mr|Mrs|Ms)\.?\s+(\w+)")  # 只捕獲姓名
```

### 反向引用

```python
# 匹配重複的詞
pattern = re.compile(r"\b(\w+)\s+\1\b")  # 匹配 "the the"
match = pattern.search("the the")
print(match.group())  # "the the"
```

### 展望

```python
# 正展望 (?=...)：前方是...
pattern = re.compile(r"\d+(?=\s+USD)")  # USD 前的數字

# 負展望 (?!...)：前方不是...
pattern = re.compile(r"\d+(?!\s+USD)")  # 非 USD 前的數字
```

### 條件

```python
# 命名捕獲組
pattern = re.compile(r"(?P<area>\d{3})-(?P<number>\d{4})")
match = pattern.search("123-4567")
print(match.group("area"))  # 123
print(match.group("number"))  # 4567
```

## 正規表達式引擎的實現

### Thompson 構造法

將正規表達式轉換為 NFA：

```python
class NFAFragment:
    """NFA 片段"""
    def __init__(self, start, accept, transitions):
        self.start = start
        self.accept = accept
        self.transitions = transitions

def regex_to_nfa(pattern):
    """將正規表達式轉換為 NFA"""
    # 使用棧操作實現 Thompson 構造法
    pass
```

## 實用範例

### 電子郵件驗證

```python
import re

email_pattern = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

def validate_email(email):
    return bool(email_pattern.match(email))

emails = ["user@example.com", "invalid@", "@example.com"]
for email in emails:
    print(f"{email}: {validate_email(email)}")
```

### URL 解析

```python
url_pattern = re.compile(
    r"^(?P<protocol>https?)://(?P<domain>[a-zA-Z0-9.-]+)(?::(?P<port>\d+))?"
    r"(?P<path>/[a-zA-Z0-9/._-]*)?$"
)

match = url_pattern.match("https://example.com:8080/api/v1/users")
if match:
    print(f"Protocol: {match.group('protocol')}")
    print(f"Domain: {match.group('domain')}")
    print(f"Port: {match.group('port')}")
    print(f"Path: {match.group('path')}")
```

### 日誌解析

```python
log_pattern = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>INFO|WARN|ERROR)\s+"
    r"(?P<message>.+)$"
)

log = "2026-01-01 12:00:00 ERROR Connection failed"
match = log_pattern.match(log)
if match:
    print(f"Time: {match.group('timestamp')}")
    print(f"Level: {match.group('level')}")
    print(f"Message: {match.group('message')}")
```

### 電話號碼

```python
phone_pattern = re.compile(
    r"^(?:\+886|0)?[-\s]?(?:9\d{8}|\d{2,4}[-\s]?\d{3,4}[-\s]?\d{4})$"
)

phones = ["0912345678", "02-1234-5678", "+886-912-345-678"]
for phone in phones:
    print(f"{phone}: {bool(phone_pattern.match(phone))}")
```

## 正規表達式的效能

### 災難性回溯

```python
# 避免：".*" 是贪婪的，可能導致回溯
# 改進：使用 "[^"]*" 代替 ".*?"

# 危險模式
# pattern = re.compile(r"(a+)+b")  # 可能造成災難性回溯

# 安全模式
pattern = re.compile(r"a+b")  # 簡單匹配
```

### 預編譯

```python
# 預編譯正規表達式（常用於迴圈中）
email_pattern = re.compile(r"...")

for line in lines:
    match = email_pattern.search(line)
    # ...
```

## 小結

正規表達式是描述正規語言的強大工具。它的語法直覺、功能豐富，在文字處理、表單驗證、資料提取等場景中不可或缺的工具。