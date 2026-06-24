# 3. 映象管理與 Dockerfile 最佳化

## Dockerfile 語法

Dockerfile 是用來自動化建置 Docker 映象的指令檔案。每個指令都會在映象中建立一個新的層級。

### 基本語法

```dockerfile
# 基礎映象
FROM python:3.9-slim

# 維護者資訊（已過時，建議使用 LABEL）
MAINTAINER author@example.com

# 使用 LABEL 而非 MAINTAINER
LABEL maintainer="author@example.com"
LABEL version="1.0"
LABEL description="My application"

# 設定工作目錄
WORKDIR /app

# 複製檔案
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式
COPY . .

# 公開連接埠
EXPOSE 5000

# 環境變數
ENV NODE_ENV=production

# 執行命令
CMD ["python", "app.py"]
```

## 映象層快取機制

Docker 會快取每個步驟的結果。當 Dockerfile 的某層內容變更時，該層以及其後所有層都會重新建置。善用快取可以大幅縮短建置時間。

```dockerfile
# 良好的範例：先複製依賴檔案再複製程式碼
FROM node:14
WORKDIR /app

# 這層通常不改變，快取命中率 高
COPY package*.json ./
RUN npm ci --only=production

# 這層時常改變，放在後面
COPY . .
CMD ["npm", "start"]
```

## 多階段建置

多階段建置可以大幅縮小最終映象的大小。將建置工具與執行環境分開，最終映象只包含執行所需的檔案。

```dockerfile
# 第一階段：建置
FROM golang:1.16 AS builder
WORKDIR /src
COPY . .
RUN go build -o myapp

# 第二階段：執行
FROM alpine:latest
WORKDIR /root
COPY --from=builder /src/myapp .
CMD ["./myapp"]
```

## 映象大小優化技巧

**選擇適當的基礎映象**：使用 `alpine`、`slim` 等輕量映象。`python:3.9-slim` 比 `python:3.9` 小很多。

**減少層級**：合併多個 RUN 指令。

```dockerfile
# 不好的寫法
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim

# 好的寫法
RUN apt-get update && \
    apt-get install -y curl vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**使用 .dockerignore**：排除不需要的檔案，防止被複製到映象中。

```dockerignore
.git
.gitignore
node_modules
*.log
.env
```

## 映象發布流程

```bash
# 建置映象
docker build -t myapp:1.0 .

# 標記映象
docker tag myapp:1.0 registry.example.com/myapp:1.0

# 登入暫存器
docker login registry.example.com

# 推送映象
docker push registry.example.com/myapp:1.0
```

## 映象清理

```bash
# 刪除未使用的映象
docker image prune -a

# 刪除已停止的容器
docker container prune

# 刪除未使用的磁碟區
docker volume prune

# 完整的系統清理
docker system prune
```

## 參考資源

- https://www.google.com/search?q=Dockerfile+撰寫+最佳化+多階段建置+映象大小+層級+快取+2016
- https://www.google.com/search?q=Docker+映象+發布+tag+push+pull+私有暫存器+registry
- https://www.google.com/search?q=dockerignore+.dockerignore+寫法+排除+檔案+最佳實踐