# Docker 與 Node.js 容器化

## 前言

Docker 讓 Node.js 應用的部署更加一致和可靠。

## Dockerfile for Node.js

```dockerfile
FROM node:0.12

WORKDIR /app

COPY package.json .
RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

## 優勢

```
Docker 優勢：
───────────
- 一致的環境（開發、生產相同）
- 快速部署
- 擴展容易
- 資源隔離
```

## docker-compose

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - mongo
```

---

## 延伸閱讀

- [Docker Node.js 部署](https://www.google.com/search?q=Docker+Node.js+deployment+tutorial)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」文章之一。*