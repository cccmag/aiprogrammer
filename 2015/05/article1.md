# pip 與虛擬環境完全指南

## pip 基礎

pip 是 Python 的套件管理器，用於安裝和管理 Python 套件。

### 基本命令

```bash
# 安裝套件
pip install requests

# 安裝特定版本
pip install requests==2.10.0

# 安裝多個套件
pip install numpy pandas matplotlib

# 從 requirements.txt 安裝
pip install -r requirements.txt

# 升級套件
pip install --upgrade requests

# 卸載套件
pip uninstall requests

# 列出已安裝的套件
pip list

# 顯示套件資訊
pip show requests

# 檢查過時的套件
pip list --outdated
```

### requirements.txt

```text
# requirements.txt 範例
requests>=2.10.0
flask>=0.10
numpy>=1.9
pandas>=0.16
```

```bash
# 凍結當前環境的套件版本
pip freeze > requirements.txt
```

## 虛擬環境

虛擬環境是一個獨立的 Python 環境，可以讓每個專案有自己的套件，不會互相衝突。

### 為何需要虛擬環境

- 避免套件版本衝突
- 保持系統環境乾淨
- 方便重現和部署

### 使用 venv（Python 3.3+）

```bash
# 建立虛擬環境
python3 -m venv myenv

# 啟動虛擬環境
# Linux/macOS
source myenv/bin/activate

# Windows
myenv\Scripts\activate

# 停用虛擬環境
deactivate
```

### virtualenv（較舊但相容）

```bash
# 安裝 virtualenv
pip install virtualenv

# 建立虛擬環境
virtualenv myenv

# 啟動
source myenv/bin/activate
```

## 完整工作流程

```bash
# 1. 建立專案目錄
mkdir myproject
cd myproject

# 2. 建立虛擬環境
python3 -m venv venv

# 3. 啟動虛擬環境
source venv/bin/activate

# 4. 安裝需要的套件
pip install flask requests numpy

# 5. 開發你的應用程式
# ...

# 6. 記錄依賴
pip freeze > requirements.txt

# 7. 部署時重建環境
# pip install -r requirements.txt
```

## 虛擬環境管理工具

### pyenv（Python 版本管理）

```bash
# 安裝 pyenv
brew install pyenv

# 安裝 Python 版本
pyenv install 3.4.3
pyenv install 3.5.0

# 設定全域版本
pyenv global 3.5.0

# 設定專案版本
pyenv local 3.4.3
```

### pew（更簡便的虛擬環境管理）

```bash
# 安裝 pew
pip install pew

# 建立環境
pew new myproject

# 切換環境
pew workon myproject
```

## pipenv（現代選擇）

Pipenv 結合了 pip 和虛擬環境的功能：

```bash
# 安裝
pip install pipenv

# 進入專案目錄
cd myproject

# 安裝套件
pipenv install requests

# 安裝開發依賴
pipenv install --dev pytest

# 啟動 shell
pipenv shell

# 執行腳本
pipenv run python app.py
```

## pip 配置

```bash
# 查看 pip 配置
pip config list

# 設定代理
pip config set global.proxy "http://proxy.example.com:8080"

# 設定額外索引
pip config set global.index-url "https://pypi.douban.com/simple"
```

## 常見問題

### 權限問題

```bash
# 如果遇到權限錯誤，使用 --user
pip install --user somepackage

# 或者使用虛擬環境
python3 -m venv myenv
```

### 網路問題

```bash
# 使用豆瓣鏡像
pip install -i https://pypi.douban.com/simple requests

# 或設定為預設
pip config set global.index-url https://pypi.douban.com/simple
```

### 安裝路徑

```python
import site
print(site.getusersitepackages())
# Linux: ~/.local/lib/python3.x/site-packages
```

## 最佳實踐

1. **總是使用虛擬環境**：不要直接在系統 Python 安裝套件
2. **記錄依賴**：使用 `pip freeze` 維護 requirements.txt
3. **定期更新**：使用 `pip list --outdated` 檢查更新
4. **指定版本**：避免使用浮動版本號
5. **使用镜像**：在網路不佳時使用鏡像源

## 結論

掌握 pip 和虛擬環境是 Python 開發者的必備技能。它們讓專案管理更加清晰，也避免了很多環境衝突的問題。