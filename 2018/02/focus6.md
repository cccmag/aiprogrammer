# Git 進階技巧

## 簡介

掌握 Git 的進階技巧可以讓你更有效率地處理複雜的版本控制場景。

## Stash

### 基本用法

stash 就像一個臨時的儲物櫃，幫你保存未提交的修改：

```bash
# 儲存當前修改
git stash
git stash save "工作進度"

# 查看 stash 清單
git stash list
# stash@{0}: WIP on master: abc123 Initial commit
# stash@{1}: On feature: WIP

# 恢復最新 stash 並刪除
git stash pop

# 恢復最新 stash 但保留
git stash apply

# 恢復指定的 stash
git stash apply stash@{1}

# 刪除 stash
git stash drop stash@{0}

# 清除所有 stash
git stash clear
```

### 互動式 Stash

```bash
# 選擇性地 stash 部分檔案
git stash -p

# Stash 包括未追蹤檔案
git stash -u

# Stash 所有檔案
git stash -a
```

## Cherry-pick

選擇性地套用某個提交：

```bash
# 套用指定提交
git cherry-pick commit-id

# 套用並繼續（可能需要解決衝突）
git cherry-pick --continue

# 套用多個提交
git cherry-pick commit1 commit2 commit3

# 套用最後 3 個提交
git cherry-pick HEAD~3..HEAD

# 不要自動提交
git cherry-pick -n commit-id
```

應用場景：
- 將 hotfix 的提交套用到 release 分支
- 恢復誤刪的提交
- 在不同分支應用特定功能

## Reflog

記錄所有 HEAD 的移動：

```bash
# 查看 reflog
git reflog
# abc123 HEAD@{0}: commit: 新功能
# def456 HEAD@{1}: rebase finished: ...
# 789abc HEAD@{2}: checkout: moving to feature

# 恢復到之前的狀態
git checkout HEAD@{2}

# 恢復被刪除的分支
git checkout -b recovered-branch HEAD@{1}
```

## Reset 深入理解

```bash
# 三種模式
git reset --soft HEAD~1   # 移動 HEAD，保留 staging 和工作區
git reset --mixed HEAD~1  # 移動 HEAD，重置 staging（預設）
git reset --hard HEAD~1   # 移動 HEAD，重置 staging 和工作區（危險）
```

### 使用情境

```bash
# 取消錯誤的 commit，但保留修改
git reset --soft HEAD~1

# 取消 staging，重新準備提交
git reset HEAD filename.txt

# 完全放棄所有修改（危險！）
git reset --hard HEAD
```

## Bisect

二分搜尋找出問題的提交：

```bash
# 開始 bisect
git bisect start

# 標記當前為 bad
git bisect bad

# 標記一個已知好的版本
git bisect good v1.0.0

# Git 會 checkout 中間版本，測試後標記
git bisect good  # 或 git bisect bad

# 完成後回到原來分支
git bisect reset
```

自動化：
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run npm test
```

## Submodules

在 Git 倉庫中嵌入另一個倉庫：

```bash
# 新增 submodule
git submodule add https://github.com/user/repo.git path/to/submodule

# 克隆帶有 submodules 的倉庫
git clone --recursive https://github.com/user/repo.git

# 更新 submodule
git submodule update --remote

# 初始化 submodules（在 clone 後）
git submodule update --init
```

## Blame

查看檔案每行的最後修改：

```bash
git blame filename.txt
git blame -L 10,20 filename.txt  # 指定行數範圍
git blame --format="%h %an" filename.txt
```

## Grep

在 Git 歷史中搜尋：

```bash
git grep "搜尋內容"
git grep "搜尋內容" v1.0.0  # 在指定版本搜尋
git grep -n "搜尋內容"       # 顯示行號
git grep -c "搜尋內容"       # 統計出現次數
```

## Bundle

將倉庫打包：

```bash
# 建立 bundle
git bundle create repo.bundle HEAD master

# 從 bundle 克隆
git clone repo.bundle

# 增量 bundle
git bundle create updates.bundle master~10..master
```

## 練習題

1. 使用 stash 暫存工作進度，切換分支處理緊急任務
2. 使用 cherry-pick 將一個提交套用到另一個分支
3. 使用 bisect 找出問題的提交
4. 練習使用 reflog 恢復誤刪的提交