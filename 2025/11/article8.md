# 容器化與 Docker

## Docker 基礎到 Docker Compose 多服務部署

## 為什麼需要容器化？

容器化將應用程式及其所有依賴打包成一個標準化的單元，解決了「在我機器上可以跑」的問題。

```
傳統部署：
  開發環境：macOS + Python 3.11 + PostgreSQL 15
  測試環境：Linux + Python 3.10 + PostgreSQL 14
  生產環境：Linux + Python 3.12 + PostgreSQL 16
  → 環境不一致導致各種奇怪問題

容器化：
  開發環境：Docker Container（Python 3.11 + PostgreSQL 15）
  測試環境：同一個 Docker Image
  生產環境：同一個 Docker Image
  → 完全一致的執行環境
```

---

## Docker 核心概念

### Image（映像檔）

唯讀的模板，包含應用程式及其執行環境。

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### Container（容器）

Image 的執行例項。

```bash
# 建立並啟動容器
docker build -t myapp .
docker run -d -p 8000:8000 --name myapp-container myapp

# 查看運行中的容器
docker ps

# 停止容器
docker stop myapp-container
```

---

## Dockerfile 最佳實踐

### 多階段建構

```dockerfile
# 第一階段：編譯
FROM python:3.12 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 第二階段：運行（更小的映像）
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

### 最佳實踐

```dockerfile
# 1. 使用 .dockerignore
# .dockerignore
# __pycache__
# .git
# *.md

# 2. 減少層數（合併 RUN）
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# 3. 使用非 root 使用者
RUN useradd -m appuser
USER appuser

# 4. 使用特定 tag 而非 latest
FROM python:3.12-slim  # 好
FROM python:latest     # 不好
```

---

## Docker Compose

管理多容器應用。

### 一個簡單的 Web + Redis 應用

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

```bash
# 啟動所有服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止並移除
docker-compose down
```

### 完整的三層應用

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - db
      - cache
      - queue
    environment:
      - DB_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379/0
      - QUEUE_URL=amqp://user:pass@queue:5672/

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s

  cache:
    image: redis:7-alpine

  queue:
    image: rabbitmq:4-management
    environment:
      RABBITMQ_DEFAULT_USER: user
      RABBITMQ_DEFAULT_PASS: pass

volumes:
  pg_data:
```

---

## 網路與通訊

### 容器網路模式

```yaml
services:
  app:
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

容器透過服務名稱互相訪問：`app` 可以透過 `db:5432` 連接 PostgreSQL。

---

## 資料持久化

### Volumes

```yaml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  postgres_data:
```

### Bind Mounts（開發用）

```yaml
services:
  app:
    volumes:
      - ./app:/app  # 即時同步程式碼
```

---

## 實際案例：容器化 Flask 應用

```python
# app.py
from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"))

@app.route("/")
def hello():
    count = cache.incr("counter")
    return f"Hello! You are visitor #{count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install flask redis
COPY app.py .
CMD ["python", "app.py"]
```

```bash
# 建構與執行
docker-compose up -d
curl http://localhost:8000
# Hello! You are visitor #1
```

---

## 監控與日誌

```bash
# 容器日誌
docker logs -f myapp-container

# 容器資源使用
docker stats

# Compose 日誌
docker-compose logs -f app
```

---

## 延伸閱讀

- [Docker Official Documentation](https://www.google.com/search?q=Docker+official+documentation+get+started)
- [Docker Compose Guide](https://www.google.com/search?q=Docker+Compose+multi+container+applications)
- [Docker Best Practices](https://www.google.com/search?q=Dockerfile+best+practices+2026)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」文章系列之八。*
