# Docker Compose 多容器應用

## 前言

現代 Web 應用通常由多個服務組成：Web 伺服器、資料庫、快取、訊息佇列等。Docker Compose 讓我們可以用宣告式的 YAML 檔案定義和執行多容器應用。

## Docker Compose 基礎

### docker-compose.yml 結構

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:12-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
```

## 進階功能

### 環境特定配置

```yaml
# docker-compose.yml
services:
  web:
    image: myapp:latest
    profiles:
      - production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

# docker-compose.override.yml（開發用）
services:
  web:
    build: .
    volumes:
      - .:/app
    environment:
      - DEBUG=true
    profiles:
      - development

# docker-compose.prod.yml
services:
  web:
    image: myapp:prod
    profiles:
      - production
```

```bash
# 使用預設配置（開發）
docker-compose up

# 使用生產配置
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 只運行生產服務
docker-compose --profile production up -d
```

### 健康檢查和依賴

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 網路配置

```yaml
services:
  web:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend
  redis:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 隔離網路
```

### 擴展和負載均衡

```bash
# 擴展服務
docker-compose up -d --scale web=3

# 負載均衡（需要額外配置）
docker-compose up -d --scale web=3 --scale lb=1
```

## 完整的 Flask 應用範例

### 專案結構

```
myflaskapp/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app.py
├── nginx.conf
└── init.sql
```

### 程式碼

```python
# app.py
from flask import Flask, jsonify
import os
import psycopg2
import redis

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def get_redis():
    return redis.from_url(os.environ['REDIS_URL'])

@app.route('/')
def index():
    return jsonify({'message': 'Hello from Flask with Docker Compose!'})

@app.route('/users')
def users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route('/cache/<key>')
def cache(key):
    r = get_redis()
    value = r.get(key)
    if value is None:
        value = f"value_for_{key}"
        r.set(key, value)
        return jsonify({'cached': False, 'key': key, 'value': value})
    return jsonify({'cached': True, 'key': key, 'value': value.decode()})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Dockerfile

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Nginx 配置

```nginx
events {
    worker_connections 1024;
}

http {
    upstream web {
        server web:5000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /health {
            proxy_pass http://web/health;
            access_log off;
        }
    }
}
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:12-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
```

## 常用指令

```bash
# 啟動所有服務
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f web

# 重新建構
docker-compose build web
docker-compose up -d --no-deps web

# 擴展
docker-compose up -d --scale web=3

# 進入服務
docker-compose exec web /bin/bash

# 停止和清理
docker-compose down
docker-compose down -v  # 同時刪除 volumes
```

## 延伸閱讀

- [Docker Compose 官方文件](https://www.google.com/search?q=Docker+Compose+official+documentation)
- [Docker Compose 檔案參考](https://www.google.com/search?q=docker-compose+yml+reference)
- [Docker Compose 網路](https://www.google.com/search?q=Docker+Compose+networking+tutorial)
- [多容器 Flask 應用](https://www.google.com/search?q=Docker+Compose+Flask+PostgreSQL+Redis)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」文章集錦之一。*