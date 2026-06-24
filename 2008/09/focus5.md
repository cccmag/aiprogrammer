# 常用 Git 命令詳解

## 基礎命令

### 初始化與克隆

```bash
# 初始化新倉庫
git init

# 克隆遠端倉庫
git clone https://github.com/user/repo.git
git clone --depth 1 https://github.com/user/repo.git  # 淺克隆
```

### 基本操作

```bash
# 查看狀態
git status

# 新增檔案到暫存區
git add file.txt           # 單一檔案
git add .                 # 所有更改
git add -p                # 互動式新增

# 提交
git commit -m "message"
git commit -am "message"  # add + commit（僅追蹤中的檔案）

# 查看歷史
git log
git log --oneline
git log -p file.txt       # 特定檔案歷史
git log --graph --oneline --all  # 圖形化
```

## 分支操作

```bash
# 列出分支
git branch                # 本地分支
git branch -r             # 遠端分支
git branch -a             # 所有分支

# 建立分支
git branch new-branch

# 切換分支
git checkout new-branch
git switch new-branch     # Git 2.23+

# 建立並切換
git checkout -b new-branch
git switch -c new-branch  # Git 2.23+

# 刪除分支
git branch -d branch-name
git branch -D branch-name  # 強制刪除
```

## 合併與 Rebase

```bash
# 合併分支
git merge branch-name

# 變基（Rebase）
git rebase main

# 解決衝突後繼續
git rebase --continue

# 取消變基
git rebase --abort
```

## 遠端操作

```bash
# 新增/移除遠端
git remote add origin https://github.com/user/repo.git
git remote remove origin

# 查看遠端
git remote -v

# 推送
git push origin main
git push -u origin main  # 設定上遊
git push --tags          # 推送標籤

# 拉取
git pull origin main     # fetch + merge
git fetch origin         # 僅獲取
git pull --rebase origin main  # fetch + rebase
```

## 標籤

```bash
# 建立標籤
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"

# 列出標籤
git tag
git tag -l "v1.*"

# 推送標籤
git push origin v1.0.0
git push origin --tags
```

## 結論

掌握這些常用命令可以應對日常開發的大部分場景。多練習是熟練 Git 的關鍵。

---

**延伸閱讀**

- [Git 進階技巧](focus6.md)
- [Git+commands+cheat+sheet](https://www.google.com/search?q=Git+commands+cheat+sheet)