#!/usr/bin/env python3
"""linux_tools.py - 模擬 Linux 命令列工具的 Python 示範"""

import os, sys, stat, shutil, subprocess, tempfile, glob, json

def demo():
    print("=== Linux 命令列工具 Python 模擬 ===\n")

    # 1. 模擬 ls：列出目錄內容
    print("--- 1. ls：列出目錄 ---")
    path = os.getcwd()
    files = os.listdir(path)
    print(f"  {path} 內有 {len(files)} 個項目:")
    for f in sorted(files)[:8]:
        fp = os.path.join(path, f)
        mtime = os.path.getmtime(fp)
        size = os.path.getsize(fp)
        mode = "d" if os.path.isdir(fp) else "-"
        print(f"  {mode}{stat.filemode(os.stat(fp).st_mode)[1:]}  {size:>8}  {f}")

    # 2. 模擬 pwd/cd
    print("\n--- 2. pwd / cd：目錄操作 ---")
    orig = os.getcwd()
    print(f"  原始目錄: {orig}")
    os.chdir(tempfile.gettempdir())
    print(f"  cd 到暫存目錄: {os.getcwd()}")
    os.chdir(orig)

    # 3. 模擬 cp/mv：檔案複製與移動
    print("\n--- 3. cp / mv：檔案操作 ---")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(b"Hello Linux!\n")
        src = f.name
    dst = src + ".bak"
    shutil.copy2(src, dst)
    with open(dst) as f:
        content = f.read()
    print(f"  cp: {src} -> {dst}")
    print(f"  內容: {content.strip()}")
    os.unlink(dst); os.unlink(src)

    # 4. 模擬 cat / wc
    print("\n--- 4. cat / wc：讀取與計數 ---")
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("line one\nline two\nline three\n")
        tmp = f.name
    with open(tmp) as f:
        lines = f.readlines()
    print(f"  cat {tmp}:")
    for l in lines:
        print(f"    {l.strip()}")
    print(f"  wc: {len(lines)} lines, {sum(len(l) for l in lines)} chars")
    os.unlink(tmp)

    # 5. 模擬 grep：搜尋文字
    print("\n--- 5. grep：搜尋 ---")
    data = ["apple", "banana", "cherry", "date", "elderberry"]
    pattern = "a"
    matches = [s for s in data if pattern in s]
    print(f"  grep '{pattern}': {matches}")

    # 6. 模擬 sed：取代文字
    print("\n--- 6. sed：取代 ---")
    text = "hello world, hello linux"
    old, new = "hello", "hi"
    replaced = text.replace(old, new)
    print(f"  sed 's/{old}/{new}/g': {replaced}")

    # 7. 模擬 awk：欄位處理
    print("\n--- 7. awk：欄位處理 ---")
    csv = "Alice,30,Engineer\nBob,25,Designer\nCharlie,35,Manager"
    for line in csv.splitlines():
        fields = line.split(",")
        print(f"  $1={fields[0]:10} $2={fields[1]:5} $3={fields[2]}")

    # 8. 環境變數
    print("\n--- 8. 環境變數與 PATH ---")
    path_env = os.environ.get("PATH", "")
    paths = path_env.split(":")
    print(f"  PATH 有 {len(paths)} 個目錄")
    print(f"  HOME={os.environ.get('HOME', 'N/A')}")
    print(f"  USER={os.environ.get('USER', 'N/A')}")
    print(f"  SHELL={os.environ.get('SHELL', 'N/A')}")

    # 9. 模擬 ps：行程
    print("\n--- 9. ps：行程檢視 ---")
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    print(f"  共有 {len(lines)-1} 個行程")
    for line in lines[:5]:
        print(f"  {line}")

    # 10. 管線與重定向
    print("\n--- 10. 管線示範 ---")
    cmd = "echo 'a b c\nd e f' | awk '{print $2}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"  {cmd}")
    print(f"  輸出: {result.stdout.strip().splitlines()}")

    # 11. 檔案權限
    print("\n--- 11. 檔案權限 ---")
    with tempfile.NamedTemporaryFile(delete=False) as f:
        fpath = f.name
    os.chmod(fpath, 0o755)
    st = os.stat(fpath)
    print(f"  chmod 755: {stat.filemode(st.st_mode)}")
    os.chmod(fpath, 0o644)
    st = os.stat(fpath)
    print(f"  chmod 644: {stat.filemode(st.st_mode)}")
    os.unlink(fpath)

    # 12. 管線串接 (pipe)
    print("\n--- 12. 管線 (pipe) 模擬 ---")
    pipeline = "ps aux | grep python | wc -l"
    result = subprocess.run(pipeline, shell=True, capture_output=True, text=True)
    print(f"  {pipeline} = {result.stdout.strip()}")

    print("\n=== 示範結束 ===")

if __name__ == "__main__":
    demo()
