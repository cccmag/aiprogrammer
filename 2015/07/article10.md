# 容器化與版本管理

## 前言

Docker 容器化和 Git 版本控制的結合，是現代部署的標準實踐。

---

## Docker 基礎

### 概念

- **Image**：唯讀模板
- **Container**：Image 的執行實例
- **Registry**：存放 Image 的地方

### 基本指令

```bash
# 建立 Image
docker build -t myapp:1.0 .

# 執行 Container
docker run -d -p 80:80 myapp:1.0

# 查看執行中的 Container
docker ps

# 查看所有 Container
docker ps -a
```

---

## Dockerfile 版本控制

```dockerfile
# Version 1.0
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]
```

### 多階段建構

```dockerfile
# 建置階段
FROM golang:1.16 AS builder
WORKDIR /build
COPY . .
RUN go build -o myapp

# 運行階段
FROM alpine:latest
WORKDIR /app
COPY --from=builder /build/myapp .
CMD ["./myapp"]
```

---

## Docker 與 Git

### 追蹤 Dockerfile

```bash
git add Dockerfile
git commit -m "Add Dockerfile for containerization"
git push
```

### .dockerignore

類似 .gitignore：

```
.git
node_modules
*.log
__pycache__
.env
```

---

## 持續整合/部署

### GitHub Actions + Docker

```yaml
name: Build and Push Docker Image
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
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_TOKEN }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myapp:${{ github.sha }}
```

### Docker Compose

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "80:80"
    depends_on:
      - db
  db:
    image: postgres:13
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

---

## 資料庫版本控制

### Liquibase

```xml
<!-- changelog.xml -->
<databaseChangeLog>
  <changeSet id="1" author="developer">
    <createTable tableName="users">
      <column name="id" type="int">
        <constraints primaryKey="true"/>
      </column>
      <column name="name" type="varchar(255)"/>
    </createTable>
  </changeSet>
</databaseChangeLog>
```

### Flyway

```sql
-- V1__Initial_schema.sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

-- V2__Add_email.sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

---

## 配置管理

### 環境變數

```bash
# 生產環境
docker run -d -e NODE_ENV=production myapp

# 秘密管理
docker run -d --env-file .env myapp
```

### Config Maps

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "db.example.com"
  LOG_LEVEL: "info"
```

---

## 部署策略

### 滾動更新

```bash
kubectl rollout undo deployment/myapp
```

### Blue-Green

```bash
# 部署新版本
docker-compose -f docker-compose.green.yml up -d

# 測試後切換
nginx -s reload
```

### Canary

```bash
# 10% 流量到新版本
kubectl scale deployment myapp-v2 --replicas=1
```

---

## 小結

Docker 和 Git 的結合提供了可重現、可追蹤的部署流程，是現代 DevOps 的基石。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Docker 官方文檔](https://docs.docker.com/)
- [Kubernetes 官方文檔](https://www.google.com/search?q=Kubernetes+official+documentation)