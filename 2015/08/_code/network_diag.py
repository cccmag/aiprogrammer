#!/usr/bin/env python3
"""
網路診斷腳本
"""

import subprocess
import socket
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def main():
    print("=== 網路診斷工具 ===")
    print()

    print("【網路介面】")
    print(run_cmd("ip addr show | grep -E '^[0-9]|inet '"))
    print()

    print("【路由表】")
    print(run_cmd("ip route show"))
    print()

    print("【DNS 測試】")
    test_domains = ['google.com', 'github.com', 'localhost']
    for domain in test_domains:
        try:
            ip = socket.gethostbyname(domain)
            print(f"  {domain} -> {ip}")
        except socket.gaierror as e:
            print(f"  {domain} -> 解析失敗: {e}")
    print()

    print("【監聽連接埠】")
    print(run_cmd("ss -tln | head -10"))
    print()

    print("診斷完成")

if __name__ == '__main__':
    main()