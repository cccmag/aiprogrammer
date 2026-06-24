# Subversion 與 CVS：集中式版本控制

## 集中式版本控制的設計

集中式版本控制系統（CVCS）使用單一伺服器儲存所有版本歷史，客戶端從伺服器取得最新檔案。

```
集中式版本控制架構：
──────────────────────
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Client 1 │     │ Client 2 │     │ Client 3 │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     └────────────────┼────────────────┘
                      │
              ┌───────┴───────┐
              │   伺服器       │
              │  （單一真相）  │
              │  /svn/repo    │
              └───────────────┘
```

## Subversion 的優勢

### 相對於 CVS 的改進

```bash
# SVN vs CVS 比較

# CVS：提交只影响单个文件
cvs commit file.c

# SVN：提交是原子操作（所有檔案同時更新）
svn commit -m "Fix multiple files"
```

### SVN 的分支和標籤

```bash
# SVN 使用「拷貝」建立分支
svn copy http://server/repo/trunk \
        http://server/repo/branches/feature \
        -m "Create feature branch"

# SVN 標籤
svn copy http://server/repo/trunk \
        http://server/repo/tags/v1.0 \
        -m "Tag v1.0"
```

### SVN 的中繼資料

```bash
# SVN 支援自訂屬性
svn propset svn:keywords "Id Author Date" file.txt

# 自動替換關鍵字
# $Id$ -> $Id: file.txt 123 2007-06-15 10:00:00Z john $
```

## CVS 的特點

### CVS 的工作方式

```bash
# CVS 仓库結構
$CVSROOT/
├── module1/
│   ├── file1.c,v
│   └── file2.c,v
└── module2/
    └── file3.c,v

# CVS 模組定義
# modules 檔案定義模組別名
```

### CVS 的標籤和分支

```bash
# CVS 標籤
cvs tag v1_0 file.c

# CVS 分支
cvs tag -b release-1.0 file.c

# 在分支上開發
cvs checkout -r release-1.0 module
```

## CVS 的問題

### CVS 的限制

```
CVS 的主要問題：
───────────────────
1. 無法重新命名檔案（只是 delete + add）
2. 無原子提交（每個檔案單獨 commit）
3. 二進制檔案處理差（沒有差異儲存）
4. 分支合併困難
5. 沒有版本化的中繼資料
6. 速度慢（網路往返多）
```

## SVN 的企業採用

### 典型企業設定

```bash
# SVN 伺服器設定（Apache + mod_dav_svn）
# /etc/apache2/mods-available/dav_svn.conf

<Location /svn>
    DAV svn
    SVNPath /var/lib/svn
    AuthType Basic
    AuthName "Subversion Repository"
    AuthUserFile /etc/apache2/dav_svn.passwd
    Require valid-user
</Location>
```

### SVN 鉤子

```bash
# pre-commit 鉤子
#!/bin/bash
REPOS="$1"
TXN="$2"

# 檢查提交訊息格式
LOG_MSG=`svnlook log -t "$TXN" "$REPOS" | grep "[a-zA-Z0-9]" | wc -c`
if [ "$LOG_MSG" -lt 5 ]; then
    echo "提交訊息至少需要 5 個字元" >&2
    exit 1
fi

exit 0
```

## Git 與 SVN 的比較

### 工作流程

```bash
# SVN 工作流
svn checkout http://server/repo
svn update
svn add newfile
svn commit -m "Message"

# Git 工作流
git clone git://server/repo.git
git add newfile
git commit -m "Message"
git push origin master
```

### 離線能力

```
Git vs SVN 離線能力：
─────────────────────
Git：
  - 完全離線工作
  - 本地完整的版本歷史
  - 提交、歸併、分支都不需要網路

SVN：
  - 需要網路進行 commit
  - 歷史記錄需要網路存取
  - 離線只能編輯和 update
```

### 速度比較

```bash
# Git 的速度優勢（典型數值）
git status    # < 0.1s（本地）
svn status    # ~1-2s（網路）

git commit   # < 0.5s（本地）
svn commit   # ~2-5s（網路）

git log      # < 0.1s（本地）
svn log      # ~2-3s（網路）
```

## 何時選擇 SVN

### SVN 適合的場景

1. **從 CVS 遷移**：已有的 CVS 基礎設施
2. **需要集中管理**：企業需要控制程式碼位置
3. **權限管理**：需要細粒度的存取控制
4. **學習曲線**：團隊對 SVN 已經熟悉

### SVN 的優勢

```bash
# SVN 的適用情況
# 1. 小型團隊（< 20 人）
# 2. 中央控制的環境
# 3. 從 CVS 遷移不想改變工作流
# 4. 對 Git 不熟悉的團隊
```

## 結語

2007 年，Subversion 正在取代 CVS 成為企業的首選版本控制系統。SVN 解決了 CVS 的大部分問題，同時保持了相似的使用模式，降低了學習曲線。

但分散式版本控制（尤其是 Git）正在興起，將在未來幾年改變版本控制的格局。

---

## 延伸閱讀

- [Subversion+vs+CVS+2007](https://www.google.com/search?q=Subversion+vs+CVS+2007)
- [Apache+Subversion+history](https://www.google.com/search?q=Apache+Subversion+history)

---

*本篇文章為「AI 程式人雜誌 2007 年 6 月號」本期焦點系列之一。*