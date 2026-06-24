# PM2 行程管理

## 1. 引言

PM2 是 Node.js 應用程式的生產環境行程管理器。它提供了行程守護、叢集模式、零停機部署和內建監控等功能。本文將全面介紹 PM2 在 DevOps 實踐中的應用。

## 2. 安裝與基本使用

```bash
# 全域安裝 PM2
npm install -g pm2

# 啟動應用程式
pm2 start index.js --name myapp

# 列出所有行程
pm2 list

# 查看日誌
pm2 logs

# 監控資源使用
pm2 monit

# 停止行程
pm2 stop myapp

# 重新啟動
pm2 restart myapp

# 刪除行程
pm2 delete myapp
```

## 3. 叢集模式

PM2 叢集模式利用 Node.js 的 cluster 模組，在多核心 CPU 上運行多個實例：

```bash
# 使用所有 CPU 核心（-i max）
pm2 start index.js -i max --name myapp

# 指定實例數
pm2 start index.js -i 4 --name myapp
```

**ecosystem.config.js**：

```javascript
module.exports = {
  apps: [{
    name: 'myapp',
    script: 'index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    env_file: '.env'
  }]
};
```

```bash
# 使用配置檔案啟動
pm2 start ecosystem.config.js
```

## 4. 零停機部署

```bash
# 零停機重新載入（逐一重啟實例）
pm2 reload myapp

# 滾動更新
pm2 start ecosystem.config.js --update-env
```

```javascript
// ecosystem.config.js with deploy
module.exports = {
  deploy: {
    production: {
      user: 'node',
      host: '192.168.1.100',
      ref: 'origin/main',
      repo: 'git@github.com:user/myapp.git',
      path: '/var/www/myapp',
      'pre-deploy': 'git pull',
      'post-deploy': 'npm ci && pm2 reload ecosystem.config.js --env production'
    }
  }
};
```

```bash
# 執行部署
pm2 deploy production
```

## 5. 日誌管理

```bash
# 查看即時日誌
pm2 logs

# 查看特定應用的日誌
pm2 logs myapp

# 清空日誌
pm2 flush

# 日誌輪替配置
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

## 6. 監控與管理

```bash
# 基於網頁的監控面板
pm2 plus

# 保存行程列表（開機自動啟動）
pm2 save
pm2 startup
```

## 7. 與 Docker 整合

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm ci && npm install -g pm2
EXPOSE 3000
CMD ["pm2-runtime", "start", "ecosystem.config.js"]
```

## 8. 結語

PM2 是 Node.js 生產環境部署的必備工具。從行程管理到叢集模式，從零停機部署到監控日誌，PM2 提供了完整的 DevOps 整合方案。
