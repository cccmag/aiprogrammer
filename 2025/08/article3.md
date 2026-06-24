# git log 與歷史檢視

## 檢視提交歷史

`git log` 是檢視專案歷史的核心命令：

```bash
# 完整日誌
git log

# 一行模式
git log --oneline

# 圖形模式（顯示分支結構）
git log --graph --oneline --all
```

### 格式化輸出

```bash
# 自訂格式
git log --pretty=format:"%h - %an, %ar : %s"

# 圖形 + 簡短統計
git log --graph --stat
```

## 過濾提交

```bash
# 依作者過濾
git log --author="Alice"

# 依日期過濾
git log --since="2025-01-01" --until="2025-06-30"

# 依檔案過濾
git log -- README.md

# 搜尋提交訊息
git log --grep="fix"
```

## 檢視變更內容

```bash
# 顯示差異
git show [commit-hash]

# 比較兩個提交
git diff [hash1]..[hash2]

# 誰修改了什麼
git blame app.py
```

## Python 解析 Git Log

```python
import subprocess
import json

class GitLogParser:
    def get_log(self, repo_path="."):
        result = subprocess.run([
            "git", "log", "--oneline",
            "--format=%H|%an|%ar|%s"
        ], capture_output=True, text=True,
           cwd=repo_path)
        
        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|", 3)
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "date": parts[2],
                "message": parts[3]
            })
        return commits
    
    def print_summary(self, commits):
        print(f"共 {len(commits)} 筆提交")
        for c in commits[:5]:
            print(f"{c['hash'][:7]} {c['message']}")

parser = GitLogParser()
commits = parser.get_log()
parser.print_summary(commits)
```

更多 git log 技巧請參考 https://www.google.com/search?q=git+log+教學+用法。
