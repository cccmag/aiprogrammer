# 網路與通訊協定程式範例

本章提供實際可運行的網路程式範例。

---

## TCP 客戶端-伺服器

```python
#!/usr/bin/env python3
"""
TCP 客戶端-伺服器範例
"""

import socket
import sys
import threading
import time

def handle_client(client_socket, client_address):
    """處理單個客戶端連線"""
    print(f"客戶端連線: {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            print(f"收到: {message}")
            
            # 回應
            if message.lower() == 'quit':
                client_socket.send(b"Goodbye!")
                break
            elif message.lower() == 'time':
                client_socket.send(time.strftime("%H:%M:%S").encode())
            else:
                client_socket.send(f"Echo: {message}".encode())
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        client_socket.close()
        print(f"客戶端斷開: {client_address}")

def start_server(host='127.0.0.1', port=9999):
    """啟動 TCP 伺服器"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"TCP 伺服器監聽 {host}:{port}")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, 
                                     args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        print("\n伺服器關閉")
    finally:
        server_socket.close()

def tcp_client(host='127.0.0.1', port=9999):
    """TCP 客戶端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    print(f"連線到 {host}:{port}")
    
    try:
        while True:
            message = input("輸入訊息 (quit 結束): ")
            sock.send(message.encode())
            
            response = sock.recv(1024)
            print(f"收到: {response.decode()}")
            
            if message.lower() == 'quit':
                break
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        start_server()
    else:
        print("啟動客戶端模式")
        tcp_client()
```

---

## UDP 程式

```python
#!/usr/bin/env python3
"""
UDP 客戶端-伺服器範例
"""

import socket
import sys

def start_server(host='127.0.0.1', port=9998):
    """啟動 UDP 伺服器"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    
    print(f"UDP 伺服器監聽 {host}:{port}")
    
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f"收到來自 {address}: {data.decode()}")
            
            response = f"Server received: {data.decode()}"
            sock.sendto(response.encode(), address)
    except KeyboardInterrupt:
        print("\n伺服器關閉")
    finally:
        sock.close()

def udp_client(host='127.0.0.1', port=9998):
    """UDP 客戶端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        for i in range(3):
            message = f"Message {i}"
            sock.sendto(message.encode(), (host, port))
            print(f"傳送: {message}")
            
            data, server = sock.recvfrom(1024)
            print(f"收到: {data.decode()}")
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        start_server()
    else:
        print("啟動客戶端模式")
        udp_client()
```

---

## HTTP 客戶端

```python
#!/usr/bin/env python3
"""
HTTP 客戶端範例
"""

import socket

def http_get(host, path='/', port=80):
    """發送 HTTP GET 請求"""
    # 建立 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    # 發送請求
    request = f"GET {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n"
    
    sock.send(request.encode())
    
    # 接收回應
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    
    sock.close()
    return response.decode()

def main():
    # 測試 HTTP 請求
    print("發送 HTTP GET 請求到 example.com...")
    
    response = http_get('example.com', '/')
    
    # 顯示回應（只顯示前 500 字元）
    print("\n=== 回應內容（前 500 字元）===")
    print(response[:500])
    
    # 解析 HTTP 標頭
    header_end = response.find('\r\n\r\n')
    if header_end != -1:
        headers = response[:header_end]
        body = response[header_end + 4:]
        
        print("\n=== HTTP 標頭 ===")
        print(headers)
        print(f"\n=== 主體長度: {len(body)} bytes ===")

if __name__ == '__main__':
    main()
```

---

## DNS 客戶端

```python
#!/usr/bin/env python3
"""
DNS 查詢範例
"""

import socket
import struct
import time

def parse_dns_response(data):
    """簡單的 DNS 回應解析"""
    # 跳過標頭（12 bytes）
    # 這裡只取回答部分
    answers = []
    idx = 12
    
    # 跳過問題部分
    qdcount = struct.unpack('!H', data[4:6])[0]
    for _ in range(qdcount):
        # 跳過查詢名稱
        while idx < len(data):
            length = data[idx]
            if length == 0:
                idx += 1
                break
            idx += length + 1
        # 跳過 QTYPE 和 QCLASS（4 bytes）
        idx += 4
    
    # 解析回答
    ancount = struct.unpack('!H', data[6:8])[0]
    for _ in range(ancount):
        # 跳過名稱
        while idx < len(data):
            length = data[idx]
            if length == 0:
                idx += 1
                break
            if (length & 0xC0) == 0xC0:  # 指標
                idx += 2
                break
            idx += length + 1
        
        # 讀取類型和資料
        if idx + 10 < len(data):
            qtype = struct.unpack('!H', data[idx:idx+2])[0]
            idx += 8  # 跳過 TYPE, CLASS, TTL
            rdlength = struct.unpack('!H', data[idx:idx+2])[0]
            idx += 2
            rdata = data[idx:idx+rdlength]
            idx += rdlength
            
            if qtype == 1:  # A record
                ip = '.'.join(str(b) for b in rdata)
                answers.append(ip)
    
    return answers

def main():
    print("=== DNS 查詢測試 ===\n")
    
    # 使用系統預設 DNS
    test_domains = [
        'example.com',
        'google.com',
        'github.com',
    ]
    
    for domain in test_domains:
        try:
            start = time.time()
            ip = socket.gethostbyname(domain)
            elapsed = (time.time() - start) * 1000
            print(f"{domain:20} -> {ip:15} ({elapsed:.1f}ms)")
        except socket.gaierror as e:
            print(f"{domain:20} -> 解析失敗: {e}")
    
    print("\n使用 socket.getaddrinfo:")
    for domain in ['example.com']:
        try:
            results = socket.getaddrinfo(domain, 80)
            for result in results[:2]:
                family, socktype, proto, canonname, sockaddr = result
                print(f"  {family} {socktype}: {sockaddr}")
        except socket.gaierror as e:
            print(f"  {domain}: 解析失敗")

if __name__ == '__main__':
    main()
```

---

## 執行測試

```bash
#!/bin/bash
set -x

cd /Users/Shared/ccc/magazine/aiprogrammer/2015/09/_code

echo "=== 執行 HTTP 客戶端 ==="
chmod +x http_client.py
python3 http_client.py

echo ""
echo "=== 執行 DNS 客戶端 ==="
chmod +x dns_client.py
python3 dns_client.py

echo ""
echo "=== 執行 TCP 範例 ==="
chmod +x tcp_echo.py
echo "test message" | timeout 5 python3 tcp_echo.py client || true

echo ""
echo "=== 所有測試完成 ==="
```

---

*作者：AI 程式人團隊*