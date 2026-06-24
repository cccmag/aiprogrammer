# 3. pip 進階技巧

## pip 20.0 的新特性

2020 年 1 月的 pip 版本來到 20.0 系列，帶來了安裝速度提升與新的功能。了解這些工具可以大幅提升開發效率。

## 基本操作回顧

```bash
# 安裝套件
pip install package_name
pip install package==1.2.3           # 指定版本
pip install "package>=1.0,<2.0"     # 版本範圍

# 升級
pip install --upgrade package_name
pip install --upgrade pip           # 升級 pip 本身

# 卸載
pip uninstall package_name

# 顯示已安裝
pip list
pip freeze                           # 輸出 requirements.txt 格式
```

## requirements.txt 管理

```bash
# 匯出當前環境
pip freeze > requirements.txt

# 安裝所有依賴
pip install -r requirements.txt

# 只更新特定套件
pip install --upgrade -r requirements.txt
```

## pip-tools 進行版本鎖定

`pip-tools` 提供了更嚴格的依賴管理：編譯依賴並鎖定到精確版本。

```bash
pip install pip-tools

# 安裝到 requirements.in（只記錄直接依賴）
echo "requests>=2.22" > requirements.in
echo "flask>=1.1" >> requirements.in

# 編譯成 requirements.txt（鎖定版本）
pip-compile requirements.in

# 安裝時使用鎖定的檔案
pip-sync requirements.txt
```

## 離線安裝

```bash
# 下載套件到本地目錄
pip download -r requirements.txt -d ./packages

# 離線安裝
pip install --no-index --find-links=./packages -r requirements.txt
```

## 使用虛擬環境時的 pip

```bash
# 透過 python -m pip 確保使用正確的 pip
python -m pip install package

# 或使用 venv 的自動 pip
python3 -m venv myenv
source myenv/bin/activate
pip install package
```

## PyPI 私人套件

```bash
# 安裝私人套件（使用 URL）
pip install git+https://github.com/user/repo.git
pip install git+https://github.com/user/repo.git@v1.0

# 安裝私有 PyPI
pip install --index-url=https://my-private-pypi.com/simple package
```

## 依賴圖檢視

```bash
# 顯示依賴關係
pip show package_name
pip show -f package_name       # 包含檔案列表

# 檢查過時套件
pip list --outdated
```

## pipenv 整合

`pipenv` 是另一種管理依賴的方式，結合了 pip 與 virtualenv：

```bash
pip install pipenv

# 安裝相依（自動建立/使用 Pipfile）
pipenv install requests

# 開發專用相依
pipenv install pytest --dev

# 執行指令
pipenv run python app.py

# 進入 shell
pipenv shell
```

## 常見問題

1. **權限錯誤**：使用 `pip install --user` 安裝到使用者目錄，或建立虛擬環境
2. **安裝過慢**：使用 `--trusted-host` 或設定鏡像源
3. **C 擴充編譯失敗**：安裝編譯工具鏈（Xcode Command Line Tools、build-essential）

## 參考資源

- https://www.google.com/search?q=pip+install+requirements.txt+tutorial+2020
- https://www.google.com/search?q=pip-tools+pip-compile+dependency+locking+Python
- https://www.google.com/search?q=pip+offline+install+private+package+Python+2020