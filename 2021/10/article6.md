# 測試報告與持續整合

## 測試報告的價值

好的測試報告讓你一眼看出專案健康狀況。Coverage.py 可以產生詳細的覆蓋率報告：

```bash
coverage run -m pytest
coverage html  # 產生 HTML 報告
coverage report  # 終端輸出
```

## pytest-html

產生視覺化的 HTML 報告：

```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

報告包含測試結果、執行時間、環境資訊等。

## JUnit XML 格式

CI 系統通常需要 JUnit XML 格式：

```bash
pytest --junit-xml=test-results.xml
```

GitHub Actions、GitLab CI 等可以直接解析這個格式。

## Allure 報告

Allure 提供更豐富的報告功能：

```bash
pip install allure-pytest
pytest --alluredir=allure-results
allure serve allure-results
```

## GitHub Actions 整合

完整的 CI 配置：

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Cache pip
        uses: actions/cache@v2
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      - name: Install
        run: pip install -r requirements.txt
      - name: Test
        run: pytest --cov=src --junitxml=test-results.xml
      - name: Coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
```

## 測試並行化

使用 pytest-xdist 加速測試：

```bash
pip install pytest-xdist
pytest -n auto  # 自動使用所有 CPU 核心
pytest -n 4     # 使用 4 個程序
```

## 測試環境配置

測試環境應與生產環境相似但隔離：

```python
# conftest.py
import os

@pytest.fixture(autouse=True)
def test_env():
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test_db"
    os.environ["REDIS_URL"] = "redis://localhost:6379/1"
```

## 結論

完善的測試報告和 CI 整合是現代開發的必要條件。投資這些基礎設施，讓團隊能及時發現和解決問題。