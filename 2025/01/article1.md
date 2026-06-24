# 安裝 Python：從零開始

## 前言

在開始寫 Python 程式之前，我們需要先在電腦上安裝 Python 執行環境。本文將帶領你一步步完成安裝，無論你使用的是 Windows、macOS 還是 Linux。

## 選擇 Python 版本

目前 Python 的最新穩定版本是 3.13.x（2025年1月止）。建議安裝 Python 3.12 或 3.13，避免使用 Python 2.x（已於 2020 年終止支援）。

## Windows 安裝

### 步驟一：下載安裝檔

1. 前往 [Python 官方網站](https://www.google.com/search?q=Python+download+official)
2. 點擊「Downloads」→ 選擇 Windows 版本
3. 下載 Windows installer (64-bit)

### 步驟二：執行安裝

```bash
# 安裝時請務必勾選
# ☑ Add Python to PATH
# 這會讓你在命令提示字元中可以直接使用 python 指令
```

### 步驟三：驗證安裝

打開命令提示字元（cmd），輸入：

```bash
python --version
# Python 3.13.0

pip --version
# pip 24.2 from ...
```

## macOS 安裝

### 方法一：官方安裝檔（推薦）

1. 前往 Python 官方網站下載 macOS 安裝檔
2. 執行 .pkg 安裝檔
3. 依照安裝精靈指示完成

### 方法二：使用 Homebrew

```bash
# 安裝 Homebrew（如尚未安裝）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 Python
brew install python@3.13

# 驗證
python3 --version
```

## Linux 安裝

大多數 Linux 發行版已內建 Python。如需要安裝或更新：

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### Fedora/RHEL

```bash
sudo dnf install python3 python3-pip
python3 --version
```

## pip：Python 套件管理器

pip 是 Python 的官方套件管理器，用於安裝第三方套件。

### 基本使用

```bash
# 安裝套件
pip install requests

# 安裝特定版本
pip install numpy==1.26.0

# 移除套件
pip uninstall requests

# 列出已安裝套件
pip list

# 匯出依賴
pip freeze > requirements.txt

# 從檔案安裝
pip install -r requirements.txt
```

## 虛擬環境

每個專案應該使用獨立的虛擬環境，避免套件版本衝突。

### 使用 venv

```bash
# 建立虛擬環境
python -m venv myproject_env

# 啟動虛擬環境
# Windows:
myproject_env\Scripts\activate
# macOS/Linux:
source myproject_env/bin/activate

# 離開虛擬環境
deactivate
```

### 使用 virtualenvwrapper（選用）

```bash
pip install virtualenvwrapper
# 設定 shell 環境變數後可使用 mkvirtualenv, workon 等指令
```

## 整合開發環境 (IDE)

### VS Code

1. 下載安裝 VS Code
2. 安裝 Python 擴充功能（由 Microsoft 提供）
3. 安裝後即可獲得語法高亮、自動補全、除錯等功能

### PyCharm

JetBrains 出品的專業 Python IDE，社群版免費使用：

- 智慧型程式碼補全
- 強大的除錯器
- 內建版本控制整合

## 第一個測試

安裝完成後，建立一個測試檔案：

```python
# hello.py
print("Hello, Python!")
print("恭喜你成功安裝 Python 環境！")

# 測試中文支援
print("你好，Python！🎉")
```

執行：

```bash
python hello.py
# Hello, Python!
# 恭喜你成功安裝 Python 環境！
# 你好，Python！🎉
```

## 常見問題排解

### 「python 不是內部或外部命令」

- 原因：Python 沒有加入 PATH
- 解決：重新安裝並勾選「Add Python to PATH」

### 「pip 指令找不到」

```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

### 多版本 Python 共存

```bash
# 使用完整版本號
python3.12 -V
python3.13 -V

# 或使用 pyenv 管理多版本
```

## 小結

安裝完成後，你已經準備好開始 Python 程式設計的旅程。後續文章將逐步引導你從「Hello, World!」到建立完整的應用程式。

---

**延伸閱讀**

- [Python 官方下載頁](https://www.google.com/search?q=Python+download)
- [pip 官方文件](https://www.google.com/search?q=pip+documentation)
- [VS Code Python 教學](https://www.google.com/search?q=VS+Code+Python+setup+tutorial)
