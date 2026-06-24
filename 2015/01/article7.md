# Docker 容器化技術在 2015 年的崛起

## 前言

Docker 在 2015 年經歷了爆發式成長，成為 DevOps 和雲端運算領域的關鍵技術。

## 核心概念

```
傳統部署 vs Docker：
──────────────────────

傳統部署：
  - 應用 + 函式庫 + 作業系統 = 完整環境
  - 「在我的機器上可以跑」問題

Docker 部署：
  - 應用 + 函式庫 + 精簡 OS（Alpine）
  - 容器隔離，環境一致
```

## 基本命令

```bash
# 建立映像檔
docker build -t myapp:1.0 .

# 執行容器
docker run -d -p 80:3000 myapp:1.0

# 查看容器
docker ps
docker logs <container_id>

# 停止/刪除
docker stop <container_id>
docker rm <container_id>
```

## Dockerfile 範例

```dockerfile
FROM node:0.12
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

## 影響

Docker 改變了軟體的部署方式，讓「容器化」成為雲端時代的標準做法。

---

## 延伸閱讀

- [Docker 官方網站](https://www.google.com/search?q=Docker+container+technology+2015)
- [Docker 教學](https://www.google.com/search?q=Docker+tutorial+beginners)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*