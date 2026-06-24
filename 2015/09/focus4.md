# Socket 程式設計基礎

Socket 是網路程式設計的基本介面，讓應用程式能夠透過網路進行通訊。

---

## Socket 概念

### 什麼是 Socket？

Socket 是作業系統提供的一種抽象，用於程序之間的網路通訊。

```
應用程式
    │
    ▼
  Socket API
    │
    ▼
  TCP/UDP 協定棧
    │
    ▼
     網路
```

### Socket 類型

| 類型 | 說明 | 應用 |
|------|------|------|
| SOCK_STREAM | 面向連接（TCP） | HTTP, SSH |
| SOCK_DGRAM | 無連接（UDP） | DNS, VoIP |
| SOCK_RAW | 原始資料包 | ping, 網路工具 |

---

## TCP Socket 程式設計

### 伺服器端

```python
import socket

# 1. 建立 socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 綁定位址和連接埠
server_socket.bind(('0.0.0.0', 8080))

# 3. 監聽連線
server_socket.listen(5)

print("伺服器監聽連接埠 8080...")

# 4. 接受連線
while True:
    client_socket, client_address = server_socket.accept()
    print(f"客戶端連線: {client_address}")
    
    # 5. 處理請求
    data = client_socket.recv(1024)
    print(f"收到: {data.decode()}")
    
    # 6. 傳送回應
    response = "Hello from server!"
    client_socket.send(response.encode())
    
    # 7. 關閉連線
    client_socket.close()
```

### 客戶端

```python
import socket

# 1. 建立 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 連線到伺服器
client_socket.connect(('127.0.0.1', 8080))

print("已連線到伺服器")

# 3. 傳送資料
message = "Hello from client!"
client_socket.send(message.encode())

# 4. 接收回應
response = client_socket.recv(1024)
print(f"收到回應: {response.decode()}")

# 5. 關閉連線
client_socket.close()
```

---

## UDP Socket 程式設計

### 伺服器端

```python
import socket

# 1. 建立 socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 綁定位址
server_socket.bind(('0.0.0.0', 8080))

print("UDP 伺服器監聽連接埠 8080...")

# 3. 接收資料（無連線）
while True:
    data, address = server_socket.recvfrom(1024)
    print(f"收到來自 {address}: {data.decode()}")
    
    # 4. 傳送回應
    server_socket.sendto(b"Message received", address)
```

### 客戶端

```python
import socket

# 1. 建立 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 傳送資料
message = "Hello UDP server!"
client_socket.sendto(message.encode(), ('127.0.0.1', 8080))

# 3. 接收回應
response, server_address = client_socket.recvfrom(1024)
print(f"收到回應: {response.decode()}")

# 4. 關閉
client_socket.close()
```

---

## 常用的 Socket 選項

### 設定逾時

```python
# 接收逾時（秒）
client_socket.settimeout(5.0)

# 逾時處理
try:
    response = client_socket.recv(1024)
except socket.timeout:
    print("連線逾時")
```

### 禁用 Nagle 演算法

```python
# 立即傳送小封包
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
```

### 保持連線

```python
# 設定 SO_KEEPALIVE
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
```

### 設定緩衝區大小

```python
# 取得緩衝區大小
recv_buffer = client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
send_buffer = client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
```

---

## 處理多個客戶端

### 使用執行緒

```python
import socket
import threading

def handle_client(client_socket, client_address):
    print(f"處理客戶端: {client_address}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        client_socket.send(data)
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)

while True:
    client_socket, client_address = server_socket.accept()
    thread = threading.Thread(target=handle_client, 
                              args=(client_socket, client_address))
    thread.start()
```

### 使用 select

```python
import select
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)

sockets_list = [server_socket]
clients = {}

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, address = server_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = address
        else:
            data = notified_socket.recv(1024)
            if data:
                notified_socket.send(data)
            else:
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
```

---

## 錯誤處理

```python
import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('example.com', 80))
except socket.error as e:
    print(f"Socket 錯誤: {e}")
except socket.gaierror as e:
    print(f"DNS 解析錯誤: {e}")
finally:
    sock.close()
```

---

## 小結

Socket 程式設計是網路應用的基礎，無論是 Web 伺服器、API 服務還是即時通訊，都離不開 Socket。

---

*作者：AI 程式人團隊*