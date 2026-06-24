# 管道與重定向

## 標準串流

Linux 中的每個行程都有三個標準串流：

| 串流 | 代號 | 檔案描述符 | 用途 |
|------|------|-----------|------|
| stdin | 標準輸入 | 0 | 接收輸入 (預設鍵盤) |
| stdout | 標準輸出 | 1 | 輸出正常結果 (預設螢幕) |
| stderr | 標準錯誤 | 2 | 輸出錯誤訊息 (預設螢幕) |

## 重定向 (Redirection)

### 輸出重定向

```bash
# 覆蓋寫入
echo "Hello" > file.txt       # stdout → file (1> 的簡寫)
echo "Error" 2> error.log     # stderr → file
echo "Both" &> output.log     # stdout+stderr → file

# 追加寫入
echo "More" >> file.txt       # 追加到檔案結尾
echo "Error" 2>> error.log    # 追加 stderr

# 丟棄輸出
echo "Discard" > /dev/null    # 輸出到黑洞
```

### 輸入重定向

```bash
# 從檔案讀取
sort < unsorted.txt           # stdin ← file
wc -l < data.txt              # 計算檔案行數

# Here Document (多行輸入)
cat << EOF > config.txt
database_host=localhost
database_port=5432
database_name=mydb
EOF

# Here String
grep "error" <<< "no error here\nerror found"  # 字串輸入
```

### 檔案描述符操作

```bash
# 合併 stderr 到 stdout
command 2>&1

# 合併 stdout 到 stderr
echo "Error" 1>&2

# 建立新的檔案描述符
exec 3> log.txt      # 開啟 fd 3 寫入 log.txt
echo "Log" >&3       # 寫入 fd 3
exec 3>&-            # 關閉 fd 3
```

## 管道 (Pipe)

管道 (`|`) 是 Unix 最具革命性的設計之一。它將前一個命令的 stdout 連接到下一個命令的 stdin。

### 基礎範例

```bash
# 分頁顯示
ls -la | less

# 計數
ps aux | wc -l

# 排序與去重
cut -d: -f1 /etc/passwd | sort | uniq

# 多層管線
ps aux | grep python | awk '{print $2}' | head -5
```

### 管線處理流程圖

```
Command1 stdout ──► pipe ──► Command2 stdin
    │                            │
    ▼                            ▼
  寫入端                       讀取端
```

## 管道與重定向的區別

```
重定向 (>)：   命令輸出 → 檔案
管道 (|)：     命令輸出 → 另一個命令的輸入
區分：
  ls > file.txt      # 輸出寫入檔案
  ls | wc -l         # 輸出傳給 wc 處理
  ls 2>&1 | wc -l    # stderr 也加入管線
```

## 命名管道 (Named Pipe / FIFO)

除了匿名管道 (`|`)，還有命名管道可以在不同行程間通訊：

```bash
# 建立命名管道
mkfifo mypipe

# 終端機 A：寫入
echo "Hello" > mypipe

# 終端機 B：讀取
cat < mypipe
```

## 進階技巧

```bash
# tee：同時輸出到檔案與螢幕
ls -la | tee output.txt | wc -l

# xargs：將標準輸入轉為命令列參數
find . -name "*.py" | xargs wc -l

# process substitution
diff <(ls dir1) <(ls dir2)
```

## Python 中的重定向與管道

```python
import subprocess, sys

# 擷取 stdout
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print("stdout:", result.stdout)

# 管線模擬
p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "python"], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen(["wc", "-l"], stdin=p2.stdout, stdout=subprocess.PIPE)
output = p3.communicate()[0]
print(f"Python 行程數: {output.decode().strip()}")

# Python 內部重定向
import io

old_stdout = sys.stdout
sys.stdout = io.StringIO()  # 重定向 stdout
print("這不會顯示在螢幕上")
captured = sys.stdout.getvalue()
sys.stdout = old_stdout
print(f"捕獲到的輸出: {captured}")
```

---

## 延伸閱讀

- [Linux 重定向教學](https://www.google.com/search?q=Linux+redirection+stdout+stderr+tutorial)
- [Unix 管道 pipe 原理](https://www.google.com/search?q=Unix+pipe+mechanism+explained)
- [Python io 重定向](https://www.google.com/search?q=Python+redirect+stdout+StringIO)
