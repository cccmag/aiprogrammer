# GitHub Actions 自動化測試

## 前言

在前面的文章中，我們已經學會如何撰寫測試。但測試只有在「被執行」的時候才有價值。如果每次程式碼變更都需要開發者手動執行測試，很快就會有人「忘記」或「沒時間」執行。GitHub Actions 讓測試自動化變得簡單——每次程式碼提交到 GitHub，CI 管線就會自動執行測試。

## 什麼是 GitHub Actions？

GitHub Actions 是 GitHub 內建的 CI/CD 服務。它使用「工作流」（Workflow）來定義自動化流程——「當某個事件發生時，執行某個工作」。

## 第一個工作流

在專案中建立 `.github/workflows/test.yml`：

```yaml
name: Run Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
    
    - name: Run tests
      run: |
        pytest tests/ -v
```

## 工作流結構解析

### on：觸發條件

```yaml
on:
  push:                 # 當程式碼被推送時
    branches: [main]    # 僅限 main 分支
  pull_request:         # 當有 Pull Request 時
    branches: [main]    # 目標分支是 main
  schedule:             # 定時執行（Cron 表達式）
    - cron: "0 0 * * *"  # 每天 UTC 0:00
  workflow_dispatch:    # 手動觸發
```

### jobs：工作定義

```yaml
jobs:
  test:
    runs-on: ubuntu-latest  # 執行環境
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
```

### strategy.matrix：多版本測試

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
    os: [ubuntu-latest, windows-latest, macos-latest]
```

這會產生 3×3 = 9 個工作，分別測試不同 Python 版本和作業系統的組合。

## 完整測試工作流

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - run: pip install flake8
    - run: flake8 src/ --max-line-length=100

  test:
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip packages
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    
    - run: pip install pytest pytest-cov
    - run: pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml

  coverage-check:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - run: echo "Coverage check passed"
```

## 常見的 Actions

```yaml
# 快取依賴
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

# 上傳測試成果
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results/

# 下載測試成果
- uses: actions/download-artifact@v4
  with:
    name: test-results

# Slack 通知
- uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
  if: always()
```

## 測試結果報告

pytest 可以產生多種格式的測試報告：

```yaml
- name: Run tests with report
  run: |
    pytest tests/ --junitxml=report.xml

- name: Upload test report
  uses: actions/upload-artifact@v4
  with:
    name: pytest-report
    path: report.xml
```

JUnit XML 格式可以被 GitHub Actions 解析，在 PR 頁面上顯示測試結果。

## 環境變數和密鑰

```yaml
- name: Run tests with secrets
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    pytest tests/
```

在 GitHub 專案設定頁面中設定 Secrets，工作流中可以用 `${{ secrets.NAME }}` 存取。

## 條件執行

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && success()
  run: |
    echo "Deploying..."

- name: Notify on failure
  if: failure()
  run: |
    echo "Tests failed!"
```

## 最佳實踐

**保持工作流快速**：10-15 分鐘內完成。如果測試太慢，考慮平行執行或減少不必要的步驟。

**使用快取**：快取 pip 套件和測試資料，避免每次建置都重新下載。

**設定品質門檻**：覆蓋率低於閾值時讓 CI 失敗。

**分離工作階段**：lint、單元測試、整合測試分開執行，快速回饋在前。

## 小結

GitHub Actions 讓自動化測試變得簡單而強大。透過 CI 管線，每次程式碼提交都會自動觸發測試執行，確保新程式碼不會破壞既有功能。設定 CI 管線可能需要一些初始工作，但它帶來的回饋——「主分支永遠是健康的」——是無價的。

## 延伸閱讀

- [GitHub Actions 官方文件](https://www.google.com/search?q=GitHub+Actions+documentation)
- [Python CI/CD 最佳實踐](https://www.google.com/search?q=Python+CI+CD+GitHub+Actions)
- [Actions Marketplace](https://www.google.com/search?q=GitHub+Actions+Marketplace)
