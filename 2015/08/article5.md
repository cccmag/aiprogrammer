# 自動化部署流程設計

## 前言

自動化部署是 DevOps 的核心實踐，能大幅提升軟體交付的速度和可靠性。

---

## CI/CD 概念

### 持續整合 (CI)

每次程式碼變更自動觸發建置和測試：

```
開發者推送 → 觸發建置 → 執行測試 → 報告結果
```

### 持續交付 (CD)

通過所有測試後，隨時可以部署：

```
CI 成功 → 部署到預備環境 → 手動審核 → 部署到生產
```

### 持續部署 (CD')

每個變更自動部署到生產環境：

```
CI 成功 → 部署到預備環境 → 自動部署到生產
```

---

## 部署流程設計

### 環境設計

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   開發環境  │ ──> │  測試環境   │ ──> │  預備環境   │
│  (本地)     │     │ (自動測試)  │     │ (整合測試)  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                                v
                                        ┌─────────────┐
                                        │  生產環境   │
                                        │  (部署)     │
                                        └─────────────┘
```

### 部署策略

1. **直接部署**：停止舊版，啟動新版
2. **滾動部署**：逐步替換
3. **藍綠部署**：準備兩套環境，瞬間切換
4. **金絲雀部署**：逐步增加流量

---

## 工具選擇

### CI 伺服器

| 工具 | 優點 |
|------|------|
| Jenkins | 免費、功能強大、擴展性高 |
| GitLab CI | 與 GitLab 緊密整合 |
| Travis CI | 與 GitHub 整合簡單 |
| CircleCI | 速度快、設定簡單 |

### 部署工具

- **Ansible**：簡單易用的配置管理
- **Chef**：基礎設施即程式碼
- **Puppet**：自動化管理
- **SaltStack**：快速遠端執行

[搜尋 CI/CD tools comparison](https://www.google.com/search?q=CI+CD+tools+comparison+2015)

---

## 部署腳本範例

### 基本部署腳本

```bash
#!/bin/bash
# deploy.sh

set -e

APP_NAME="myapp"
DEPLOY_DIR="/opt/$APP_NAME"
REPO_URL="https://github.com/user/$APP_NAME.git"
BRANCH="${1:-main}"

echo "=== 開始部署 $APP_NAME ==="

# 備份當前版本
if [ -d "$DEPLOY_DIR" ]; then
    backup_dir="${DEPLOY_DIR}.backup.$(date +%Y%m%d%H%M%S)"
    mv "$DEPLOY_DIR" "$backup_dir"
    echo "備份已建立: $backup_dir"
fi

# 部署新版本
git clone -b "$BRANCH" "$REPO_URL" "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# 安裝依賴
npm install
npm run build

# 重啟服務
systemctl restart "$APP_NAME"

echo "=== 部署完成 ==="
```

---

## 滾動部署

```bash
#!/bin/bash
# rolling_deploy.sh

set -e

APP_NAME="myapp"
NEW_IMAGE="myapp:2.0"

# 取得當前運行的容器
containers=$(docker ps -q -f name=$APP_NAME)
count=$(echo "$containers" | wc -l)

# 逐步替換
echo "$containers" | while read container; do
    # 啟動新容器
    new_container=$(docker run -d $NEW_IMAGE)
    
    # 停止舊容器
    docker stop "$container"
    docker rm "$container"
    
    echo "已替換容器: $container -> $new_container"
done
```

---

## 藍綠部署

```bash
#!/bin/bash
# blue_green_deploy.sh

set -e

APP_NAME="myapp"
CURRENT_COLOR=$1  # "blue" 或 "green"
NEW_COLOR=$2

if [ "$CURRENT_COLOR" = "blue" ]; then
    NEXT_COLOR="green"
else
    NEXT_COLOR="blue"
fi

echo "部署到 $NEXT_COLOR 環境..."

# 部署到新環境
docker-compose -f docker-compose-$NEXT_COLOR.yml up -d

# 健康檢查
sleep 10
if curl -f http://$NEXT_COLOR.local/health; then
    echo "健康檢查通過，切換流量..."
    # 切換負載均衡
    # 這個具體實現取決於基礎設施
else
    echo "健康檢查失敗，部署失敗"
    exit 1
fi

echo "部署完成: $NEXT_COLOR"
```

---

## 監控與回滾

### 監控部署

```bash
#!/bin/bash
monitor_deploy() {
    local app=$1
    local timeout=300
    local start_time=$(date +%s)
    
    while true; do
        if curl -f http://$app/health; then
            echo "應用正常運行"
            return 0
        fi
        
        elapsed=$(($(date +%s) - start_time))
        if [ $elapsed -gt $timeout ]; then
            echo "超時，部署可能失敗"
            return 1
        fi
        
        sleep 5
    done
}
```

### 回滾

```bash
#!/bin/bash
rollback() {
    local app=$1
    local backup_dir=$2
    
    echo "開始回滾到: $backup_dir"
    
    systemctl stop "$app"
    rm -rf "/opt/$app"
    mv "$backup_dir" "/opt/$app"
    systemctl start "$app"
    
    echo "回滾完成"
}
```

---

## 小結

良好的自動化部署流程能提升交付速度、減少人為錯誤並改善軟體品質。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Jenkins 使用指南](https://www.google.com/search?q=Jenkins+tutorial)
- [Ansible 官方文檔](https://www.google.com/search?q=Ansible+documentation)