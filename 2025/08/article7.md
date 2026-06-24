# Pull Request 流程

## 什麼是 Pull Request

Pull Request (PR) 是 GitHub 提供的協作機制，讓開發者通知團隊成員自己已完成某個功能，請求審查並合併。

## PR 完整流程

### 第一步：準備工作

```bash
# 1. Fork 專案（在 GitHub 上點擊 Fork）

# 2. Clone 到本機
git clone https://github.com/yourname/project.git
cd project

# 3. 新增上游遠端
git remote add upstream https://github.com/original/project.git

# 4. 建立功能分支
git checkout -b fix-bug-456
```

### 第二步：開發與提交

```bash
# 修改程式碼...
git add .
git commit -m "修復 issue #456：處理空值錯誤"
git push origin fix-bug-456
```

### 第三步：建立 PR

在 GitHub 上點擊 "New Pull Request"，選擇：
- base: original/main
- compare: yourname/fix-bug-456

### 第四步：Code Review

審查者回饋後進行修改，持續推送即可自動更新 PR：

```bash
git add .
git commit -m "根據 review 意見修正"
git push origin fix-bug-456
```

## Python 模擬 PR 流程

```python
class PullRequest:
    def __init__(self, title, branch):
        self.title = title
        self.branch = branch
        self.reviews = []
        self.merged = False
    
    def approve(self, reviewer):
        self.reviews.append(reviewer)
        print(f"{reviewer} 核准")
    
    def merge(self):
        if len(self.reviews) > 0:
            self.merged = True
            print(f"PR 已合併：{self.title}")
        else:
            print("需要核准")

pr = PullRequest("修復登入錯誤", "fix-login")
pr.approve("Alice")
pr.merge()
```

更多 PR 流程請參考 https://www.google.com/search?q=Pull+Request+流程+教學。
