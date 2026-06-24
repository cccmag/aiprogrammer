# Linux 工具 Python 實作

## 前言

理論說得再多，不如親手實作。本篇文章將透過 Python 模擬 Linux 命令列工具的核心功能，幫助讀者理解檔案操作、文字處理、環境變數和行程管理等底層機制。

完整原始碼請參考：[_code/linux_tools.py](_code/linux_tools.py)

## 核心功能實作

### 1. 檔案系統操作

模擬 `ls` 命令列出目錄內容：

```python
import os, stat

def list_directory(path="."):
    files = os.listdir(path)
    for f in sorted(files):
        fp = os.path.join(path, f)
        st = os.stat(fp)
        mode = "d" if os.path.isdir(fp) else "-"
        perm = stat.filemode(st.st_mode)
        print(f"{mode}{perm[1:]}  {st.st_size:>8}  {f}")
```

### 2. 文字搜尋 (grep)

用 Python 實作 grep 的過濾功能：

```python
import re

def grep(pattern, lines, ignore_case=False):
    flag = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flag)
    return [line for line in lines if regex.search(line)]
```

### 3. 文字取代 (sed)

用 Python 實作 sed 的取代功能：

```python
def sed(pattern, replacement, lines):
    import re
    return [re.sub(pattern, replacement, line) for line in lines]
```

### 4. 欄位處理 (awk)

用 Python 處理類似 awk 的欄位分割：

```python
import csv

def awk_like(text, delimiter=",", field=None):
    lines = text.strip().split("\n")
    reader = csv.reader(lines, delimiter=delimiter)
    results = []
    for row in reader:
        if field:
            results.append(row[field - 1])
        else:
            results.append(row)
    return results
```

### 5. 環境變數

讀取和操作環境變數：

```python
import os

def show_env():
    for key in ["HOME", "USER", "SHELL", "PATH", "PWD"]:
        print(f"{key}={os.environ.get(key, 'N/A')}")
```

### 6. 行程管理

組合 `ps` 和 `grep` 來過濾行程：

```python
import subprocess

def find_process(name):
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    header = lines[0]
    matches = [line for line in lines[1:] if name in line]
    return header, matches
```

### 7. 管線串接

模擬 Unix 管線 (pipe) 的資料流：

```python
def pipeline(data, *functions):
    """依序將資料通過所有函式處理"""
    result = data
    for func in functions:
        result = func(result)
    return result

# 範例: ps aux | grep python | wc -l
data = subprocess.run(["ps", "aux"], capture_output=True, text=True)
filtered = [line for line in data.stdout.split("\n") if "python" in line]
count = len(filtered)
print(f"Python 行程數: {count}")
```

## 執行結果

```bash
$ python3 linux_tools.py
=== Linux 命令列工具 Python 模擬 ===

--- 1. ls：列出目錄 ---
  /path/to/code 內有 2 個項目:
  -rw-r--r--  4222  linux_tools.py
  -rw-r--r--    30  test.sh

--- 5. grep：搜尋 ---
  grep 'a': ['apple', 'banana', 'date']

--- 6. sed：取代 ---
  sed 's/hello/hi/g': hi world, hi linux

--- 7. awk：欄位處理 ---
  $1=Alice      $2=30    $3=Engineer

--- 8. 環境變數與 PATH ---
  PATH 有 34 個目錄
  HOME=/Users/cccuser

--- 11. 檔案權限 ---
  chmod 755: -rwxr-xr-x
  chmod 644: -rw-r--r--
```

## 設計理念

Linux 工具的核心哲學是「組合勝過整合」。每一個工具只做好一件事，但透過管線組合可以建構出極其強大的資料處理鏈。

Python 的模擬展示了同樣的思想——我們的每個函式都很簡單，但將它們組合起來就能完成複雜的任務：

```
ls_output → grep("\.py") → awk("{print $NF}") → sort → uniq
```

這種「資料流程式設計」(Dataflow Programming) 不僅是 Unix 的精髓，也深深影響了現代大資料處理框架 (如 Hadoop 的 MapReduce、Apache Spark 的 RDD)。

## 延伸練習

1. 嘗試實作 `sort` 命令的 Python 版本
2. 實作 `uniq -c` 的計數功能
3. 建立一個類 Unix 管線的鏈式處理 API
4. 用 Python 實作完整版的 `wc` (支援行數、字數、字元數)

---

## 延伸閱讀

- [Linux 命令列工具 Python 模擬](_code/linux_tools.py) — 完整原始碼
- [文字處理工具](focus4.md) — grep、sed、awk 深入介紹
- [Shell 腳本程式設計](focus5.md) — Bash 自動化技巧
