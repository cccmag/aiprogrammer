# Git 的資料模型

理解 Git 的內部資料模型，能幫助你更有效地使用 Git，解決合併衝突等複雜問題。

---

## 四種物件

Git 的核心是四種資料物件：

### 1. Blob

Blob（Binary Large Object）儲存檔案內容。每個檔案內容都會產生一個唯一的 SHA-1 哈希值作為物件 ID。

### 2. Tree

Tree 物件代表目錄結構，包含：
- 指向 blob 或其他 tree 的指標
- 檔案或目錄名稱
- 檔案模式（權限）

### 3. Commit

Commit 物件包含：
- 指向 tree 的指標（專案在該時間點的快照）
- 父 commit 的指標
- 作者和提交者的資訊
- 提交時間和訊息

### 4. Tag

Tag 物件用於標記特定的 commit，通常用於版本發布。

---

## 引用（References）

引用是指向 commit 的指標，是我們操作 Git 的主要方式。

### 分支

```bash
# 查看所有分支
git branch

# 檢視分支指向
git show-ref

# 查看 HEAD 指向
cat .git/HEAD
```

### 標籤

```bash
# 列出標籤
git tag

# 建立輕量標籤
git tag v1.0

# 建立附注標籤
git tag -a v1.0 -m "版本 1.0"
```

---

## 倉庫結構

```
.git/
├── HEAD          # 目前所在的分支
├── refs/
│   ├── heads/    # 本地分支
│   ├── tags/     # 標籤
│   └── remotes/  # 遠端分支
├── objects/      # 所有 Git 物件
├── config        # 倉庫設定
└── index         # 暫存區
```

---

## 物件儲存

Git 使用 zlib 壓縮來儲存物件：

```bash
# 查看物件內容
git cat-file -p <object-id>

# 查看物件類型
git cat-file -t <object-id>

# 查看物件大小
git cat-file -s <object-id>
```

---

## Pack Files

為了節省空間，Git 會定期將多個物件打包成 pack file：

```bash
# 手動執行 garbage collection
git gc

# 查看 pack files
ls .git/objects/pack/
```

---

## 分支操作原理

建立分支只是建立一個新的引用，指向當前 commit：

```bash
git branch feature # 建立分支，但不移轉
git checkout feature # 切換到該分支
git checkout -b feature # 建立並切換
```

---

## 小結

理解 Git 的資料模型——blob、tree、commit、tag 四種物件，以及 refs 引用——能幫助你更好地理解 Git 的運作方式，在解決問題時更加得心應手。

---

*作者：AI 程式人團隊*