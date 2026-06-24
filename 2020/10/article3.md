# GitHub Actions 自動化工作流

## 前言

GitHub Actions 是 GitHub 提供的 CI/CD 功能，允許你在 GitHub 倉庫中自動建構、測試和部署程式碼。它與 GitHub 深度整合，無需額外的外部服務就能實現完整的自動化流程。

## 基本概念

### Workflow、Job、Step、Action

```
GitHub Actions 結構：
────────────────────────────────

Workflow（工作流）
  └── Job（任務）1
        ├── Step 1: Checkout code
        ├── Step 2: Setup Python
        ├── Step 3: Run tests
        └── Step 4: Deploy
  └── Job（任務）2
        └── ...

Action（動作）：可重用的功能單元
Runner：執行 workflow 的伺服器
```

### 第一個 Workflow

```yaml
# .github/workflows/ci.yml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v --tb=short
```

## 觸發條件

### 多元的觸發方式

```yaml
on:
  # 推送時觸發
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]
    paths:
      - '**.py'
      - 'requirements.txt'
  
  # PR 時觸發
  pull_request:
    branches: [ main ]
    types: [ opened, synchronize, closed ]
  
  # 排程觸發（cron）
  schedule:
    - cron: '0 0 * * *'  # 每天午夜
  
  # 手動觸發
  workflow_dispatch:
    inputs:
      version:
        description: '版本號'
        required: true
        default: '1.0.0'
  
  # 其他事件
  release:
    types: [ published, created ]
  issue_comment:
    types: [ created, edited ]
```

## 矩陣策略

### 同時測試多個環境

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.7, 3.8, 3.9]
        exclude:
          - os: macos-latest
            python-version: 3.7

    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest --tb=short
```

## 快取加速

### 依賴快取

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
          cache: 'pip'  # 自動快取 pip 依賴
      
      # 或者手動設定快取
      - name: Cache pip packages
        uses: actions/cache@v2
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: pip install -r requirements.txt
```

## 部署

### 部署到 PyPI

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install setuptools wheel twine
      
      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: |
          python setup.py sdist bdist_wheel
          twine upload dist/*
```

### 部署到 Heroku

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

### 部署到 AWS

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Build and deploy
        run: |
          aws s3 sync ./dist s3://my-bucket/
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DISTRIBUTION_ID }} --paths "/*"
```

## 環境和 Secrets

### 管理敏感資訊

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    
    env:
      APP_ENV: production
      # 從 secrets 注入
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    
    steps:
      - name: Deploy
        run: |
          echo "Deploying to ${{ env.APP_ENV }}"
          echo "Database: ${{ secrets.DATABASE_URL }}"
```

### 在 Secrets 中設定敏感資訊

```
Settings → Secrets → New secret

常用 Secrets：
- PYPI_TOKEN: PyPI API token
- HEROKU_API_KEY: Heroku API key
- AWS_ACCESS_KEY_ID: AWS access key
- DATABASE_URL: 資料庫連接字串
```

## 完整範例

```yaml
name: Python Package CI/CD

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install lint tools
        run: pip install black flake8
      - name: Check formatting
        run: black --check .
      - name: Run linter
        run: flake8 .

  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: [3.7, 3.8, 3.9]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov
      - name: Run tests
        run: pytest --cov=src --cov-report=xml

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Build distribution
        run: |
          python setup.py sdist bdist_wheel
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: dist
          path: dist/

  release:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    steps:
      - uses: actions/download-artifact@v2
        with:
          name: dist
          path: dist/
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@master
        with:
          password: ${{ secrets.PYPI_TOKEN }}
```

## 延伸閱讀

- [GitHub Actions 官方文件](https://www.google.com/search?q=GitHub+Actions+documentation)
- [Actions 市場](https://www.google.com/search?q=GitHub+Actions+marketplace)
- [Python 測試範例](https://www.google.com/search?q=GitHub+Actions+Python+testing+example)
- [快取依賴](https://www.google.com/search?q=GitHub+Actions+cache+pip+dependencies)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」文章集錦之一。*