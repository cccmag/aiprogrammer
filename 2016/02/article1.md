# Docker Compose 多容器應用

## Docker Compose 簡介

Docker Compose 是用於定義與執行多容器 Docker 應用程式的工具。透過 YAML 設定檔，可以聲明應用程式所需的服務、網路、磁碟區，然後使用單一指令啟動或停止所有服務。

## 安裝

```bash
# Linux
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# macOS / Windows（隨 Docker Desktop 安裝）
# 已包含 docker-compose
```

## 基本設定檔

```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    networks:
      - frontend
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - backend

networks:
  frontend:
  backend:

volumes:
  db_data:
```

## 常用指令

```bash
# 啟動所有服務（背景執行）
docker-compose up -d

# 啟動並重新建置映象
docker-compose up -d --build

# 停止所有服務
docker-compose down

# 停止並刪除磁碟區
docker-compose down -v

# 檢視服務狀態
docker-compose ps

# 檢視服務日誌
docker-compose logs -f web

# 執行一次性命令
docker-compose run web python manage.py migrate

# 進入服務的 Shell
docker-compose exec web /bin/bash

# 擴展服務（需要 Swarm 模式）
docker-compose up -d --scale web=3
```

## 環境變數檔案

可使用 `.env` 檔案設定環境變數：

```bash
# .env
POSTGRES_PASSWORD=secret
POSTGRES_DB=myapp
IMAGE_TAG=1.0
```

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
```

## 實際範例：WordPress 網站

```yaml
version: "3.8"
services:
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - db

volumes:
  db_data:
```

```bash
docker-compose up -d
# 拜訪 http://localhost:8080
```

## 開發環境範例

```yaml
version: "3.8"
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: development
      DB_HOST: db
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: devpassword
    volumes:
      - pg_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  pg_data:
```

## 參考資源

- https://www.google.com/search?q=Docker+Compose+多容器+YAML+設定+教學+2016
- https://www.google.com/search?q=Docker+Compose+常用指令+up+down+logs+exec+scale
- https://www.google.com/search?q=Docker+Compose+.env+環境變數+設定+範例