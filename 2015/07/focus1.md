# Git 基礎概念

Git 是一個分散式版本控制系統，由 Linus Torvalds 於 2005 年開發。與早期的集中式版本控制系統（如 CVS、SVN）不同，Git 每個克隆都是完整的倉庫副本，包含完整的歷史記錄。

---

## 安裝 Git

### macOS

```bash
# 使用 Homebrew 安裝
brew install git

# 或使用 Xcode Command Line Tools
xcode-select --install
```

### Linux

```bash
# Debian/Ubuntu
sudo apt-get install git

# Fedora
sudo yum install git
```

### Windows

從 [git-scm.com](https://git-scm.com/download/win) 下載安裝程式，或使用 [Git for Windows](https://gitforwindows.org/)。

---

## 基本設定

安裝完成後，需要設定使用者名稱和電子郵件：

```bash
git config --global user.name "你的名稱"
git config --global user.email "your.email@example.com"
```

其他實用的設定：

```bash
# 設定預設編輯器
git config --global core.editor vim

# 設定别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --all"

# 設定預設分支名稱
git config --global init.defaultBranch main
```

---

## 建立倉庫

### 初始化新倉庫

```bash
mkdir my-project
cd my-project
git init
```

執行 `git init` 後，Git 會在目錄中建立 `.git` 子目錄，這是 Git 存放所有版本資訊的地方。

### 克隆現有倉庫

```bash
# 克隆公開倉庫
git clone https://github.com/torvalds/linux.git

# 深度克隆（只下載最新版本）
git clone --depth 1 https://github.com/torvalds/linux.git

# 克隆特定分支
git clone -b develop https://github.com/user/repo.git
```

---

## 基本操作

### 檢視狀態

```bash
git status
```

這會顯示：
- 當前所在分支
- 追蹤中的檔案變更
- 未追蹤的新檔案
- 準備提交的變更

### 暫存檔案

```bash
# 暫存特定檔案
git add filename.txt

# 暫存所有變更
git add .

# 暫存所有已追蹤檔案的變更
git add -u
```

### 提交變更

```bash
git commit -m "提交訊息"
```

### 檢視歷史

```bash
# 簡潔格式
git log --oneline

# 圖形化顯示分支
git log --graph --oneline --all

# 顯示變更統計
git log --stat
```

---

## 忽略檔案

建立 `.gitignore` 檔案來排除不需要追蹤的檔案：

```
# 編譯產物
*.o
*.class
*.pyc

# 依賴目錄
node_modules/
__pycache__/

# 環境設定
.env
*.log

# 系統檔案
.DS_Store
Thumbs.db
```

---

## 比較差異

```bash
# 查看工作區變更
git diff

# 查看已暫存變更
git diff --staged

# 比較兩個分支
git diff main..develop
```

---

## 小結

本章介紹了 Git 的基本概念和操作，包括安裝、初始化、克隆、基本的暫存和提交操作。這些是使用 Git 的基礎，在後續章節中我們將深入探討分支、合併等進階主題。

---

*作者：AI 程式人團隊*