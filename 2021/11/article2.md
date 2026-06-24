# Docker Compose 多容器應用

## 為何需要 Docker Compose？

當應用由多個服務組成時，手動管理每個容器非常繁瑣。Docker Compose 讓你用 YAML 檔案定義和管理多容器應用。

## 基本結構

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - dbdata:/var/lib/postgresql/data
  redis:
    image: redis:6-alpine
volumes:
  dbdata:
```

## 執行操作

```bash
# 啟動所有服務
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f web

# 停止服務
docker-compose down

# 重新構建
docker-compose up -d --build
```

## 環境變數

```yaml
services:
  web:
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
```

## 網路配置

Docker Compose 自動為每個專案建立一個網路：

```yaml
services:
  web:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend
networks:
  frontend:
  backend:
```

服務可以通過服務名稱互相訪問。

## 健康檢查

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 擴展服務

```bash
# 擴展 web 服務到 3 個實例
docker-compose up -d --scale web=3

# 負載均衡需要結合別的工具
```

## 結論

Docker Compose 是開發和測試環境的理想工具，能快速啟動完整的多容器應用。掌握其用法，能大幅提升開發效率。