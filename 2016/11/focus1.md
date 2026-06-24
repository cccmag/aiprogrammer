# CI/CD 基礎概念（2010-2016）

## 前言

持續整合（CI）與持續交付（CD）是現代軟體開發的基石，讓團隊能快速、可靠地交付軟體。

## CI/CD 流程

```
提交 → 建置 → 測試 → 分析 → 部署（測試）→ 部署（正式）
 │        │       │       │         │            │
 Git    Build   Unit    Code     Staging     Production
 Hook   Server  Test    Analysis   Deploy       Deploy
```

## 持續整合（CI）

### 核心原則

1. **頻繁提交**：每天多次提交程式碼
2. **自動化建置**：每次提交觸發建置
3. **快速回饋**：盡快發現問題
4. **透明可見**：所有人看到狀態

### CI 流程

```bash
#!/bin/bash
# ci-build.sh

set -e

echo "=== CI Build Started ==="
echo "Commit: $GIT_COMMIT"
echo "Branch: $GIT_BRANCH"

# 安裝依賴
echo "Installing dependencies..."
npm install

# Lint
echo "Running linter..."
npm run lint
if [ $? -ne 0 ]; then
    echo "Lint failed!"
    exit 1
fi

# 單元測試
echo "Running tests..."
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi

# 建置
echo "Building..."
npm run build
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo "=== CI Build Completed ==="
```

## 持續交付（CD）

### 部署環境層級

```yaml
# deployment-stages.yaml
stages:
  - name: development
    auto_deploy: true
    description: 開發環境，自動部署
  
  - name: staging
    auto_deploy: false
    description: 測試環境，需手動核准
  
  - name: production
    auto_deploy: false
    description: 正式環境，需嚴格審核
```

### 部署腳本

```bash
#!/bin/bash
# deploy.sh

DEPLOY_ENV=$1
APP_NAME="myapp"
DEPLOY_DIR="/var/www/$APP_NAME"

case $DEPLOY_ENV in
    development)
        DEPLOY_DIR="/var/www/dev-$APP_NAME"
        ;;
    staging)
        DEPLOY_DIR="/var/www/staging-$APP_NAME"
        ;;
    production)
        DEPLOY_DIR="/var/www/prod-$APP_NAME"
        ;;
    *)
        echo "Unknown environment: $DEPLOY_ENV"
        exit 1
        ;;
esac

echo "Deploying to $DEPLOY_ENV..."

# 備份
if [ -d "$DEPLOY_DIR" ]; then
    rsync -av --delete "$DEPLOY_DIR/" "/backup/$(date +%Y%m%d%H%M%S)/"
fi

# 部署新版本
rsync -av --exclude='.git' --exclude='node_modules' ./ "$DEPLOY_DIR/"

# 重啟服務
ssh deploy@server "sudo systemctl restart $APP_NAME"

echo "Deployment completed!"
```

## 版本控制策略

### Git Flow

```bash
# 主要分支
main (production)
develop (integration)

# 支援分支
feature/xxx     # 功能分支
release/x.x.x   # 發布分支
hotfix/x.x.x    # 緊急修復
```

### 語意化版本

```
major.minor.patch
  │     │     │
  │     │     └── 修正問題
  │     └──────── 新功能（向後相容）
  └────────────── 破壞性改變
```

## CI/CD 工具比較

| 工具 | 類型 | 優勢 | 劣勢 |
|------|------|------|------|
| Jenkins | 開源 | 功能豐富、插件多 | 設定複雜 |
| Travis CI | 雲端 | 與 GitHub 整合佳 | 私人專案收費 |
| GitLab CI | 整合 | 完整 DevOps 平台 | 規模限制 |
| CircleCI | 雲端 | 速度快 | 配置限制 |

## 相關資源

- [CI/CD 基礎概念](https://www.google.com/search?q=CI+CD+pipeline+basics+2016)
- [Jenkins 官方文檔](https://www.google.com/search?q=jenkins+tutorial+2016)
- [DevOps 最佳實踐](https://www.google.com/search?q=devops+best+practices+2016)

## 結語

CI/CD 不只是工具鏈，更是開發文化的轉變。自動化每一個步驟，讓交付變得可預測且快速。

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*