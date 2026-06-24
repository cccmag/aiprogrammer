#!/usr/bin/env python3
"""
Git 操作示範腳本
"""

import subprocess
import os
import sys

def run_cmd(cmd, capture=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if capture:
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
    return result

def main():
    demo_dir = 'git_demo_python'
    
    # 清理並建立目錄
    run_cmd(f'rm -rf {demo_dir}')
    os.makedirs(demo_dir)
    
    # 初始化 Git 倉庫
    print("=== 初始化 Git 倉庫 ===")
    run_cmd(f'cd {demo_dir} && git init')
    run_cmd(f'cd {demo_dir} && git config user.name "Demo"')
    run_cmd(f'cd {demo_dir} && git config user.email "demo@demo.com"')
    
    # 建立初始檔案
    print("\n=== 建立初始檔案 ===")
    with open(f'{demo_dir}/hello.py', 'w') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('print("Hello, Git!")\n')
    
    # 添加並提交
    run_cmd(f'cd {demo_dir} && git add hello.py')
    run_cmd(f'cd {demo_dir} && git commit -m "Initial commit"')
    
    # 建立分支
    print("\n=== 建立並切換到功能分支 ===")
    run_cmd(f'cd {demo_dir} && git checkout -b feature/add-goodbye')
    
    # 修改檔案
    with open(f'{demo_dir}/hello.py', 'a') as f:
        f.write('print("Goodbye, Git!")\n')
    
    run_cmd(f'cd {demo_dir} && git add hello.py')
    run_cmd(f'cd {demo_dir} && git commit -m "feat: 新增 Goodbye 訊息"')
    
    # 切回主分支
    print("\n=== 切回主分支 ===")
    run_cmd(f'cd {demo_dir} && git checkout main')
    
    # 查看檔案內容
    print("\n=== 主分支上的檔案內容 ===")
    with open(f'{demo_dir}/hello.py') as f:
        print(f.read())
    
    # 合併分支
    print("\n=== 合併功能分支 ===")
    run_cmd(f'cd {demo_dir} && git merge feature/add-goodbye -m "merge: 合併功能分支"')
    
    # 顯示歷史
    print("\n=== Git 歷史 ===")
    run_cmd(f'cd {demo_dir} && git log --oneline')
    
    # 清理
    print("\n=== 清理測試目錄 ===")
    run_cmd(f'rm -rf {demo_dir}')
    
    print("\nGit Python 示範完成！")

if __name__ == '__main__':
    main()