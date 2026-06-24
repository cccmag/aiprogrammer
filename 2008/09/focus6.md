# Git 進階技巧

## Stash（儲藏）

### 基本用法

```bash
# 儲藏當前更改
git stash
git stash save "message"

# 列出儲藏
git stash list

# 應用儲藏（保留副本）
git stash apply
git stash apply stash@{0}

# 應用並刪除
git stash pop
```

### 互動式儲藏

```bash
# 僅儲藏部分更改
git stash -p

# 從儲藏建立分支
git stash branch new-branch
```

## Bisect（二分搜尋）

### 找bug

```bash
# 開始二分搜尋
git bisect start

# 標記壞的提交
git bisect bad

# 標記好的提交
git bisect good v1.0.0

# Git 自動 checkout 中間版本
# 測試後標記好或壞
git bisect good  # 或 git bisect bad

# 重複直到找到問題提交
# 結束搜尋
git bisect reset
```

### 自動化

```bash
# 自動化二分搜尋
git bisect start
git bisect bad HEAD
git bisect good v1.0.0

# 執行測試腳本
git bisect run ./test.sh
```

## Cherry-pick

### 選擇性合併

```bash
# 選擇單一提交應用
git cherry-pick commit-hash

# 選擇多個提交
git cherry-pick hash1 hash2 hash3

# 選擇範圍
git cherry-pick start..end

# 繼續 cherry-pick
git cherry-pick --continue

# 取消 cherry-pick
git cherry-pick --abort
```

## Reset 與 Restore

### 三種模式

```bash
# 軟重置（保留更改在暫存區）
git reset --soft HEAD~1

# 混合重置（保留更改在工作目錄）
git reset --mixed HEAD~1
git reset HEAD~1  # 預設

# 硬重置（丟棄更改）
git reset --hard HEAD~1
```

### Restore（Git 2.23+）

```bash
# 恢復檔案到上次提交
git restore file.txt

# 恢復到特定版本
git restore --source=HEAD~1 file.txt

# 恢復暫存區
git restore --staged file.txt
```

## Reflog

### 恢復遺失的提交

```bash
# 查看所有操作歷史
git reflog

# 恢復到特定狀態
git checkout HEAD@{2}

# 恢復分支
git reset --hard HEAD@{5}
```

## 子模組

### 管理依賴

```bash
# 新增子模組
git submodule add https://github.com/user/repo.git path/to/submodule

# 初始化子模組
git submodule init

# 更新子模組
git submodule update

# 克隆含子模組的倉庫
git clone --recurse-submodules URL
```

## 結論

這些進階技巧可以幫助你更高效地處理複雜的 Git 情境。

---

**延伸閱讀**

- [常用 Git 命令詳解](focus5.md)
- [Git+advanced+技巧](https://www.google.com/search?q=Git+advanced+tips+tricks)