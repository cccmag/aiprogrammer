# 主題七：檔案操作與網路程式設計

## 檔案操作

### 基本讀寫

```python
# 寫入檔案
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# 讀取檔案
with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 按行讀取
with open("output.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

### 檔案模式

| 模式 | 說明 |
|------|------|
| `r` | 唯讀（預設） |
| `w` | 唯寫（會截斷檔案） |
| `a` | 附加（從檔案末尾寫入） |
| `x` | 新建並唯寫（檔案存在則失敗） |
| `b` | 二進位模式（如 `rb`、`wb`） |
| `+` | 讀寫（如 `r+`、`w+`） |

### JSON 檔案

```python
import json

data = {
    "name": "張小明",
    "age": 28,
    "skills": ["Python", "JavaScript"]
}

# 寫入 JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 讀取 JSON
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded)
```

### CSV 檔案

```python
import csv

# 寫入 CSV
with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Age"])
    writer.writerow([1, "張小明", 28])
    writer.writerow([2, "李小華", 35])

# 讀取 CSV
with open("users.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

### 二進位檔案

```python
# 寫入二進位
data = bytes([0x48, 0x65, 0x6c, 0x6c, 0x6f])  # "Hello"
with open("binary.bin", "wb") as f:
    f.write(data)

# 讀取二進位
with open("binary.bin", "rb") as f:
    content = f.read()
    print(content)  # b'Hello'
```

## 網路程式設計

### socket 基礎

```python
# 伺服器端
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8080))
server.listen(5)

print("等待客戶端連線...")
conn, addr = server.accept()
print(f"客戶端連線：{addr}")

data = conn.recv(1024)
print(f"收到：{data.decode()}")

conn.sendall("Hello from server".encode())
conn.close()
server.close()
```

```python
# 客戶端
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8080))

client.sendall("Hello from client".encode())
response = client.recv(1024)
print(f"收到回應：{response.decode()}")

client.close()
```

### HTTP 請求

#### 使用 urllib

```python
from urllib.request import urlopen, Request
from urllib.parse import urlencode

# GET 請求
response = urlopen("https://httpbin.org/get")
print(response.read().decode())

# POST 請求
data = urlencode({"key": "value"}).encode()
response = urlopen("https://httpbin.org/post", data=data)
print(response.read().decode())
```

#### 使用 requests 庫

```bash
pip install requests
```

```python
import requests

# GET 請求
response = requests.get("https://httpbin.org/get")
print(response.status_code)
print(response.json())

# POST 請求
payload = {"username": "user", "password": "pass"}
response = requests.post("https://httpbin.org/post", data=payload)
print(response.json())

# 帶 Header
headers = {"User-Agent": "Python Client"}
response = requests.get("https://httpbin.org/headers", headers=headers)
print(response.json())

# 下載檔案
response = requests.get("https://httpbin.org/bytes/1024", stream=True)
with open("downloaded.bin", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### 簡單 HTTP 伺服器

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Python HTTP Server</title></head>
        <body>
            <h1>Hello, World!</h1>
            <p>這是一個簡單的 HTTP 伺服器</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"POST received!")

server = HTTPServer(("localhost", 8080), MyHandler)
print("伺服器運行於 http://localhost:8080")
server.serve_forever()
```

## 電子郵件

### 發送郵件

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    from_email = "your_email@gmail.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        print("郵件發送成功")
    except Exception as e:
        print(f"發送失敗：{e}")

# 使用（需要開啟低安全性應用程式存取）
# send_email("測試郵件", "這是郵件內容", "recipient@example.com")
```

## 檔案下載範例

```python
import os
import requests

def download_file(url, dest_folder):
    """下載檔案並顯示進度"""
    filename = os.path.join(dest_folder, url.split("/")[-1])

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("Content-Length", 0))

    with open(filename, "wb") as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r進度：{percent:.1f}%", end="")

    print(f"\n已儲存至：{filename}")
    return filename

# 使用
# download_file("https://example.com/file.zip", "/tmp")
```

## 結論

Python 提供了豐富的工具來處理檔案操作和網路程式設計。從基本的檔案讀寫到複雜的 HTTP 請求，Python 的標準庫和第三方庫都能勝任。