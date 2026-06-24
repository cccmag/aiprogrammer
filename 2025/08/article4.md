# 分支建立與切換

## 分支管理命令

分支是 Git 的輕量級功能，建立成本極低：

```bash
# 列出所有分支
git branch

# 建立新分支
git branch feature-search

# 切換分支
git checkout feature-search

# 建立並切換（一行完成）
git checkout -b feature-search

# 重新命名分支
git branch -m old-name new-name

# 刪除分支
git branch -d feature-search
```

## 分支的本質

Git 分支只是一個指向特定提交的指標：

```bash
# 檢視分支與提交的關係
git log --oneline --graph --all

# 檢視每個分支的最新提交
git branch -v

# 檢視已合併的分支
git branch --merged

# 檢視未合併的分支
git branch --no-merged
```

## 分支操作策略

### 功能分支
```bash
git checkout -b feature/user-auth
# ... 開發程式碼 ...
git add . && git commit -m "完成使用者認證"
git checkout main
git merge feature/user-auth
```

### 追蹤遠端分支
```bash
# 建立本地分支追蹤遠端
git checkout -b feature origin/feature

# 推送本地分支到遠端
git push -u origin feature-user
```

## Python 分支管理

```python
import subprocess

class BranchManager:
    def __init__(self):
        self.current = "main"
        self.branches = ["main"]
    
    def create(self, name, switch=True):
        self.branches.append(name)
        if switch:
            self.current = name
        print(f"分支 '{name}' 已建立")
    
    def switch(self, name):
        assert name in self.branches
        self.current = name
        print(f"切換到 '{name}'")
    
    def delete(self, name):
        if name in self.branches:
            self.branches.remove(name)
            print(f"分支 '{name}' 已刪除")
    
    def list_branches(self):
        for b in self.branches:
            marker = "* " if b == self.current else "  "
            print(f"{marker}{b}")

mgr = BranchManager()
mgr.create("feature-login")
mgr.create("feature-search")
mgr.switch("feature-login")
mgr.list_branches()
```

更多分支操作請參考 https://www.google.com/search?q=git+branch+教學。
