# Docker 核心概念與生態系統

## 容器 vs 虛擬機

容器和 VM 都提供隔離環境，但方式不同。VM 包含完整的作業系統和應用，重量級但完全隔離。容器共享主機 OS 核心，輕量級但共享核心意味著某種程度的耦合。

## Docker 基本概念

### 映像檔（Image）

映像檔是容器的模板，是唯讀的。包含執行應用所需的所有檔案：

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 容器（Container）

容器是映像檔的運行實例。可以啟動、停止、刪除。

```bash
docker run -d -p 8000:8000 --name myapp myimage:latest
```

### 倉庫（Registry）

Docker Hub 是公共倉庫，儲存和分發映像檔。可以架設私有倉庫如 Harbor。

## Docker 命令列基礎

```bash
# 構建映像檔
docker build -t myapp:latest .

# 列出容器
docker ps -a

# 啟動/停止容器
docker start myapp
docker stop myapp

# 查看日誌
docker logs -f myapp

# 進入容器
docker exec -it myapp bash
```

## 多階段構建

使用多階段構建減小映像檔大小：

```dockerfile
# 階段 1：構建
FROM python:3.9 AS builder
WORKDIR /app
COPY . .
RUN pip install --user -r requirements.txt

# 階段 2：運行
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .
CMD ["python", "app.py"]
```

## Docker 網路

```bash
# 創建網路
docker network create mynetwork

# 連接容器到網路
docker network connect mynetwork myapp
```

## Docker 卷（Volumes）

持久化資料：

```bash
# 創建卷
docker volume create mydata

# 掛載卷
docker run -v mydata:/data myapp
```

## Docker Compose

定義多容器應用：

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:8000"
  db:
    image: postgres:13
    volumes:
      - dbdata:/var/lib/postgresql/data
volumes:
  dbdata:
```

## 結論

Docker 已經成為現代開發的必備工具。其簡單的介面和強大的生態系統，使容器化變得人人可及。掌握 Docker 是雲端原生之旅的第一步。