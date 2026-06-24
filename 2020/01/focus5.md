# 5. 現代封裝工具：Poetry 與 Pipenv

## 為什麼需要現代工具？

傳統的 `setup.py` + `requirements.txt` 方式在 2020 年已經顯得過時。Poetry 與 Pipenv 提供了更現代的依賴管理方式：一個設定檔（pyproject.toml 或 Pipfile）管理專案相依、安裝、開發依賴與封裝。

## Poetry 快速上手

Poetry 使用 `pyproject.toml` 作為設定檔，整合了相依管理與封裝功能。

```bash
# 安裝 Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/install.poetry.org/master/get-poetry.py | python3

# 建立新專案
poetry new my-project
cd my-project

# 新增依賴
poetry add requests
poetry add pytest --dev

# 安裝所有依賴
poetry install

# 執行指令
poetry run python app.py

# 進入 shell
poetry shell
```

### pyproject.toml 範例
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A sample project"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.7"
requests = "^2.22"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### 鎖定與更新
```bash
poetry lock          # 更新 poetry.lock
poetry update        # 更新所有相依
poetry update requests  # 更新特定套件
```

## Pipenv 完整教學

Pipenv 使用 Pipfile 與 Pipfile.lock 管理相依，自動建立與管理虛擬環境。

```bash
# 安裝
pip install pipenv

# 安裝套件
pipenv install requests
pipenv install pytest --dev

# 執行指令
pipenv run python app.py

# 進入 shell
pipenv shell

# 安裝 Pipfile.lock 中的確切版本
pipenv sync
```

### Pipfile 範例
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

## 比較 Poetry 與 Pipenv

| 特性 | Poetry | Pipenv |
|------|--------|--------|
| 設定檔格式 | pyproject.toml | Pipfile |
| 鎖定檔案 | poetry.lock | Pipfile.lock |
| 封裝支援 | 原生支援 | 需額外設定 |
| 速度 | 較快 | 中等 |
| 社群活躍度 | 快速成長 | 穩定 |

## 遷移建議

從傳統專案遷移到 Poetry：

```bash
# 假設有 requirements.txt
poetry init
poetry add $(cat requirements.txt | tr '\n' ' ')
poetry add --dev $(cat requirements-dev.txt | tr '\n' ' ')
```

## 結論

Poetry 適合需要封裝與發布 Python 庫的專案。Pipenv 適合純應用程式開發。兩者都比傳統的 setup.py + requirements.txt 更加現代且易用。

## 參考資源

- https://www.google.com/search?q=Poetry+Python+dependency+management+tutorial+2020
- https://www.google.com/search?q=Pipenv+Python+environment+management+workflow+2020
- https://www.google.com/search?q=Poetry+vs+Pipenv+comparison+Python+2020