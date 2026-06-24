# 遠端儲存庫與 GitHub

## 遠端協作

Git 的分散式架構讓團隊協作變得簡單。遠端儲存庫 (remote repository) 是團隊共享程式碼的中樞。

### 連結遠端儲存庫

```bash
# 複製遠端儲存庫
git clone https://github.com/user/project.git

# 查看遠端設定
git remote -v

# 新增遠端
git remote add origin https://github.com/user/project.git
```

### 推送與拉取

```bash
# 推送本機分支到遠端
git push origin main

# 拉取遠端變更
git pull origin main

# 拉取但不合併
git fetch origin
```

### GitHub 平台

GitHub 是目前最大的 Git 代管平台，提供了：

- Issue 追蹤系統
- Pull Request 機制
- GitHub Actions CI/CD
- Wiki 和 Pages

### 認證方式

連接到遠端儲存庫需要認證：

1. **HTTPS**：使用 Personal Access Token
2. **SSH**：使用 SSH 金鑰對

```bash
# SSH 設定
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub  # 複製到 GitHub 設定
```

### Python 範例

```python
import subprocess

class RemoteGit:
    def __init__(self, url):
        self.url = url
    
    def clone(self, path):
        subprocess.run(["git", "clone", self.url, path])
        print(f"cloned {self.url} to {path}")
    
    def push(self, branch="main"):
        subprocess.run(["git", "push", "origin", branch])
        print(f"pushed to origin/{branch}")
    
    def pull(self, branch="main"):
        subprocess.run(["git", "pull", "origin", branch])
        print(f"pulled from origin/{branch}")

# 使用示例（需在 Git 儲存庫中執行）
# remote = RemoteGit("https://github.com/example/repo.git")
# remote.clone("./myrepo")
```

更多關於遠端儲存庫的操作請參考 https://www.google.com/search?q=Git+remote+push+pull+教學。
