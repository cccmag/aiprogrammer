# Git 基礎：初始化、提交、日誌

## 開始使用 Git

### 初始化儲存庫

使用 `git init` 在目錄中建立新的 Git 儲存庫：

```bash
mkdir my-project
cd my-project
git init
```

這會在目錄中建立一個 `.git` 隱藏資料夾，存放所有版本資訊。

### 第一個提交

Git 的工作流程分為三個區域：工作目錄、暫存區 (staging area) 和儲存庫 (repository)。

```bash
# 建立檔案
echo "Hello Git" > README.md

# 加入暫存區
git add README.md

# 提交到儲存庫
git commit -m "Initial commit"
```

### 檢視提交歷史

`git log` 顯示提交歷史：

```bash
git log
git log --oneline  # 簡潔模式
git log --graph    # 圖形化顯示
```

### Python 模擬

以下 Python 程式模擬了 Git 的基本操作：

```python
class SimpleGit:
    def __init__(self):
        self.objects = {}
        self.staging = set()
        self.branches = {"main": []}
        self.head = "main"
    
    def add(self, filename, content):
        import hashlib
        oid = hashlib.sha1(content.encode()).hexdigest()[:7]
        self.objects[oid] = content
        self.staging.add(oid)
        print(f"add {filename} -> {oid}")
    
    def commit(self, message):
        if not self.staging:
            print("nothing to commit")
            return
        self.branches[self.head].append({
            "message": message,
            "objects": list(self.staging)
        })
        self.staging.clear()
        print(f"commit: {message}")

git = SimpleGit()
git.add("file1.txt", "content1")
git.add("file2.txt", "content2")
git.commit("第一次提交")
```

更多 Git 基礎知識請參考 https://www.google.com/search?q=Git+init+add+commit+教學。
