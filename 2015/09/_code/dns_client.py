#!/usr/bin/env python3
"""
DNS 客戶端範例
"""

import socket
import time

def main():
    print("=== DNS 查詢測試 ===\n")
    
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