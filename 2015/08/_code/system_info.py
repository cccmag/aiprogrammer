#!/usr/bin/env python3
"""
系統資訊收集腳本
"""

import subprocess
import platform
import os
from datetime import datetime

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    print("=" * 60)
    print(" Linux 系統資訊報告")
    print(" 時間: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    print()

    print("【系統資訊】")
    print(f"主機名稱: {platform.node()}")
    print(f"系統: {platform.system()} {platform.release()}")
    print(f"架構: {platform.machine()}")
    print(f"Python 版本: {platform.python_version()}")
    print()

    print("【CPU 資訊】")
    print(run_cmd("cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d: -f2"))
    print(f"核心數: {os.cpu_count()}")
    print(run_cmd("cat /proc/loadavg"))
    print()

    print("【記憶體資訊】")
    print(run_cmd("free -h"))
    print()

    print("【磁碟資訊】")
    print(run_cmd("df -h | grep -E '^/dev'"))
    print()

    print("【網路資訊】")
    print(run_cmd("ip addr show | grep 'inet ' | head -5"))
    print()

    print("【連線統計】")
    print(run_cmd("ss -tuln | head -10"))
    print()

    print("=" * 60)
    print("報告完成")
    print("=" * 60)

if __name__ == '__main__':
    main()