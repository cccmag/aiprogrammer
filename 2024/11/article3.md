# Docker 常用指令

## 1. 引言

Docker 指令眾多，但日常開發中常用的只有少數。本文整理了一份 Docker 指令速查手冊，按照使用場景分類，每個指令附有實例說明。

## 2. 映像管理

```bash
# 列出本機映像
docker images

# 搜尋遠端倉庫的映像
docker search nginx

# 下載映像
docker pull nginx:alpine

# 刪除映像
docker rmi nginx:alpine

# 建立映像（從 Dockerfile）
docker build -t myapp:latest .

# 標記映像
docker tag myapp:latest user/myapp:v1

# 推送映像到倉庫
docker push user/myapp:v1
```

## 3. 容器生命週期

```bash
# 啟動容器
docker run -d --name web -p 3000:3000 myapp

# 列出運行中的容器
docker ps

# 列出所有容器（包含已停止）
docker ps -a

# 停止容器
docker stop web

# 啟動已停止的容器
docker start web

# 重啟容器
docker restart web

# 刪除容器（需先停止）
docker rm web

# 強制刪除運行中的容器
docker rm -f web
```

## 4. 容器互動

```bash
# 進入容器互動介面
docker exec -it web sh

# 查看容器日誌
docker logs web

# 即時追蹤日誌
docker logs -f web

# 查看容器詳情
docker inspect web

# 查看容器資源使用
docker stats web

# 複製檔案到容器
docker cp app.js web:/app/

# 從容器複製檔案
docker cp web:/app/log.txt ./
```

## 5. 網路管理

```bash
# 列出網路
docker network ls

# 建立網路
docker network create mynet

# 連接容器到網路
docker network connect mynet web

# 斷開容器與網路
docker network disconnect mynet web

# 查看網路詳情
docker network inspect mynet
```

## 6. 儲存管理

```bash
# 列出卷
docker volume ls

# 建立卷
docker volume create mydata

# 查看卷詳情
docker volume inspect mydata

# 刪除卷
docker volume rm mydata
```

## 7. Compose 相關

```bash
# 啟動服務
docker compose up -d

# 停止服務
docker compose down

# 查看服務日誌
docker compose logs -f

# 重建服務
docker compose up -d --build

# 查看服務狀態
docker compose ps
```

## 8. 實用技巧

**清除未使用的資源**：

```bash
# 清除所有未使用的容器
docker container prune

# 清除所有未使用的映像
docker image prune

# 一鍵清理所有未使用資源
docker system prune -a
```

**查看磁碟使用**：

```bash
docker system df
```

## 9. 結語

掌握這些常用指令足以應付大部分 Docker 日常操作。建議將本文件收藏為速查手冊，遇到不熟悉的指令時可以快速查閱。
