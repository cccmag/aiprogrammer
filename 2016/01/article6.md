# Docker 容器化基礎

## Docker 介紹

Docker 是一個開源的容器化平台，讓開發者能將應用程式及其相依環境封裝成一個可攜的映象（Image），在任何支援 Docker 的環境中一致運行。2016 年的 Docker 生態系已經相當成熟，Docker Hub 有數十萬個公開映象可供使用。

## 安裝 Docker

macOS 或 Windows 可下載 Docker Toolbox 或 Docker for Mac/Windows Installer。Linux 各 distribution 可使用官方安裝脚本：

```bash
curl -fsSL https://get.docker.com/ | sh
sudo usermod -aG docker $USER
newgrp docker
```

## 核心概念

**映象（Image）**：唯讀的模板，包含應用程式與所有依賴。一個映象可用於建立多個容器。

**容器（Container）**：映象的執行實例，類似輕量級虛擬機。可啟動、停止、刪除。

**暫存器（Registry）**：儲存與分發映象的服務。Docker Hub 是最大的公有暫存器。

**Dockerfile**：文字格式的建置指令，用於自動建立映象。

## 基礎指令

```bash
# 拉取映象
docker pull ubuntu:20.04

# 列出本機映象
docker images

# 啟動互動式容器
docker run -it ubuntu:20.04 /bin/bash

# 在背景執行容器
docker run -d --name myapp -p 8080:80 nginx

# 列出執行中的容器
docker ps

# 列出所有容器（含已停止）
docker ps -a

# 停止容器
docker stop myapp

# 刪除容器
docker rm myapp

# 刪除映象
docker rmi nginx
```

## 建立自訂映象

建立簡單的 Python Web 服務映象：

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
# 建置映象
docker build -t mypythonapp .

# 執行
docker run -p 5000:5000 mypythonapp
```

## Docker Hub 使用

```bash
# 登入 Docker Hub
docker login

# 標記映象
docker tag mypythonapp username/mypythonapp:v1.0

# 推送至 Docker Hub
docker push username/mypythonapp:v1.0

# 從 Docker Hub 拉取
docker pull username/mypythonapp:v1.0
```

## 參考資源

- https://www.google.com/search?q=Docker+安裝+基本指令+容器+映象+教學+2016+1月
- https://www.google.com/search?q=Dockerfile+撰寫+範例+FROM+RUN+COPY+EXPOSE+CMD
- https://www.google.com/search?q=Docker+Hub+映象+發布+分享+使用+教学