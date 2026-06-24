# Git 高級操作：Rebase 與 Bisect

## 前言

掌握 Git 高級操作可以大幅提升開發效率。

## Rebase

```bash
# 將 feature 分支 rebase 到 main
git checkout feature
git rebase main

# 互動式 rebase
git rebase -i HEAD~3
# 支援 squash、fixup、reorder 等操作
```

## Bisect

```bash
# 二分查找找到 bug 引進的 commit
git bisect start
git bisect bad  # 當前版本有 bug
git bisect good v1.0  # 已知好的版本

# Git 會自動 checkout 中間版本
# 測試後標記
git bisect good  # 或 git bisect bad

# 完成後回到原分支
git bisect reset
```

## 延伸閱讀

- [Git 高級操作指南](https://www.google.com/search?q=git+rebase+bisect+tutorial)