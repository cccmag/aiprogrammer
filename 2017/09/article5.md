# 版本控制 Git

## 基本操作

```bash
git init                 # 初始化
git clone <url>         # 複製
git status              # 查看狀態
git add <file>          # 暫存
git commit -m "message" # 提交
git log                 # 歷史
```

## 分支

```bash
git branch              # 列出分支
git branch <name>       # 建立分支
git checkout <branch>  # 切換
git checkout -b <new>   # 建立並切換
git merge <branch>      # 合併
git branch -d <branch>  # 刪除
```

## 遠端

```bash
git remote add origin <url>
git push -u origin master
git pull origin master
git fetch origin
```

## 復原

```bash
git checkout -- <file>    # 丟棄修改
git reset HEAD <file>      # 取消暫存
git revert <commit>        # 復原提交
git reset --soft HEAD~1   # 取消上次提交
```

## 衝突

解決衝突：
1. 編輯衝突檔案
2. git add <file>
3. git commit

## 總結

Git 是必備的版本控制工具。掌握基本操作與分支管理能大幅提升開發效率。