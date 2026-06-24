# Pipenv 完整教學

## 安裝與基本操作

```bash
# 安裝
pip install pipenv

# 進入專案目錄
cd myproject

# 安裝套件
pipenv install requests
pipenv install pytest --dev
```

## Pipfile 結構

```toml
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]
pytest = "*"

[packages]
requests = "*"
flask = "*"

[requires]
python_version = "3.7"
```

## Pipfile.lock

`pipenv lock` 生成 Pipfile.lock，鎖定所有相依的精確版本：

```bash
pipenv lock
pipenv sync
```

## 執行與 Shell

```bash
# 在虛擬環境中執行
pipenv run python app.py

# 進入 shell
pipenv shell

# 退出 shell
exit
```

## 從 requirements.txt 遷移

```bash
# 安裝 requirements.txt 中的依賴
pipenv install -r requirements.txt

# 匯出到 requirements.txt
pipenv lock -r > requirements.txt

# 只匯出 dev 依賴
pipenv lock -r --dev > requirements-dev.txt
```

## 圖形化檢視

```bash
# 顯示依賴圖
pipenv graph
```

## 環境變數

Pipenv 支援 `.env` 檔案：

```bash
# .env
DATABASE_URL=postgres://localhost/mydb
SECRET_KEY=mysecret
```

## 移除套件

```bash
pipenv uninstall requests
```

## Pipenv 與 pyenv

結合 pyenv 管理 Python 版本：

```bash
# 安裝特定 Python 版本
pyenv install 3.8.1

# Pipfile 指定版本
[requires]
python_version = "3.8"
```

## 參考資源

- https://www.google.com/search?q=Pipenv+tutorial+Python+environment+management+2020
- https://www.google.com/search?q=Pipenv+Pipfile+lock+workflow+guide+2020
- https://www.google.com/search?q=Pipenv+vs+Poetry+Python+dependency+2020