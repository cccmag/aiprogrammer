# Docker Compose 多容器應用

## 前言

Docker Compose 讓你用一個檔案定義和管理多個容器，輕鬆處理開發、測試、與部署環境。

## 基本語法

```yaml
# docker-compose.yml
version: '3'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/myapp

  db:
    image: postgres:9.6
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword

  redis:
    image: redis:3.2-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 常見指令

```bash
# 啟動所有服務
docker-compose up

# 在背景啟動
docker-compose up -d

# 重新建置並啟動
docker-compose up --build

# 停止服務
docker-compose down

# 顯示狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 執行一次性命令
docker-compose exec app npm test
```

## 多環境設定

```yaml
# docker-compose.yml (預設)
version: '3'

services:
  app:
    build: .
    environment:
      - NODE_ENV=development

---

# docker-compose.prod.yml (正式環境)
version: '3'

services:
  app:
    image: myapp:latest
    restart: always
    environment:
      - NODE_ENV=production
```

```bash
# 使用正式環境設定
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 網路設定

```yaml
version: '3'

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    networks:
      - webnet
  
  backend:
    build: ./backend
    networks:
      - webnet
      - backendnet
  
  db:
    image: postgres:9.6
    networks:
      - backendnet

networks:
  webnet:
  backendnet:
```

## 依賴與健康檢查

```yaml
version: '3'

services:
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
  
  db:
    image: postgres:9.6
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  redis:
    image: redis:3.2-alpine
```

## 擴展與負載平衡

```bash
# 擴展服務到 3 個實例
docker-compose up -d --scale app=3

# 負載平衡（在 docker-compose.yml 中定義）
```

```yaml
version: '3'

services:
  app:
    build: .
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.role == worker
```

## 資料庫迁移

```yaml
version: '3'

services:
  app:
    build: .
  
  migrate:
    build: .
    command: npm run migrate
    depends_on:
      db:
        condition: service_healthy
```

```bash
# 執行 migration
docker-compose run migrate
```

## 開發環境最佳化

```yaml
# docker-compose.dev.yml
version: '3'

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*
    command: npm run dev
  
  db:
    ports:
      - "5432:5432"  # 暴露給主機
```

```bash
# 開發模式啟動
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 延伸閱讀

- [Docker Compose 文檔](https://www.google.com/search?q=docker+compose+tutorial+2016)
- [Docker Compose 網路](https://www.google.com/search?q=docker+compose+networking+2016)
- [多容器應用部署](https://www.google.com/search?q=multi+container+deployment+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*