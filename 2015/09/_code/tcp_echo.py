#!/usr/bin/env python3
"""
TCP Echo 範例：客戶端和伺服器
"""

import socket
import sys
import time

def echo_server(host='127.0.0.1', port=9999):
    """TCP Echo 伺服器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    
    print(f"TCP Echo 伺服器監聽 {host}:{port}")
    
    conn, addr = server.accept()
    print(f"客戶端連線: {addr}")
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"收到: {data.decode()}")
            conn.send(data)
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        conn.close()
        server.close()
        print("伺服器關閉")

def echo_client(host='127.0.0.1', port=9999):
    """TCP Echo 客戶端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    print(f"連線到 {host}:{port}")
    
    messages = ["Hello", "World", "Test", "quit"]
    for msg in messages:
        sock.send(msg.encode())
        print(f"傳送: {msg}")
        
        response = sock.recv(1024)
        print(f"收到回應: {response.decode()}")
        
        if msg == "quit":
            break
    
    sock.close()
    print("連線關閉")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        echo_server()
    else:
        echo_client()