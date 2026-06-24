# 版本控制最佳實踐

良好的版本控制習慣能提升團隊效率和程式碼品質。

---

## 提交訊息規範

### 好的提交訊息

```
feat: 新增使用者登入功能

實作 OAuth 2.0 認證流程
- 新增 Google 登入
- 新增 Facebook 登入
- 更新使用者模型

Closes #123
```

### 結構

- **Header**：類型 + 簡短描述（最多 50 字）
- **Body**：詳細說明（可選）
- **Footer**：關聯的 Issues（可選）

### 類型

| 類型 | 說明 |
|------|------|
| feat | 新功能 |
| fix | 錯誤修復 |
| docs | 文件變更 |
| style | 格式變更（不影響程式碼） |
| refactor | 重構 |
| test | 測試相關 |
| chore | 建置或輔助工具變更 |

---

## 提交頻率

### 建議

- **小而頻繁**：每完成一個小功能就提交
- **邏輯完整**：每個提交是一個邏輯單元
- **可部署**：每個 commit 都能正常運作

### 壞範例

```bash
git commit -m "stuff"
git commit -m "WIP"
git commit -m "asdfadsf"
```

---

## Gitignore 最佳實踐

```gitignore
# 依賴
node_modules/
venv/
__pycache__/

# 構建產物
dist/
build/
*.class
*.o

# 環境
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# 系統
.DS_Store
Thumbs.db

# 日誌
*.log
npm-debug.log*

# 測試
coverage/
.nyc_output/
```

---

## 保護分支

```bash
# 在 GitHub 設定
# Settings → Branches → Add rule

# 保護 main 分支
- Require pull request reviews before merging
- Require status checks to pass before merging
- Include administrators
- Do not allow force pushes
- Do not allow deletions
```

---

## Hooks

Git hooks 能在特定事件觸發自訂腳本：

```bash
# 安裝 hooks
ln -s ../../scripts/pre-commit .git/hooks/pre-commit
```

### 常見用途

- 執行測試
- 檢查程式碼風格
- 自動格式化
- 檢查提交訊息格式

---

## 分支命名

```
feature/user-authentication
feature/login-oauth
bugfix/fix-login-redirect
hotfix/security-patch
release/v1.2.0
```

---

## 常用別名

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.df diff
git config --global alias.lg "log --oneline --graph --all"
git config --global alias.last "log -1 HEAD"
git config --global alias.unstage "reset HEAD --"
```

---

## 清理本地分支

```bash
# 刪除已合併的本地分支
git branch --merged main | grep -v "main" | xargs git branch -d

# 刪除所有追蹤的遠端已刪除的分支
git fetch --prune
```

---

## 小結

遵循這些最佳實踐，能讓你的專案更容易維護，團隊協作更順暢。

---

*作者：AI 程式人團隊*