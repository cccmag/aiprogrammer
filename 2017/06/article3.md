# 文章 3：檔案處理與 I/O

## 前言

檔案處理是 Python 程式設計的基礎技能。本章節介紹檔案讀寫、目錄操作等 I/O 相關功能。

## 基本檔案讀寫

```python
# 寫入檔案
with open('example.txt', 'w', encoding='utf-8') as f:
    f.write("Hello, World!\n")
    f.write("第二行")

# 讀取檔案
with open('example.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 逐行讀取
with open('example.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())
```

## 檔案模式

| 模式 | 說明 |
|------|------|
| 'r' | 讀取（預設） |
| 'w' | 寫入（覆蓋） |
| 'a' | 附加 |
| 'x' | 新建（若存在則失敗） |
| 'b' | 二進制模式 |
| 't' | 文字模式（預設） |

## JSON 檔案

```python
import json

data = {"name": "Alice", "age": 25, "skills": ["Python", "ML"]}

# 寫入 JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 讀取 JSON
with open('data.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)
    print(loaded)
```

## CSV 檔案

```python
import csv

# 寫入 CSV
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Age', 'City'])
    writer.writerow(['Alice', 25, 'Taipei'])
    writer.writerow(['Bob', 30, 'Kaohsiung'])

# 讀取 CSV
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

## 目錄操作

```python
import os

print(os.getcwd())           # 當前目錄
print(os.listdir('.'))       # 列出目錄內容
os.makedirs('new_dir', exist_ok=True)  # 建立目錄
os.rmdir('empty_dir')        # 刪除空目錄
os.remove('file.txt')        # 刪除檔案

# 路徑處理
print(os.path.join('dir', 'file.txt'))  # 路徑連接
print(os.path.exists('file.txt'))        # 檢查存在
print(os.path.isfile('file.txt'))        # 是否為檔案
print(os.path.isdir('dir'))              # 是否為目錄
```

## 路徑處理

```python
from pathlib import Path

p = Path('dir/subdir/file.txt')

print(p.parent)       # dir/subdir
print(p.name)         # file.txt
print(p.stem)         # file
print(p.suffix)       # .txt
print(p.parts)        # ('dir', 'subdir', 'file.txt')
```

## 總結

Python 的 I/O 功能簡潔強大。熟練掌握檔案讀寫與目錄操作是處理數據的基礎技能。

## 延伸閱讀

- https://www.google.com/search?q=Python+file+I/O+操作
- https://www.google.com/search?q=Python+JSON+CSV+handling