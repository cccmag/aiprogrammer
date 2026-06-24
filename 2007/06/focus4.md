# 分散式版本控制的概念：DVCS 的優勢

## 分散式版本控制的設計

分散式版本控制系統（DVCS）每個客戶端都有完整的倉庫副本，包括所有歷史記錄。

```
分散式版本控制架構：
──────────────────────

    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ Client 1│     │ Client 2│     │ Client 3│
    │ (完整的)│     │ (完整的)│     │ (完整的)│
    │ 倉庫    │     │ 倉庫    │     │ 倉庫    │
    └───┬─────┘     └───┬─────┘     └───┬─────┘
        │                │                │
        │   pull/push    │                │
        └────────────────┼────────────────┘
                         │
                 ┌───────┴───────┐
                 │  共享伺服器    │
                 │（可選，純供備份）│
                 └───────────────┘
```

## Git 的分散式特性

### 每個客戶端都有完整歷史

```bash
# Git 克隆後本地有完整歷史
ls .git

# 離線可做的操作
git log               # 查看歷史
git diff              # 比較版本
git branch            # 建立分支
git commit            # 提交（本地）
git merge             # 合併（本地）
git blame             # 查看修改者
```

### 與 SVN 的對比

```bash
# SVN 需要網路的操作
svn commit            # 需要網路
svn log                # 需要網路（默認）
svn update             # 需要網路

# Git 離線可做幾乎所有操作
git commit             # 本地
git log                # 本地
git diff               # 本地
git branch             # 本地
git merge              # 本地
git blame              # 本地
git push               # 需要網路（推送）
git pull               # 需要網路（拉取）
```

## DVCS 的優勢

### 1. 真正的離線開發

```bash
# 在飛機上開發（完全離線）
git add .
git commit -m "WIP: Feature implementation"
git commit -m "Continue work"
git commit -m "Complete feature"

# 落地後同步
git push origin master
```

### 2. 快速的操作

```bash
# 本地操作（毫秒級）
time git status        # ~10ms
time git commit        # ~50ms
time git log           # ~20ms

# SVN 操作（秒級）
time svn status        # ~1-2s
time svn commit        # ~2-3s
time svn log           # ~1-2s
```

### 3. 強大的分支能力

```bash
# Git 分支是輕量級的
git branch feature1
git checkout feature1

# 開發完成後合併
git checkout master
git merge feature1

# 合併後可刪除分支
git branch -d feature1
```

### 4. 靈活的工作流

```bash
# 多种工作流
# 1. 集中式（像 SVN）
git push origin master

# 2. 整合管理員模式
git pull-request

# 3.  dictatorial（Linux 核心模式）
#    副手審查 → 整合者審查 → 主線
```

## DVCS 的挑戰

### 1. 學習曲線

```bash
# Git 的概念比 SVN 複雜
git reset              # 三種模式
git rebase            # 可能造成問題
git reflog            # 需要理解
.gitignore            # 需要手動管理
```

### 2. 權限控制

```bash
# Git 原生不支援精細的目錄權限
# 需要外部工具
gitolite             # SSH 層級權限
Gitosis              # 早期方案
```

### 3. 大型檔案

```bash
# Git 對大型二進制檔案不友好
# 解決方案
git lfs              # Large File Storage
```

## Mercurial：另一個 DVCS 選擇

2007 年，Mercurial 是 Git 的主要競爭對手。

### Mercurial 的特點

```bash
# Mercurial 命令
hg init
hg clone
hg add
hg commit
hg push
hg pull

# 與 Git 概念對應
# Mercurial  vs Git
# repo       vs .git
# changeset  vs commit
# revision   vs SHA-1 hash
# branch     vs branch
# head       vs HEAD
```

### Git vs Mercurial

```
Git vs Mercurial：
──────────────────────────────────────────────────
特性          Git          Mercurial
──────────────────────────────────────────────────
速度          極快         很快
學習曲線      較陡         較平緩
Windows 支援  一般（現在很好）更好
社群          更大         較小
大型專案      優秀         優秀
──────────────────────────────────────────────────
```

## 結語

分散式版本控制代表了版本控制的未來。Git 雖然學習曲線較陡，但其強大的功能和靈活性使其成為 2007 年後的首選工具。

選擇 DVCS 的理由：
1. 離線工作能力
2. 快速的本地操作
3. 強大的分支和歸併
4. 靈活的工作流支援

---

## 延伸閱讀

- [distributed+version+control+Git+Mercurial](https://www.google.com/search?q=distributed+version+control+Git+Mercurial)
- [DVCS+advantages+2007](https://www.google.com/search?q=DVCS+advantages+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 6 月號」本期焦點系列之一。*