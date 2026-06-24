# GitHub Actions 實戰

## 工作流語法與應用

### 前言

GitHub Actions 是 GitHub 內建的 CI/CD 平台，它以事件驅動的方式自動化軟體開發工作流程。本節將從實戰角度探討如何使用 GitHub Actions 構建完整的 CI/CD 管線。

### 工作流基礎

每個工作流程定義在 `.github/workflows/` 目錄下的 YAML 檔案中：

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

### 事件觸發器

GitHub Actions 支援多種觸發事件：

```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'tests/**'
  pull_request:
    types: [opened, synchronize, reopened]
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨 2 點
  workflow_dispatch:       # 手動觸發
```

### 矩陣構建（Matrix Build）

使用矩陣策略同時測試多種環境：

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
        include:
          - os: ubuntu-latest
            node: 20
            coverage: true
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
      - if: ${{ matrix.coverage }}
        run: npm run coverage
```

### 快取依賴

加速工作流程執行：

```yaml
- name: Cache Node.js modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 建置與推送 Docker 映像

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: user/myapp:${{ github.sha }}
```

### 部署到雲端

```yaml
deploy:
  needs: [test, build]
  runs-on: ubuntu-latest
  environment: production
  steps:
    - name: Deploy to AWS ECS
      run: |
        aws ecs update-service \
          --cluster my-cluster \
          --service my-service \
          --force-new-deployment
```

### 自訂 Action

建立可重複使用的 Action：

```yaml
# .github/actions/deploy/action.yml
name: 'Deploy to Server'
description: 'Deploy application to remote server'
inputs:
  server:
    description: 'Target server'
    required: true
runs:
  using: 'composite'
  steps:
    - run: ssh ${{ inputs.server }} "docker compose pull && docker compose up -d"
      shell: bash
```

### 安全實踐

- 使用 Secrets 管理敏感資訊
- 限制工作流程權限
- 審查第三方 Action

### 小結

GitHub Actions 提供了強大且靈活的 CI/CD 平台。通過矩陣構建、快取機制和自訂 Action，團隊可以建立適合自身專案的高效自動化管線。

---

**下一步**：[監控與日誌管理](focus6.md)

## 延伸閱讀

- [GitHub Actions 文件](https://www.google.com/search?q=GitHub+Actions+documentation)
- [Actions Marketplace](https://www.google.com/search?q=GitHub+Actions+Marketplace)
