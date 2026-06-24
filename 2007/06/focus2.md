# Git 1.5 的新功能：2007 年 6 月的重大更新

## 前言

2007 年 6 月，Git 1.5.0 正式發布。這是 Git 發展史上的重要里程碑，標誌著 Git 從一個「核心開發者專用工具」向更廣泛的應用領域邁進。

## Git 1.5.0 的主要新功能

### 1. 改進的 Git Web 介面

```bash
# Git 1.5 新增的 git-instaweb
git instaweb --httpd=webrick --port=8080

# 自動啟動 web 介面檢視倉庫
```

### 2. 更好的 SHA-1 處理

```bash
# Git 1.5 的 SHA-1 計算更快
# 使用 OpenSSL 加速
git log --pretty=oneline

# 效能提升約 30%
```

### 3. 改進的歸併支援

```bash
# Git 1.5 更好的自動歸併
git merge feature-branch

# 衝突解決助手
git mergetool

# 改進的圖形化歸併工具支援
```

### 4. git-svn 改進

```bash
# Git 1.5 的 git-svn 更加穩定
git svn clone http://svn.example.com/repo
git svn rebase
git svn dcommit
```

## Git 1.5 的效能改進

### 索引檔案優化

```bash
# Git 1.5 使用更好的索引格式
# .git/index 使用 V2 格式
time git status

# 在大型專案中效能提升明顯
```

### 網路傳輸優化

```bash
# Git 1.5 改進了 git clone
git clone git://kernel.org/pub/scm/git/git.git

# 使用更高效的打包協議
```

## Git 1.5 的新命令

### git-rebase 的改進

```bash
# 互動式 rebase
git rebase -i HEAD~3

# 可以在 rebase 中squash、reorder、edit commits
```

### git-stash 的改進

```bash
# 儲存工作進度
git stash save "work in progress"
git stash list
git stash pop
```

## Git 1.5 的範例工作流

```bash
# Git 1.5 典型工作流
# 1. 初始化或克隆
git init
git clone git://server/repo.git

# 2. 新增和提交
git add file.txt
git commit -m "Add file"

# 3. 建立分支
git branch feature
git checkout feature

# 4. 在分支上開發
git add .
git commit -m "Implement feature"

# 5. 合併回主分支
git checkout master
git merge feature

# 6. 推送到遠端
git push origin master
```

## Git 1.5 的配置

### .gitconfig 範例

```ini
# ~/.gitconfig 範例
[user]
    name = John Doe
    email = john@example.com

[core]
    editor = vim
    autocrlf = input

[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --

[color]
    ui = auto
```

## Git 1.5 對社群的影響

### 採用率提升

```
Git 採用率（估計）：
─────────────────────
2005      Linux 核心等少數專案
2006      更多開源專案開始使用
2007      Git 1.5 發布，更多專案遷移
2008      GitHub 上線，加速採用
```

### 工具生態系統

Git 1.5 催生了更多工具：

```bash
# Git 1.5 時期的可用工具
gitk          # 圖形化歷史檢視
git-gui       # 圖形化 commit 工具
git-svn       # SVN 互動
cogito        # 早期 Git 輔助工具（後來被弃用）
```

## 結語

Git 1.5.0 的發布標誌著 Git 已經足夠成熟，可以用於大型專案。從 Linux 核心到 Ruby on Rails，越來越多的知名專案開始採用 Git。

這個版本奠定了 Git 日後成為主流版本控制系統的基礎。

---

## 延伸閱讀

- [Git+1.5.0+release+2007](https://www.google.com/search?q=Git+1.5.0+release+2007)
- [Git+history+timeline](https://www.google.com/search?q=Git+history+timeline)

---

*本篇文章為「AI 程式人雜誌 2007 年 6 月號」本期焦點系列之一。*