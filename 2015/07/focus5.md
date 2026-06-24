# 多人協作開發

多人協作是現代軟體開發的核心。本章探討如何有效管理多人協作的 Git 工作流程。

---

## 同步遠端倉庫

```bash
# 克隆倉庫
git clone https://github.com/team/project.git
cd project

# 檢視已設定的遠端
git remote -v

# 新增上游倉庫（fork 情境）
git remote add upstream https://github.com/original/project.git

# 獲取遠端分支
git fetch origin
git fetch upstream

# 拉取更新
git pull origin main
```

---

## 處理合併衝突

當多人同時修改同一檔案時，會產生衝突。

### 識別衝突

```bash
git status
# 會顯示 "both modified: filename.txt"
```

### 解決衝突

1. 開啟衝突檔案

```markdown
<<<<<<< HEAD
我的修改
=======
他人的修改
>>>>>>> branch-name
```

2. 編輯檔案，保留正確的內容

```markdown
整合後的正確內容
```

3. 標記為已解決

```bash
git add filename.txt
git commit -m "Resolve merge conflict"
```

### 使用工具

```bash
# 使用 vimdiff
git mergetool

# 安裝 Beyond Compare
git config --global merge.tool bc3
```

---

## Rebase 與合併

### Rebase

將当前分支的提交在另一分支的頂端重新應用：

```bash
git checkout feature
git rebase main
```

### 合併

```bash
git checkout main
git merge feature
```

### 選擇策略

| 情境 | 建議 |
|------|------|
| 公共分支 | 使用 merge |
| 本地清理 | 使用 rebase |
| Pull Request | 保持乾淨的 commit 歷史 |

---

## 工作流程

### Feature Branch Workflow

1. 從 main 建立 feature 分支
2. 在分支上開發
3. 定時與 main 同步
4. 完成後建立 Pull Request

```bash
git checkout -b feature/new-ui main
# 開發...
git push origin feature/new-ui
# 建立 Pull Request
```

### Fork 流程

1. Fork 倉庫到自己的帳號
2. 克隆 Fork 的倉庫
3. 新增上游倉庫
4. 同步上游變更
5. 建立 PR 回原倉庫

```bash
git remote add upstream https://github.com/original/repo.git

# 定期同步
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## 程式碼審查

### 審查清單

- 程式碼風格一致
- 是否有測試
- 註解是否清楚
- 是否有效能問題
- 安全性考量

### 審查技巧

- 小而頻繁的 PR 更容易審查
- PR 描述要清楚
- 自動化測試要通過

---

## 小結

良好的協作需要清晰的流程、有效的溝通和工具的配合。

---

*作者：AI 程式人團隊*