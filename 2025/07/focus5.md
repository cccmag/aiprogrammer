# Shell 腳本程式設計

## 為什麼要學 Shell 腳本

Shell 腳本是將命令列指令串接成自動化流程的程式設計語言。它特別適合檔案操作、系統管理和自動化任務。如果你發現自己在重複輸入相同的命令序列，那就是寫腳本的時候了。

### 腳本基本結構

```bash
#!/bin/bash
# 這是一個註解

echo "Hello, Linux!"
```

第一行 `#!/bin/bash` 稱為 shebang，告訴系統用哪個直譯器執行此腳本。

## 變數與引數

```bash
#!/bin/bash

# 變數賦值 (等號兩邊不能有空格)
name="Alice"
count=42

# 使用變數
echo "Hello, $name"
echo "You have $count messages"

# 命令替換
files=$(ls)
today=$(date +%Y-%m-%d)

# 特殊變數
echo "腳本名稱: $0"
echo "參數數量: $#"
echo "所有參數: $@"
echo "第一個參數: $1"
```

## 條件判斷

```bash
#!/bin/bash

# if-then-else
if [ -f "$1" ]; then
    echo "$1 是一個檔案"
elif [ -d "$1" ]; then
    echo "$1 是一個目錄"
else
    echo "$1 不存在"
fi

# 比較運算子
# 字串: =, !=, -z (空字串)
# 數字: -eq, -ne, -lt, -gt, -le, -ge
# 檔案: -f (檔案), -d (目錄), -e (存在), -s (非空)

# case 語句
case "$1" in
    start) echo "啟動..." ;;
    stop)  echo "停止..." ;;
    restart) echo "重啟..." ;;
    *)     echo "用法: $0 {start|stop|restart}" ;;
esac
```

## 迴圈

```bash
#!/bin/bash

# for 迴圈
echo "--- for 迴圈 ---"
for file in *.txt; do
    echo "處理: $file"
    wc -l "$file"
done

# while 迴圈
echo "--- while 迴圈 ---"
count=1
while [ $count -le 5 ]; do
    echo "計數: $count"
    count=$((count + 1))
done

# 讀取檔案
echo "--- 讀取檔案 ---"
while read -r line; do
    echo "行: $line"
done < /etc/hostname
```

## 函式

```bash
#!/bin/bash

# 定義函式
log() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}

# 使用函式
log "INFO" "系統啟動完成"
log "ERROR" "磁碟空間不足"

# 函式回傳值
is_directory() {
    [ -d "$1" ]
    return $?
}

if is_directory "/tmp"; then
    echo "/tmp 是目錄"
fi
```

## Python 模擬 Shell 腳本

```python
#!/usr/bin/env python3
"""用 Python 取代 Shell 腳本"""

import os, sys, glob, subprocess
from datetime import datetime

def log(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def backup_files(src_pattern, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for f in glob.glob(src_pattern):
        dst = os.path.join(dst_dir, os.path.basename(f))
        subprocess.run(["cp", f, dst])
        log("INFO", f"已備份 {f} -> {dst}")

if __name__ == "__main__":
    backup_files("*.txt", "/tmp/backup")
```

## 除錯技巧

```bash
# 啟用除錯模式
bash -x script.sh          # 執行時顯示每個命令
set -x                     # 腳本中啟用
set +x                     # 腳本中停用

# Shell 檢查語法
bash -n script.sh          # 語法檢查，不執行
```

---

## 延伸閱讀

- [Bash 腳本入門教學](https://www.google.com/search?q=Bash+shell+scripting+tutorial+for+beginners)
- [Shell 腳本除錯技巧](https://www.google.com/search?q=shell+script+debugging+set+x+bash)
- [Bash 程式設計指南](https://www.google.com/search?q=Bash+programming+guide+variables+loops+functions)
