#!/usr/bin/env python3
"""
HTTP 客戶端範例
"""

import socket

def http_get(host, path='/', port=80):
    """發送 HTTP GET 請求"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    request = f"GET {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n"
    
    sock.send(request.encode())
    
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    
    sock.close()
    return response.decode()

def main():
    print("=== HTTP 客戶端測試 ===\n")
    
    print("測試 HTTP 請求到 example.com...")
    response = http_get('example.com', '/')
    
    print("\n=== 回應內容（前 500 字元）===")
    print(response[:500])
    
    header_end = response.find('\r\n\r\n')
    if header_end != -1:
        headers = response[:header_end]
        body = response[header_end + 4:]
        
        print("\n=== HTTP 標頭 ===")
        print(headers)
        print(f"\n=== 主體長度: {len(body)} bytes ===")

if __name__ == '__main__':
    main()