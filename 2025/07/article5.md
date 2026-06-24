# grep 搜尋技巧

## grep 基礎回顧

grep (Global Regular Expression Print) 從檔案或標準輸入中搜尋符合模式的行。這是最常用的命令列搜尋工具。

```bash
grep "pattern" file.txt
```

## 實用選項大全

### 控制輸出

```bash
grep -n "error" log.txt       # 加上行號
grep -c "error" log.txt       # 只計算行數
grep -l "main" *.c            # 只顯示檔名
grep -L "main" *.c            # 顯示不匹配的檔名
grep -o "error" log.txt       # 只顯示匹配的文字
grep -m 10 "error" log.txt    # 只顯示前 10 個匹配
```

### 搜尋模式

```bash
grep -i "warning" log.txt     # 忽略大小寫
grep -v "debug" log.txt       # 反向匹配
grep -w "error" log.txt       # 全字匹配
grep -x "ERROR" log.txt       # 整行匹配
grep -F "*.py" files.txt      # 固定字串 (無正則)
```

### 上下文控制

```bash
grep -A 3 "error" log.txt     # 顯示匹配後 3 行
grep -B 2 "error" log.txt     # 顯示匹配前 2 行
grep -C 2 "error" log.txt     # 顯示匹配前後各 2 行
```

### 遞迴搜尋

```bash
grep -r "TODO" src/           # 遞迴搜尋目錄
grep -R "function" .          # 跟隨符號連結
grep -r --include="*.py" "def" .    # 只搜尋特定檔案
grep -r --exclude="*.min.js" "var" .  # 排除特定檔案
grep -r --exclude-dir="node_modules" "require" .  # 排除目錄
```

## 正規表示法深入

### 基礎正則 (BRE)

```bash
grep "^Start" file            # 行首
grep "End$" file              # 行尾
grep "a.b" file               # 單一字元 (.)
grep "ab*" file               # 零或多個 b (*)
grep "[abc]" file             # 字元集合
grep "[^abc]" file            # 排除字元
grep "a\{3\}" file            # 精確重複 3 次 (使用 \{ \})
```

### 擴展正則 (ERE)

```bash
grep -E "error|fail" log      # 多選 (|)
grep -E "ba+" file            # 一次或多次 (+)
grep -E "col(o|ou)r" file     # 分組
grep -E "[0-9]{3}-[0-9]{4}" file  # 重複次數
grep -E "foo?" file           # 零或一次 (?)
```

### Perl 相容正則 (PCRE)

```bash
grep -P "\d{3}-\d{4}" file    # 數字 (\d)
grep -P "\w+@\w+\.\w+" file   # 單字字元 (\w)
grep -P "\s+" file            # 空白字元 (\s)
grep -P "(?<=@)\w+" file      # lookbehind
grep -P "foo(?=bar)" file     # lookahead
```

## 實戰案例

### 日誌分析

```bash
# 統計錯誤類型
grep -o "ERROR\|WARN\|INFO" app.log | sort | uniq -c | sort -rn

# 找出 5XX 錯誤
grep -E '" 5[0-9][0-9] ' access.log

# 找出特定時間範圍
grep "2026-07-01 1[0-9]:" access.log

# IP 位址提取
grep -oP "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" access.log | sort | uniq -c | sort -rn | head -10
```

### 程式碼搜尋

```bash
# 找出函式定義
grep -rn "^def " src/

# 找出 TODO 註解
grep -rn "TODO\|FIXME\|HACK" src/ --include="*.py"

# 找出 import 陳述
grep -rn "^import\|^from" src/ | sort | uniq
```

### Python 實作 grep

```python
import re, os

def pygrep(pattern, paths, recursive=False, ignore_case=False):
    """Python 版 grep"""
    flag = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flag)
    results = []

    for path in paths:
        if os.path.isfile(path):
            files = [path]
        elif recursive and os.path.isdir(path):
            files = []
            for root, dirs, filenames in os.walk(path):
                files.extend(os.path.join(root, f) for f in filenames)
        else:
            continue

        for filepath in files:
            try:
                with open(filepath, "r", errors="ignore") as f:
                    for lineno, line in enumerate(f, 1):
                        if regex.search(line):
                            results.append((filepath, lineno, line.rstrip()))
            except (IOError, OSError):
                pass

    return results

# 使用範例
matches = pygrep("def ", ["src/"], recursive=True)
for filepath, lineno, line in matches[:5]:
    print(f"{filepath}:{lineno}:{line}")
```

---

## 延伸閱讀

- [grep 命令完整教學](https://www.google.com/search?q=grep+command+Linux+tutorial+examples)
- [正規表示法入門](https://www.google.com/search?q=regular+expression+tutorial+for+beginners)
- [grep 遞迴搜尋進階技巧](https://www.google.com/search?q=grep+recursive+search+advanced+tips)
