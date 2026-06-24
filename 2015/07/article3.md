# 大型專案的 Git 實踐

## 前言

Linux Kernel 是使用 Git 管理的大型專案代表，其經驗值得學習。

---

## Linux Kernel 的 Git 使用

### 規模

- 超過 2,500 萬行程式碼
- 超過 17,000 位貢獻者
- 每年數萬次提交

### 分支模式

Linus Torvalds 維護主倉庫，使用 subsystem maintainer 模型。

```bash
# 克隆 Linux Kernel
git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

# 查看穩定版本
git branch -a | grep stable
```

---

## 效能優化

### SHA-1 加速

Git 使用硬連結和快取加速大型倉庫操作。

### Pack Files

```bash
# 查看 pack files
ls .git/objects/pack/

# 手动打包
git gc --aggressive
```

### Partial Clone

```bash
# 只克隆最近的历史
git clone --depth 1 https://github.com/torvalds/linux.git

# 懶惰加載大檔案
git clone --filter=blob:none https://github.com/torvalds/linux.git
```

---

## 大型專案最佳實踐

### 1. 明確的分支策略

```
main          - 穩定版本
next          - 下一版本整合
linux-next    - 明日合併測試
```

### 2. 自動化測試

```bash
# kernelci.org
# 自動化建置和測試
```

### 3. 簽核政策

```bash
# 使用 GPG 簽名
git tag -s v4.0 -m "Linux 4.0"
git push --signed origin main
```

---

## 案例研究：Git Kernel

### 提交規範

```
[PATCH] subsystem: brief description

Detailed explanation if needed.

Signed-off-by: Name <email>
```

### 審查流程

1. 開發者發送 patch 到 mailing list
2. Maintainer 審查並測試
3. 通過後合併到 subsystem 分支
4. 定期同步到 main 分支

[搜尋 Linux Kernel development workflow](https://www.google.com/search?q=Linux+Kernel+Git+development+workflow)

---

## 工具推薦

### git-bisect

定位問題提交：

```bash
git bisect start
git bisect bad
git bisect good v4.0
# 自動化測試
git bisect run make test
```

### git-blame

查看程式碼歷史：

```bash
git blame kernel/sched/core.c | head -30
```

---

## 大型企業案例

### Google

使用 Git 的内部定制品 Piper。

### Microsoft

Windows 開發使用 Git GVFS (Git Virtual File System)。

---

## 小結

大型專案需要謹慎的流程、先進的工具和嚴格的紀律。Git 提供了足夠的靈活性來適應不同需求。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Linux Kernel Git repository](https://git.kernel.org/)
- [KernelNewbies Git 指南](https://www.google.com/search?q=KernelNewbies+Git+guide)