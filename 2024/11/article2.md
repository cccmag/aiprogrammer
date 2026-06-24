# Dockerfile 撰寫

## 1. 引言

Dockerfile 是 Docker 映像構建的藍圖。一個好的 Dockerfile 不僅能產出安全高效的映像，還能大幅減少構建時間。本文將從基礎到進階，全面講解 Dockerfile 的撰寫技巧。

## 2. Dockerfile 基礎指令

```dockerfile
# FROM：指定基礎映像
FROM node:20-alpine

# WORKDIR：設定工作目錄
WORKDIR /app

# COPY：複製檔案
COPY package.json package-lock.json ./

# RUN：執行命令
RUN npm ci --production

# 複製原始碼
COPY . .

# EXPOSE：宣告連接埠
EXPOSE 3000

# CMD：容器啟動命令
CMD ["node", "index.js"]
```

## 3. 多階段構建

多階段構建是減小映像體積的關鍵技術：

```dockerfile
# 第一階段：構建階段
FROM node:20 AS builder
WORKDIR /app
COPY package.json .
RUN npm ci
COPY . .
RUN npm run build

# 第二階段：運行階段
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

多階段構建的優勢很明顯：最終映像只包含運行所需的最小檔案，不包含構建工具鏈。上例中將 Node.js 映像從 1.2GB 縮小到約 200MB。

## 4. 層級快取優化

Docker 建構時會快取每一層。利用這個機制可以大幅加速構建：

```dockerfile
# 錯誤的寫法：每次修改程式碼都需重新安裝依賴
COPY . .
RUN npm ci

# 正確的寫法：利用快取
COPY package.json package-lock.json ./
RUN npm ci        # 只有依賴變更時才會重新執行
COPY . .          # 程式碼變更不會觸發 npm install
```

## 5. 生產環境最佳實踐

**使用特定版本標籤**：避免使用 `node:latest`

```dockerfile
FROM node:20.11.0-alpine3.19
```

**非 root 使用者**：增強安全性

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

**健康檢查**：

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
```

## 6. 映像瘦身技巧

| 技巧 | 說明 | 節省空間 |
|------|------|---------|
| 選擇小型基礎映像 | alpine slim 等 | 200-800MB |
| 多階段構建 | 分離構建和運行 | 50-80% |
| 清理快取 | `rm -rf /var/cache/*` | 10-50MB |
| 合併 RUN 指令 | 減少層數 | 依情況 |

## 7. 結語

Dockerfile 的品質直接影響部署效率和安全性。掌握多階段構建、層級快取和安全性最佳實踐，是成為 DevOps 工程師的必備技能。
