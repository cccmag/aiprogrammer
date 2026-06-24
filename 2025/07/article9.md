# 環境變數與 PATH

## 什麼是環境變數？

環境變數是作業系統中用來儲存系統資訊的鍵值對。它們影響應用程式的行為、定義系統路徑，並傳遞設定資訊給行程。

```bash
# 檢視所有環境變數
env

# 檢視特定變數
echo $HOME
echo $PATH
echo $USER

# 設定環境變數 (當前 Shell)
export MY_VAR="hello"
```

## 重要的環境變數

| 變數 | 說明 | 典型值 |
|------|------|--------|
| `HOME` | 使用者家目錄 | `/home/alice` |
| `USER` | 目前使用者名 | `alice` |
| `SHELL` | 預設 Shell | `/bin/bash` |
| `PATH` | 可執行檔搜尋路徑 | `/usr/bin:/bin` |
| `PWD` | 當前目錄 | `/home/alice/project` |
| `LANG` | 語言設定 | `zh_TW.UTF-8` |
| `EDITOR` | 預設編輯器 | `vim` |
| `TERM` | 終端機類型 | `xterm-256color` |

## PATH 變數詳解

`PATH` 是最重要的環境變數。當你在命令列輸入一個命令時，Shell 會依照 `PATH` 中列出的目錄順序搜尋可執行檔。

```bash
# 查看 PATH
echo $PATH
# 輸出: /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:~/.local/bin

# 路徑搜尋流程
當你輸入 python3 時：
1. Shell 檢查是否為內建命令 → 否
2. 搜尋 PATH 中的目錄:
   /usr/local/bin/python3 → 找到了！執行
```

### 修改 PATH

```bash
# 暫時新增 (當前 Shell)
export PATH=$PATH:~/my_scripts

# 永久修改
# 在 ~/.bashrc 或 ~/.zshrc 中加入
echo 'export PATH=$PATH:~/my_scripts' >> ~/.bashrc
```

## 設定環境變數的位置

### Shell 設定檔載入順序

```bash
# 登入 Shell
/etc/profile → ~/.profile (或 ~/.bash_profile) → ~/.bashrc

# 非登入互動式 Shell
/etc/bash.bashrc → ~/.bashrc

# 建議
# 在 ~/.bashrc 中設定個人環境變數
```

### 範例設定

```bash
# ~/.bashrc 範例

# PATH 設定
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/go/bin:$PATH"

# 開發環境
export EDITOR="code --wait"
export VISUAL="code --wait"
export PAGER="less"

# Python 相關
export PIP_REQUIRE_VIRTUALENV=true
export PYTHONUNBUFFERED=1

# 專案特定
export PROJECT_HOME="$HOME/projects"
export DATABASE_URL="postgresql://localhost:5432/mydb"
```

## 環境變數的繼承

行程會繼承父行程的環境變數。這意味著你在 Shell 中設定的變數，會傳遞給從該 Shell 啟動的所有子行程：

```
Shell (export FOO=bar)
  ├─ python3 (FOO=bar)
  ├─ node (FOO=bar)
  └─ bash (FOO=bar)
       └─ go run (FOO=bar)
```

## Python 中的環境變數

```python
import os

# 讀取環境變數
home = os.environ.get("HOME", "/tmp")
path = os.environ.get("PATH", "")
debug = os.environ.get("DEBUG", "false").lower() == "true"

print(f"家目錄: {home}")
print(f"PATH: {path[:50]}...")

# 設定環境變數 (只影響當前行程和子行程)
os.environ["MYAPP_CONFIG"] = "/etc/myapp/config.json"

# 使用環境變數設定應用程式
class Config:
    def __init__(self):
        self.database_url = os.environ.get(
            "DATABASE_URL",
            "sqlite:///default.db"
        )
        self.debug = os.environ.get(
            "DEBUG",
            "false"
        ).lower() == "true"
        self.port = int(os.environ.get("PORT", 8080))

# 執行子行程時傳遞環境變數
import subprocess

env = os.environ.copy()
env["MYAPP_MODE"] = "production"
subprocess.run(["python3", "app.py"], env=env)
```

## 使用 dotenv 管理環境變數

```bash
# .env 檔案範例
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=sk-abc123def456
DEBUG=true
PORT=3000
```

```python
# Python 讀取 .env
def load_dotenv(path=".env"):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                os.environ[key.strip()] = value.strip()

load_dotenv()
print(f"DB: {os.environ.get('DATABASE_URL')}")
```

---

## 延伸閱讀

- [Linux 環境變數教學](https://www.google.com/search?q=Linux+environment+variables+PATH+tutorial)
- [Bash 設定檔載入順序](https://www.google.com/search?q=bash+bashrc+bash_profile+loading+order)
- [Python os.environ 使用](https://www.google.com/search?q=Python+os+environ+environment+variables)
