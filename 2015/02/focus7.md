# 部署與維運：PM2、Docker、雲端部署

## 前言

開發完成後，需要將應用部署到生產環境。本篇介紹 Node.js 應用的部署與維運工具。

## PM2 程序管理

### 安裝

```bash
npm install -g pm2
```

### 基本命令

```bash
# 啟動應用
pm2 start app.js

# 列出所有程序
pm2 list

# 停止
pm2 stop app

# 重啟
pm2 restart app

# 刪除
pm2 delete app
```

### 進階功能

```bash
# 監視檔案變更自動重啟
pm2 start app.js --watch

# 設定名稱
pm2 start app.js --name my-app

# 設定環境變數
pm2 start app.js --env production

# 叢集模式（利用多核心）
pm2 start app.js -i max

# 日誌
pm2 logs
pm2 logs --lines 100
pm2 flush  # 清除日誌
```

### 生產環境設定

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'my-app',
    script: 'app.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/error.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    merge_logs: true,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
```

```bash
pm2 start ecosystem.config.js --env production
```

### 負載平衡

```
PM2 Cluster Mode：
──────────────────

        ┌─────────────────────────┐
        │       PM2 Master        │
        └─────────┬───────────────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
  ┌─────┐     ┌─────┐     ┌─────┐
  │Worker│     │Worker│     │Worker│
  │  1   │     │  2   │     │  3   │
  └──┬──┘     └──┬──┘     └──┬──┘
     │            │            │
     └────────────┼────────────┘
                  │
                  ▼
              使用者請求
```

## Docker 容器化

### Dockerfile

```dockerfile
FROM node:0.12

WORKDIR /app

COPY package.json .
RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]
```

### docker-compose.yml

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    depends_on:
      - mongo
      - redis
    restart: unless-stopped

  mongo:
    image: mongo:3.0
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped

  redis:
    image: redis:3.0
    restart: unless-stopped

volumes:
  mongo-data:
```

### 建置與執行

```bash
# 建置映像
docker build -t myapp:latest .

# 執行
docker run -d -p 3000:3000 myapp:latest

# Docker Compose
docker-compose up -d
docker-compose logs
docker-compose down
```

## Nginx 反向代理

### 基本設定

```nginx
upstream node_app {
    server 127.0.0.1:3000;
    keepalive 64;
}

server {
    listen 80;
    server_name example.com;

    # 靜態檔案
    location /static/ {
        alias /var/www/static/;
        expires 30d;
    }

    # API 代理
    location /api/ {
        proxy_pass http://node_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket 代理
    location /socket.io/ {
        proxy_pass http://node_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### HTTPS 設定

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;

    # 其他設定...

    location / {
        proxy_pass http://node_app;
        # SSL 相關 header
        proxy_set_header X-Forwarded-Proto https;
    }
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## 雲端部署

### Heroku

```bash
# 登入
heroku login

# 建立應用
heroku create my-app

# 部署
git push heroku master

# 調整規模
heroku ps:scale web=2

# 查看日誌
heroku logs --tail

# 環境變數
heroku config:set NODE_ENV=production
```

### 環境變數

```bash
# .env 檔案（本地開發）
NODE_ENV=development
PORT=3000
DATABASE_URL=mongodb://localhost:27017/mydb

# 生產環境
heroku config:set DATABASE_URL=mongodb://user:pass@mongo.com/mydb
```

## 監控與除錯

### PM2 監控

```bash
# 查看詳細狀態
pm2 show app

# 監控 CPU/記憶體
pm2 monit

# 叢集監控
pm2 plus
```

### 日誌集中

```javascript
// Winston 日誌
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

## 結論

Node.js 應用的部署有多種選擇：PM2 適合傳統 VPS、Docker 適合容器化環境、雲端平台適合快速部署。選擇適合的方式，讓你的應用穩定運行。

---

## 延伸閱讀

- [PM2 官方文檔](https://www.google.com/search?q=PM2+process+manager+Node.js)
- [Docker+Node.js](https://www.google.com/search?q=Docker+Node.js+deployment+tutorial)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」歷史回顧系列之一。*