# 主題一：Docker 與容器化革命

## 什麼是容器化？

容器化是一種作業系統層級的虛擬化技術，允許在單一 Linux 系統上運行多個隔離的應用程式實例。每個容器都有自己隔離的檔案系統、網路和程序空間。

### 容器 vs 虛擬機

```
傳統 VM:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│     App     │  │     App     │  │     App     │
├─────────────┤  ├─────────────┤  ├─────────────┤
│    Guest    │  │    Guest    │  │    Guest    │
│     OS      │  │     OS      │  │     OS      │
├─────────────┤  ├─────────────┤  ├─────────────┤
│  Hypervisor │  │  Hypervisor │  │  Hypervisor │
└─────────────┘  └─────────────┘  └─────────────┘
     ▲               ▲               ▲
     │               │               │
     └───────────────┴───────────────┘
                   Host OS
              (耗費資源多)

Container:
┌──────────┐  ┌──────────┐  ┌──────────┐
│   App    │  │   App    │  │   App    │
├──────────┤  ├──────────┤  ├──────────┤
│  Cntnr   │  │  Cntnr   │  │  Cntnr   │
├──────────┤  ├──────────┤  ├──────────┤
│          │  │          │  │          │
│     Docker Engine (共用 Host OS)     │
└──────────┘  └──────────┘  └──────────┘
              (資源節省)
```

## Docker 基礎概念

### Docker 核心元件

```python
docker_components = {
    'Docker Engine': '核心執行時，開源的容器平台',
    'Docker Hub': '公用映象倉庫',
    'Dockerfile': '定義容器構建指令的檔案',
    'Docker Compose': '多容器應用的定義和執行工具',
    'Docker Swarm': '容器編排和叢集管理工具',
}
```

### Docker 核心概念

```dockerfile
# Dockerfile 示例
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]
```

## Docker 命令列

```bash
# 映象操作
docker pull ubuntu:20.04
docker images
docker rmi ubuntu:20.04

# 容器操作
docker run -d --name myapp -p 8080:80 myimage
docker ps
docker stop myapp
docker rm myapp

# 日誌和除錯
docker logs myapp
docker exec -it myapp /bin/bash
docker inspect myapp

# 建構
docker build -t myapp:latest .
```

## Python 容器化實作

```python
# app.py
def app():
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello from Docker!"

    return app

if __name__ == '__main__':
    app().run(host='0.0.0.0', port=80)
```

```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install flask
COPY . .
CMD ["python", "app.py"]
```

```bash
# 建構和執行
docker build -t myapp .
docker run -d -p 8080:80 myapp
```

## Docker Compose 多容器應用

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8080:80"
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  db_data:
```

```bash
# 執行多容器應用
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 容器網路

```python
# Docker 網路模式
network_modes = {
    'bridge': '預設模式，隔離的網路命名空間',
    'host': '直接使用主機網路',
    'overlay': '跨多個 Docker 守護進程',
    'macvlan': '為容器分配 MAC 位址',
}
```

```bash
# 網路操作
docker network create mynetwork
docker network connect mynetwork myapp
docker network ls
```

## 資料管理和Volumes

```bash
# 建立和使用 volumes
docker volume create mydata
docker run -v mydata:/data myapp

# 綁定主機目錄
docker run -v /host/path:/container/path myapp

# 查看 volumes
docker volume ls
docker volume inspect mydata
```

## 容器安全最佳實踐

```dockerfile
# 安全 Dockerfile
FROM python:3.9-slim AS builder

# 使用非 root 用戶
RUN useradd --create-home appuser
WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "app.py"]
```

```python
# 安全最佳實踐
security_practices = {
    '最小化映象': '使用 alpine 或 slim 版本',
    '不要儲存密鑰': '使用環境變數或 Docker secrets',
    '掃描漏洞': '使用 docker scan 或 trivy',
    '限制資源': '設定 CPU 和記憶體限制',
    '只讀檔案系統': '使用 --read-only 標誌',
}
```

## Dockerfile 最佳化

```dockerfile
# 不好的範例
FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3
RUN pip install django
COPY . /app
RUN chmod 755 /app

# 好的範例
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir django
COPY . .
USER 1000
```

## 常用 Dockerfile 指令

```dockerfile
# 基礎指令
FROM          # 指定基礎映象
MAINTAINER    # 維護者資訊（已廢棄）
LABEL         # 映象標籤

# 執行指令
RUN           # 在映象中執行命令
CMD           # 容器啟動時預設執行的命令
ENTRYPOINT    # 容器啟動時必定執行的命令
EXPOSE        # 宣告埠口

# 檔案操作
COPY          # 複製檔案到映象
ADD           # 複製檔案（支援 URL 和壓縮檔）
WORKDIR       # 設定工作目錄

# 使用者管理
USER          # 設定使用者
GROUP         # 設定群組
```

## 小結

Docker 代表的容器化技術徹底改變了我們的軟體部署方式。透過不可變基礎設施、隔離執行環境和快速的部署能力，容器化讓 DevOps 和雲端原生開發成为可能。理解 Docker 的核心概念和最佳實踐，是每個現代開發者的必備技能。

---

**延伸閱讀**

- [Docker Official Documentation](https://www.google.com/search?q=Docker+official+documentation)
- [Docker Best Practices](https://www.google.com/search?q=Docker+best+practices)
- [Dockerfile Reference](https://www.google.com/search?q=Dockerfile+reference)