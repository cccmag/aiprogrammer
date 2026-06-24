# Git Flow 與協作流程

## Git Flow 工作流程

Git Flow 是 Vincent Driessen 在 2010 年提出的分支模型，已成為許多團隊的標準協作流程。

### 分支角色

```
main        → 穩定發布版本
  ↓
develop     → 開發主線
  ├── feature/*   → 功能開發
  ├── release/*   → 發布準備
  └── hotfix/*    → 緊急修復
```

### 流程說明

1. **功能開發**：從 develop 建立 feature 分支
2. **完成功能**：合併 feature 回 develop
3. **準備發布**：從 develop 建立 release 分支
4. **正式發布**：合併 release 到 main 和 develop
5. **緊急修復**：從 main 建立 hotfix 分支

### GitHub Flow

更簡潔的流程，適合持續部署：

```bash
# 從 main 建立功能分支
git checkout -b feature-xyz

# 開發、提交、推送
git add . && git commit -m "完成功能 xyz"
git push origin feature-xyz

# 開 PR → 審查 → 合併回 main
# 立即部署
```

### Python 模擬 Git Flow

```python
class GitFlow:
    def __init__(self):
        self.branches = {
            "main": [],
            "develop": []
        }
    
    def feature_start(self, name):
        self.branches[f"feature/{name}"] = []
        print(f"start feature/{name}")
    
    def feature_finish(self, name):
        fb = f"feature/{name}"
        self.branches["develop"].extend(self.branches[fb])
        del self.branches[fb]
        print(f"finish feature/{name} -> develop")
    
    def release_start(self, version):
        self.branches[f"release/{version}"] = []
        print(f"start release/{version}")
    
    def release_finish(self, version):
        rb = f"release/{version}"
        self.branches["main"].extend(self.branches[rb])
        self.branches["develop"].extend(self.branches[rb])
        del self.branches[rb]
        print(f"release {version} finished")
    
    def hotfix(self, name):
        self.branches["main"].append(f"hotfix: {name}")
        self.branches["develop"].append(f"hotfix: {name}")
        print(f"hotfix '{name}' applied")

flow = GitFlow()
flow.feature_start("login")
flow.feature_finish("login")
flow.release_start("1.0.0")
flow.release_finish("1.0.0")
flow.hotfix("fix crash")
```

更多 Git Flow 資訊請參考 https://www.google.com/search?q=Git+Flow+分支模型+教學。
