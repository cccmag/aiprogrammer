# 用 Python 取代 Shell 腳本

## 為什麼要考慮取代 Shell？

Shell 腳本在簡單任務中表現出色，但當腳本變得複雜時，Python 提供了更好的選擇：

| 比較 | Shell 腳本 | Python |
|------|-----------|--------|
| 可讀性 | 語法簡潔但晦澀 | 清晰易讀 |
| 除錯 | set -x 除錯 | pdb, 單步追蹤 |
| 資料結構 | 只有字串和陣列 | 串列、字典、集合 |
| 錯誤處理 | exit code | try/except |
| 跨平台 | Linux 限定 | Linux/macOS/Windows |
| 函式庫 | 需外部命令 | 豐富的標準函式庫 |

## 對應關係速查

```python
# Shell → Python 對應

import os, shutil, glob, subprocess, sys

# ls → os.listdir()
files = os.listdir(".")

# cp → shutil.copy()
shutil.copy("src.txt", "dst.txt")

# mv → shutil.move()
shutil.move("old.txt", "new.txt")

# rm → os.remove()
os.remove("file.txt")

# rm -rf → shutil.rmtree()
shutil.rmtree("temp_dir/")

# mkdir -p → os.makedirs()
os.makedirs("a/b/c", exist_ok=True)

# find → glob.glob()
for f in glob.glob("**/*.py", recursive=True):
    print(f)

# grep → re.search()
import re
with open("file.txt") as f:
    matches = [line for line in f if re.search("pattern", line)]

# sort → sorted()
sorted_lines = sorted(open("file.txt"))

# uniq → set()
unique = set(open("file.txt"))
```

## 完整替代範例

### Shell 版本

```bash
#!/bin/bash
# 分析日誌：找出每個 IP 的請求次數

LOG_FILE="access.log"
OUTPUT_FILE="ip_count.txt"

if [ ! -f "$LOG_FILE" ]; then
    echo "錯誤: $LOG_FILE 不存在" >&2
    exit 1
fi

grep -oP '^\S+' "$LOG_FILE" | sort | uniq -c | sort -rn > "$OUTPUT_FILE"
echo "分析完成，結果已寫入 $OUTPUT_FILE"
```

### Python 版本

```python
#!/usr/bin/env python3
"""分析日誌：找出每個 IP 的請求次數"""

import re, sys
from collections import Counter

def analyze_log(log_path, output_path):
    try:
        with open(log_path) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"錯誤: {log_path} 不存在", file=sys.stderr)
        sys.exit(1)

    ip_pattern = re.compile(r'^\S+')
    ips = []

    for line in lines:
        match = ip_pattern.match(line)
        if match:
            ips.append(match.group())

    counter = Counter(ips)

    with open(output_path, "w") as f:
        for ip, count in counter.most_common():
            f.write(f"{count:>8} {ip}\n")

    print(f"分析完成，結果已寫入 {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"用法: {sys.argv[0]} <輸入日誌> <輸出檔案>", file=sys.stderr)
        sys.exit(1)
    analyze_log(sys.argv[1], sys.argv[2])
```

## 檔案系統監控

```python
#!/usr/bin/env python3
"""監控目錄變化"""

import os, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"修改: {event.src_path}")

    def on_created(self, event):
        print(f"建立: {event.src_path}")

    def on_deleted(self, event):
        print(f"刪除: {event.src_path}")

def watch_directory(path):
    observer = Observer()
    observer.schedule(ChangeHandler(), path, recursive=True)
    observer.start()
    print(f"監控中: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_directory(".")
```

## 命令列參數處理

```bash
# Shell 方式
while getopts "i:o:v" opt; do
    case $opt in
        i) input="$OPTARG" ;;
        o) output="$OPTARG" ;;
        v) verbose=true ;;
    esac
done
```

```python
# Python 方式
import argparse

parser = argparse.ArgumentParser(description="檔案處理工具")
parser.add_argument("-i", "--input", required=True, help="輸入檔案")
parser.add_argument("-o", "--output", default="output.txt", help="輸出檔案")
parser.add_argument("-v", "--verbose", action="store_true", help="詳細輸出")
args = parser.parse_args()

print(f"輸入: {args.input}, 輸出: {args.output}")
```

## 何時該用 Shell vs Python？

| 場景 | 建議 |
|------|------|
| 簡單的檔案操作 (`cp`, `mv`, `rm`) | Shell |
| 管線命令 (`ps aux | grep foo`) | Shell |
| 安裝套件 (`apt install`) | Shell |
| 複雜的資料處理 | Python |
| 條件邏輯多的腳本 | Python |
| 跨平台需求 | Python |
| 需要外部 API / 資料庫 | Python |

---

## 延伸閱讀

- [Python subprocess 模組](https://www.google.com/search?q=Python+subprocess+module+run+shell+commands)
- [Python argparse 命令列參數](https://www.google.com/search?q=Python+argparse+command+line+arguments+tutorial)
- [Python 取代 Shell 腳本指南](https://www.google.com/search?q=Python+replace+shell+scripting+guide)
