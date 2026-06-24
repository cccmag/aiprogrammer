# 正規表達式在文字處理的應用

## 前言

正規表達式（Regular Expression）是程式設計中處理文字的強大工具。它基於正規語言理論，可以精確地描述字串的模式。本文將探討正規表達式在各種文字處理場景中的應用。

## 基本概念回顧

正規表達式描述的是正規語言，可以用有限自動機（DFA/NFA）識別。

```python
import re

# 基礎匹配
pattern = re.compile(r"hello")
print(pattern.match("hello world"))  # 匹配

# 字元類
pattern = re.compile(r"[aeiou]")  # 任意母音
print(pattern.findall("hello"))  # ['e', 'o']

# 量詞
pattern = re.compile(r"\d+")  # 一或多個數字
pattern = re.compile(r"\d*")  # 零或多個數字
pattern = re.compile(r"\d?")  # 零或一個數字
```

## 常見應用場景

### 1. 資料驗證

```python
def validate_inputs():
    # 電子郵件驗證
    email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    assert re.match(email, "user@example.com")
    assert not re.match(email, "invalid")

    # URL 驗證
    url = r"^https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:/[^s]*)?$"
    assert re.match(url, "https://example.com/path")

    # IP 位址驗證
    ip = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    assert re.match(ip, "192.168.1.1")
    assert not re.match(ip, "256.0.0.1")

    print("All validations passed!")

validate_inputs()
```

### 2. 文字搜尋與取代

```python
def text_operations():
    text = "The quick brown fox jumps over the lazy dog"

    # 找出所有單字
    words = re.findall(r"\b\w+\b", text)
    print(f"Words: {words}")

    # 找出所有大寫單字
    capital_words = re.findall(r"\b[A-Z]\w*\b", text)
    print(f"Capital words: {capital_words}")

    # 取代
    result = re.sub(r"\b\w+\b", lambda m: m.group().upper(), text)
    print(f"Uppercase: {result}")

    # 分割
    parts = re.split(r"[\s,]+", "apple, banana, cherry, date")
    print(f"Split: {parts}")

text_operations()
```

### 3. 日誌解析

```python
def parse_logs():
    log_lines = [
        "2026-06-01 10:00:00 INFO Server started",
        "2026-06-01 10:00:01 ERROR Connection failed: timeout",
        "2026-06-01 10:00:02 WARN Retry attempt 1 of 3",
    ]

    pattern = re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
        r"(?P<level>INFO|ERROR|WARN)\s+"
        r"(?P<message>.+)"
    )

    for line in log_lines:
        match = pattern.match(line)
        if match:
            print(f"Time: {match.group('timestamp')}, "
                  f"Level: {match.group('level')}, "
                  f"Message: {match.group('message')}")

parse_logs()
```

### 4. 網頁爬蟲

```python
def web_scraping():
    html = """
    <div class="product">
        <h2 class="title">iPhone 15</h2>
        <span class="price">$999</span>
    </div>
    <div class="product">
        <h2 class="title">MacBook Pro</h2>
        <span class="price">$1999</span>
    </div>
    """

    # 提取產品資訊
    product_pattern = re.compile(
        r'<div class="product">.*?<h2 class="title">([^<]+)</h2>.*?<span class="price">([^<]+)</span>.*?</div>',
        re.DOTALL
    )

    for match in product_pattern.finditer(html):
        print(f"Product: {match.group(1)}, Price: {match.group(2)}")

web_scraping()
```

### 5. 密碼強度檢查

```python
def password_strength():
    def check_password(pwd):
        if len(pwd) < 8:
            return "Weak"
        if not re.search(r"[A-Z]", pwd):
            return "Weak"
        if not re.search(r"[a-z]", pwd):
            return "Weak"
        if not re.search(r"\d", pwd):
            return "Weak"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            return "Medium"
        return "Strong"

    passwords = ["abc", "Password1", "P@ssw0rd", "MyStr0ng!Pass"]
    for pwd in passwords:
        print(f"{pwd}: {check_password(pwd)}")

password_strength()
```

### 6. 電話號碼格式化

```python
def format_phone():
    def format_number(num):
        digits = re.sub(r"\D", "", num)
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return num

    numbers = ["0912345678", "(02) 1234-5678", "+886-912-345-678"]
    for num in numbers:
        print(f"{num} -> {format_number(num)}")

format_phone()
```

### 7. CSV 解析增強

```python
def parse_csv():
    csv_line = 'John Doe, "New York, NY", 1985, "A "great" person"'

    parts = re.findall(r'(?:[^,"]|"(?:[^"]*"")*[^"]*)+', csv_line)
    print([p.strip().strip('"') for p in parts])

parse_csv()
```

## 正規表達式的效能優化

### 避免災難性回溯

```python
def avoid_catastrophic_backtracking():
    # 危險：可能造成災難性回溯
    # pattern = re.compile(r"(a+)+b")

    # 安全：明確表達意圖
    pattern = re.compile(r"a+b")

    # 或者使用原子組
    # pattern = re.compile(r"(?>a+)+b")

    print("Safe pattern used")

avoid_catastrophic_backtracking()
```

### 預編譯

```python
def precompile_patterns():
    patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        r"https?://[^\s]+",
    ]

    compiled = [re.compile(p) for p in patterns]

    text = "Contact us at 2026-06-01 or email info@example.com"
    for pattern in compiled:
        matches = pattern.findall(text)
        if matches:
            print(f"Found: {matches}")

precompile_patterns()
```

## 小結

正規表達式是文字處理的瑞士刀，從簡單的驗證到複雜的解析都能勝任。理解其背後的正規語言理論，可以幫助我們更有效地設計模式、避免常見錯誤。

---

**延伸閱讀**

- [Python re module documentation](https://www.google.com/search?q=python+re+module+documentation)
- [Regex performance tips](https://www.google.com/search?q=regex+performance+tips)
- [Regular Expressions Quick Reference](https://www.google.com/search?q=regular+expressions+quick+reference)