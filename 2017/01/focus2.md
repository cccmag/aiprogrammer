# pip 與虛擬環境：Python 包管理的藝術

## 前言

Python 的強大之處在於其豐富的套件生態系。然而，如何有效地管理這些套件，特別是當專案數量增加時避免依賴衝突，是每個 Python 開發者必須面對的問題。本篇文章介紹 pip、virtualenv 和 pipenv 等工具，幫助讀者建立乾淨、可重現的 Python 開發環境。

## pip：Python 套件管理器

### pip 的基礎

pip 是 Python 官方推薦的套件管理器，從 Python 3.4 起預設包含在 Python 安裝中。

```bash
# 安裝套件
pip install requests

# 安裝特定版本
pip install requests==2.18.0

# 安裝版本範圍
pip install "requests>=2.18.0,<3.0.0"

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

requirements.txt 是 Python 專案中最常見的依賴檔案格式：

```bash
# 產出當前環境的依賴
pip freeze > requirements.txt

# 常見格式：
# requests==2.18.0
# numpy==1.12.0
# pandas==0.19.2
```

```txt
# requirements.txt 範例
# 注释：主要依賴
Django==1.11
djangorestframework==3.6.0

# 注释：開發依賴
pytest==3.0.6
coverage==4.4

# 注释：可選依賴
MySQL-python==1.2.5; python_version < '3.0'
pymysql==0.6.6; python_version >= '3.0'
```

### 安裝依賴

```bash
# 從 requirements.txt 安裝
pip install -r requirements.txt

# 生產環境（不含開發依賴）
pip install -r requirements.txt --production

# 安裝到用戶目錄（不需要 root）
pip install --user requests
```

### 使用镜像

在中國大陸等地区，使用國内镜像可以大幅加速下載：

```bash
# 使用豆瓣镜像
pip install requests -i https://pypi.doubanio.com/simple/

# 設置為默認镜像
pip config set global.index-url https://pypi.doubanio.com/simple/
```

## virtualenv：隔離的 Python 環境

### 為什麼需要虛擬環境？

每個 Python 專案可能有不同的依賴需求：

```
專案 A：Django 1.11
專案 B：Django 2.0
專案 C：需要 Python 2.7
專案 D：需要 Python 3.6
```

如果所有專案共享同一個 Python 環境，依賴衝突在所難免。virtualenv 解決了這個問題。

### 使用 virtualenv

```bash
# 安裝 virtualenv
pip install virtualenv

# 創建虛擬環境
virtualenv myproject_env

# 或者指定 Python 版本
virtualenv -p python3.6 myproject_env

# 激活虛擬環境
# Linux/macOS:
source myproject_env/bin/activate

# Windows:
myproject_env\Scripts\activate

# 確認激活成功
which python  # 應該指向 myproject_env

# 退出虛擬環境
deactivate
```

### virtualenvwrapper：更好的管理體驗

virtualenvwrapper 提供了一組便捷的命令來管理多個虛擬環境：

```bash
# 安裝
pip install virtualenvwrapper

# 在 ~/.bashrc 或 ~/.zshrc 中添加
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

```bash
# 常用命令
mkvirtualenv myproject      # 創建新環境
workon myproject            # 激活環境
deactivate                  # 退出環境
rmvirtualenv myproject      # 刪除環境
lsvirtualenv                # 列出所有環境
lssitepackages              # 查看當前環境的套件
```

## pipenv：現代的 Python 開發體驗

### pipenv 簡介

pipenv 將 pip 和 virtualenv 合併，提供統一的開發體驗。它使用 Pipfile 和 Pipfile.lock 來管理依賴。

```bash
# 安裝 pipenv
pip install pipenv

# 進入專案目錄，pipenv 會自動創建虛擬環境
cd myproject
pipenv install requests

# 激活虛擬環境
pipenv shell

# 運行 Python 腳本（在虛擬環境中）
pipenv run python app.py

# 安裝開發依賴
pipenv install pytest --dev
```

### Pipfile 格式

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"
flask = "*"
django = "==1.11"

[dev-packages]
pytest = "*"
coverage = "*"

[requires]
python_version = "3.6"
```

### Pipfile.lock

Pipfile.lock 記錄了確切的版本號和依賴樹，確保團隊成員和部署環境的一致性：

```bash
# 更新 lock 文件
pipenv lock

# 安裝鎖定版本
pipenv sync
```

### 常用 pipenv 命令

```bash
pipenv install              # 安裝所有依賴
pipenv install requests     # 安裝單個套件
pipenv uninstall requests   # 卸載套件
pipenv --rm                # 刪除虛擬環境
pipenv graph               # 查看依賴圖
pipenv check               # 檢查安全性
pipenv run pip freeze      # 查看已安裝套件
```

## 最佳實踐

### 專案結構建議

```
myproject/
├── Pipfile              # 依賴定義
├── Pipfile.lock         # 鎖定版本（提交到 git）
├── app.py               # 主程式碼
├── tests/
│   └── test_app.py      # 測試
└── README.md
```

### .gitignore 建議

```
# 虛擬環境
venv/
.venv/
env/
.env

# pipenv 產生的環境目錄
.Python

# 不要提交 Pipfile.lock 到公開專案（可選）
# Pipfile.lock
```

### CI/CD 整合

```bash
# 在 CI 環境中安裝依賴
pip install pipenv
pipenv install --dev --deploy
pipenv run pytest
```

## 結論

Python 的包管理工具經歷了從 raw pip 到 virtualenv，再到 pipenv 的演進歷程。選擇適合的工具可以大幅提升開發效率：

- **個人小專案**：直接用 pip + virtualenv
- **團隊專案**：使用 pipenv 獲得更好的可重現性
- **大型專案**：考慮 Pipenv + 嚴格的依賴管理策略

無論選擇哪種工具，養成良好的依賴管理習慣是每個 Python 開發者的必修課。

---

## 延伸閱讀

- [pip 官方文檔](https://www.google.com/search?q=pip+python+package+manager+documentation)
- [virtualenv 官方文檔](https://www.google.com/search?q=virtualenv+python+tutorial)
- [pipenv 官方文檔](https://www.google.com/search?q=pipenv+python+package+management)
- [Python 虛擬環境最佳實踐](https://www.google.com/search?q=python+virtual+environment+best+practices)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」焦點系列之一。*