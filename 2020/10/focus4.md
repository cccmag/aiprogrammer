# CI/CD 與 GitHub Actions：自動化測試與部署

## 持續整合/持續部署的概念

### CI/CD 是什麼？

```
CI/CD 流程：
────────────────────────────────────────────────────────

  程式碼提交     自動化測試     建構         部署
     │              │           │            │
     ▼              ▼           ▼            ▼
┌────────┐    ┌──────────┐   ┌────────┐   ┌────────┐
│  Git   │───►│  CI 伺服器 │──►│ Build  │──►│  Production │
│ Commit │    │ (測試)   │   │        │   │  Server     │
└────────┘    └──────────┘   └────────┘   └────────┘
                   │                         ▲
                   ▼                         │
              ┌──────────┐              ┌──────────┐
              │  回報結果 │              │  CD 系統 │
              └──────────┘              └──────────┘
```

**持續整合（CI）**：開發者頻繁地將程式碼整合到主分支，每次整合都自動執行測試

**持續部署（CD）**：透過自動化將通過測試的程式碼部署到各種環境

### 為什麼需要 CI/CD？

- **快速發現問題**：每次提交都執行測試，及早發現 Bug
- **確保程式碼品質**：沒有通過測試的程式碼不會被部署
- **加速交付**：自動化減少了人為錯誤和等待時間
- **可追溯性**：每次部署都有完整的記錄

## GitHub Actions

### 基本概念

GitHub Actions 是 GitHub 提供的 CI/CD 功能，現在幾乎每個開源專案都在使用：

```
GitHub Actions 核心概念：
────────────────────────────────

Workflow（工作流）：整個自動化流程（.yml 檔案）
Job（任務）：一個 workflow 中的獨立工作單元
Step（步驟）：一個 job 中的具體操作
Action（動作）：可重用的 action，可以是市集的或自訂的
Runner：執行 workflow 的伺服器（GitHub-hosted 或 self-hosted）
```

### 第一個 Workflow

```yaml
# .github/workflows/test.yml
name: Python Tests

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
    
    - name: Cache pip packages
      uses: actions/cache@v2
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
```

### 測試矩陣

同時測試多個 Python 版本和作業系統：

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.7, 3.8, 3.9]
    
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Run tests
        run: pytest
```

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
          heroku_app_name: "my-app"
          heroku_email: "my@email.com"
```

## 其他 CI/CD 工具

### GitLab CI

```yaml
# .gitlab-ci.yml
image: python:3.8

stages:
  - test
  - deploy

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest

deploy:
  stage: deploy
  script:
    - pip install fabric
    - fab deploy
  only:
    - main
```

### Travis CI

```yaml
# .travis.yml
language: python
python:
  - "3.7"
  - "3.8"
  - "3.9"

install:
  - pip install -r requirements.txt

script:
  - pytest --cov=src

deploy:
  provider: pypi
  user: __token__
  password: $PYPI_PASSWORD
  on:
    tags: true
```

## 自動化工作流範例

### 完整的 Python 專案工作流

```yaml
name: Python Project CI/CD

on:
  push:
    branches: [ main ]
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
      - name: Lint with black and flake8
        run: |
          pip install black flake8
          black --check .
          flake8 .

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9]
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -r requirements.txt pytest
      - name: Run tests
        run: pytest -v

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker tag myapp:${{ github.sha }} myregistry/myapp:latest

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to staging
        run: |
          # 部署到測試環境的指令
          echo "Deploying to staging..."

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    steps:
      - name: Deploy to production
        run: |
          # 部署到生產環境的指令
          echo "Deploying to production..."
```

## 延伸閱讀

- [GitHub Actions 官方文件](https://www.google.com/search?q=GitHub+Actions+documentation)
- [GitHub Actions 市場](https://www.google.com/search?q=GitHub+Actions+marketplace)
- [Python 測試最佳實踐](https://www.google.com/search?q=Python+testing+best+practices+CI)
- [Pytest GitHub Actions](https://www.google.com/search?q=pytest+GitHub+Actions+example)
- [GitLab CI Python 教學](https://www.google.com/search?q=GitLab+CI+Python+tutorial)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」歷史回顧系列之一。*