# 分支與合併

## Git 分支模型

分支是 Git 最強大的功能之一。分支允許開發者在獨立的開發線上工作，不影響主線程式碼。

### 分支的本質

在 Git 中，分支只是一個指向提交的指標。建立新分支幾乎是即時的：

```bash
# 建立分支
git branch feature-login

# 切換分支
git checkout feature-login

# 或者一行完成
git checkout -b feature-login
```

### 合併分支

當功能開發完成後，將分支合併回主線：

```bash
git checkout main
git merge feature-login
```

Git 會自動進行三方合併 (three-way merge)，根據兩個分支的最新提交和共同的祖先提交來產生合併結果。

### 分支策略

常見的分支策略包括：

- **Git Flow**：main、develop、feature、release、hotfix
- **GitHub Flow**：main + feature branch，搭配 PR
- **Trunk-Based Development**：頻繁合併到主線

### Python 模擬分支

```python
class BranchDemo:
    def __init__(self):
        self.commits = []
        self.branches = {"main": 0}
        self.current = "main"
    
    def commit(self, msg):
        self.commits.append(msg)
        self.branches[self.current] = len(self.commits)
        print(f"[{self.current}] commit: {msg}")
    
    def branch(self, name):
        self.branches[name] = self.branches[self.current]
        print(f"branch '{name}' created at commit {self.branches[name]}")
    
    def switch(self, name):
        self.current = name
        print(f"switched to '{name}'")
    
    def merge(self, branch):
        target = self.branches[branch]
        current = self.branches[self.current]
        self.branches[self.current] = max(target, current)
        print(f"merged '{branch}' into '{self.current}'")

demo = BranchDemo()
demo.commit("initial")
demo.branch("feature")
demo.switch("feature")
demo.commit("add login")
demo.switch("main")
demo.merge("feature")
```

更多分支管理請參考 https://www.google.com/search?q=Git+分支+合併+教學。
