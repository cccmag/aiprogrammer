# 自動化測試與 CI/CD

## 前言

持續整合和持續交付是現代軟體開發的核心實踐。

---

## CI/CD 概念

### 持續整合 (CI)

開發者頻繁地將程式碼合併到主分支，每次合併都會自動建置和測試。

### 持續交付 (CD)

程式碼變更可以隨時部署到生產環境。

### 持續部署

每個通過測試的變更自動部署到生產環境。

---

## CI 系統比較

| 系統 | 優點 |
|------|------|
| Jenkins | 開源、強大、社群豐富 |
| Travis CI | 與 GitHub 整合簡單 |
| CircleCI | 速度快、設定簡單 |
| GitLab CI | 與 GitLab 緊密整合 |
| GitHub Actions | GitHub 原生、功能豐富 |

[搜尋 CI tools comparison 2015](https://www.google.com/search?q=CI+tools+comparison+2015)

---

## 測試金字塔

```
        /\
       /  \      E2E Tests (少量)
      /    \
     /------\    Integration Tests (適量)
    /        \
   /----------\  Unit Tests (大量)
  /            \
 /______________\ Source Code
```

---

## 測試範例

### 單元測試

```python
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
    
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

if __name__ == '__main__':
    unittest.main()
```

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Python Tests
on: [push, pull_request]
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
          pip install pytest
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

### Travis CI

```yaml
# .travis.yml
language: python
python:
  - "3.8"
install:
  - pip install -r requirements.txt
script:
  - pytest
```

---

## 自動化部署

### 部署流程

```bash
# 建置
npm run build

# 測試
npm test

# 部署
npm run deploy
```

### Blue-Green Deployment

```bash
# 啟動新版本（green）
docker-compose up -d green

# 測試新版本
curl http://green.example.com/health

# 切換流量
nginx -s reload

# 關閉舊版本（blue）
docker-compose stop blue
```

### Canary Deployment

逐漸將流量轉移到新版本：

```bash
# 10% 流量到新版本
kubectl scale deployment myapp-v2 --replicas=1
# 逐漸增加...
```

---

## 鉤子 (Hooks)

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 執行測試
npm test

if [ $? -ne 0 ]; then
    echo "測試失敗，提交被拒絕"
    exit 1
fi

# Lint 檢查
npm run lint
if [ $? -ne 0 ]; then
    echo "Lint 失敗，提交被拒絕"
    exit 1
fi
```

### Pre-push Hook

```bash
#!/bin/bash
# .git/hooks/pre-push

# 確保分支是最新的
git fetch origin
main_local=$(git rev-parse HEAD)
main_remote=$(git rev-parse origin/main)

if [ "$main_local" != "$main_remote" ]; then
    echo "主分支落後於遠端，請先 pull"
    exit 1
fi
```

---

## 小結

自動化測試和 CI/CD 是提升軟體品質和交付速度的關鍵實踐。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Travis CI 教學](https://www.google.com/search?q=Travis+CI+tutorial)
- [Jenkins 使用指南](https://www.google.com/search?q=Jenkins+tutorial+for+beginners)