# 模組與套件管理

## 為什麼需要模組？

隨著程式規模增長，將所有程式碼放在同一個檔案中會變得難以維護。模組（Module）讓我們可以將相關的函數和類別分組到不同的檔案中。

### 模組的優點

- **組織性**：相關功能集中在同一個檔案
- **可重用性**：一次編寫，多處使用
- **命名空間**：避免名稱衝突
- **維護性**：修改一個模組不影響其他部分

## 建立與匯入模組

### 建立模組

建立一個 `math_utils.py` 檔案：

```python
# math_utils.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("不能除以零")
    return a / b

PI = 3.14159

class Calculator:
    """簡單的計算器類別"""
    def __init__(self):
        self.history = []

    def calculate(self, op, a, b):
        operations = {
            "+": add,
            "-": subtract,
            "*": multiply,
            "/": divide
        }
        if op not in operations:
            raise ValueError(f"不支援的操作：{op}")
        result = operations[op](a, b)
        self.history.append(f"{a} {op} {b} = {result}")
        return result
```

### 匯入與使用

```python
# 方法一：匯入整個模組
import math_utils
print(math_utils.add(5, 3))      # 8
print(math_utils.PI)             # 3.14159

# 方法二：匯入特定名稱
from math_utils import Calculator, PI
calc = Calculator()
print(calc.calculate("+", 10, 5))  # 15

# 方法三：匯入所有名稱（不推薦）
from math_utils import *

# 方法四：使用別名
import math_utils as mu
print(mu.multiply(4, 7))  # 28
```

## 套件 (Package)

套件是包含多個模組的目錄。

### 建立套件結構

```
mypackage/
├── __init__.py
├── math_ops.py
├── string_ops.py
└── io_ops.py
```

```python
# __init__.py
from .math_ops import add, subtract
from .string_ops import reverse, capitalize
from .io_ops import read_file, write_file

__version__ = "1.0.0"
```

### 使用套件

```python
import mypackage
print(mypackage.add(5, 3))     # 8
print(mypackage.reverse("hello"))  # olleh

# 或
from mypackage.math_ops import add, subtract
from mypackage.io_ops import read_file
```

## Python 標準庫精選

Python 自帶了豐富的標準庫，不需要額外安裝：

### 常用標準庫

```python
import os
import sys
import json
import math
import random
import datetime
import collections
import itertools
import re
import hashlib
import csv
import pathlib
```

### 實用範例

```python
# 路徑操作
from pathlib import Path

current = Path(".")
for f in current.glob("*.py"):
    print(f.name, f.stat().st_size, "bytes")

# 時間處理
from datetime import datetime, timedelta

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
yesterday = now - timedelta(days=1)
print(f"昨天：{yesterday.date()}")

# 隨機功能
import random

print(random.randint(1, 100))       # 隨機整數
print(random.choice(["A", "B", "C"]))  # 隨機選擇
print(random.sample(range(100), 5))    # 不重複隨機抽樣

# 數學運算
import math

print(math.sqrt(16))      # 4.0
print(math.factorial(5))  # 120
print(math.pi)            # 3.14159...
```

## pip 與第三方套件

### 搜尋與安裝套件

```bash
# 搜尋套件
pip search requests

# 安裝套件
pip install requests
pip install "numpy>=1.20,<2.0"

# 從 requirements.txt 安裝
pip install -r requirements.txt
```

### 常用第三方套件

```python
# requests — HTTP 請求
import requests
response = requests.get("https://api.github.com")
print(response.status_code)
print(response.json()["current_user_url"])

# beautifulsoup4 — HTML 解析
from bs4 import BeautifulSoup
soup = BeautifulSoup("<html><body><h1>標題</h1></body></html>", "html.parser")
print(soup.h1.text)  # 標題
```

## __name__ == "__main__"

這個慣用語讓一個檔案既可以作為模組匯入，也可以作為腳本執行：

```python
# calculator.py
def add(a, b):
    return a + b

def main():
    print("=== 計算機 ===")
    while True:
        expr = input("請輸入運算式（或按 q 離開）：")
        if expr.lower() == "q":
            break
        try:
            a, op, b = expr.split()
            result = eval(f"{a} {op} {b}")
            print(f"結果：{result}")
        except:
            print("輸入格式錯誤")

if __name__ == "__main__":
    main()
```

```bash
# 作為腳本執行
python calculator.py

# 作為模組匯入（main 不會被執行）
from calculator import add
print(add(5, 3))  # 8
```

## 實戰：建立自己的套件

```python
"""
textutils — 文字處理工具套件
"""

# textutils/__init__.py
from .cleaning import clean_text, remove_punctuation
from .stats import word_count, char_count, line_count

# textutils/cleaning.py
def clean_text(text):
    """清理文字：移除多餘空白、轉為小寫"""
    return ' '.join(text.lower().split())

def remove_punctuation(text):
    """移除標點符號"""
    import string
    return text.translate(str.maketrans('', '', string.punctuation))

# textutils/stats.py
def word_count(text):
    return len(text.split())

def char_count(text):
    return len(text)

def line_count(text):
    return len(text.splitlines())

# 使用範例
import textutils

text = "Hello, World!  This is Python."
cleaned = textutils.clean_text(text)
print(cleaned)  # "hello, world! this is python."
print(textutils.word_count(cleaned))  # 5
```

## 小結

模組與套件管理是 Python 生態系統的核心。學會如何組織自己的程式碼成為可重用的模組，以及如何利用豐富的第三方套件，將讓你的開發效率大幅提升。

---

**延伸閱讀**

- [Python 官方文件 — 模組](https://www.google.com/search?q=Python+modules+tutorial)
- [PyPI — Python 套件索引](https://www.google.com/search?q=PyPI+Python+package+index)
