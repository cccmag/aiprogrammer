# 部署策略：藍綠、滾動

## 1. 引言

部署策略決定了新版本軟體如何取代舊版本上線。好的部署策略可以實現零停機時間、快速回滾和逐步驗證。本文將深入探討兩種主流部署策略：藍綠部署和滾動更新。

## 2. 藍綠部署（Blue-Green Deployment）

### 概念

藍綠部署維護兩個完全相同的生產環境：藍色（當前版本）和綠色（新版本）。切換流量即可完成部署。

```
用戶 ──→ 負載均衡器 ──→ 藍色環境（v1）✅ 運行中
                      └── 綠色環境（v2）待部署

1. 部署 v2 到綠色環境
2. 驗證綠色環境正常
3. 切換負載均衡器到綠色環境
4. 藍色環境作為回滾備用
```

### Docker Compose 實作

```yaml
# docker-compose.blue.yml
services:
  web-blue:
    image: myapp:v1
    ports:
      - "3001:3000"

# docker-compose.green.yml
services:
  web-green:
    image: myapp:v2
    ports:
      - "3002:3000"
```

### Nginx 切換配置

```nginx
upstream app {
    server localhost:3001;  # 藍色
    # server localhost:3002;  # 綠色（切換時取消註解）
}

server {
    listen 80;
    location / {
        proxy_pass http://app;
    }
}
```

## 3. 滾動更新（Rolling Update）

### 概念

滾動更新逐步替換容器實例，每次更新一部分，保持服務在更新期間可用。

```
初始： [v1] [v1] [v1] [v1]
步驟1：[v2] [v1] [v1] [v1]
步驟2：[v2] [v2] [v1] [v1]
步驟3：[v2] [v2] [v2] [v1]
步驟4：[v2] [v2] [v2] [v2] ✅ 完成
```

### 使用 Node.js 模擬

```javascript
async function rollingUpdate(instances, newVersion) {
  for (let i = 0; i < instances.length; i++) {
    console.log(`停止實例 ${i + 1}`);
    instances[i].status = 'stopped';
    
    console.log(`啟動 v${newVersion}`);
    instances[i].version = newVersion;
    instances[i].status = 'running';
    
    await healthCheck(instances[i]);
    console.log(`實例 ${i + 1} 更新完成`);
  }
}
```

### 使用 Docker Compose

```bash
# 逐個更新服務實例
docker service update --image myapp:v2 --update-parallelism 1 myapp_web
```

## 4. 策略比較

| 面向 | 藍綠部署 | 滾動更新 |
|------|---------|---------|
| 資源需求 | 2 倍資源 | 現有資源 + 1 |
| 切換速度 | 即時 | 逐步 |
| 回滾速度 | 即時切回 | 逐步回滾 |
| 驗證機會 | 切換前完整驗證 | 逐步驗證 |
| 成本 | 較高 | 較低 |

## 5. 進階：金絲雀部署

金絲雀部署是滾動更新的變體，先將一小部分流量導向新版本：

```nginx
upstream app {
    server localhost:3001 weight=90;  # 舊版本 90%
    server localhost:3002 weight=10;  # 新版本 10%
}
```

## 6. 結語

選擇部署策略需要綜合考慮資源、風險和速度。藍綠部署適合關鍵服務，滾動更新適合資源受限的場景。建議根據服務特性選擇最適合的策略。
