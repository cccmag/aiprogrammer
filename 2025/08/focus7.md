# 開源貢獻實戰

## 參與開源的第一步

貢獻開源專案是提升程式能力的絕佳方式。Git 和 GitHub 讓這個過程變得簡單且有條理。

### 尋找適合的專案

- 從常用工具開始，如 Flask、Requests、Django
- 搜尋標籤：good first issue、help wanted
- 檢視專案的貢獻指南 CONTRIBUTING.md

### 貢獻流程

1. **Fork 儲存庫**：在 GitHub 上複製一份到自己的帳號
2. **Clone 到本機**：`git clone https://github.com/yourname/project.git`
3. **建立分支**：`git checkout -b fix-bug-123`
4. **修改程式碼**：進行修改並提交
5. **推送變更**：`git push origin fix-bug-123`
6. **發起 PR**：在 GitHub 上建立 Pull Request

### PR 最佳實踐

```python
class PullRequest:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.reviews = []
        self.status = "open"
    
    def add_review(self, reviewer, approved, comment=""):
        self.reviews.append({
            "reviewer": reviewer,
            "approved": approved,
            "comment": comment
        })
        if all(r["approved"] for r in self.reviews):
            self.status = "approved"
    
    def merge(self):
        if self.status == "approved":
            print(f"Merged: {self.title}")
            return True
        print("Need approval first")
        return False

pr = PullRequest("Fix login bug", 
    "修正在特定情況下登入失敗的問題")
pr.add_review("alice", True, "LGTM!")
pr.add_review("bob", True)
pr.merge()
```

### 貢獻守則

- 保持友善的溝通態度
- 遵循專案的程式碼風格
- 撰寫清晰的提交訊息
- 確保測試通過

### 從哪裡開始

推薦搜尋 https://www.google.com/search?q=open+source+good+first+issue 尋找適合您的第一個開源貢獻。

貢獻開源不僅能幫助社群，也能累積自己的作品集，對職涯發展大有幫助！
