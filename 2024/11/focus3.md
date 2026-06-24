# Docker Compose 多容器

## 服務定義與編排

### 前言

現代應用程式通常由多個服務組成：Web 伺服器、資料庫、快取、訊息佇列等。Docker Compose 提供了一個宣告式的方式來定義和運行多容器應用，讓開發者可以用一個命令啟動整個應用棧。

### docker-compose.yml

Docker Compose 使用 YAML 格式的設定檔來定義服務：

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis
    environment:
      - DB_URL=postgres://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379

  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### 常用 Compose 命令

```bash
# 啟動所有服務
docker compose up -d

# 查看服務日誌
docker compose logs -f web

# 重建並啟動
docker compose up -d --build

# 停止並移除
docker compose down

# 查看運行中的服務
docker compose ps

# 在服務中執行命令
docker compose exec web sh
```

### 網路配置

Compose 會自動建立一個預設網路，所有服務可以通過服務名稱互相訪問：

```yaml
services:
  web:
    networks:
      - frontend
      - backend

  api:
    networks:
      - backend

networks:
  frontend:
  backend:
```

### 環境變數管理

**使用 .env 檔案**

Compose 自動載入與 docker-compose.yml 同目錄的 `.env` 檔案：

```
DB_USER=admin
DB_PASS=secret123
REDIS_HOST=redis
```

**在 Compose 中引用**

```yaml
services:
  db:
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASS}
```

### healthcheck 與依賴管理

確保服務在依賴就緒後才啟動：

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy

  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 生產環境配置

使用 profiles 或 override 檔案管理不同環境：

```yaml
# docker-compose.override.yml（開發用）
services:
  web:
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development
```

```bash
# 使用不同配置檔案
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 小結

Docker Compose 讓多容器應用的管理變得簡單直觀。通過宣告式的配置，開發者可以在本地開發環境中完整重現生產環境的服務架構，同時 CI/CD 管線也可以使用相同的配置進行整合測試。

---

**下一步**：[CI/CD 管線設計](focus4.md)

## 延伸閱讀

- [Docker Compose 文件](https://www.google.com/search?q=Docker+Compose+documentation)
- [Compose 生產環境最佳實踐](https://www.google.com/search?q=Docker+Compose+production+best+practices)
