# 部署 Node.js 應用

## 部署前的準備

在將 Node.js 應用部署到生產環境之前，需要完成以下準備工作：

```javascript
// config/production.js
module.exports = {
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'production',
  db: {
    uri: process.env.MONGODB_URI,
    options: { maxPoolSize: 10 }
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '15m'
  },
  cors: {
    origin: process.env.CORS_ORIGIN || 'https://myapp.com'
  },
  rateLimit: {
    windowMs: 15 * 60 * 1000,
    max: 100
  }
};
```

## 環境變數管理

```bash
# .env.production（永遠不提交到版本控制）
NODE_ENV=production
PORT=3000
MONGODB_URI=mongodb://user:pass@prod-host:27017/myapp
JWT_SECRET=your-prod-secret-key
CORS_ORIGIN=https://myapp.com
```

## 程序管理：PM2

```bash
# 安裝 PM2
npm install -g pm2

# 啟動應用
pm2 start app.js --name my-app

# 啟用叢集模式（使用所有 CPU）
pm2 start app.js -i max --name my-app

# 其他常用命令
pm2 list                 # 查看所有程序
pm2 logs                 # 查看日誌
pm2 monit                # 監控面板
pm2 restart my-app       # 重啟
pm2 stop my-app          # 停止
pm2 delete my-app        # 刪除

# 設定開機自啟
pm2 startup
pm2 save
```

### ecosystem.config.js

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'my-app',
    script: 'server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    },
    watch: false,
    max_memory_restart: '1G',
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss'
  }]
};
```

## Docker 部署

```dockerfile
# Dockerfile
FROM node:20-alpine

WORKDIR /app

# 先複製依賴檔案（利用快取）
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# 複製應用程式碼
COPY . .

# 建立非 root 使用者
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 3000

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - MONGODB_URI=mongodb://mongo:27017/myapp
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - mongo
    restart: unless-stopped

  mongo:
    image: mongo:7
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped

volumes:
  mongo-data:
```

## Nginx 反向代理

```nginx
# /etc/nginx/sites-available/my-app
server {
    listen 80;
    server_name myapp.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 靜態檔案快取
    location /static/ {
        alias /var/www/my-app/public/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 限制請求大小
    client_max_body_size 10M;
}
```

## CI/CD 流程

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test
      - run: npm run build
      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/my-app
            git pull
            npm ci --only=production
            pm2 restart my-app
```

## Node.js 生產環境最佳實踐

```javascript
// server.js
const app = require('./app');
const config = require('./config');

// 優雅關閉
const server = app.listen(config.port, () => {
  console.log(`Server running in ${config.nodeEnv} on port ${config.port}`);
});

process.on('SIGTERM', () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  server.close(() => {
    console.log('Process terminated');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received. Shutting down gracefully...');
  server.close(() => {
    process.exit(0);
  });
});
```

## 健康檢查端點

```javascript
// 在 app.js 中加入
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage()
  });
});
```

## 總結

部署 Node.js 應用需要考慮多方面因素：程序管理、環境隔離、反向代理、CI/CD 自動化、監控與日誌。使用 PM2、Docker、Nginx 等工具組合，可以建構一個穩定且可擴展的生產環境。

## 延伸閱讀

- [PM2 官方文件](https://www.google.com/search?q=PM2+process+manager+documentation)
- [Docker Node.js 最佳實踐](https://www.google.com/search?q=Docker+Node.js+best+practices)
- [Nginx 反向代理設定](https://www.google.com/search?q=Nginx+reverse+proxy+Node.js)
