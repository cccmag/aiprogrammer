# Bash 腳本入門

## 什麼是 Bash 腳本？

Bash 腳本是將一系列 Shell 命令寫入檔案，讓系統自動依序執行。當你需要重複執行相同操作時，腳本就是你的最佳選擇。

### 腳本建立

```bash
#!/bin/bash
# 我的第一個腳本

echo "Hello, World!"
echo "今天是 $(date)"
echo "目前目錄: $PWD"
```

```bash
# 執行程式
chmod +x myscript.sh
./myscript.sh

# 或用 bash 直接執行
bash myscript.sh
```

## 變數深度解析

### 變數類型

```bash
# 字串變數
name="Alice"
echo "Hello, $name"

# 數字 (Bash 只有整數)
count=10
echo $((count + 5))

# 唯讀變數
readonly MAX_COUNT=100

# 陣列
colors=("red" "green" "blue")
echo ${colors[0]}        # red
echo ${colors[@]}        # 所有元素
echo ${#colors[@]}       # 陣列長度

# 關聯陣列 (Bash 4+)
declare -A capitals
capitals[Taiwan]="Taipei"
capitals[Japan]="Tokyo"
echo ${capitals[Taiwan]}
```

### 變數擴展

```bash
filename="photo.jpg"
echo ${filename%.*}      # photo (移除最短尾碼)
echo ${filename%%.*}     # photo (移除最長尾碼)
echo ${filename#*.}      # jpg (移除最短前綴)
echo ${filename##*.}     # jpg (移除最長前綴)

text="Hello World"
echo ${text:0:5}         # Hello (子字串)
echo ${text/World/Linux} # Hello Linux (取代)

# 預設值
echo ${name:-Guest}      # 若 name 未設定，使用 Guest
echo ${name:?錯誤}       # 若未設定則顯示錯誤並退出
```

## 條件判斷深入

### 檔案測試

```bash
[ -f "file" ]    # 是檔案
[ -d "dir" ]     # 是目錄
[ -e "path" ]    # 存在
[ -s "file" ]    # 非空檔案
[ -x "file" ]    # 可執行
[ -w "file" ]    # 可寫入
[ -r "file" ]    # 可讀取
[ -L "link" ]    # 是符號連結
```

### 複合條件

```bash
# && (AND) || (OR)
[ -f "$1" ] && echo "是檔案" || echo "不是檔案"

# 雙中括號 (Bash 擴展)
if [[ "$name" == A* ]]; then
    echo "以 A 開頭"
fi

# 正則匹配
if [[ "$email" =~ ^[a-z]+@[a-z]+\.[a-z]+$ ]]; then
    echo "有效 Email"
fi
```

## 函式與作用域

```bash
#!/bin/bash

# 定義函式
usage() {
    echo "用法: $0 <input> [output]"
    echo "參數:"
    echo "  input  輸入檔案"
    echo "  output 輸出檔案 (預設: output.txt)"
    exit 1
}

process_file() {
    local input="$1"    # local 限定函式內作用域
    local output="${2:-output.txt}"

    if [[ ! -f "$input" ]]; then
        echo "錯誤: $input 不存在" >&2
        return 1
    fi

    sort "$input" | uniq > "$output"
    echo "處理完成: $output"
}

# 主程式
if [[ $# -lt 1 ]]; then
    usage
fi

process_file "$1" "$2"
```

## 實戰腳本範例

### 批次備份腳本

```bash
#!/bin/bash
# 備份所有 .txt 檔案

BACKUP_DIR="/tmp/backup_$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

for file in *.txt; do
    if [[ -f "$file" ]]; then
        cp -v "$file" "$BACKUP_DIR/"
    fi
done

echo "備份完成: $BACKUP_DIR"
```

### 系統資訊腳本

```bash
#!/bin/bash
echo "=== 系統資訊 ==="
echo "主機名: $(hostname)"
echo "核心: $(uname -r)"
echo "CPU: $(nproc) 核心"
echo "記憶體: $(free -h | awk '/Mem:/ {print $3 "/" $2}')"
echo "磁碟: $(df -h / | awk 'NR==2 {print $3 "/" $2}')"
echo "負載: $(uptime | awk -F'load average:' '{print $2}')"
```

## Python 中的 Bash 腳本等效

```python
#!/usr/bin/env python3
"""Python 版備份腳本"""

import os, shutil, glob
from datetime import datetime

def backup_txt_files():
    backup_dir = f"/tmp/backup_{datetime.now():%Y%m%d}"
    os.makedirs(backup_dir, exist_ok=True)

    for filepath in glob.glob("*.txt"):
        if os.path.isfile(filepath):
            dest = os.path.join(backup_dir, os.path.basename(filepath))
            shutil.copy2(filepath, dest)
            print(f"已備份: {filepath} -> {dest}")

    print(f"備份完成: {backup_dir}")

if __name__ == "__main__":
    backup_txt_files()
```

---

## 延伸閱讀

- [Bash 腳本教學](https://www.google.com/search?q=Bash+shell+scripting+tutorial+beginners)
- [Bash 陣列與關聯陣列](https://www.google.com/search?q=Bash+array+associative+array+tutorial)
- [Bash 條件判斷大全](https://www.google.com/search?q=Bash+conditional+statements+test+bracket)
