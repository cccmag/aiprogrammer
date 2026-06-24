# CI/CD 中的 Python 環境

## GitHub Actions

```yaml
# .github/workflows/python.yml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8]
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v1
        with:
          python-version: ${{ matrix.python-version }}
      - name: Cache pip
        uses: actions/cache@v1
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## 使用 Poetry

```yaml
- name: Install Poetry
  run: |
    curl -sSL https://raw.githubusercontent.com/python-poetry/install.poetry.org/master/get-poetry.py | python3
- name: Install dependencies
  run: poetry install
- name: Run tests
  run: poetry run pytest
```

## 使用 Pipenv

```yaml
- name: Install Pipenv
  run: pip install pipenv
- name: Install dependencies
  run: pipenv install --dev
- name: Run tests
  run: pipenv run pytest
```

## 使用 Docker

```yaml
- name: Build Docker
  run: docker build -t myapp .
- name: Test with Docker
  run: docker run myapp pytest
```

## 多平台測試

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v1
        with:
          python-version: 3.8
      - name: Install
        run: pip install -r requirements.txt
      - name: Test
        run: pytest
```

## 自動化發布

```yaml
- name: Publish to PyPI
  if: startsWith(github.ref, 'refs/tags/')
  run: |
    poetry build
    poetry publish
  env:
    POETRY_PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

## 快取依賴

```yaml
- name: Cache pip
  uses: actions/cache@v2
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

## 參考資源

- https://www.google.com/search?q=GitHub+Actions+Python+CI+CD+tutorial+2020
- https://www.google.com/search?q=Python+Poetry+Pipenv+GitHub+Actions+workflow
- https://www.google.com/search?q=Python+automated+testing+CI+pipeline+best+practices