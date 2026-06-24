# docker-compose 配置

## 1. 引言

Docker Compose 是用於定義和運行多容器 Docker 應用程式的工具。通過一個 YAML 檔案，你可以定義應用程式的所有服務、網路和卷，然後用一條命令啟動整個應用棧。本文將深入探討 docker-compose.yml 的配置語法與最佳實踐。

## 2. 服務定義

最基本的服務定義包括映像來源、連接埠映射和依賴關係：

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - "80:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - api
      - redis

  api:
    image: myapi:latest
    ports:
      - "4000:4000"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 3. 環境變數管理

**使用 env_file 載入多個變數**：

```yaml
services:
  db:
    image: postgres:16
    env_file:
      - ./config/db.env
      - ./config/app.env
```

**使用 environment 直接定義**：

```yaml
services:
  web:
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - DB_HOST=db
      - DB_PORT=5432
```

## 4. 網路配置

```yaml
services:
  proxy:
    networks:
      - public

  web:
    networks:
      - public
      - private

  db:
    networks:
      - private

networks:
  public:
    driver: bridge
  private:
    driver: bridge
    internal: true  # 不連接到外部
```

## 5. Volume 掛載

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  web:
    volumes:
      - ./src:/app/src:ro     # 開發用 bind mount
      - /app/node_modules     # 匿名卷

volumes:
  pgdata:
    driver: local
```

## 6. 生產環境配置

使用多個 Compose 檔案分離環境配置：

```yaml
# docker-compose.base.yml
services:
  web:
    image: myapp
    ports:
      - "3000:3000"

# docker-compose.prod.yml
services:
  web:
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

```bash
docker compose -f docker-compose.base.yml -f docker-compose.prod.yml up -d
```

## 7. 健康檢查與重啟策略

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
```

## 8. 結語

Docker Compose 讓多容器應用的管理變得簡單直觀。善用環境變數、網路隔離和健康檢查，可以建立既適合開發又可用於生產的配置方案。
