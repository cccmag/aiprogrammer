# Docker 與容器化部署（2015-2016）

## 前言

Docker 徹底改變了軟體部署的方式。容器化讓「在我的機器上能跑」成為過去。

## Docker 基礎

### Dockerfile

```dockerfile
FROM node:6-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["npm", "start"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db/myapp
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3

  db:
    image: postgres:9.6
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword

  redis:
    image: redis:3.2-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 容器化 CI/CD

### 建置階段

```dockerfile
# Dockerfile.build
FROM node:6 AS builder

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
RUN npm test

FROM builder AS test
RUN npm run test:ci

FROM node:6-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### CI Pipeline 中的 Docker

```groovy
// Jenkinsfile
pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.build'
        }
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    def image = docker.build("myapp:${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    docker.image("myapp:${env.BUILD_NUMBER}").inside {
                        sh 'npm test'
                    }
                }
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        def image = docker.build("myapp:${env.BUILD_NUMBER}")
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
    }
}
```

## Docker Swarm Mode

```bash
# 初始化 Swarm
docker swarm init

# 建立服務
docker service create \
  --name myapp \
  --replicas 3 \
  --publish 3000:3000 \
  --update-delay 10s \
  --update-parallelism 1 \
  myapp:latest

# 更新服務
docker service update \
  --image myapp:2.0.0 \
  myapp

# 滾動更新
docker service update \
  --image myapp:2.0.0 \
  --update-parallelism 2 \
  --update-delay 20s \
  myapp
```

## 容器化部署腳本

```bash
#!/bin/bash
# deploy-docker.sh

IMAGE_NAME="myapp"
CONTAINER_NAME="myapp-prod"
REGISTRY="docker.io"
TAG=${1:-latest}
PORT=3000

echo "Deploying $IMAGE_NAME:$TAG..."

# 拉取新映像
docker pull $REGISTRY/$IMAGE_NAME:$TAG

# 停止舊容器
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

# 啟動新容器
docker run -d \
  --name $CONTAINER_NAME \
  --restart unless-stopped \
  --env-file .env.production \
  -p $PORT:3000 \
  $REGISTRY/$IMAGE_NAME:$TAG

# 健康檢查
sleep 5
if docker ps | grep -q $CONTAINER_NAME; then
    echo "Deployment successful!"
else
    echo "Deployment failed!"
    exit 1
fi

# 清理舊映像
docker image prune -f
```

## Docker 監控

```yaml
# docker-compose.monitoring.yml
version: '3'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - app

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus

  app:
    image: myapp:latest
    ports:
      - "3000:3000"
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=3000"
```

## 延伸閱讀

- [Docker 官方文檔](https://www.google.com/search?q=docker+tutorial+2016)
- [Docker Compose 教學](https://www.google.com/search?q=docker+compose+tutorial+2016)
- [Docker Swarm 部署](https://www.google.com/search?q=docker+swarm+deployment+2016)

## 結語

Docker 讓部署變得一致且可重現。結合 CI/CD，實現真正的「一次建置，到處執行」。

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*