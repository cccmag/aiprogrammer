# 合併與 rebase

## 合併 (Merge)

`git merge` 將兩個分支的開發歷史合併在一起：

```bash
# 切換到目標分支
git checkout main

# 合併功能分支
git merge feature-user

# 使用 --no-ff 保留分支歷史
git merge --no-ff feature-user
```

### 合併類型

1. **Fast-forward**：無分歧，直接前進
2. **Three-way merge**：有分歧，建立合併提交
3. **Squash merge**：壓縮為單一提交

## Rebase

`git rebase` 將提交重新應用到另一個基礎上：

```bash
# 接在 main 之後
git checkout feature
git rebase main

# 互動式 rebase（整理歷史）
git rebase -i HEAD~3
```

### Rebase 的優勢與風險

**優點**：提交歷史更乾淨、線性
**風險**：改寫歷史，不應用於已推送的分支

## Merge vs Rebase

```bash
# Merge: 保留完整歷史
#     A---B---C feature
#    /         \
# D---E---F---G---H main

# Rebase: 線性歷史
# D---E---F---A'---B'---C' main
```

## Python 模擬

```python
class MergeRebaseDemo:
    def __init__(self):
        self.commits = []
    
    def fast_forward(self, feature, main):
        print(f"Fast-forward: main 移到 {feature}")
    
    def three_way_merge(self, feature, main):
        self.commits.append(f"Merge {feature} into {main}")
        print(f"三方合併完成")
    
    def rebase(self, branch, onto):
        print(f"將 {branch} rebase 到 {onto} 之上")
        print("提交歷史已改寫（線性）")
    
    def simulate(self):
        # main: A - B
        self.commits.extend(["A", "B"])
        # feature: A - B - C - D
        self.commits = ["A", "B", "C", "D"]
        
        print("合併前歷史：A - B - C - D")
        self.three_way_merge("feature", "main")
        
        print(f"合併後：{' - '.join(self.commits)}")
        
        self.commits = ["A", "B", "C", "D"]
        print("\nRebase 替代方案：")
        self.rebase("feature", "main")
        print("結果：A - B - C' - D'")

demo = MergeRebaseDemo()
demo.simulate()
```

更多合併與 rebase 比較請參考 https://www.google.com/search?q=git+merge+vs+rebase+比較。
