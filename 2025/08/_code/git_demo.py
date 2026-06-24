#!/usr/bin/env python3
"""Git 版本控制示範 - AI 程式人雜誌 202508"""

import os
import subprocess
import tempfile
import shutil


def run_git(args, cwd):
    result = subprocess.run(
        ["git"] + args, capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        print(f"Git 錯誤: {result.stderr}")
    return result


def demo():
    print("=== Git 版本控制示範 ===\n")

    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)

    # 1. git init
    run_git(["init"], tmpdir)
    print("✓ git init 完成")

    # 2. Create and commit a file
    with open("hello.py", "w") as f:
        f.write('print("Hello, Git!")\n')
    run_git(["add", "hello.py"], tmpdir)
    run_git(["commit", "-m", "Initial commit"], tmpdir)
    print("✓ 首次提交完成")

    # 3. git log
    log_result = run_git(["log", "--oneline"], tmpdir)
    print(f"✓ 提交歷史:\n{log_result.stdout}")

    # 4. Branch: create and switch
    run_git(["checkout", "-b", "feature"], tmpdir)
    with open("feature.py", "w") as f:
        f.write('print("Feature branch")\n')
    run_git(["add", "feature.py"], tmpdir)
    run_git(["commit", "-m", "Add feature file"], tmpdir)
    print("✓ 分支建立與提交完成")

    # 5. Switch back to main and merge
    run_git(["checkout", "main"], tmpdir)
    run_git(["merge", "feature"], tmpdir)
    print("✓ 合併完成")

    # 6. Final log with graph
    log_result = run_git(["log", "--oneline", "--graph", "--all"], tmpdir)
    print(f"✓ 最終提交圖:\n{log_result.stdout}")

    # Cleanup
    os.chdir("/tmp")
    shutil.rmtree(tmpdir)
    print("\n✓ 清理完成")


if __name__ == "__main__":
    demo()
