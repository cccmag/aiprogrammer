# Docker 容器化

## 映像、容器、倉庫

### 前言

Docker 自 2013 年發布以來，徹底改變了軟體部署的方式。容器技術讓應用程式與其依賴環境打包在一起，確保在任何環境中都能一致地執行。本節將深入探討 Docker 的核心概念與實務操作。

### 核心概念

**映像（Image）**

映像是唯讀的範本，包含了運行應用程式所需的一切：程式碼、運行時、系統工具、函式庫和配置。映像是分層構建的，每一層都是 Dockerfile 中的一條指令。

```dockerfile
# 一個簡單的 Node.js 應用映像
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["node", "index.js"]
```

**容器（Container）**

容器是映像的可執行實例。它是一個輕量級的隔離環境，擁有自己的檔案系統、網路和行程空間。多個容器可以在同一台主機上運行，共享作業系統核心。

```bash
# 從映像啟動容器
docker run -d -p 3000:3000 --name myapp myapp:latest

# 查看運行中的容器
docker ps

# 進入容器內部
docker exec -it myapp sh
```

**倉庫（Registry）**

倉庫用於儲存和分發映像。Docker Hub 是最著名的公共倉庫，私有倉庫可以使用 Docker Registry、AWS ECR 或 Harbor 等方案。

```bash
# 上傳映像到倉庫
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest

# 下載映像
docker pull username/myapp:latest
```

### Dockerfile 最佳實踐

**使用 `.dockerignore`**

類似 `.gitignore`，避免將不必要的檔案複製到映像中：

```
node_modules
.git
*.md
.env
```

**多階段構建（Multi-stage Build）**

將構建環境與運行環境分離，大幅減小映像體積：

```dockerfile
# 第一階段：構建
FROM node:20 AS builder
WORKDIR /app
COPY package.json .
RUN npm ci
COPY . .
RUN npm run build

# 第二階段：運行
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### Docker 網路模式

Docker 提供多種網路模式，滿足不同的隔離需求：

| 模式 | 說明 | 使用場景 |
|------|------|---------|
| bridge | 預設，容器間互通 | 單機多容器 |
| host | 共用主機網路 | 效能敏感場景 |
| none | 無網路 | 安全隔離 |
| overlay | 跨主機網路 | Swarm/K8s |

### Docker 儲存管理

容器的檔案系統是短暫的，容器刪除後資料也會消失。使用 Volume 或 Bind Mount 持久化資料：

```bash
# 建立 Volume
docker volume create mydata

# 掛載 Volume
docker run -v mydata:/app/data myapp

# Bind Mount（開發時常用）
docker run -v $(pwd):/app myapp
```

### 小結

Docker 容器化是 DevOps 自動化部署的基石。理解映像、容器和倉庫三大概念，掌握 Dockerfile 撰寫技巧，就能為 CI/CD 管線建立穩固的基礎。下一節將探討如何使用 Docker Compose 管理多容器應用。

---

**下一步**：[Docker Compose 多容器](focus3.md)

## 延伸閱讀

- [Docker 官方文件](https://www.google.com/search?q=Docker+official+documentation)
- [Dockerfile 最佳實踐](https://www.google.com/search?q=Dockerfile+best+practices)
- [多階段構建指南](https://www.google.com/search?q=Docker+multi-stage+build)
