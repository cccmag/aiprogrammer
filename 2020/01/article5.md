# Poetry 快速上手

## 安裝

```bash
# macOS/Linux
curl -sSL https://raw.githubusercontent.com/python-poetry/install.poetry.org/master/get-poetry.py | python3

# 或使用 pip
pip install poetry

# 確認安裝
poetry --version
```

## 建立新專案

```bash
poetry new my-project
cd my-project

# 專案結構
# my-project/
# ├── pyproject.toml
# ├── README.rst
# ├── my_project/
# │   └── __init__.py
# └── tests/
#     └── __init__.py
```

## 安裝依賴

```bash
# 新增執行依賴
poetry add requests
poetry add flask

# 新增開發依賴
poetry add pytest --dev

# 安裝所有依賴
poetry install
```

## pyproject.toml 範例

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A sample project"
authors = ["Name <email@example.com>"]

[tool.poetry.dependencies]
python = "^3.7"
requests = "^2.22"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

## 執行與 Shell

```bash
# 執行指令
poetry run python app.py

# 進入虛擬環境 shell
poetry shell

# 離開
exit
```

## 鎖定與更新

```bash
# 更新 lock 檔案
poetry lock

# 更新所有相依到最新相容版本
poetry update

# 更新特定套件
poetry update requests
```

## 建置與發布

```bash
# 建置 distribution
poetry build

# 發布到 PyPI（需要設定）
poetry publish

# 發布到私人 PyPI
poetry publish --repository=myrepo
```

## 從現有專案遷移

```bash
# 初始化 poetry 專案
poetry init

# 互動式新增依賴
poetry add $(cat requirements.txt | tr '\n' ' ')
```

## 參考資源

- https://www.google.com/search?q=Poetry+Python+dependency+management+tutorial+2020
- https://www.google.com/search?q=Poetry+pyproject.toml+setup+publish+PyPI+guide
- https://www.google.com/search?q=Poetry+vs+pipenv+Python+2020+comparison