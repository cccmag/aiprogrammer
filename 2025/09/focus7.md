# CI/CD 與自動化測試

## 讓測試成為開發流程的一部分

### 前言

即使你在本地端寫了完美的測試，如果沒有人定期執行它們，這些測試的價值就大打折扣。持續整合（Continuous Integration，CI）和持續部署（Continuous Deployment，CD）的核心思想是：**每次程式碼變更都應該自動觸發測試和部署流程**。

### 什麼是 CI/CD？

**持續整合（CI）**：開發者頻繁地（每天多次）將程式碼合併到主分支，每次合併都自動觸發建置和測試流程。目的是及早發現整合問題。

**持續部署（CD）**：通過所有測試的程式碼自動部署到生產環境。目標是讓軟體交付變得快速、可靠、可重複。

```
開發者提交程式碼 → CI 伺服器觸發建置 → 執行測試 → 
通過 → 自動部署到測試環境 → 自動部署到生產環境
```

### GitHub Actions 基礎

GitHub Actions 是 GitHub 內建的 CI/CD 服務。以下是一個基本的 Python 測試工作流：

```yaml
# .github/workflows/test.yml
name: Run Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
    
    - name: Run tests with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
```

### 測試在 CI 管線中的角色

一個完整的 CI 管線通常包含以下階段：

**1. 程式碼檢查（Lint）**

```yaml
- name: Lint with flake8
  run: |
    flake8 src/ tests/ --max-line-length=100
```

**2. 靜態型別檢查（Type Check）**

```yaml
- name: Type check with mypy
  run: |
    mypy src/
```

**3. 單元測試**

```yaml
- name: Run unit tests
  run: |
    pytest tests/unit/ --cov=src --cov-fail-under=80
```

**4. 整合測試**

```yaml
- name: Run integration tests
  run: |
    docker-compose up -d
    pytest tests/integration/ --timeout=60
    docker-compose down
```

**5. 程式碼覆蓋率報告**

```yaml
- name: Upload coverage report
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: htmlcov/
```

### 多階段 CI 工作流

對於較大的專案，可以將 CI 分成多個工作（job），平行執行以加快速度：

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install flake8 && flake8 src/

  test:
    runs-on: ubuntu-latest
    needs: lint  # 依賴 lint 完成
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest && pytest tests/

  deploy:
    runs-on: ubuntu-latest
    needs: test  # 依賴 test 完成
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "Deploying to production..."
```

### 常見的 CI 服務比較

| 服務 | 免費額度 | 優點 | 缺點 |
|------|---------|------|------|
| GitHub Actions | 2000 分鐘/月 | 整合 GitHub、生態豐富 | 僅限 GitHub |
| GitLab CI | 400 分鐘/月 | 整合 GitLab、Kubernetes | 學習曲線較高 |
| Jenkins | 完全免費 | 高度可自訂 | 需要自行維護 |
| CircleCI | 6000 分鐘/月 | 速度快、快取機制佳 | 設定較複雜 |

### CI/CD 中的測試策略

**閘門（Quality Gates）**

設定最低品質標準，未達標的建置直接拒絕：

- 測試通過率：100%（不能有失敗的測試）
- 程式碼覆蓋率：不低於 80%
- 靜態分析：零重大違規

**分層測試**

在 CI 管線中分層執行測試，快速回饋在前：

```yaml
# 先在 2 分鐘內執行單元測試
- run: pytest tests/unit/ --timeout=30 -x

# 再執行較慢的整合測試
- run: pytest tests/integration/ --timeout=120

# 最後執行 E2E 測試（只在 main 分支執行）
- if: github.ref == 'refs/heads/main'
  run: pytest tests/e2e/
```

**快取依賴**

善用 CI 的快取功能，避免每次建置都重新安裝依賴：

```yaml
- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 自動化測試報告

當測試失敗時，開發者需要立即知道出了什麼問題。現代 CI 工具支援多種通知方式：

- **PR 註解**：在 Pull Request 上自動加上測試結果註解
- **Slack/Email 通知**：測試失敗時即時通知相關開發者
- **Badge**：在 README 上顯示建置狀態徽章

### 小結

CI/CD 將測試從「開發者的選擇」變成了「開發流程的強制環節」。當每次提交都會自動觸發測試執行，測試就不再是被忽略的選項，而是程式碼品質的保障。更重要的是，CI/CD 讓團隊對「主分支永遠是可部署的」這件事建立了信心——這正是敏捷開發和持續交付的基礎。

---

## 延伸閱讀

- [GitHub Actions 文件](https://www.google.com/search?q=GitHub+Actions+documentation)
- [CI/CD 最佳實踐](https://www.google.com/search?q=CI+CD+best+practices)
- [Python CI/CD 管線設定](https://www.google.com/search?q=Python+CI+CD+pipeline+setup)
