# Docker 容器化 Python：將應用包裝成容器

## Docker 基礎概念

### 什麼是容器？

容器是一種輕量級的虛擬化技術，與傳統 VM 相比，容器共享宿主機的核心，啟動更快、資源佔用更少：

```
傳統 VM：                      容器：
┌──────────────────────┐    ┌──────────────────────┐
│    App1   │   App2   │    │    App1   │   App2   │
├───────────┼──────────┤    ├───────────┼──────────┤
│   Guest   │   Guest  │    │   Runtime │   Runtime│
│   OS      │   OS     │    └───────────┼──────────┘
├───────────┼──────────┤    ┌───────────┼──────────┤
│   Hypervisor        │    │      Docker          │
└──────────────────────┘    └───────────┴──────────┘
      完整作業系統                共享核心
```

### Docker 的核心概念

- **映像檔（Image）**：唯讀的模板，用於建立容器
- **容器（Container）**：映像檔的執行實例
- **倉庫（Registry）**：儲存和分發映像檔的地方（Docker Hub）
- **Dockerfile**：描述如何構建映像檔的指令檔

## 第一個 Dockerfile

### 基本結構

```dockerfile
# 使用官方 Python 運行時作為父映像
FROM python:3.8-slim

# 設定工作目錄
WORKDIR /app

# 將當前目錄內容複製到容器中
COPY . .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 對外暴露連接埠
EXPOSE 8000

# 執行時的命令
CMD ["python", "main.py"]
```

### 建構和執行

```bash
# 建構映像檔
docker build -t mypythonapp .

# 執行容器
docker run -p 8000:8000 mypythonapp

# 後台執行
docker run -d -p 8000:8000 --name myapp mypythonapp

# 查看執行中的容器
docker ps

# 停止容器
docker stop myapp

# 刪除容器
docker rm myapp
```

## Python Dockerfile 最佳實踐

### 使用 slim 映像

Python 官方映像有多種變體：

```dockerfile
# ❌ 不推薦：完整的 Debian 映像，約 900MB
FROM python:3.8

# ✅ 推薦：精簡的 Debian 映像，約 120MB
FROM python:3.8-slim

# ✅ 更好的選擇：Alpine Linux，約 45MB
FROM python:3.8-alpine
```

### 多階段建構

多階段建構可以大幅減小最終映像大小：

```dockerfile
# 階段 1：建構階段
FROM python:3.8 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 階段 2：執行階段
FROM python:3.8-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

### 使用 .dockerignore

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.venv/
venv/
.git/
.gitignore
*.md
tests/
.coverage
htmlcov/
```

### 分離依賴和應用程式

```dockerfile
# 先複製依賴檔案，單獨安裝
# 這樣可以充分利用 Docker 的快取層
FROM python:3.8-slim
WORKDIR /app

# 只複製依賴檔案
COPY requirements.txt .

# 安裝依賴（會被快取）
RUN pip install --no-cache-dir -r requirements.txt

# 再複製應用程式碼（經常變動）
COPY . .

CMD ["python", "main.py"]
```

## Docker Compose

### 多容器應用

Docker Compose 讓你可以定義和執行多容器應用：

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379

  db:
    image: postgres:12-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp

  redis:
    image: redis:6-alpine

volumes:
  postgres_data:
```

```bash
# 啟動所有服務
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f web

# 停止所有服務
docker-compose down
```

### 開發和生產環境

```yaml
# docker-compose.yml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
    ports:
      - "5000:5000"
```

## 常用 Docker 指令

```bash
# 映像檔管理
docker images                          # 列出本地映像
docker rmi <image>                     # 刪除映像
docker pull python:3.8-slim             # 拉取映像
docker push myregistry/myapp:latest    # 推送映像

# 容器管理
docker ps -a                           # 列出所有容器
docker stop $(docker ps -aq)           # 停止所有容器
docker rm $(docker ps -aq)             # 刪除所有容器
docker logs -f <container>             # 查看容器日誌
docker exec -it <container> /bin/bash  # 進入容器

# 清理
docker system prune                    # 清理未使用的資源
docker image prune                     # 清理未使用的映像
docker container prune                 # 清理已停止的容器
```

## 延伸閱讀

- [Docker 官方文件](https://www.google.com/search?q=Docker+official+documentation)
- [Python Docker 映像](https://www.google.com/search?q=Python+official+Docker+image)
- [Dockerfile 最佳實踐](https://www.google.com/search?q=Dockerfile+best+practices+Python)
- [Docker Compose 使用指南](https://www.google.com/search?q=Docker+Compose+tutorial)
- [多階段建構教學](https://www.google.com/search?q=Docker+multi-stage+build+Python)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」歷史回顧系列之一。*