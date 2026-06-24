# 正規表達式進階應用

正規表達式（Regular Expressions）是處理文字的強大工具。本文介紹進階技巧，幫助讀者處理複雜的文字模式。

## 1. 群組與命名群組

使用括號分組，方便提取和引用：

```python
import re

text = "2021-07-15"

pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
match = re.search(pattern, text)

if match:
    print(f"年: {match.group('year')}")
    print(f"月: {match.group('month')}")
    print(f"日: {match.group('day')}")
```

## 2. 前瞻與後顧

只匹配特定上下文中的模式：

```python
text = "$100 USD and 200 EUR"

lookahead = re.findall(r'\d+(?= USD)', text)
print(lookahead)  # ['100']
```

## 3. 非貪心匹配

使用 `*?` 或 `+?` 進行最小匹配：

```python
html = "<div>content</div><div>more</div>"

greedy = re.findall(r'<div>.*</div>', html)
non_greedy = re.findall(r'<div>.*?</div>', html)

print(f"貪心: {greedy}")
print(f"非貪心: {non_greedy}")
```

## 4. 複雜替代

使用回調函數進行複雜的替換邏輯：

```python
def convert_date(match):
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = int(match.group(2))
    return f"{match.group(1)}-{month_names[month-1]}-{match.group(3)}"

text = "Date: 2021-07-15"
result = re.sub(r'(\d{4})-(\d{2})-(\d{2})', convert_date, text)
print(result)  # Date: 15-Jul-2021
```

## 5. 編譯與複用

預先編譯模式以提高效能：

```python
pattern = re.compile(r'\b[\w.-]+@[\w.-]+\.\w+\b')

emails1 = pattern.findall(text1)
emails2 = pattern.findall(text2)
```

---

## 延伸閱讀

- [Python re 模組文檔](https://www.google.com/search?q=Python+re+module+documentation)
- [正規表達式語法參考](https://www.google.com/search?q=regular+expression+syntax+reference)