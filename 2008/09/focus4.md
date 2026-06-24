# 分支策略與工作流程

## 分支類型

```python
# 常見分支類型
branch_types = {
    'main/master': '主要分支，永遠可部署',
    'develop': '開發分支，整合功能',
    'feature': '功能分支',
    'release': '發布分支',
    'hotfix': '熱修補分支'
}
```

## Git Flow

### 流程圖

```bash
# Git Flow 分支策略
main ───●──────────────●─────────────●──→ (production)
        │              │             │
        │    release/1.0│             │release/2.0
        │        │      │             │
        │        ↓      │             ↓
develop ──●──●──●──●──●──●──●──●──●──●───→ (next release)
              ↑  ↑  ↑  ↑
         feature/A  feature/B
```

### 常用命令

```bash
# 初始化 Git Flow
git flow init

# 開始功能分支
git flow feature start new-feature

# 完成功能
git flow feature finish new-feature

# 開始發布
git flow release start v1.0.0

# 完成發布
git flow release finish v1.0.0
```

## GitHub Flow

### 簡化流程

```python
github_flow = {
    'main': '永遠可部署',
    'feature/*': '功能分支',
    'PR': '所有更改透過 Pull Request',
    'review': '審查後合併'
}
```

### 工作流程

```bash
# 1. 建立分支
git checkout -b feature/new-feature

# 2. 開發和提交
git add .
git commit -m "Add new feature"

# 3. 推送
git push origin feature/new-feature

# 4. 發起 Pull Request

# 5. 審查和討論

# 6. 合併到 main
```

## 熱修補流程

```bash
# 建立熱修補分支
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 修復並測試
# ...

# 合併到 main
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1 -m "Critical bug fix"

# 合併回 develop
git checkout develop
git merge --no-ff hotfix/critical-bug

# 刪除熱修補分支
git branch -d hotfix/critical-bug
```

## 分支命名

```python
# 分支命名規範
naming_conventions = {
    'feature/': '功能分支',
    'bugfix/': '錯誤修復分支',
    'hotfix/': '熱修補分支',
    'release/': '發布分支',
    'wip/': '工作中的分支'
}
```

## 結論

選擇適合的分支策略取決於團隊規模和專案特性。Git Flow 適合正式發布週期的專案，GitHub Flow 適合持續部署的網頁應用。

---

**延伸閱讀**

- [Git 核心概念與架構](focus2.md)
- [GitHub 與社交程式設計](focus3.md)
- [Git+flow](https://www.google.com/search?q=Git+flow+branching+strategy)