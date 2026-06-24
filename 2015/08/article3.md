# Git 與 Linux 的完美結合

## 前言

對於 Linux 開發者來說，Git 是不可或缺的工具。本 文探討如何有效地在 Linux 環境中使用 Git。

---

## Linux 上安裝 Git

### 主流發行版

```bash
# Debian/Ubuntu
sudo apt-get install git

# Fedora
sudo yum install git

# Arch Linux
sudo pacman -S git

# openSUSE
sudo zypper install git
```

### 從原始碼編譯

```bash
# 安裝依賴
sudo apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev

# 下載並編譯
wget https://github.com/git/git/archive/v2.4.0.tar.gz
tar -xzf v2.4.0.tar.gz
cd git-2.4.0
make prefix=/usr/local all
sudo make prefix=/usr/local install
```

---

## 基本 Git 操作

### 初始化與設定

```bash
# 初始化
git init

# 設定
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 設定編輯器
git config --global core.editor vim
```

### 日常工作流程

```bash
git status
git add .
git commit -m "message"
git push origin main
```

---

## SSH 金鑰設定

```bash
# 產生金鑰
ssh-keygen -t rsa -b 4096 -C "your@email.com"

# 複製公鑰
cat ~/.ssh/id_rsa.pub

# 測試連線
ssh -T git@github.com
```

---

## 與 GitHub 整合

### SSH 設定

```bash
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa
```

### 推送現有專案

```bash
git remote add origin git@github.com:user/repo.git
git push -u origin main
```

---

## 實用別名

```bash
# ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    df = diff
    lg = log --oneline --graph --all
    last = log -1 HEAD
    unstage = reset HEAD --
```

使用方式：

```bash
git st
git lg
```

---

## Git 在遠端伺服器

### 裸倉庫

```bash
# 在伺服器上建立裸倉庫
git init --bare /srv/repo.git

# 本地端推送
git remote add origin ssh://user@server/srv/repo.git
git push -u origin main
```

### Gitolite

輕量級 Git 閘道器：

```bash
# 安裝
git clone https://github.com/sitaramc/gitolite.git
cd gitolite
./install -to /usr/local
```

設定管理員：

```bash
# 在客戶端
gitolite setup -pk admin.pub
```

---

## CI/CD 整合

### Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
set -e
npm test

# .git/hooks/post-receive
#!/bin/bash
git --work-tree=/var/www checkout -f
```

### Jenkins Git 整合

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/user/repo.git'
            }
        }
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
    }
}
```

[搜尋 Jenkins Git plugin](https://www.google.com/search?q=Jenkins+Git+plugin)

---

## 小結

Git 是 Linux 開發者的必備技能，熟練掌握 Git 能大幅提升開發效率。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Pro Git 書籍](https://git-scm.com/book/zh-tw/v2)
- [Git 官方網站](https://git-scm.com/)