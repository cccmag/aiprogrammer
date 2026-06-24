# GitHub Actions 開放：CI/CD 整合新選擇

## 前言

GitHub Actions 於 2019 年 8 月正式開放，為開源專案和商業專案提供了免費的 CI/CD 解決方案。

## 基本概念

### Workflow（工作流程）

```yaml
# .github/workflows/ci.yml
name: CI

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
        uses: actions/setup-python@v1
        with:
          python-version: '3.7'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/
```

## 常見工作流程

### 自動測試

```yaml
- name: Run pytest
  run: |
    pytest --cov=src tests/
```

### 自動部署

```yaml
- name: Deploy to Heroku
  if: github.ref == 'refs/heads/main'
  run: |
    git push https://heroku:${{ secrets.HEROKU_API_KEY }}@git.heroku.com/${{ secrets.HEROKU_APP_NAME }}.git main
```

### Docker 構建

```yaml
- name: Build Docker image
  run: |
    docker build -t myapp:${{ github.sha }} .
    docker tag myapp:${{ github.sha }} myapp:latest
```

## 使用別人的 Action

```yaml
# 使用市場上的 Action
- uses: actions/setup-node@v1
  with:
    node-version: '12.x'

- uses: actions/cache@v1
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

## 結論

GitHub Actions 的開放使得 CI/CD 流程更加便捷，許多開源專案已經從其他 CI 服務遷移到 GitHub Actions。

---

**延伸閱讀**

- [GitHub Actions 文檔](https://www.google.com/search?q=GitHub+Actions+documentation)
- [GitHub Actions 市場](https://www.google.com/search?q=GitHub+Actions+marketplace)