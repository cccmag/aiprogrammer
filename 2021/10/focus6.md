# CI/CD 整合與自動化測試

## CI/CD 的價值

持續整合（CI）和持續交付（CD）是現代軟體開發的基石。每次程式碼變更都會觸發自動化測試，確保品質不會隨時間推移而下降。對於 Python 專案，有許多工具可以實現這一點。

## GitHub Actions

GitHub Actions 是最流行的 CI 工具之一，與 GitHub 緊密整合：

```yaml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=my_package
```

## 測試矩陣

使用矩陣策略在多個 Python 版本和作業系統上測試：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: [3.8, 3.9, "3.10"]
```

這確保了你的程式碼在不同環境下都能正常運作。

## 自動化檢查

除了測試，CI 流程還可以包含：

- 程式碼風格檢查（Black、Flake8）
- 靜態類型檢查（mypy）
- 安全掃描（Bandit）
- 依賴審查（pip-audit）

## 部署自動化

測試通過後，CI 可以自動部署到各種環境：

```yaml
- name: Deploy to PyPI
  if: github.ref == 'refs/heads/main'
  run: |
    pip install twine
    twine upload dist/*
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

## 快取依賴

加速 CI 執行：

```yaml
- name: Cache pip packages
  uses: actions/cache@v2
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

## 測試報告

上傳測試結果供視覺化分析：

```yaml
- name: Upload coverage
  uses: codecov/codecov-action@v2
  with:
    file: ./coverage.xml
```

## 最佳實踐

保持 CI 快速（幾分鐘內完成），使用並行測試，早期失敗（快速檢查先執行）。好的 CI 設定能讓團隊有信心地持續交付高品質軟體。