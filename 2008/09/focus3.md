# GitHub 與社交程式設計

## GitHub 概述

GitHub 於 2008 年 2 月正式上線，是基於 Git 的程式碼托管平台。

### 核心功能

```python
github_features = {
    'repository': '程式碼倉庫托管',
    'fork': '派生其他人的專案',
    'pull_request': '請求合併更改',
    'issue': '追蹤問題和功能請求',
    'wiki': '專案文檔',
    'gist': '程式碼片段分享'
}
```

## Fork 模式

### Fork 工作流程

```bash
# 1. Fork 倉庫
# 透過 GitHub UI 操作

# 2. 克隆到本地
git clone https://github.com/yourname/project.git

# 3. 新增功能
git checkout -b new-feature
# ... 編輯檔案 ...
git add .
git commit -m "Add new feature"

# 4. 推送分支
git push origin new-feature

# 5. 發起 Pull Request
# 透過 GitHub UI 操作
```

### 同步上游

```bash
# 新增上游倉庫
git remote add upstream https://github.com/original/project.git

# 拉取上游更改
git fetch upstream

# 合併到本地
git checkout main
git merge upstream/main
```

## Pull Request

### 工作流程

```python
# Pull Request 流程
pull_request_flow = [
    'Fork 倉庫',
    '建立功能分支',
    '提交更改',
    '推送分支',
    '發起 Pull Request',
    '程式碼審查',
    '合併分支'
]
```

### 審查功能

```python
# GitHub 提供的審查功能
review_features = [
    '程式碼注釋',
    '提議修改',
    '批准/請求更改',
    '自動化檢查'
]
```

## 社交功能

### 關注

```python
# 社交互動
social_features = [
    'Watch（關注專案）',
    'Star（收藏專案）',
    'Follow（關注開發者）',
    'Gist（分享片段）'
]
```

### 組織

```python
# 組織功能
organization_features = [
    '團隊管理',
    '許可權控制',
    '組織倉庫',
    '審計日誌'
]
```

## GitHub 的影響

### 開源專案

```python
# 2008 年熱門 GitHub 專案
popular_repos = [
    'rails/rails',
    'jquery/jquery',
    'homebrew/homebrew',
    'django/django'
]
```

### 社交程式設計

```python
# 新的協作模式
collaboration_model = {
    '任何人都能貢獻': '透過 Fork 和 Pull Request',
    '透明的開發過程': '所有人可見討論和程式碼',
    '去中心化': '無需正式授權即可參與'
}
```

## 結論

GitHub 開創了社交程式設計的新模式。Fork 和 Pull Request 使得開源貢獻變得更加簡單和民主。

---

**延伸閱讀**

- [分散式版本控制的興起](focus1.md)
- [分支策略與工作流程](focus4.md)
- [GitHub+about](https://www.google.com/search?q=GitHub+about+page)