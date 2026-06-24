#!/bin/bash
# Git 工作流程示範腳本

set -x

# 初始化倉庫
rm -rf demo && mkdir demo && cd demo
git init

# 設定使用者
git config user.name "Demo User"
git config user.email "demo@example.com"

# 建立初始檔案
echo "# 我的專案" > README.md
git add README.md
git commit -m "Initial commit"

# 建立 develop 分支
git checkout -b develop
echo "開始開發" > dev.txt
git add dev.txt
git commit -m "feat: 新增開發檔案"

# 建立 feature 分支
git checkout -b feature/new-feature develop
echo "新功能實作" > feature.txt
git add feature.txt
git commit -m "feat: 新功能第一版"

# 修改並提交
echo "更多功能" >> feature.txt
git add feature.txt
git commit -m "feat: 新增功能細節"

# 切回 develop 並合併
git checkout develop
git merge --no-ff feature/new-feature -m "merge: 合併新功能"

# 建立 release 分支
git checkout -b release/1.0.0
echo "1.0.0" > version.txt
git add version.txt
git commit -m "chore: 版本更新至 1.0.0"

# 合併到 main
git checkout main
git merge --no-ff release/1.0.0 -m "merge: 發布版本 1.0.0"
git tag -a v1.0.0 -m "版本 1.0.0"

# 顯示最終分支狀態
echo "=== 分支狀態 ==="
git branch -a

echo "=== 提交歷史 ==="
git log --oneline --graph --all

echo "工作流程完成"
cd ..
rm -rf demo