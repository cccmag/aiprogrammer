# Docker 容器化實戰

## 前言

Docker 徹底改變了應用程式的部署方式，讓我們來了解這個強大的工具。

---

## 基本概念

### 容器 vs 虛擬機

```
傳統虛擬機：
┌─────────────────────────┐
│ Guest OS                │
│ ├─ App1                │
│ ├─ App2                │
│ └─ App3                │
│ Kernel                 │
└─────────────────────────┘

Docker 容器：
┌─────────────────────────┐
│ Container               │
│ ├─ App1                │
│ ├─ App2                │
│ └─ App3                │
│ Libs/Dependencies      │
├─────────────────────────┤
│ Docker Engine          │
│ Kernel                 │
└─────────────────────────┘
```

### 核心元件

- **Image**：唯讀模板
- **Container**：Image 的執行實例
- **Registry**：存放 Image 的地方（Docker Hub）
- **Dockerfile**：定義 Image 的腳本

---

## 基本指令

### 管理 Image

```bash
# 搜尋 Image
docker search ubuntu

# 拉取 Image
docker pull ubuntu:20.04

# 列出 Image
docker images

# 刪除 Image
docker rmi ubuntu:20.04

# 建立 Image
docker build -t myapp:1.0 .
```

### 管理 Container

```bash
# 執行 Container
docker run -d --name web nginx

# 列出執行中的 Container
docker ps

# 列出所有 Container
docker ps -a

# 停止 Container
docker stop web

# 啟動已停止的 Container
docker start web

# 刪除 Container
docker rm web

# 進入 Container
docker exec -it web bash
```

---

## Dockerfile 範例

### 簡單 Python 應用

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

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

# 執行階段
FROM alpine:latest
WORKDIR /app
COPY --from=builder /build/myapp .
CMD ["./myapp"]
```

---

## Docker Compose

### 基本設定

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "80:80"
    depends_on:
      - db
    environment:
      - DB_HOST=db
  db:
    image: postgres:13
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secret
volumes:
  db-data:
```

### 常用指令

```bash
docker-compose up -d
docker-compose down
docker-compose ps
docker-compose logs -f
docker-compose exec web bash
```

---

## 網路

### 預設網路

```bash
docker network ls
docker inspect bridge
```

### 自訂網路

```bash
docker network create mynet
docker run --network=mynet --name=web nginx
```

---

## 資料管理

### 資料卷

```bash
# 建立資料卷
docker volume create mydata

# 使用資料卷
docker run -v mydata:/data nginx

# 主機目錄掛載
docker run -v /host/path:/container/path nginx
```

---

## 最佳實踐

### Dockerfile 優化

1. **使用多階段建構**減少 Image 大小
2. **順序安排**經常變更的層在上方
3. **使用 .dockerignore**
4. **避免安裝不必要的套件**
5. **使用特定版本標籤**

### 安全

```dockerfile
# 不要用 root 執行
USER nobody

# 掃描漏洞
docker scan myapp:1.0
```

[搜尋 Docker security best practices 2015](https://www.google.com/search?q=Docker+security+best+practices+2015)

---

## 小結

Docker 已成為現代部署的標準工具，熟練掌握 Docker 能大幅提升開發和部署效率。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Docker 官方文檔](https://docs.docker.com/)
- [Docker Compose 文檔](https://docs.docker.com/compose/)