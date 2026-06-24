# GitHub 協作流程

## 簡介

GitHub 是全球最大的開源程式碼代管平台，擁有超過 2500 萬開發者。本篇介紹如何在 GitHub 上進行團隊協作。

## 基本概念

### 倉庫操作

```bash
# 克隆倉庫
git clone https://github.com/username/repository.git

# 新增遠端
git remote add upstream https://github.com/original/repo.git

# 查看遠端
git remote -v
```

### Fork 與 Pull Request 流程

1. Fork 倉庫到自己的帳號
2. Clone 到本地
3. 建立功能分支
4. 開發並提交
5. Push 到自己的 Fork
6. 在 GitHub 發起 Pull Request

## 同步上游倉庫

### 設定上游

```bash
# 假設 clone 了某人的倉庫
git remote add upstream https://github.com/original-owner/repo.git

# 查看遠端
git remote -v
# origin    https://github.com/your-username/repo.git (fetch)
# origin    https://github.com/your-username/repo.git (push)
# upstream  https://github.com/original-owner/repo.git (fetch)
# upstream  https://github.com/original-owner/repo.git (push)
```

### 同步更新

```bash
# 取得上游更新
git fetch upstream

# 切換到本地 master
git checkout master

# 合併上游 master
git merge upstream/master

# 推送更新
git push origin master
```

### 使用 rebase

```bash
git fetch upstream
git rebase upstream/master
```

## Pull Request

### 發起 Pull Request

1. 在 GitHub 上點擊 "New pull request"
2. 選擇要合併的分支
3. 填寫 PR 描述
4. 指派審核者
5. 提交 PR

### PR 描述範本

```markdown
## 變更內容
- 新增功能：...
- 修正問題：...

## 測試方式
1. 執行測試
2. 手動驗證

## 相關 Issue
Fixes #123
```

### Code Review

```bash
# 查看 PR 的變更
git fetch origin
git checkout -b pr/123 origin/pull/123

# 或使用 GitHub CLI
gh pr checkout 123
```

### 合併 PR

```bash
# 在本地合併 PR
git checkout master
git merge pr/123
git push origin master

# 或在 GitHub 上點擊 "Merge"
# 選項：Merge, Squash and merge, Rebase and merge
```

## 組織與團隊

### GitHub Organizations

- 建立組織管理多個專案
- 設定團隊與權限
- 統一管理成員

### 權限等級

| 角色 | 讀取 | 提 Issue | 推送 | 管理設定 |
|------|------|----------|------|----------|
| Pull requests only | ✓ | ✓ | ✗ | ✗ |
| Read | ✓ | ✓ | ✗ | ✗ |
| Triage | ✓ | ✓ | ✓ | ✗ |
| Write | ✓ | ✓ | ✓ | ✗ |
| Maintain | ✓ | ✓ | ✓ | ✓ |
| Admin | ✓ | ✓ | ✓ | ✓ |

## GitHub 功能

### Issues

追蹤任務、錯誤、功能請求：

```markdown
## 標題
詳細描述

## 重現步驟
1. 點擊...
2. 輸入...
3. 錯誤發生

## 預期行為
應該...

## 環境
- OS: macOS 10.13
- Version: 1.0.0
```

### Projects

專案管理面板（Kanban）：

- 待處理（To Do）
- 進行中（In Progress）
- 已完成（Done）

### Wiki

建立專案文件：

- API 文件
- 開發指南
- 部署說明

### Releases

發布版本：

```bash
git tag v1.0.0
git push origin v1.0.0

# 在 GitHub 上建立 Release
# 上傳編譯後的二進位檔案
# 撰寫發布說明
```

## 安全相關

### .github 目錄

存放 GitHub 設定檔：

```
.github/
├── ISSUE_TEMPLATE/
│   └── bug_report.md
├── PULL_REQUEST_TEMPLATE.md
└── workflows/
    └── ci.yml
```

### Branch Protection

保護重要分支：

- Require pull request reviews
- Require status checks
- Include administrators
- Restrict pushes

## 練習題

1. Fork 一個開源專案並發起 PR
2. 設定上游倉庫並同步更新
3. 使用 Projects 功能管理任務
4. 設定 Branch Protection 規則