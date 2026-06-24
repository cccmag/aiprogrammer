# Git 核心概念與架構

## Git 物件模型

### 四種主要物件

```python
# Git 物件類型
git_objects = {
    'blob': '儲存檔案內容',
    'tree': '儲存目錄結構',
    'commit': '儲存提交資訊',
    'tag': '儲存標籤資訊'
}
```

### Blob

```bash
# Blob 儲存檔案內容（無檔名）
echo "Hello, Git!" | git hash-object --stdin -w
# 輸出：8ab686eafeb1f44702738c8b0f24f2567c36da6d
```

### Tree

```bash
# Tree 儲存目錄和 blob 的映射
git cat-file -p HEAD^{tree}
# 100644 blob a1b2c3... README.md
# 040000 tree d4e5f6... src
```

### Commit

```bash
# Commit 儲存提交
git cat-file -p HEAD
# tree a1b2c3...
# parent d4e5f6...
# author John <john@example.com> 1222233600 +0800
# committer John <john@example.com> 1222233600 +0800
#
# Initial commit
```

## 物件儲存

### 內容定址

```python
# 每個物件以其 SHA-1 雜湊值命名
# SHA-1(text) → hash
# 相同內容總是產生相同雜湊
```

### .git 目錄結構

```bash
.git/
├── HEAD              # 當前分支
├── objects/          # 所有物件
│   ├── 00/           #  packfiles
│   ├── ab/
│   └── ...
├── refs/
│   ├── heads/        # 本地分支
│   └── tags/         # 標籤
├── config            # 倉庫配置
└── index             # 暫存區
```

## 指標系統

### Branch

```bash
# 分支是指向 commit 的指標
cat .git/refs/heads/main
# a1b2c3d4e5f6...

# HEAD 指向當前分支
cat .git/HEAD
# ref: refs/heads/main
```

### Tag

```bash
# 標籤通常用於標記發布版本
git tag v1.0.0 a1b2c3d
```

## 工作區域

### 四大區域

```python
# Git 的四大區域
git_areas = {
    'working_directory': '工作目錄（編輯檔案）',
    'staging_area': '暫存區（git add）',
    'local_repository': '本地倉庫（.git）',
    'remote_repository': '遠端倉庫（GitHub）'
}
```

### 狀態轉換

```bash
# 檔案狀態流程
working_directory → git add → staging_area
                                    ↓ git commit
                               local_repository
                                    ↓ git push
                          remote_repository
```

## 結論

Git 的物件模型雖然簡單但極其強大。理解 blob、tree、commit 的關係是掌握 Git 的基礎。

---

**延伸閱讀**

- [常用 Git 命令詳解](focus5.md)
- [Git+internals](https://www.google.com/search?q=Git+internals+objects)