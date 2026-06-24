# Git 分散式版本控制：Linus 的新專案

Git 是 Linux 核心作者 Linus Torvalds 於 2005 年創作的分散式版本控制系統。2007 年，Git 已經成熟並被廣泛採用。

## Git 的核心概念

### 分散式架構

```bash
# 每個開發者都有完整的儲存庫副本
git clone https://github.com/user/repo.git

# 無需網路即可大多數操作
git status      # 本地操作
git diff        # 本地操作
git log         # 本地操作
```

### 快照而非差異

```bash
# Git 儲存快照，而非差異
# 每次提交都是完整的檔案快照

# 快速分支切換
git checkout -b new-feature
git checkout master
```

## Git 的效能優勢

```bash
# Git 的效能測試
# 對比 Subversion：
# - 提交：快 10-100 倍
# - 分支：快 100 倍
# - 查看歷史：快 10 倍

git log --oneline          # 快速查看歷史
git branch -a              # 快速列出分支
git diff HEAD~5             # 快速比較
```

## 常用的 Git 工作流程

```bash
# 集中式工作流程
git clone url
git add .
git commit -m "message"
git pull origin master
git push origin master

# Gitflow 工作流程
git checkout -b develop
git checkout -b feature/new
# ... 開發 ...
git checkout develop
git merge feature/new
git checkout master
git merge develop
```

## 結語

Git 的發明徹底改變了版本控制的格局，其分散式設計和優異效能使其成為現代軟體開發的標準工具。

---

*延伸閱讀：[Git 官方網站](https://developers.google.com/search/?q=git+official)*