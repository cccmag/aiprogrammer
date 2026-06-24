# CI/CD 管線設計

## 持續整合與持續交付

### 前言

CI/CD（持續整合/持續交付）是 DevOps 的核心實踐。它通過自動化管線將程式碼從開發者的機器一路送到生產環境，確保每次變更都經過完整的測試和驗證。本節將探討如何設計高效的 CI/CD 管線。

### 持續整合（CI）

CI 的核心是讓開發者頻繁地將程式碼合併到共用分支，每次合併都觸發自動化構建和測試。

**CI 的目標**：
- 及早發現整合問題
- 確保程式碼品質
- 提供快速反饋

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

### 持續交付（CD）

CD 在 CI 的基礎上確保軟體可以隨時部署到生產環境。持續交付意味著每次提交都是可部署的。

**CD 的目標**：
- 自動化部署流程
- 確保發布可靠性
- 支援快速回滾

### 管線階段劃分

典型的 CI/CD 管線包含以下階段：

**1. 程式碼檢查（Lint）**

確保程式碼風格和基本品質：

```bash
npm run lint
npx prettier --check .
```

**2. 單元測試**

驗證每個模組的正確性：

```bash
npm run test:unit
npm run test:coverage
```

**3. 構建（Build）**

產出可部署的構建產物：

```bash
npm run build
docker build -t myapp .
```

**4. 整合測試**

驗證各元件間的協作：

```bash
docker compose up -d
npm run test:integration
docker compose down
```

**5. 部署（Deploy）**

將產物部署到目標環境：

```bash
# 藍綠部署
kubectl set image deployment/myapp-blue myapp=myapp:v2
kubectl rollout status deployment/myapp-blue
kubectl set image deployment/myapp-green myapp=myapp:v1
```

### 品質閘道（Quality Gate）

在管線關鍵階段設置檢查點，確保只有符合品質標準的程式碼才能進入下一階段：

```javascript
const qualityGate = {
  testCoverage: 80,         // 測試覆蓋率 ≥ 80%
  lintErrors: 0,            // 無 lint 錯誤
  securityScan: 'pass',     // 安全掃描通過
  buildSize: '50MB'         // 構建產物 ≤ 50MB
};
```

### 管線設計原則

**1. 快速反饋**

管線應在短時間內（通常 < 10 分鐘）提供反饋。將耗時任務（如 E2E 測試）放在審批階段之前。

**2. 冪等性**

管線應可重複執行，無論執行多少次，結果應一致。

**3. 並行執行**

獨立任務應並行執行以節省時間：

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

**4. 環境一致性**

管線各階段應使用一致的執行環境。容器化是實現環境一致性的最佳方式。

### 小結

CI/CD 管線是 DevOps 自動化部署的核心。從程式碼提交到生產環境部署，每個環節都經過自動化驗證，既加快了交付速度，又保證了軟體品質。下一節將深入探討 GitHub Actions 的實戰應用。

---

**下一步**：[GitHub Actions 實戰](focus5.md)

## 延伸閱讀

- [CI/CD Pipeline 設計模式](https://www.google.com/search?q=CI+CD+pipeline+design+patterns)
- [持續交付：可靠軟體發布](https://www.google.com/search?q=Continuous+Delivery+book)
