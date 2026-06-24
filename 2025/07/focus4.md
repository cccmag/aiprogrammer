# 文字處理工具：grep、sed、awk

## grep：全域搜尋正規表示法

grep (Global Regular Expression Print) 是 Unix 中最常用的搜尋工具。它可以在檔案或標準輸入中搜尋符合模式的行。

### 基本用法

```bash
grep "error" log.txt          # 搜尋包含 error 的行
grep -i "warning" log.txt     # 忽略大小寫
grep -r "TODO" src/           # 遞迴搜尋目錄
grep -l "main" *.c            # 只顯示檔名
grep -n "function" script.py  # 顯示行號
grep -c "error" log.txt       # 計算匹配行數
grep -v "debug" log.txt       # 反向匹配 (不含 debug)
```

### 正規表示法範例

| 模式 | 說明 | 範例 |
|------|------|------|
| `^start` | 行首 | `grep "^from" mail.txt` |
| `end$` | 行尾 | `grep "done$" log.txt` |
| `[0-9]` | 數字 | `grep "[0-9]\{3\}" file` |
| `error\|fail` | 多選 | `grep -E "error|fail" log` |

### Python 中的 grep 模擬

```python
import re

def pygrep(pattern, lines, ignore_case=False):
    flag = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flag)
    return [line for line in lines if regex.search(line)]

data = ["error: connection failed", "info: server started", "warning: disk full"]
matches = pygrep("error|warning", data)
print(matches)  # ['error: connection failed', 'warning: disk full']
```

## sed：串流編輯器

sed (Stream Editor) 用於對文字串流進行編輯操作。它不會修改原始檔案，除非使用 `-i` 選項。

### 常用命令

```bash
sed 's/old/new/g' file.txt       # 全域取代
sed '/error/d' log.txt           # 刪除匹配行
sed -n '10,20p' file.txt         # 列印 10-20 行
sed 's/^/  /' file.txt           # 每行開頭加空格
sed -i.bak 's/foo/bar/g' file    # 原地取代並備份
```

### Python 中的 sed 模擬

```python
def pysed(pattern, replacement, lines, global_replace=True):
    import re
    count = 0 if global_replace else 1
    return [re.sub(pattern, replacement, line, count=count) for line in lines]

text = ["hello world", "hello linux", "hi everyone"]
result = pysed("hello", "hi", text)
print(result)  # ['hi world', 'hi linux', 'hi everyone']
```

## awk：資料驅動的程式語言

awk 不僅僅是一個工具，它是一門完整的程式語言，專門用於處理結構化文字資料。awk 自動將每行分割成欄位 (`$1`, `$2`, ...)。

### 基本模式

```bash
awk '{print $1, $3}' data.txt      # 列印第 1 和第 3 欄
awk '$3 > 1000 {print $0}' sales   # 條件篩選
awk 'NR > 1 {sum += $3} END {print "Avg:", sum/NR}' data
awk -F: '{print $1}' /etc/passwd   # 自訂分隔符
```

### Python 中的 awk 模擬

```python
import csv

def pyawk(text, delimiter=None, select_cols=None):
    lines = text.strip().split("\n")
    reader = csv.reader(lines, delimiter=delimiter or ",")
    result = []
    for row in reader:
        if select_cols:
            result.append([row[i-1] for i in select_cols])
        else:
            result.append(row)
    return result

data = "Alice,30,Engineer\nBob,25,Designer"
print(pyawk(data, select_cols=[1, 3]))
# [['Alice', 'Engineer'], ['Bob', 'Designer']]
```

## 三劍客組合

最強大的用法是將三個工具組合在一起：

```bash
grep "ERROR" app.log | sed 's/\[.*\] //' | awk '{print $1, $NF}'
```

這行命令從日誌中過濾錯誤行、移除時間戳、然後列印第一個和最後一個欄位。

---

## 延伸閱讀

- [grep 正規表示法教學](https://www.google.com/search?q=grep+regular+expression+tutorial+Linux)
- [sed 串流編輯器入門](https://www.google.com/search?q=sed+stream+editor+tutorial+Linux)
- [awk 程式設計](https://www.google.com/search?q=awk+programming+tutorial+Linux)
- [Linux 文字處理工具組合](https://www.google.com/search?q=Linux+grep+sed+awk+pipeline+text+processing)
