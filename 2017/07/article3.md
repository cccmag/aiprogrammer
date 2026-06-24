# 檔案處理與 JSON

## 檔案讀寫基礎

### 開啟檔案

```python
# 讀取
f = open("file.txt", "r", encoding="utf-8")
content = f.read()
f.close()

# 使用 with（自動關閉）
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 寫入檔案

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")

# 附加
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("Another line\n")
```

### 讀取模式

| 模式 | 說明 |
|------|------|
| r | 唯讀（預設） |
| w | 唯寫（覆蓋） |
| a | 附加 |
| rb/wb | 二進位模式 |

## 逐行讀取

```python
# readlines()
with open("file.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        print(line.rstrip())

# 直接迭代（記憶體效率更好）
with open("file.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip())
```

## JSON 處理

### 基本操作

```python
import json

# Python 物件轉 JSON 字串
data = {"name": "Alice", "age": 30, "scores": [90, 85, 88]}
json_str = json.dumps(data)
print(json_str)
# {"name": "Alice", "age": 30, "scores": [90, 85, 88]}

# JSON 字串轉 Python 物件
parsed = json.loads(json_str)
print(parsed["name"])  # Alice
```

### 格式化輸出

```python
# 縮排
print(json.dumps(data, indent=2))

# 排序 key
print(json.dumps(data, sort_keys=True, indent=2))
```

### 檔案操作

```python
# 寫入 JSON 檔案
data = {"name": "Bob", "age": 25}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 讀取 JSON 檔案
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded)
```

### 中文處理

```python
data = {"name": "王小明", "city": "台北"}

# ensure_ascii=False 保持中文
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## CSV 處理

### 基本讀寫

```python
import csv

# 讀取
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 寫入
data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

### 使用字典

```python
# 讀取為字典
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["Name"], row["Age"])

# 寫入字典
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["Name", "Age"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"Name": "Alice", "Age": 30})
```

## 路徑處理

```python
import os
from pathlib import Path

# 路徑拼接
path = os.path.join("dir", "subdir", "file.txt")

# 檢查存在
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("directory")

# 取得目錄
dirname = os.path.dirname("/path/to/file.txt")  # /path/to
basename = os.path.basename("/path/to/file.txt")  # file.txt

# Path 物件（Python 3.4+）
p = Path("/path/to/file.txt")
print(p.parent, p.name, p.stem, p.suffix)
```

## 檔案壓縮

```python
import gzip
import zipfile

# gzip 壓縮
with gzip.open("file.txt.gz", "wt", encoding="utf-8") as f:
    f.write("Hello, compressed world!")

# zip 檔案
with zipfile.ZipFile("archive.zip", "w") as zf:
    zf.write("file.txt")
    zf.write("another.txt")

# 讀取 zip
with zipfile.ZipFile("archive.zip", "r") as zf:
    print(zf.namelist())
    content = zf.read("file.txt").decode("utf-8")
```

## 總結

Python 的檔案處理簡潔直觀。with 語句自動管理資源。json 模組處理 JSON 格式，csv 模組處理 CSV 格式。pathlib 提供更現代的路徑操作。