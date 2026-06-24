# 字串與檔案操作

## 字串的基本操作

字串是 Python 中最常用的資料型別之一。無論是處理使用者輸入、讀取檔案內容，還是生成報表，字串操作都無所不在。

### 字串的建立

```python
# 使用單引號或雙引號
s1 = 'Hello'
s2 = "World"

# 多行字串
s3 = """這是
多行
字串"""

# 字串串接
full = s1 + " " + s2
print(full)  # Hello World
```

### 字串索引與切片

```python
text = "Python"

# 索引（從 0 開始）
print(text[0])   # P
print(text[-1])  # n (最後一個字元)

# 切片 [start:stop:step]
print(text[0:3])    # Pyt
print(text[2:])     # thon
print(text[::-1])   # nohtyP (反轉)
```

### 常用字串方法

```python
text = "  Hello, Python World!  "

# 大小寫轉換
print(text.lower())      # "  hello, python world!  "
print(text.upper())      # "  HELLO, PYTHON WORLD!  "
print(text.strip())      # "Hello, Python World!"

# 搜尋與取代
print(text.find("Python"))   # 9 （位置）
print(text.replace("World", "程式人"))  # "  Hello, Python 程式人!  "

# 分割與連接
csv = "apple,banana,orange"
fruits = csv.split(",")
print(fruits)  # ['apple', 'banana', 'orange']

joined = "-".join(fruits)
print(joined)  # apple-banana-orange

# 檢查字串
print("Python".startswith("Py"))  # True
print("hello123".isalpha())       # False （包含數字）
print("hello".isalpha())          # True
```

## f-string 格式化

Python 3.6+ 引入了 f-string，這是最推薦的字串格式化方式：

```python
name = "Alice"
age = 25
height = 165.5

# 基本用法
print(f"姓名：{name}，年齡：{age}")

# 格式化數字
print(f"身高：{height:.1f} cm")  # 165.5 cm

# 表達式
print(f"明年 {age + 1} 歲")

# 對齊與補齊
print(f"|{name:>10}|")  # |     Alice|
print(f"|{name:<10}|")  # |Alice     |
```

## 檔案操作

### 開啟與讀取檔案

```python
# 讀取整個檔案
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# 逐行讀取
with open("data.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())  # strip() 移除換行符號

# 讀取所有行到列表
with open("data.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    print(f"共有 {len(lines)} 行")
```

### 寫入檔案

```python
# 寫入（覆蓋原有內容）
with open("output.txt", "w", encoding="utf-8") as file:
    file.write("Hello, World!\n")
    file.write("這是一行新文字\n")

# 附加（在檔案末尾添加）
with open("output.txt", "a", encoding="utf-8") as file:
    file.write("這行會附加在末尾\n")
```

### 使用 `with` 語句

`with` 語句會自動管理檔案的開啟與關閉：

```python
# 不需手動呼叫 close()
with open("data.txt", "r") as f:
    data = f.read()
# 離開 with 區塊後檔案自動關閉
```

## 實戰範例：日誌分析

```python
def analyze_log(filename):
    """分析伺服器日誌檔案"""
    error_count = 0
    warning_count = 0
    info_count = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                error_count += 1
            elif "WARNING" in line:
                warning_count += 1
            elif "INFO" in line:
                info_count += 1

    print(f"=== 日誌分析結果 ===")
    print(f"錯誤：{error_count}")
    print(f"警告：{warning_count}")
    print(f"資訊：{info_count}")
    print(f"總計：{error_count + warning_count + info_count}")

# 建立測試檔案
with open("server.log", "w", encoding="utf-8") as f:
    f.write("INFO: 伺服器啟動\n")
    f.write("ERROR: 連線逾時\n")
    f.write("WARNING: 磁碟空間不足\n")
    f.write("INFO: 請求處理完成\n")
    f.write("ERROR: 資料庫連線失敗\n")

analyze_log("server.log")
# === 日誌分析結果 ===
# 錯誤：2
# 警告：1
# 資訊：2
# 總計：5
```

## 小結

字串與檔案操作是開發實用程式的必備技能。無論是處理使用者輸入、讀取設定檔、還是寫入執行日誌，這些操作都會在每個 Python 專案中反覆出現。熟練掌握這些技巧，將讓你的程式開發效率大幅提升。

---

**延伸閱讀**

- [Python 官方文件 — 字串方法](https://www.google.com/search?q=Python+string+methods+documentation)
- [Python 官方文件 — 檔案 I/O](https://www.google.com/search?q=Python+file+IO+documentation)
