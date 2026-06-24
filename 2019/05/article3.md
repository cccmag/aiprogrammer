# Docker 容器化：ML 開發環境

## 前言

Docker 容器化技術可以幫助 AI 開發者建立一致、可重現的開發環境。

## 基本概念

```dockerfile
# Dockerfile
FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
    tensorflow-gpu==1.13.1 \
    pytorch==1.1.0 \
    numpy \
    pandas

WORKDIR /workspace
COPY . .

CMD ["python3", "train.py"]
```

## 常用命令

```bash
# 構建映像
docker build -t ml-project:v1 .

# 執行容器
docker run --gpu --rm -v $(pwd):/workspace ml-project:v1

# GPU 支持
docker run --gpu all --rm nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04 nvidia-smi
```

## Docker Compose

```yaml
# docker-compose.yml
version: '3'
services:
  jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/workspace
    gpu: true
    command: jupyter notebook --ip=0.0.0.0
```

## 延伸閱讀

- [Docker 官方文檔](https://www.google.com/search?q=docker+for+machine+learning)