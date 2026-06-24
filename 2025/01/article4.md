# 字串操作技巧

## 字串的內部表示

Python 中的字串是 Unicode 字元的不可變序列。從 Python 3 開始，所有字串都是 Unicode，這意味著你可以直接處理中文、日文、表情符號等各種字元。

```python
text = "你好，世界！🌍"
print(len(text))  # 8 (每個中文字和表情符號都算一個字元)
```

## 進階字串格式化

### f-string 的進階用法

```python
name = "Alice"
age = 25
salary = 123456.789

# 數字格式化
print(f"薪資：{salary:,.2f}")        # 123,456.79
print(f"百分比：{0.856:.1%}")        # 85.6%
print(f"十六進位：{255:#x}")         # 0xff

# 對齊
print(f"|{name:>10}|")   # 右對齊
print(f"|{name:<10}|")   # 左對齊
print(f"|{name:^10}|")   # 置中

# 日期格式化
from datetime import datetime
now = datetime.now()
print(f"{now:%Y-%m-%d %H:%M:%S}")  # 2025-01-15 14:30:00
```

### format() 方法

```python
# 位置參數
print("{0} 是 {1} 歲".format("Alice", 25))

# 關鍵字參數
print("{name} 住在 {city}".format(name="Bob", city="台北"))

# 字典解包
data = {"name": "Charlie", "age": 30}
print("我叫 {name}，今年 {age} 歲".format(**data))
```

## 正規表示式入門

正規表示式是字串模式匹配的強大工具：

```python
import re

text = "我的 email 是 alice@example.com，電話是 0912-345-678"

# 搜尋 email
email_pattern = r'\b[\w.+-]+@[\w-]+\.[\w.]+\b'
emails = re.findall(email_pattern, text)
print(emails)  # ['alice@example.com']

# 搜尋電話號碼
phone_pattern = r'\d{4}-\d{3}-\d{3}'
phones = re.findall(phone_pattern, text)
print(phones)  # ['0912-345-678']

# 替換
censored = re.sub(r'\d{4}-\d{3}-\d{3}', '***-***-***', text)
print(censored)
```

### 常用正則模式

```python
# 驗證輸入
def is_valid_email(email):
    pattern = r'^[\w.+-]+@[\w-]+\.[\w.]+$'
    return bool(re.match(pattern, email))

def is_valid_phone(phone):
    pattern = r'^\d{2,4}-\d{3,4}-\d{3,4}$'
    return bool(re.match(pattern, phone))

print(is_valid_email("test@example.com"))  # True
print(is_valid_phone("02-1234-5678"))      # True
```

## 字串的實際應用

### 資料清理

```python
def clean_text(text):
    """清理文字資料"""
    # 移除多餘空白
    text = ' '.join(text.split())
    # 移除標點符號
    import string
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 轉為小寫
    text = text.lower()
    return text

dirty = "  Hello,  World!!   This is   Python.  "
print(clean_text(dirty))  # "hello world this is python"
```

### CSV 解析

```python
def parse_csv_line(line):
    """解析 CSV 一行（處理引號）"""
    result = []
    current = ""
    in_quotes = False

    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            result.append(current.strip())
            current = ""
        else:
            current += char

    result.append(current.strip())
    return result

line = 'Alice,25,"台北市,大安區",工程師'
print(parse_csv_line(line))
# ['Alice', '25', '台北市,大安區', '工程師']
```

### 密碼強度檢查

```python
import re

def check_password_strength(password):
    """檢查密碼強度"""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("長度至少 8 個字元")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("需要大寫字母")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("需要小寫字母")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("需要數字")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("需要特殊字元")

    levels = ["極弱", "弱", "中等", "強", "極強"]
    return levels[score], feedback

strength, issues = check_password_strength("Abc123!@")
print(f"密碼強度：{strength}")
if issues:
    print("建議：", ", ".join(issues))
```

## 字串效能考量

```python
from time import perf_counter

# 不推薦：使用 + 串接大量字串
def slow_join(items):
    result = ""
    for item in items:
        result += item + ", "
    return result

# 推薦：使用 join
def fast_join(items):
    return ", ".join(items)

items = ["item"] * 10000

start = perf_counter()
slow_join(items)
print(f"慢速方法：{perf_counter() - start:.4f} 秒")

start = perf_counter()
fast_join(items)
print(f"快速方法：{perf_counter() - start:.4f} 秒")
```

## 小結

字串操作是程式設計中最常見的任務之一。從基本的格式化到正規表示式，從資料清理到驗證，熟練掌握這些技巧將讓你的 Python 程式更強大、更高效。

---

**延伸閱讀**

- [Python 官方文件 — 字串](https://www.google.com/search?q=Python+string+methods+documentation)
- [正規表示式教學](https://www.google.com/search?q=Python+regex+tutorial)
