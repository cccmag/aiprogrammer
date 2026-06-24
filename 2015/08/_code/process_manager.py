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

    print("啟動測試程序...")
    proc = subprocess.Popen(['sleep', '100'])
    pid = proc.pid
    print(f"程序 PID: {pid}")
    print()

    print("檢查程序狀態:")
    print(run_cmd(f"ps -p {pid} -o pid,ppid,state,cmd"))
    print()

    print("發送 SIGTERM 信號...")
    proc.terminate()
    time.sleep(1)

    returncode = proc.poll()
    print(f"程序返回碼: {returncode}")
    print()

    print("程序管理示範完成")

if __name__ == '__main__':
    main()