# Git 安裝與設定

## 在 macOS 安裝 Git

macOS 可使用 Homebrew 安裝：

```bash
brew install git
```

或安裝 Xcode Command Line Tools：

```bash
xcode-select --install
```

## 在 Windows 安裝 Git

下載 Git for Windows 安裝程式，或使用 winget：

```bash
winget install --id Git.Git -e --source winget
```

## 在 Linux 安裝 Git

```bash
# Ubuntu/Debian
sudo apt install git

# Fedora
sudo dnf install git

# Arch Linux
sudo pacman -S git
```

## 初始設定

安裝後必須設定使用者名稱和電子郵件：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 其他重要設定

```bash
# 設定預設分支名稱為 main
git config --global init.defaultBranch main

# 啟用彩色輸出
git config --global color.ui auto

# 設定編輯器
git config --global core.editor "code --wait"

# 檢視所有設定
git config --list
```

## Python 驗證安裝

```python
import subprocess
import sys

def check_git():
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"Git 已安裝：{result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("Git 未安裝")
        return False

def configure_git(name, email):
    subprocess.run(["git", "config", "--global", 
        "user.name", name])
    subprocess.run(["git", "config", "--global",
        "user.email", email])
    print(f"設定完成：{name} <{email}>")

if __name__ == "__main__":
    if check_git():
        configure_git("AI 程式人", 
            "ai-programmer@example.com")
```

更多安裝資訊請參考 https://www.google.com/search?q=Git+安裝+教學。
