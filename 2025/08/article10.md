# 用 Python 操作 Git

## 為什麼用 Python 操作 Git

自動化版本控制操作可以大幅提升效率，例如：
- 批次處理多個儲存庫
- CI/CD 流程中自動化操作
- 分析專案提交歷史
- 產生版本報表

## 使用 subprocess

最直接的方式是透過 `subprocess` 呼叫 Git 命令：

```python
import subprocess

def run_git_command(args, cwd="."):
    result = subprocess.run(
        ["git"] + args,
        capture_output=True, text=True,
        cwd=cwd
    )
    if result.returncode != 0:
        raise Exception(f"Git 錯誤：{result.stderr}")
    return result.stdout.strip()

# 範例使用
status = run_git_command(["status", "-s"])
log = run_git_command(["log", "--oneline", "-5"])
branch = run_git_command(["branch", "--show-current"])
```

## 使用 GitPython

安裝 GitPython 取得更高階的 API：

```bash
pip install GitPython
```

```python
from git import Repo

repo = Repo(".")
repo.git.add(A=True)
repo.index.commit("自動化提交")
branches = [b.name for b in repo.branches]
commits = [c.message.strip() for c in
           repo.iter_commits(max_count=5)]
print(f"分支：{branches}")
print(f"最近提交：{commits}")
```

## 純 Python 模擬

不需要實際安裝 Git 的簡化模擬：

```python
class GitSimulator:
    def __init__(self):
        self.objects = {}
        self.refs = {"HEAD": None, "main": None}
        self.index = set()
    
    def hash_object(self, content):
        import hashlib
        return hashlib.sha1(content.encode()).hexdigest()
    
    def add(self, path, content):
        oid = self.hash_object(content)
        self.objects[oid] = content
        self.index.add((path, oid))
    
    def commit(self, message):
        import time
        commit_obj = {
            "message": message,
            "timestamp": time.time(),
            "parent": self.refs["HEAD"],
            "files": dict(self.index)
        }
        oid = self.hash_object(str(commit_obj))
        self.objects[oid] = commit_obj
        self.refs["HEAD"] = oid
        self.refs["main"] = oid
        self.index.clear()
        print(f"[{oid[:7]}] {message}")

sim = GitSimulator()
sim.add("readme.md", "# Hello")
sim.commit("Initial commit")
sim.add("app.py", "print('hello')")
sim.commit("Add app")
```

更多 Python + Git 整合請參考 https://www.google.com/search?q=Python+操作+Git+教學。
