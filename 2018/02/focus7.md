# 版本控制最佳實踐

## 簡介

良好的版本控制習慣可以提升團隊效率和程式碼品質。本篇介紹業界推薦的最佳實踐。

## 提交規範

### 提交訊息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

類型（type）：
- `feat` - 新功能
- `fix` - 錯誤修復
- `docs` - 文件
- `style` - 格式（不影響程式碼）
- `refactor` - 重構
- `perf` - 效能改善
- `test` - 測試
- `chore` - 建構/工具

範例：
```
feat(auth): 新增 Facebook 登入功能

- 新增 FacebookOAuthProvider
- 更新 User 模型
- 新增對應的測試

Closes #123
```

### 提交粒度

一個提交應該：
- 只做一件事
- 可以快速描述
- 可以輕鬆回復

```bash
# 好：每個提交邏輯清晰
git commit -m "feat: 新增用戶登入"
git commit -m "fix: 修正登入逾時問題"
git commit -m "refactor: 簡化 AuthService"

# 不好：把所有東西放在一起
git commit -m "更新很多東西"
```

### 提交頻率

- 經常提交，不要憋很久才提交
- 每次完成一個小功能就提交
- 使用 rebase 整理本地提交後再推送

## 分支策略

### 命名規範

```
feature/功能名稱        # 新功能
bugfix/問題描述         # 錯誤修復
hotfix/緊急問題         # 緊急修復
release/版本號           # 發布準備
docs/更新的文件         # 文件更新
```

### 保護分支

```bash
# master/main 保護設定
- 禁止直接推送
- 必須透過 PR
- 需要 code review
- 需要通過測試
```

### 處理衝突

```bash
# 1. 確保分支是最新的
git checkout master
git pull origin master

# 2. 切換到你的分支
git checkout feature/your-feature

# 3. 合併 master
git merge master

# 4. 解決衝突
# ... 編輯衝突檔案 ...
git add .
git commit -m "merge: resolve conflicts with master"
```

## 團隊協作

### 流程建議

```
1. 每天開始工作前 pull 最新程式碼
2. 建立自己的功能分支
3. 經常 commit（小而美的提交）
4. 定時 sync master 到你的分支
5. 準備好後發起 PR
6. 等待 review 再合併
```

### Code Review 建議

#### 審核者
- 及時回應 PR（24 小時內）
- 具體說明問題所在
- 區分 must-fix 和 nice-to-have

#### 開發者
- 回應所有意見
- 不要把討論變成爭執
- 感謝審核者的時間

### 避免的錯誤

1. **不要 force push 到 shared 分支**
2. **不要 commit 大型二進位檔案**
3. **不要把個人設定檔提交進去**
4. **不要忽視測試**

## .gitignore

常見需要忽略的檔案：

```
# 依賴
node_modules/
venv/
__pycache__/

# 組建產出
dist/
build/
*.class
*.o

# 環境設定
.env
*.local

# IDE
.vscode/
.idea/

# 日誌
*.log
npm-debug.log*

# 系統檔案
.DS_Store
Thumbs.db

# 測試覆蓋率
coverage/
```

### 全域 .gitignore

```bash
git config --global core.excludesfile ~/.gitignore
echo "*.log" >> ~/.gitignore
```

## 緊急修復

### Hotfix 流程

```bash
# 1. 從 master 建立 hotfix 分支
git checkout master
git checkout -b hotfix/critical-bug

# 2. 修復並測試
# ... 緊急修復 ...
git commit -m "fix: 緊急修正登入漏洞"

# 3. 合併回 master 並 tag
git checkout master
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1 -m "緊急安全更新"

# 4. 合併回 develop（如果有的話）
git checkout develop
git merge --no-ff hotfix/critical-bug

# 5. 刪除 hotfix 分支
git branch -d hotfix/critical-bug
```

## 備份與復原

### 備份

```bash
# 打包整個倉庫
git bundle create backup.bundle --all

# 備份到 GitHub（私有倉庫）
git push -u origin master
```

### 從備份復原

```bash
git clone backup.bundle backup-repo
```

## 練習題

1. 為你的專案建立 `.gitignore`
2. 練習撰寫符合規範的 commit message
3. 建立一個安全的分支策略
4. 演練一次完整的 PR 流程