#!/usr/bin/env python3
"""
UDP Echo 範例：客戶端和伺服器
"""

import socket
import sys

def udp_server(host='127.0.0.1', port=9998):
    """UDP Echo 伺服器"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    
    print(f"UDP Echo 伺服器監聽 {host}:{port}")
    
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"收到來自 {addr}: {data.decode()}")
            sock.sendto(data, addr)
    except KeyboardInterrupt:
        print("\n伺服器關閉")
    finally:
        sock.close()

def udp_client(host='127.0.0.1', port=9998):
    """UDP Echo 客戶端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"傳送訊息到 {host}:{port}")
    
    messages = ["Hello", "World", "Test"]
    for msg in messages:
        sock.sendto(msg.encode(), (host, port))
        print(f"傳送: {msg}")
        
        data, server = sock.recvfrom(1024)
        print(f"收到回應: {data.decode()}")
    
    sock.close()
    print("連線關閉")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        udp_server()
    else:
        udp_client()