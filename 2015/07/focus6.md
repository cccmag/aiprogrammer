# 進階 Git 技巧

本章介紹一些實用的進階 Git 技巧。

---

## Stash

Stash 讓你暫存目前的變更，稍後再恢復：

```bash
# 暫存變更
git stash
git stash save "work in progress"

# 查看暫存清單
git stash list

# 恢復最近的暫存
git stash pop

# 恢復特定暫存
git stash apply stash@{0}

# 刪除暫存
git stash drop stash@{0}

# 暫存包括未追蹤檔案
git stash -u
```

---

## Rebase 進階

### 互動式 rebase

```bash
# 修改最近 3 個提交
git rebase -i HEAD~3
```

可用的指令：
- `pick` - 使用該提交
- `reword` - 修改提交訊息
- `edit` - 暂停以修改
- `squash` - 與前一個合併
- `fixup` - 拋棄提交訊息
- `drop` - 刪除提交

### 變基於遠端分支

```bash
git rebase upstream/main
```

### 解決 rebase 衝突

```bash
# 標記解決後繼續
git add resolved-file.txt
git rebase --continue

# 放棄 rebase
git rebase --abort
```

---

## Reflog

Reflog 記錄所有 HEAD 的變動：

```bash
# 查看 reflog
git reflog

# 恢复到之前的狀態
git checkout HEAD@{5}
git reset --hard HEAD@{5}
```

---

## Bisect

二分查找定位問題提交：

```bash
# 開始二分
git bisect start

# 標記當前為壞的
git bisect bad

# 標記好的版本
git bisect good v1.0

# Git 會自動 checkout 中間版本
# 測試後標記
git bisect good  # 或 git bisect bad

# 重複直到找到
git bisect reset
```

自動化：

```bash
git bisect start
git bisect bad
git bisect good v1.0
git bisect run make test
```

---

## Submodules

在一個倉庫中嵌入另一個倉庫：

```bash
# 新增 submodule
git submodule add https://github.com/user/lib.git libs/lib

# 克隆含 submodules 的倉庫
git clone --recursive https://github.com/user/project.git

# 更新 submodule
git submodule update --remote libs/lib

# 初始化 submodules
git submodule update --init --recursive
```

---

## Subtrees

另一種依賴管理方式：

```bash
# 新增 subtree
git subtree add --prefix=libs/lib https://github.com/user/lib.git main

# 更新 subtree
git subtree pull --prefix=libs/lib https://github.com/user/lib.git main
```

---

## Blame

查看檔案每行的最後修改：

```bash
git blame filename.txt
git blame -L 10,20 filename.txt  # 指定範圍
```

---

## Archive

打包倉庫：

```bash
# 打包成 zip
git archive -o snapshot.zip HEAD

# 打包特定分支
git archive -o snapshot.tar main
```

---

## 小結

這些進階技巧能幫助你更有效率地使用 Git，解決複雜的版本控制問題。

---

*作者：AI 程式人團隊*