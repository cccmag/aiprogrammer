# Git 1.6.5：分散式版本控制的成熟

## 前言

2009 年，Git 已經成為最流行的分散式版本控制系統。GitHub 用戶突破 100 萬，各大开源專案紛紛從其他版本控制系統遷移到 Git。

## Git 的核心概念

### 分散式架構

```bash
# 傳統集中式 vs 分散式

# 集中式：
#     [Server]
#     /      \
#   [Dev A]  [Dev B]

# 分散式：
#   [Dev A]  [Dev B]  [Dev C]
#      \      |      /
#       \     |     /
#        [GitHub]
#          |
#        [Upstream]
```

### 基本操作

```bash
# 初始化
git init

# 克隆
git clone https://github.com/user/repo.git

# 添加檔案
git add file.txt
git commit -m "Add file"

# 推送
git push origin master

# 拉取
git pull origin master

# 分支
git branch feature
git checkout feature
```

## Git 1.6.5 的新功能

### 改進的合併工具

```bash
# 更好的衝突解決
git mergetool

# 圖形化合併工具支援
git config merge.tool kdiff3
```

### 更好的效能

```bash
# Git 1.6 vs 1.5 效能對比
# 克隆大型專案：快 30%
# 推送：快 50%
# 合併：快 40%
```

## GitHub 的崛起

### 社交程式設計

```markdown
GitHub 的特色：

1. Fork & Pull Request
   - 任何人可以貢獻開源專案
   - 程式碼審查機制

2. 社交網路
   - 追蹤其他開發者
   - 關注專案更新

3. 組織
   - 團隊協作
   - 權限管理

4. Wiki 和 Issue
   - 專案文件
   - 問題追蹤
```

### 知名專案

```bash
# 2009 年使用 Git 的知名專案
linux kernel
android
ruby on rails
jquery
node.js
perl
php
```

## 結語

Git 和 GitHub 的結合徹底改變了開源開發的方式。2009 年標誌著分散式版本控制成為主流。

## 延伸閱讀

- [Git 官方網站](https://www.google.com/search?q=Git+official+website)
- [GitHub 2009](https://www.google.com/search?q=GitHub+100000+users+2009)
- [Git 教程](https://www.google.com/search?q=Git+tutorial+beginners)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*