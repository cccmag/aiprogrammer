# Linux 系統管理程式範例

本章提供實際可運行的 Linux 系統管理範例腳本。

---

## 系統資訊收集腳本

```python
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

    # 系統資訊
    print("【系統資訊】")
    print(f"主機名稱: {platform.node()}")
    print(f"系統: {platform.system()} {platform.release()}")
    print(f"架構: {platform.machine()}")
    print(f"Python 版本: {platform.python_version()}")
    print()

    # CPU 資訊
    print("【CPU 資訊】")
    print(run_cmd("cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d: -f2"))
    print(f"核心數: {os.cpu_count()}")
    print(run_cmd("cat /proc/loadavg"))
    print()

    # 記憶體資訊
    print("【記憶體資訊】")
    print(run_cmd("free -h"))
    print()

    # 磁碟資訊
    print("【磁碟資訊】")
    print(run_cmd("df -h | grep -E '^/dev'"))
    print()

    # 網路資訊
    print("【網路資訊】")
    print(run_cmd("ip addr show | grep 'inet ' | head -5"))
    print()

    # 連線統計
    print("【連線統計】")
    print(run_cmd("ss -tuln | head -10"))
    print()

    print("=" * 60)
    print("報告完成")
    print("=" * 60)

if __name__ == '__main__':
    main()
```

---

## 程序管理腳本

```python
#!/usr/bin/env python3
"""
程序管理示範腳本
"""

import subprocess
import os
import signal
import time

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def main():
    print("=== 程序管理示範 ===")
    print()

    # 啟動一個測試程序
    print("啟動測試程序...")
    proc = subprocess.Popen(['sleep', '100'])
    pid = proc.pid
    print(f"程序 PID: {pid}")
    print()

    # 檢查程序狀態
    print("檢查程序狀態:")
    print(run_cmd(f"ps -p {pid} -o pid,ppid,state,cmd"))
    print()

    # 終止程序
    print("發送 SIGTERM 信號...")
    proc.terminate()
    time.sleep(1)

    # 檢查程序是否已終止
    returncode = proc.poll()
    print(f"程序返回碼: {returncode}")
    print()

    print("程序管理示範完成")

if __name__ == '__main__':
    main()
```

---

## 網路診斷腳本

```python
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

    # 網路介面
    print("【網路介面】")
    print(run_cmd("ip addr show | grep -E '^[0-9]|inet '"))
    print()

    # 路由表
    print("【路由表】")
    print(run_cmd("ip route show"))
    print()

    # DNS 解析
    print("【DNS 測試】")
    test_domains = ['google.com', 'github.com', 'localhost']
    for domain in test_domains:
        try:
            ip = socket.gethostbyname(domain)
            print(f"  {domain} -> {ip}")
        except socket.gaierror as e:
            print(f"  {domain} -> 解析失敗: {e}")
    print()

    # 連接埠掃描（本地）
    print("【監聽連接埠】")
    print(run_cmd("ss -tln | head -10"))
    print()

    print("診斷完成")

if __name__ == '__main__':
    main()
```

---

## 磁碟使用分析腳本

```bash
#!/bin/bash
# disk_analysis.sh - 磁碟使用分析

set -x

echo "=== 磁碟使用分析 ==="
echo ""

echo "【磁碟總覽】"
df -h

echo ""
echo "【目錄大小排名 (前10)】"
du -ah / 2>/dev/null | sort -rh | head -10

echo ""
echo "【大型檔案 (大於100MB)】"
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null | head -10

echo ""
echo "【磁碟 I/O 統計】"
if command -v iostat &> /dev/null; then
    iostat -x 1 1
else
    echo "iostat 未安裝"
fi

echo ""
echo "分析完成"
```

---

## 執行測試

```bash
#!/bin/bash
set -x

cd /Users/Shared/ccc/magazine/aiprogrammer/2015/08/_code

echo "=== 執行系統資訊腳本 ==="
chmod +x system_info.py
python3 system_info.py

echo ""
echo "=== 執行程序管理腳本 ==="
chmod +x process_manager.py
python3 process_manager.py

echo ""
echo "=== 執行網路診斷腳本 ==="
chmod +x network_diag.py
python3 network_diag.py

echo ""
echo "=== 執行磁碟分析腳本 ==="
chmod +x disk_analysis.sh
./disk_analysis.sh

echo ""
echo "=== 所有測試完成 ==="
```

---

*作者：AI 程式人團隊*