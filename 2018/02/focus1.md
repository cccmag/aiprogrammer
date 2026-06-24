# Git 基礎概念

## 簡介

Git 是由 Linus Torvalds 於 2005 年開發的分散式版本控制系統，目前由 Junio Hamano 維護。Git 設計初衷是為了管理 Linux 核心開發，現已成為全球最廣泛使用的版本控制工具。

## 核心思想

### 快照 vs 差異

Git 採用快照（snapshot）方式记录版本，而非像 SVN 那样存储差異。這使得 Git 的分支操作非常快速。

```
SVN: 儲存差異
v1 → diff(v1,v2) → diff(v1,v3)
     ↑_________________|

Git: 儲存快照
v1: [snapshot A]
v2: [snapshot B] → 指向 A
v3: [snapshot C] → 指向 B
```

### 分散式架構

每個開發者都有完整的本地倉庫，包含所有歷史記錄。這使得離線工作成為可能。

```
開發者 A (本地) ←→ GitHub (遠端)
    ↕完整副本           ↕完整副本
開發者 B (本地)
```

## 基本概念

### 三棵樹（Three Trees）

Git 使用三棵樹來管理檔案：

1. **Working Directory** - 工作目錄，你在編輯檔案的地方
2. **Staging Area (Index)** - 暫存區，準備提交的文件列表
3. **HEAD** - 指向最新提交的指標

### 檔案狀態

```bash
# Git 追蹤的檔案有四種狀態

Untracked (未追蹤)
  └── 新檔案，Git 尚未開始追蹤

Modified (已修改)
  └── 已追蹤的檔案被修改，但未暫存

Staged (已暫存)
  └── 將修改的檔案加入到暫存區

Committed (已提交)
  └── 已提交到本地倉庫的檔案
```

### Git 的四大物件

1. **Blob** - 儲存檔案內容
2. **Tree** - 儲存目錄結構與檔案列表
3. **Commit** - 儲存版本快照與元數據
4. **Tag** - 給 commit 起的別名

```
Commit 物件
├── tree (指向目錄結構)
├── parent (指向上一個 commit)
├── author (作者資訊)
└── committer (提交者資訊)
```

## Git 安裝與設定

### 安裝

```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git

# Windows
# 下載安裝程式: https://git-scm.com/download/win
```

### 基本設定

```bash
# 設定使用者名稱與郵箱
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 設定預設編輯器
git config --global core.editor vim

# 設定別名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

### 查詢設定

```bash
git config --list
git config user.name
```

## 創建倉庫

### 初始化新倉庫

```bash
# 在當前目錄初始化
git init

# 在指定目錄初始化
git init myproject
```

### 複製現有倉庫

```bash
# 複製 GitHub 倉庫
git clone https://github.com/username/repository.git

# 複製到指定資料夾
git clone https://github.com/username/repository.git myfolder

# 淺層複製（只複製最新版本）
git clone --depth 1 https://github.com/username/repository.git
```

## 基礎工作流程

```bash
# 1. 查看狀態
git status

# 2. 新增檔案到暫存區
git add filename.txt
git add .              # 新增所有更動

# 3. 提交到本地倉庫
git commit -m "Initial commit"

# 4. 查看提交歷史
git log

# 5. 推送到遠端（如果有的話）
git push origin master
```

## .gitignore 檔案

指定 Git 忽略的檔案：

```
# 註解
*.log              # 忽略所有 .log 檔案
build/             # 忽略 build 目錄
.env               # 忽略 .env 檔案
node_modules/      # 忽略依賴目錄
```

## 練習題

1. 安裝 Git 並設定使用者資訊
2. 創建一個新專案並初始化 Git 倉庫
3. 練習基本的 add、commit、status、log 指令