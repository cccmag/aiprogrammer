# sed 串流編輯器

## sed 是什麼？

sed (Stream Editor) 是一個非互動式的文字編輯器。它讀取輸入串流，執行編輯操作，然後輸出結果。sed 不會修改原始檔案 (除非使用 `-i` 選項)。

### 基本語法

```bash
sed '命令' file.txt          # 基本用法
sed -i '命令' file.txt       # 原地修改
sed -n '命令' file.txt       # 靜默模式 (只列印明確要求的行)
sed -e '命令1' -e '命令2'    # 多個命令
sed -f script.sed file.txt   # 從檔案讀取命令
```

## 核心命令

### 取代 (s)

```bash
sed 's/old/new/' file              # 取代每行第一個匹配
sed 's/old/new/g' file             # 全域取代
sed 's/old/new/2' file             # 取代每行第二個匹配
sed 's/old/new/gi' file            # 忽略大小寫

# 使用不同分隔符
sed 's|/usr/local|/opt|' file      # 使用 | 分隔
sed 's@foo@bar@g' file             # 使用 @ 分隔

# 取代並備份
sed -i.bak 's/foo/bar/g' file.txt  # 產生 file.txt.bak
```

### 列印 (p) 與刪除 (d)

```bash
sed -n '5p' file               # 列印第 5 行
sed -n '10,20p' file           # 列印 10-20 行
sed -n '/error/p' file         # 列印匹配行
sed '/^#/d' config             # 刪除註解行
sed '/^$/d' file               # 刪除空白行
sed '5d' file                  # 刪除第 5 行
```

### 插入與附加

```bash
sed '2i\新行內容' file         # 在第 2 行前插入
sed '2a\新行內容' file         # 在第 2 行後附加
sed '5c\取代整行' file         # 取代第 5 行
```

## 位址定址

sed 命令可以指定操作範圍：

| 位址 | 範例 | 說明 |
|------|------|------|
| 行號 | `5s/foo/bar/` | 只在第 5 行取代 |
| 範圍 | `10,20d` | 刪除 10-20 行 |
| 模式 | `/error/d` | 刪除匹配行 |
| 複合 | `/start/,/end/p` | 從 start 到 end |
| 步進 | `1~2d` | 奇數行 (1, 3, 5...) |

### 進階位址範例

```bash
# 從第 10 行到檔尾
sed '10,$s/foo/bar/' file

# 從 START 到 END 標記之間
sed '/START/,/END/s/foo/bar/' file

# 除了匹配行之外
sed '/pattern/!s/foo/bar/' file

# 從匹配行到檔尾
sed '/pattern/,$d' file
```

## 實戰案例

### 設定檔修改

```bash
# 取消註解
sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config

# 修改設定值
sed -i 's/^max_connections = 100/max_connections = 200/' postgresql.conf

# 加入新設定
sed -i '/^\[mysqld\]/a\max_allowed_packet=64M' my.cnf
```

### 文字格式化

```bash
# 移除 HTML 標籤
sed 's/<[^>]*>//g' page.html

# 縮排
sed 's/^/    /' file.txt

# 行尾加字
sed 's/$/END/' file.txt

# 多行空白縮減為一行
sed '/^$/d' file.txt | sed '/./,/^$/!d'
```

### Python 實作 sed 取代

```python
import re, os

def pysed(pattern, replacement, filepath, inplace=False, backup=None):
    """Python 版 sed"""
    with open(filepath, "r") as f:
        content = f.read()

    new_content = re.sub(pattern, replacement, content)

    if inplace:
        if backup:
            os.rename(filepath, filepath + backup)
        with open(filepath, "w") as f:
            f.write(new_content)
        return f"已修改 {filepath}"
    return new_content

# 使用範例
# pysed("foo", "bar", "file.txt", inplace=True, backup=".bak")

def sed_lines(pattern, replacement, lines, global_replace=True):
    """在行串流上執行 sed 取代"""
    count = 0 if global_replace else 1
    result = []
    for line in lines:
        result.append(re.sub(pattern, replacement, line, count=count))
    return result

# 示範
lines = ["Hello World", "Hello Linux", "Hi there"]
result = sed_lines("Hello", "Hi", lines)
print(result)  # ['Hi World', 'Hi Linux', 'Hi there']
```

---

## 延伸閱讀

- [sed 串流編輯器教學](https://www.google.com/search?q=sed+stream+editor+tutorial+examples)
- [sed 正規表示法](https://www.google.com/search?q=sed+regular+expression+substitution)
- [sed 實用範例集](https://www.google.com/search?q=sed+practical+examples+cheat+sheet)
