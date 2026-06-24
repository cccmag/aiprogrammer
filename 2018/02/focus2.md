# Git 常用指令

## 簡介

掌握 Git 的常用指令是每個開發者的必備技能。本篇介紹日常開發中最常用的 Git 指令。

## 基本指令

### git init

初始化新的 Git 倉庫：

```bash
git init
git init myproject
```

### git clone

複製現有倉庫：

```bash
git clone https://github.com/username/repo.git
git clone --depth 1 https://github.com/username/repo.git  # 淺克隆
```

### git status

查看倉庫狀態：

```bash
git status
git status -s  # 簡短格式
```

輸出含義：
- `A` - 新增的檔案（Staged）
- `M` - 修改的檔案（Modified）
- `D` - 刪除的檔案（Deleted）
- `??` - 未追蹤的檔案（Untracked）

## 暫存與提交

### git add

新增檔案到暫存區：

```bash
git add filename.txt          # 新增單一檔案
git add .                     # 新增所有更動
git add -A                    # 新增所有更動（包括刪除）
git add -p                    # 互動式新增（可選擇部分更動）
```

### git commit

提交暫存的更動：

```bash
git commit -m "提交訊息"
git commit -am "訊息"         # 直接提交所有已追蹤檔案的更動（不含新檔案）
git commit --amend           # 修改最後一次提交
```

提交訊息規範：

```
feat: 新功能
fix: 修正錯誤
docs: 文件更新
style: 格式調整
refactor: 重構
test: 測試相關
chore: 建構/工具相關
```

### git rm

刪除檔案：

```bash
git rm filename.txt          # 刪除檔案並暫存
git rm --cached filename.txt # 從追蹤中移除（但保留檔案）
git rm -r directory/         # 刪除目錄
```

## 查看歷史

### git log

查看提交歷史：

```bash
git log
git log --oneline            # 精簡格式
git log --graph              # 圖形化顯示
git log -n 5                 # 只顯示最後 5 筆
git log --author="name"      # 篩選作者
git log --since="2 weeks ago" # 時間範圍
git log --all                # 所有分支
```

### git show

查看特定提交的內容：

```bash
git show commit-id
git show --stat commit-id    # 只顯示變更統計
```

### git diff

查看變更：

```bash
git diff                     # 工作區 vs 暫存區
git diff --staged            # 暫存區 vs HEAD
git diff HEAD~1              # 與上一次提交比較
git diff branch1..branch2    # 兩個分支間的差異
```

## 復原操作

### git checkout / git restore

復原檔案：

```bash
# 從暫存區取回（取消暫存）
git restore --staged filename.txt
git reset HEAD filename.txt   # 舊語法

# 從 HEAD 取回（取消修改）
git restore filename.txt
git checkout -- filename.txt # 舊語法
```

### git reset

回退版本：

```bash
git reset --soft HEAD~1      # 保留修改在暫存區
git reset --mixed HEAD~1     # 保留修改在工作區（預設）
git reset --hard HEAD~1      # 刪除所有修改（危險！）
```

### git revert

反轉提交（安全的回退）：

```bash
git revert commit-id          # 建立新提交來反轉指定提交
```

## 遠端操作

### git remote

管理遠端倉庫：

```bash
git remote -v                # 查看已設定的遠端
git remote add origin url    # 新增遠端
git remote remove origin     # 移除遠端
git remote rename origin upstream # 重新命名
```

### git fetch

获取遠端更新（不下載）：

```bash
git fetch origin
git fetch --all
```

### git pull

获取並合併遠端更新：

```bash
git pull                    # 相当于 git fetch + git merge
git pull --rebase           # 使用 rebase 代替 merge
```

### git push

推送提交到遠端：

```bash
git push origin master
git push -u origin feature   # 首次推送並設定上游
git push --force            # 強制推送（危險！）
```

## 標籤管理

### git tag

管理標籤：

```bash
git tag                     # 列出標籤
git tag v1.0.0              # 建立輕量標籤
git tag -a v1.0.0 -m "版本 1.0.0"  # 建立註釋標籤
git tag -a v1.0.0 commit-id # 為舊提交建立標籤
git push origin v1.0.0      # 推送標籤
git push origin --tags      # 推送所有標籤
```

## 練習題

1. 創建一個 Git 倉庫並練習基本的 add、commit 流程
2. 使用 git log 查看提交歷史
3. 學會使用 git diff 比較變更
4. 練習使用 git reset 回退版本