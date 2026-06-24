# 從 CVS 到 Git：版本控制演進史

## 前言

版本控制系統的發展反映了軟體工程的進步。讓我們回顧這段歷史。

---

## 1970 年代：SCCS

Source Code Control System (SCCS) 由 Marc Rochkind 於 1972 年在 IBM 開發。

**特點：**
- 只能追蹤單一檔案
- 使用鎖定模式
- 只儲存差異

---

## 1980 年代：RCS

Revision Control System (RCS) 由 Walter Tichy 於 1985 年發布。

**改進：**
- 可以一次管理多個檔案
- 本地端操作
- 更好的差異儲存

---

## 1990 年代：CVS

Concurrent Versions System (CVS) 於 1986 年開始開發，1990 年發布。

**創新：**
- 用戶端/伺服器架構
- 網路操作支援
- 多人協作

**限制：**
- 不支援原子提交
- 不可重命名/移動檔案
- 分支操作困難

---

## 2000 年代：SVN

Apache Subversion (SVN) 由 CollabNet 於 2000 年發布。

**改進：**
- 原子提交
- 完整目錄版本化
- 更好的效能

**範例：**

```bash
svn checkout http://svn.example.com/repo
svn commit -m "提交訊息"
svn update
svn diff -r HEAD
```

---

## 2005 年：Git 誕生

Linus Torvalds 因為 BitKeeper 授權問題，決定自己開發 Git。

**設計目標：**
- 速度
- 簡單設計
- 強力支援非線性開發
- 完全分散式
- 處理大型專案（如 Linux Kernel）

[搜尋 Linus Torvalds Git history](https://www.google.com/search?q=Linus+Torvalds+Git+history+2005)

---

## Git 的創新

### 內容定址

Git 使用 SHA-1 哈希作為物件 ID，確保完整性：

```bash
$ git hash-object file.txt
3b18e512dba79e4c8300dd08aeb37f8e728b8dad
```

### Snapshots, not diffs

Git 儲存完整檔案快照，而非差異。

### 區域性

几乎所有操作都在本地執行，無需網路。

---

## 其他現代系統

### Mercurial

與 Git 类似的分散式系統，Python 編寫。

### Fossil

整合了 wiki、bug 追蹤的版本控制系統。

### Perforce

大型企業常用的集中式系統。

---

## 版本控制未來

版本控制持續演化：
- Git 2.4+ 的效能優化
- Git LFS (Large File Storage)
- 與容器技術的整合

---

## 結論

從 SCCS 到 Git，版本控制系統的演進體現了對更好協作工具的追求。理解這些歷史能幫助我們更好地使用現有工具。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Git 官方網站 - History](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Pro Git 書籍](https://git-scm.com/book/zh-tw/v2)