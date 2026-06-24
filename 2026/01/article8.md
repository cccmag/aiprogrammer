# docker-compose 多容器

## 為什麼需要 docker-compose？

AI 專案通常不只一個服務：訓練程式、Jupyter Lab、資料庫、模型 API。docker-compose 讓你能用一個 YAML 檔案定義並運行多個容器。

## 基本範例

```yaml
version: '3.8'

services:
  jupyter:
    image: jupyter/datascience-notebook:latest
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
    environment:
      - JUPYTER_ENABLE_LAB=yes

  training:
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    volumes:
      - ./data:/data
      - ./models:/models
    depends_on:
      - jupyter

  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - training
```

## 常用指令

```bash
# 啟動所有服務
docker compose up -d

# 查看日誌
docker compose logs -f

# 重新建置並啟動特定服務
docker compose up -d --build training

# 停止服務
docker compose down

# 停止並移除 volume
docker compose down -v
```

## GPU 支援

```yaml
services:
  train:
    image: pytorch/pytorch:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## 資料持久化

```yaml
services:
  postgres:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## 多環境配置

```bash
# 開發環境
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# 生產環境
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## 參考資源

- https://www.google.com/search?q=docker-compose+GPU+support+YAML+config
- https://www.google.com/search?q=docker-compose+multi+container+AI+workflow
