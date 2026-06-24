# git init、add、commit

## 初始化儲存庫

`git init` 在當前目錄建立 Git 儲存庫：

```bash
mkdir myapp
cd myapp
git init
```

成功後會出現提示：`Initialized empty Git repository in ...`

## 檔案狀態追蹤

Git 的檔案有四種狀態：
- **Untracked**：尚未追蹤
- **Modified**：已修改
- **Staged**：已暫存
- **Committed**：已提交

### 檢視狀態

```bash
git status           # 完整狀態
git status -s        # 簡潔模式
```

## 加入暫存區

```bash
# 加入單一檔案
git add main.py

# 加入所有變更
git add .

# 加入特定類型
git add *.py
```

## 提交變更

```bash
# 基本提交
git commit -m "Add login feature"

# 跳過暫存區直接提交
git commit -a -m "Quick fix"

# 修改最後一次提交
git commit --amend -m "修正提交訊息"
```

## Python 模擬

```python
import os
import subprocess

def git_workflow():
    repo_dir = "demo_repo"
    os.makedirs(repo_dir, exist_ok=True)
    os.chdir(repo_dir)
    
    # init
    subprocess.run(["git", "init"], 
        capture_output=True)
    print("✓ 初始化完成")
    
    # 建立檔案
    with open("app.py", "w") as f:
        f.write("# My App\nprint('hello')\n")
    
    # add
    subprocess.run(["git", "add", "app.py"],
        capture_output=True)
    print("✓ 已暫存 app.py")
    
    # commit
    subprocess.run(["git", "commit", "-m",
        "Initial commit"], capture_output=True)
    print("✓ 提交完成")
    
    # status
    result = subprocess.run(["git", "status", "-s"],
        capture_output=True, text=True)
    print(f"狀態：{result.stdout or '乾淨'}")

if __name__ == "__main__":
    git_workflow()
```

更多操作細節請參考 https://www.google.com/search?q=git+init+add+commit+用法。
