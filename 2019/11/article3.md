# GitHub Actions 正式版：CI/CD 新選擇

## 前言

GitHub Actions 在 2019 年 11 月正式脫離 Beta，成為 GitHub 的核心功能。本篇文章將介紹 GitHub Actions 的功能、優勢以及如何使用它來自動化軟體開發流程。

## GitHub Actions 概述

### 什麼是 GitHub Actions

GitHub Actions 是 GitHub 提供的 CI/CD 和自動化平臺：

```
功能：
- 自動化建構、測試、部署
- 自訂工作流程
- 與 GitHub 深度整合
```

### 核心概念

GitHub Actions 的核心概念：

```
Workflow（工作流程）：
- YAML 檔案定義
- 觸發條件
- 多個 Jobs

Job（任務）：
- 由 Steps 組成
- 在 Runner 上執行
- 可以並行

Step（步驟）：
- 單一操作
- 可以使用 Action 或 shell 命令

Action（動作）：
- 可重用的組件
- 可以是市場上的或自訂的
```

## 快速開始

### 建立第一個 Workflow

在專案根目錄建立 `.github/workflows/main.yml`：

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Node.js
        uses: actions/setup-node@v1
        with:
          node-version: '12.x'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test
```

## 常用功能

### 矩陣建構

支援同時測試多個版本組合：

```yaml
jobs:
  test:
    strategy:
      matrix:
        node-version: [10.x, 12.x, 14.x]
        os: [ubuntu-latest, windows-latest]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v2
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v1
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### 快取依賴

可以快取 node_modules 加速建構：

```yaml
- name: Cache node_modules
  uses: actions/cache@v2
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### 部署到雲端

GitHub Actions 支援多種部署目標：

```yaml
# 部署到 AWS
- name: Deploy to AWS
  uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1
```

## 與其他 CI/CD 工具的比較

| 特性 | GitHub Actions | Jenkins | Travis CI |
|------|----------------|---------|-----------|
| 費用 | 免費（有限額） | 自架 | 免費/付費 |
| 整合 | GitHub 深度整合 | 需要設定 | 需要設定 |
| 學習曲線 | 較低 | 較高 | 中等 |
| 市場 | 豐富的 Action 市場 | 豐富的插件 | 一般 |

## GitHub Actions 的優勢

### 與 GitHub 無縫整合

最大的優勢是與 GitHub 的深度整合：

```
整合優勢：
- PR 狀態直接在 PR 頁面顯示
- 自動觸發基於 Git 事件
- 與 Issues、Releases 整合
- 簡單的 secrets 管理
```

### 共享和可重用

Action 市場讓工作流程更容易共享：

```yaml
# 使用市場上的 Action
- name: Send to Slack
  uses: rtCamp/action-slack-notify@v2
  env:
    SLACK_CHANNEL: general
```

### 免費配額

GitHub Actions 有免費配額：

```
免費配額（公共倉庫）：
- 無限建構分鐘數

免費配額（私人倉庫）：
- 2000 分鐘/月（免費版）
- 3000 分鐘/月（付費版）
```

## 實用技巧

### 條件執行

可以根據條件跳過或執行特定步驟：

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

### 並行 Jobs

加速建構：

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - ...

  lint:
    runs-on: ubuntu-latest
    steps:
      - ...
```

## 結論

GitHub Actions 的正式版為開發者提供了一個強大且易用的 CI/CD 平臺。與 GitHub 的深度整合、豐富的 Action 市場、以及合理的免費配額，使其成為中小型專案的理想選擇。建議開發者開始探索 GitHub Actions，為自己的專案建立自動化工作流程。

---

**延伸閱讀**

- [GitHub+Actions+官方文檔](https://www.google.com/search?q=GitHub+Actions+documentation)
- [GitHub+Actions+tutorial](https://www.google.com/search?q=GitHub+Actions+workflow+tutorial)
- [GitHub+Marketplace+Actions](https://www.google.com/search?q=GitHub+Marketplace+Actions)