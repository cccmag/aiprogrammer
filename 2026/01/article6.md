# Docker 基本指令

## 安裝 Docker

```bash
# macOS（使用 Homebrew）
brew install --cask docker

# Ubuntu
sudo apt update
sudo apt install docker.io docker-compose-v2

# 啟動 Docker
sudo systemctl enable docker && sudo systemctl start docker

# 將使用者加入 docker 群組（避免每次使用 sudo）
sudo usermod -aG docker $USER
# 重新登入後生效
```

## 映像管理

```bash
# 從 Docker Hub 搜尋映像
docker search pytorch

# 下載映像
docker pull pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# 列出本地已下載的映像
docker images

# 移除映像
docker rmi pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# 移除所有未使用的映像
docker image prune -a
```

## 容器基本操作

```bash
# 互動模式執行容器（退出後自動刪除）
docker run -it --rm pytorch/pytorch:latest bash

# 背景執行容器
docker run -d --name my_container pytorch/pytorch:latest sleep infinity

# 列出運行中的容器
docker ps

# 列出所有容器（包含已停止的）
docker ps -a

# 進入運行中的容器
docker exec -it my_container bash

# 查看容器日誌
docker logs my_container

# 停止容器
docker stop my_container

# 啟動已停止的容器
docker start my_container

# 移除容器
docker rm my_container
```

## GPU 容器

安裝 NVIDIA Container Toolkit 後，使用 `--gpus` 參數傳遞 GPU：

```bash
docker run --gpus all -it pytorch/pytorch:latest python -c "
import torch
print(f'CUDA: {torch.cuda.is_available()}, GPU: {torch.cuda.get_device_name(0)}')
"
```

## 資料掛載

將主機目錄掛載到容器中，實現資料共享：

```bash
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  pytorch/pytorch:latest bash
```

## 參考資源

- https://www.google.com/search?q=Docker+basic+commands+cheat+sheet+container+management
- https://www.google.com/search?q=Docker+GPU+access+NVIDIA+Container+Toolkit+run+command
- https://www.google.com/search?q=Docker+bind+mount+volume+data+persistence+guide
