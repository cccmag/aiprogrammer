# 容器的生產環境實踐

## 前言

Docker 容器為開發和部署帶來了極大的便利，但在生產環境中使用容器需要更多的考量。本文探討 Docker 在生產環境中的最佳實踐和注意事項。

## 容器隔離與安全

### 使用非 root 用戶

```dockerfile
# 建立非 root 用戶
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 複製應用程式碼
COPY --chown=appuser:appuser . .

# 切換到非 root 用戶
USER appuser

CMD ["python", "app.py"]
```

### 檔案系統權限

```dockerfile
# 設定唯讀檔案系統
security_opt:
  - no-new-privileges:true

read_only: true

tmpfs:
  - /tmp
```

### 資源限制

```yaml
# docker-compose.yml
services:
  web:
    image: myapp:latest
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## 映象建構優化

### 多階段建構

```dockerfile
# 第一階段：建構
FROM python:3.9 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 第二階段：執行
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --chown=appuser:appuser . .
USER appuser

CMD ["python", "app.py"]
```

### .dockerignore

```
__pycache__
*.pyc
.git
.gitignore
*.md
tests/
docs/
.env
.env.*
venv/
```

## 日誌管理

### 日誌驅動

```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

```bash
# 查看日誌
docker logs -f myapp
docker logs --tail 100 myapp
docker logs --since 1h myapp
```

### 集中式日誌

```python
# 使用結構化日誌
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        })

logging.setFormatter(JSONFormatter())
```

## 健康檢查

### Dockerfile HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1
```

### Docker Compose 健康檢查

```yaml
services:
  web:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

## 網路配置

### 網路隔離

```yaml
# 隔離網路
services:
  web:
    networks:
      - frontend
  db:
    networks:
      - backend

networks:
  frontend:
  backend:
```

### DNS 配置

```bash
# 容器間通訊
docker network create mynet
docker network connect mynet container1
docker network connect mynet container2
```

## 儲存管理

### Volumes

```yaml
services:
  db:
    image: postgres:13
    volumes:
      - pg_data:/var/lib/postgresql/data
      - ./config:/etc/postgresql:ro

volumes:
  pg_data:
```

### 持久化注意事項

```python
# 不要在容器內儲存重要資料
# 使用 volumes 或雲端儲存
# 定期備份
```

## CI/CD 整合

### GitHub Actions

```yaml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Run tests
        run: docker run myapp:${{ github.sha }} pytest
      - name: Push to registry
        run: |
          docker tag myapp:${{ github.sha }} registry/myapp:latest
          docker push registry/myapp:latest
```

## 監控和警報

### Prometheus 指標

```python
from prometheus_client import Counter, generate_latest

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])

@app.route('/')
def index():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return 'Hello'
```

```yaml
# Prometheus 抓取配置
scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['myapp:8000']
```

## 高可用性

### 多副本部署

```yaml
services:
  web:
    image: myapp:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3
```

### 健康檢查和自我修復

```yaml
restart_policy:
  condition: on-failure
  delay: 5s
  max_attempts: 3
  window: 120s
```

## 小結

生產環境中的 Docker 需要全面的考量：安全、效能、可觀測性、高可用性和災難恢復。遵循這些最佳實踐可以幫助您構建穩定、安全的容器化應用程式。

---

**延伸閱讀**

- [Docker Production Best Practices](https://www.google.com/search?q=Docker+production+best+practices)
- [Docker Security](https://www.google.com/search?q=Docker+security+best+practices)
- [Docker Monitoring](https://www.google.com/search?q=Docker+monitoring+prometheus)