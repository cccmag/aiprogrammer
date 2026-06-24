# 版本控制的演化：從 RCS 到 Git

## 版本控制的起源

版本控制（Version Control）的概念始於 1980 年代。隨著軟體開發規模擴大，如何追蹤程式碼變更、協調多人合作成為重要課題。

## RCS：單一檔案版控

1982 年，Walter Tichy 開發了 RCS（Revision Control System）。RCS 是最早的版本控制系統之一，專門用於管理單一檔案。

### RCS 的運作原理

```bash
# RCS 基本操作
ci file.c      # 將檔案 check in（存入 RCS）
co file.c      # 將檔案 check out（取出）
rcs -l file.c  # 鎖定檔案（防止衝突）
```

RCS 的工作方式：
1. 每個原始檔案對應一個 `,v` 檔案
2. `,v` 檔案儲存所有版本的完整內容
3. 採用鎖定模式防止同時編輯

## CVS：多人協作的突破

1990 年，Dick Grune 發布了 CVS（Concurrent Versions System）。CVS 是第一個支援多人協作的版本控制系統。

### CVS 的創新

```
CVS 的突破：
─────────────
1. 客戶端-伺服器架構
2. 不需要鎖定檔案（merge 取代 lock）
3. 模組化專案管理
4. 網路存取支援
```

### CVS 基本操作

```bash
# CVS 基本操作
cvs checkout module     # 取出模組
cvs update              # 更新到最新
cvs commit              # 提交變更
cvs add file            # 新增檔案
cvs remove file         # 刪除檔案
```

### CVS 的問題

```bash
# CVS 的限制：
# 1. 沒有原子提交
# 2. 分支管理複雜
# 3. 重新命名/移動檔案支援差
# 4. 標籤/分支只是檔案副本
```

## Subversion：CVS 的改進

2004 年，CollabNet 發布了 Subversion（SVN），這是對 CVS 的重新設計。

### Subversion 的改進

```bash
# SVN 基本操作
svn checkout http://server/repo/trunk
svn update
svn commit -m "Fixed bug #123"
svn add newfile
svn delete oldfile
svn move oldname newname   # SVN 支援重新命名！
```

### SVN 的新特性

```
Subversion 的優勢：
─────────────────────
1. 原子提交 - 提交要么全部成功，要么全部失敗
2. 有效的重新命名支援
3. 中繼資料（properties）
4. 有效的分支和標籤（cp，不是檔案副本）
5. 差異儲存（節省空間）
6. 優異的效能
```

### SVN 的工作副本

```bash
# SVN 工作副本範例
$ ls -la
total 4.0K Jun 15 10:00 .
total 4.0K Jun 15 09:30 ..
drwxr-xr-x  Jun 15 10:00 ./..
drwxr-xr-x  Jun 15 10:00 .svn/    # SVN 管理目錄
-rw-r--r--  Jun 15 09:30  README
-rw-r--r--  Jun 15 09:30  Makefile
```

## BitKeeper：商業版控的嘗試

2000 年，BitMover 發布了 BitKeeper，這是第一個商業化的分散式版本控制系統。

Linux 核心開發在 2002-2005 年間使用了 BitKeeper。

### BitKeeper 的創新

```
BitKeeper 的貢獻：
─────────────────
1. 真正的分散式
2. 優異的效能
3. 免費開源專案使用
```

### 授權爭議

2005 年，BitMover 終止了 Linux 核心的免費使用許可。這直接促成了 Git 的誕生。

## Git 的誕生

2005 年 4 月，Linus Torvalds 宣佈開發 Git，一個新的版本控制系統。

### Linus 的設計原則

Linus Torvalds 對 Git 的期望：
- 速度
- 簡單設計
- 強力支援非線性開發（分支和歸併）
- 完全分散式
- 能夠有效處理大型專案（如 Linux 核心，數萬個檔案）

### Git 與其他系統的比較

```
Git vs 其他版本控制系統：
────────────────────────────────────────────────────────
特性          Git        SVN       CVS       BitKeeper
────────────────────────────────────────────────────────
分散式        ✓         ✗         ✗         ✓
分支/歸併     優秀       一般       差        優秀
效能          極快       快        慢        快
學習曲線      高        低        低        中
完整歷史      ✓         ✗（需伺服器）✗       ✓
原子提交      ✓         ✓         ✗         ✓
────────────────────────────────────────────────────────
```

## 結語

版本控制的演化反映了軟體開發的變化：

- **1980s**：單一開發者、單一檔案
- **1990s**：團隊合作、集中式管理
- **2000s**：分散式開發、網路協作
- **2005+**：分散式版本控制時代

Git 的出現標誌著一個新時代的開始——真正的分散式版本控制。

---

## 延伸閱讀

- [RCS+CVS+version+control+history](https://www.google.com/search?q=RCS+CVS+version+control+history)
- [Git+creation+Linus+Torvalds+2005](https://www.google.com/search?q=Git+creation+Linus+Torvalds+2005)
- [Subversion+history+2004](https://www.google.com/search?q=Subversion+history+2004)

---

*本篇文章為「AI 程式人雜誌 2007 年 6 月號」本期焦點系列之一。*