# 檔案處理與例外處理

## 簡介

程式中常需要讀寫檔案和處理錯誤。Python 提供了簡潔的檔案操作和例外處理機制。

## 檔案讀寫

### 基本讀寫

```python
# 寫入檔案
with open("example.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("第二行")

# 讀取檔案
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

### 按行讀取

```python
with open("example.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

### 讀取所有行

```python
with open("example.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())
```

### 附加內容

```python
with open("example.txt", "a", encoding="utf-8") as f:
    f.write("\n附加內容")
```

## 例外處理

### 基本語法

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
```

### 多種例外

```python
try:
    num = int(input("輸入數字: "))
    result = 10 / num
except ValueError:
    print("請輸入有效數字")
except ZeroDivisionError:
    print("不能除以零")
```

### 取得例外物件

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"錯誤: {e}")
```

### 完整範例

```python
try:
    number = int(input("輸入一個整數: "))
    print(f"你輸入的是: {number}")
except ValueError as e:
    print(f"輸入錯誤: {e}")
else:
    print("輸入成功!")
finally:
    print("程式結束")
```

### 拋出例外

```python
def divide(a, b):
    if b == 0:
        raise ValueError("除數不能為零")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print(f"錯誤: {e}")
```

## 實用範例

### 讀取 CSV 檔案

```python
import csv

with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(",".join(row))
```

### 寫入 CSV 檔案

```python
import csv

data = [
    ["Name", "Age", "City"],
    ["Alice", "30", "Taipei"],
    ["Bob", "25", "Kaohsiung"]
]

with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

### 讀取 JSON

```python
import json

# 讀取 JSON
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    print(config)

# 寫入 JSON
data = {"name": "Alice", "age": 30}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
```

### 處理不存在的檔案

```python
import os

filename = "nonexistent.txt"

if os.path.exists(filename):
    with open(filename, "r") as f:
        print(f.read())
else:
    print(f"檔案 {filename} 不存在")
```

### 使用 pathlib

```python
from pathlib import Path

# 讀取檔案
p = Path("example.txt")
if p.exists():
    content = p.read_text(encoding="utf-8")
    print(content)

# 寫入檔案
p.write_text("Hello!", encoding="utf-8")

# 列出目錄內容
for item in Path(".").iterdir():
    print(item.name)
```

## 最佳實踐

1. **永遠使用 with 語句** - 自動關閉檔案
2. **指定 encoding** - 避免編碼問題
3. **處理所有可能的錯誤** - 包括檔案不存在、權限不足等
4. **使用 pathlib** - 更現代的檔案處理方式

## 練習題

1. 寫一個程式複製檔案內容
2. 寫一個程式統計文字檔中的行數、字數、字元數
3. 寫一個程式搜尋資料夾中所有 .txt 檔案