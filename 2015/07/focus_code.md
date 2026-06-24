# Git 程式範例

本章提供實際可運行的 Git 操作範例。

---

## 範例：完整的工作流程

```bash
#!/bin/bash
# 標準的 Git 工作流程範例

set -x

# 初始化倉庫
rm -rf demo && mkdir demo && cd demo
git init

# 設定使用者
git config user.name "Demo User"
git config user.email "demo@example.com"

# 建立初始檔案
echo "# 我的專案" > README.md
git add README.md
git commit -m "Initial commit"

# 建立 develop 分支
git checkout -b develop
echo "開始開發" > dev.txt
git add dev.txt
git commit -m "feat: 新增開發檔案"

# 建立 feature 分支
git checkout -b feature/new-feature develop
echo "新功能實作" > feature.txt
git add feature.txt
git commit -m "feat: 新功能第一版"

# 修改並提交
echo "更多功能" >> feature.txt
git add feature.txt
git commit -m "feat: 新增功能細節"

# 切回 develop 並合併
git checkout develop
git merge --no-ff feature/new-feature -m "merge: 合併新功能"

# 建立 release 分支
git checkout -b release/1.0.0
echo "1.0.0" > version.txt
git add version.txt
git commit -m "chore: 版本更新至 1.0.0"

# 合併到 main
git checkout main
git merge --no-ff release/1.0.0 -m "merge: 發布版本 1.0.0"
git tag -a v1.0.0 -m "版本 1.0.0"

echo "工作流程完成"
```

---

## 範例：解決合併衝突

```python
#!/usr/bin/env python3
"""
Git 衝突解決示範腳本
"""
import subprocess
import os

def run_cmd(cmd, capture=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if capture:
        print(result.stdout)
    return result

def main():
    os.makedirs('conflict-demo', exist_ok=True)
    os.chdir('conflict-demo')
    
    run_cmd('rm -rf .git && git init')
    run_cmd('git config user.name "Demo"')
    run_cmd('git config user.email "demo@demo.com"')
    
    # 初始提交
    with open('file.txt', 'w') as f:
        f.write('Line 1\nLine 2\nLine 3\n')
    run_cmd('git add . && git commit -m "Initial"')
    
    # 建立分支並修改
    run_cmd('git checkout -b branch1')
    with open('file.txt', 'w') as f:
        f.write('Branch 1 Line 1\nLine 2\nLine 3\n')
    run_cmd('git commit -am "Branch 1 changes"')
    
    # 回主分支並建立另一分支
    run_cmd('git checkout main')
    run_cmd('git checkout -b branch2')
    with open('file.txt', 'w') as f:
        f.write('Branch 2 Line 1\nLine 2\nLine 3\n')
    run_cmd('git commit -am "Branch 2 changes"')
    
    # 合併
    run_cmd('git checkout main')
    print("嘗試合併 branch1:")
    run_cmd('git merge branch1 --no-edit || true')
    print("\n嘗試合併 branch2:")
    result = run_cmd('git merge branch2 || echo "衝突發生"')
    
    # 顯示衝突檔案
    if os.path.exists('file.txt'):
        print("\n衝突檔案內容:")
        with open('file.txt') as f:
            print(f.read())
    
    print("\n衝突解決示範完成")

if __name__ == '__main__':
    main()
```

---

## 範例：使用 Git Python 程式庫

```python
#!/usr/bin/env python3
"""
使用 GitPython 程式庫操作 Git
"""

try:
    from git import Repo
    import os
    
    # 克隆倉庫
    repo_url = "https://github.com/git/git"
    repo_path = "/tmp/git-demo"
    
    if not os.path.exists(repo_path):
        repo = Repo.clone_from(repo_url, repo_path)
        print(f"已克隆倉庫到 {repo_path}")
    else:
        repo = Repo(repo_path)
        print(f"使用現有倉庫 {repo_path}")
    
    # 獲取資訊
    print(f"目前分支: {repo.active_branch}")
    print(f"最後提交: {repo.head.commit.hexsha[:8]}")
    print(f"提交訊息: {repo.head.commit.message.strip()}")
    
    # 操作分支
    new_branch = repo.create_head('my-feature')
    new_branch.checkout()
    
    # 新增檔案
    readme_path = os.path.join(repo_path, "my_notes.txt")
    with open(readme_path, 'w') as f:
        f.write("這是我的筆記")
    
    # 提交
    repo.index.add([readme_path])
    repo.index.commit("新增個人筆記")
    
    print("分支 my-feature 已建立並提交")
    
except ImportError:
    print("請先安裝 GitPython: pip install gitpython")
    print("執行中的範例腳本將繼續執行基本的 Git 操作")
```

---

## 執行測試

```bash
#!/bin/bash
set -x

cd /Users/Shared/ccc/magazine/aiprogrammer/2015/07/_code

echo "=== 執行 Git 流程範例 ==="
chmod +x git_workflow.sh
./git_workflow.sh

echo ""
echo "=== 執行 Git Python 範例 ==="
chmod +x git_python.py
python3 git_python.py

echo ""
echo "=== 所有測試完成 ==="
```

---

*作者：AI 程式人團隊*