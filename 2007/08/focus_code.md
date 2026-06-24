# Linux 指令實作

## 概述

本文介紹 Linux 命令列工具的 Python 實作概念，幫助讀者理解 Linux 系統管理的基本操作。我們將展示如何使用 Python 模擬常見的 Linux 指令功能。

## 環境設定

大多數 Linux 指令都可以透過 Python 的標準函式庫來實現：

```python
import os
import shutil
import subprocess
import glob
import pathlib
```

## 檔案操作

### 列出目錄內容

```python
import os

def list_directory(path="."):
    """模擬 ls -la 命令"""
    for entry in os.scandir(path):
        stat = entry.stat()
        file_type = "d" if entry.is_dir() else "-"
        size = stat.st_size
        name = entry.name
        print(f"{file_type} {size:>10} {name}")

# 輸出類似：
# drwxr-xr-x   4096 docs
# -rw-r--r--   1024 readme.txt
```

### 複製和移動檔案

```python
import shutil

def copy_file(src, dst):
    """複製檔案 - 類似 cp 命令"""
    shutil.copy2(src, dst)  # 保留元資料

def move_file(src, dst):
    """移動/重新命名 - 類似 mv 命令"""
    shutil.move(src, dst)
```

### 建立和刪除目錄

```python
import os

def create_directory(path):
    """建立目錄 - 類似 mkdir -p 命令"""
    os.makedirs(path, exist_ok=True)

def delete_directory(path):
    """刪除目錄 - 類似 rm -rf 命令"""
    shutil.rmtree(path)

def delete_file(path):
    """刪除檔案 - 類似 rm 命令"""
    os.remove(path)
```

## 權限管理

```python
import os

def change_permissions(path, mode):
    """改變權限 - 類似 chmod 命令"""
    os.chmod(path, mode)

def change_owner(path, user, group=None):
    """改變擁有者 - 類似 chown 命令"""
    import pwd
    import grp
    uid = pwd.getpwnam(user).pw_uid
    gid = grp.getgrnam(group).gr_gid if group else pwd.getpwnam(user).pw_gid
    os.chown(path, uid, gid)
```

## 系統監控

```python
import psutil
import os

def show_processes():
    """顯示行程 - 類似 ps aux 命令"""
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            print(f"{info['pid']:>6} {info['name']:>20} {info['cpu_percent']:>6.1f}% {info['memory_percent']:>6.1f}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def show_disk_usage():
    """顯示磁碟空間 - 類似 df -h 命令"""
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"{partition.device:>15} {usage.total // (2**30):>6}G {usage.used // (2**30):>6}G {usage.percent:>3}% {partition.mountpoint:>15}")
        except PermissionError:
            pass

def show_memory():
    """顯示記憶體 - 類似 free -m 命令"""
    mem = psutil.virtual_memory()
    print(f"總計: {mem.total // (2**20):>8} MB")
    print(f"已使用: {mem.used // (2**20):>8} MB")
    print(f"可用: {mem.available // (2**20):>8} MB")
    print(f"使用率: {mem.percent:>6.1f}%")
```

## 網路操作

```python
import subprocess

def check_connectivity(host="8.8.8.8", count=4):
    """測試網路連線 - 類似 ping 命令"""
    result = subprocess.run(['ping', '-c', str(count), host],
                          capture_output=True, text=True)
    return result.stdout

def show_network_interfaces():
    """顯示網路介面 - 類似 ifconfig 命令"""
    import psutil
    for iface, addrs in psutil.net_if_addrs().items():
        print(f"{iface}:")
        for addr in addrs:
            print(f"  {addr.family.name}: {addr.address}")

def scan_ports(host="localhost", ports=[21, 22, 23, 25, 80, 443, 3306, 5432]):
    """掃描連接埠 - 類似 netstat 命令"""
    import socket
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port}: OPEN")
        sock.close()
```

## 文字處理

```python
def grep(pattern, filename):
    """搜尋文字 - 類似 grep 命令"""
    with open(filename, 'r') as f:
        for i, line in enumerate(f, 1):
            if pattern in line:
                print(f"{filename}:{i}:{line.rstrip()}")

def sed_replace(filename, old, new):
    """取代文字 - 類似 sed 命令"""
    with open(filename, 'r') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filename, 'w') as f:
        f.write(content)

def word_count(filename):
    """計算行數 - 類似 wc -l 命令"""
    with open(filename, 'r') as f:
        lines = len(f.readlines())
    with open(filename, 'r') as f:
        words = len(f.read().split())
    with open(filename, 'r') as f:
        chars = len(f.read())
    return lines, words, chars
```

## 壓縮與打包

```python
import tarfile
import zipfile
import gzip

def create_tarball(directory, output):
    """建立 tar 封存 - 類似 tar -cvf 命令"""
    with tarfile.open(output, "w") as tar:
        tar.add(directory, arcname=os.path.basename(directory))

def extract_tarball(tarfile_path, destination="."):
    """解開 tar 封存 - 類似 tar -xvf 命令"""
    with tarfile.open(tarfile_path, "r") as tar:
        tar.extractall(path=destination)

def create_zip(directory, output):
    """建立 zip 封存"""
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, directory)
                zipf.write(filepath, arcname)
```

## 演示函式

```python
def demo():
    print("=" * 50)
    print("Linux 指令 Python 實作展示")
    print("=" * 50)

    print("\n可用函式：")
    print("  list_directory(path)     # 列出目錄")
    print("  copy_file(src, dst)       # 複製檔案")
    print("  move_file(src, dst)       # 移動檔案")
    print("  create_directory(path)    # 建立目錄")
    print("  show_processes()         # 顯示行程")
    print("  show_disk_usage()         # 顯示磁碟使用")
    print("  show_memory()             # 顯示記憶體")
    print("  show_network_interfaces() # 顯示網路介面")
    print("  grep(pattern, filename)  # 搜尋文字")
    print("  create_tarball(dir, out)  # 建立 tar")
    print("  extract_tarball(tar, dst) # 解開 tar")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    demo()