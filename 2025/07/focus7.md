# 開發環境建置：VS Code、Python、Git

## 為什麼需要好的開發環境

一個良好的開發環境能顯著提升生產力。它不僅僅是編輯器本身，還包括版本控制、語言工具鏈、偵錯工具和擴展生態系統。

## VS Code：現代 IDE 的典範

Visual Studio Code 是微軟開發的免費、開源編輯器，已成為最受歡迎的程式開發工具。

### 必裝擴展

```json
{
  "recommendations": [
    "ms-python.python",          // Python 支援
    "ms-vscode.cpptools",         // C/C++ 支援
    "eamodio.gitlens",            // Git 增強
    "github.copilot",             // AI 輔助編碼
    "ms-vscode-remote.remote-ssh", // 遠端 SSH 開發
    "ms-azuretools.vscode-docker", // Docker 管理
    "yzhang.markdown-all-in-one",  // Markdown 編輯
  ]
}
```

### 遠端開發

VS Code 的遠端開發功能允許你在本機編輯，在遠端伺服器執行：

```bash
# 透過 SSH 連線到遠端開發機
# VS Code 會自動在遠端安裝伺服端元件
# 支援: SSH 容器 WSL GitHub Codespaces
```

Remote-SSH 特別適合 Linux 伺服器開發——你的 VS Code 執行在筆電上，但編輯、編譯、執行都發生在遠端 Linux 主機上。

## Python 開發環境

### 虛擬環境

```bash
# 建立虛擬環境
python3 -m venv venv

# 啟用虛擬環境
source venv/bin/activate     # Linux/macOS
# venv\Scripts\activate      # Windows

# 安裝套件
pip install flask requests

# 匯出依賴
pip freeze > requirements.txt

# 還原環境
pip install -r requirements.txt
```

### Python 開發工具

```python
# pyproject.toml (現代 Python 專案設定)
"""
[build-system]
requires = ["setuptools", "wheel"]

[project]
name = "myproject"
version = "0.1.0"
dependencies = [
    "flask>=3.0",
    "requests>=2.32",
]
"""
```

## Git：版本控制

### 基本工作流程

```bash
git init                     # 初始化倉庫
git clone url                # 克隆遠端倉庫
git add file.py              # 加入暫存區
git commit -m "訊息"         # 提交
git push origin main         # 推送至遠端
git pull                     # 拉取更新
```

### 分支策略

```bash
git branch feature-x         # 建立分支
git checkout feature-x       # 切換分支
git checkout -b feature-x    # 建立並切換
git merge feature-x          # 合併分支
git branch -d feature-x      # 刪除分支
```

### .gitignore 範例

```
__pycache__/
*.pyc
venv/
.env
.DS_Store
*.log
dist/
```

## 完整的開發流程

```
開發流程範例：
─────────────────

1. 設定環境
   $ git clone git@github.com:user/project.git
   $ cd project
   $ python3 -m venv venv && source venv/bin/activate
   $ pip install -r requirements.txt
   $ code .

2. 開發新功能
   $ git checkout -b feature/new-feature
   (編輯程式碼)
   $ python -m pytest tests/
   $ git add . && git commit -m "feat: 新增功能"

3. 程式碼審查
   $ git push origin feature/new-feature
   (在 GitHub/GitLab 建立 PR)

4. 部署
   $ git checkout main
   $ git pull
   $ ./deploy.sh
```

```python
# Python 偵測開發環境
import os, sys, subprocess

def check_dev_env():
    info = {
        "python": sys.version,
        "git": subprocess.run(["git", "--version"],
            capture_output=True, text=True).stdout.strip(),
        "os": os.uname().sysname,
        "editor": os.environ.get("EDITOR", "N/A"),
    }
    for k, v in info.items():
        print(f"{k}: {v}")

check_dev_env()
```

---

## 延伸閱讀

- [VS Code 遠端開發](https://www.google.com/search?q=VS+Code+remote+development+SSH+container)
- [Python 虛擬環境教學](https://www.google.com/search?q=Python+virtual+environment+venv+tutorial)
- [Git 版本控制入門](https://www.google.com/search?q=Git+version+control+tutorial+for+beginners)
