# 遠端儲存庫操作

## 複製與連結

### git clone

從遠端複製整個儲存庫到本機：

```bash
git clone https://github.com/user/project.git
git clone git@github.com:user/project.git  # SSH
git clone --depth 1 https://...             # 淺複製
```

### 管理遠端

```bash
# 檢視遠端
git remote -v

# 新增遠端
git remote add upstream https://github.com/original/repo.git

# 移除遠端
git remote remove origin

# 重新命名遠端
git remote rename origin upstream
```

## 推送與拉取

### git push

```bash
# 推送分支
git push origin main

# 設定上游並推送
git push -u origin feature

# 強制推送（謹慎使用）
git push --force origin feature

# 刪除遠端分支
git push origin --delete feature
```

### git pull 與 git fetch

```bash
# fetch：只下載，不合併
git fetch origin

# pull：下載並合併
git pull origin main

# pull 使用 rebase
git pull --rebase origin main
```

## Python 遠端操作

```python
import subprocess
import os

class RemoteManager:
    def __init__(self, url):
        self.url = url
    
    def clone(self, path):
        result = subprocess.run(
            ["git", "clone", self.url, path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✓ 複製完成：{path}")
        else:
            print(f"✗ 錯誤：{result.stderr}")
    
    def add_remote(self, name, url):
        subprocess.run(
            ["git", "remote", "add", name, url],
            capture_output=True
        )
        print(f"✓ 新增遠端 {name} -> {url}")
    
    def list_remotes(self):
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True, text=True
        )
        print(result.stdout)
    
    def push(self, remote, branch):
        result = subprocess.run(
            ["git", "push", remote, branch],
            capture_output=True, text=True
        )
        print(result.stdout or "✓ 推送成功")

# rm = RemoteManager("https://github.com/example/repo.git")
# rm.clone("./myclone")
# rm.add_remote("upstream", "https://github.com/upstream/repo.git")
# rm.push("origin", "main")
```

更多遠端操作請參考 https://www.google.com/search?q=git+remote+push+pull+clone+教學。
