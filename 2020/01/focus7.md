# 7. Python 專案最佳實踐

## 標準專案結構

一個良好的 Python 專案結構：

```
my-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
└── docs/
```

## 版本控制設定

.gitignore 範例：
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.venv/
venv/
env/
*.egg
.pytest_cache/
.mypy_cache/
```

## 程式碼品質工具

### Black（格式化）
```bash
pip install black
black .
```

### isort（匯入排序）
```bash
pip install isort
isort .
```

### Flake8（風格檢查）
```bash
pip install flake8
flake8 .
```

### pre-commit
```bash
pip install pre-commit
# 建立 .pre-commit-config.yaml
pre-commit install
```

## 測試

### pytest
```bash
pip install pytest pytest-cov
pytest --cov=src tests/
```

## 型態檢查

### mypy
```bash
pip install mypy
mypy src/
```

## CI/CD

GitHub Actions 範例（.github/workflows/ci.yml）：
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v1
        with:
          python-version: 3.8
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run tests
        run: poetry run pytest
```

## 文件

使用 Sphinx 或 MkDocs 建立文件：

```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs
```

## 發布到 PyPI

```bash
# Poetry 發布
poetry build
poetry publish

# 自動化發布（需設定 API token）
```

## 開源授權

常見授權選擇：
- **MIT**：最寬鬆，適合開源專案
- **Apache 2.0**：允許專利授權
- **GPL 3.0**：要求衍生作品也必須開源

## 參考資源

- https://www.google.com/search?q=Python+project+structure+best+practices+2020+template
- https://www.google.com/search?q=Python+code+quality+tools+Black+isort+flake8+pre-commit+2020
- https://www.google.com/search?q=Python+CI+CD+GitHub+Actions+setup+best+practices