# 登錄與私有暫存器

## Docker Hub 使用

Docker Hub 是最大的公有 Docker 映象暫存器，類似 GitHub 之於程式碼。

### 基本操作

```bash
# 登入 Docker Hub
docker login

# 搜尋映象
docker search nginx

# 拉取映象
docker pull nginx:1.21

# 推送映象到 Docker Hub
docker tag myapp:1.0 username/myapp:1.0
docker push username/myapp:1.0
```

### 建立組織與團隊

Docker Hub 的組織功能允許團隊共享私人映象。免費方案可建立一個私人儲存庫，付費方案可建立多個。

## 私有暫存器

對於企業內部的映象，通常會架設私有 Docker 暫存器。

### 部署私有暫存器

```bash
# 執行 Registry 容器
docker run -d \
    --name registry \
    -p 5000:5000 \
    --restart=always \
    -v registry_data:/var/lib/registry \
    registry:2

# 驗證
curl http://localhost:5000/v2/_catalog
```

### 使用私有暫存器

```bash
# 標記映象以指向私有暫存器
docker tag myapp:1.0 registry.example.com:5000/myapp:1.0

# 推送到私有暫存器
docker push registry.example.com:5000/myapp:1.0

# 從私有暫存器拉取
docker pull registry.example.com:5000/myapp:1.0
```

### 設定 insecure-registries

若使用 HTTP（而非 HTTPS），需要設定 Docker 信任該暫存器。

```json
// /etc/docker/daemon.json
{
    "insecure-registries": ["registry.example.com:5000"]
}
```

```bash
sudo systemctl restart docker
```

## TLS 認證的私有暫存器

正式環境應該為私有暫存器設定 TLS 認證。使用 Let's Encrypt 取得免費 SSL 憑證：

```bash
# 安裝 Nginx 與 Let's Encrypt
apt-get install nginx certbot

# 取得憑證
certbot certonly --standalone -d registry.example.com

# Nginx 設定
```

## Harbor 企業級暫存器

Harbor 是 VMware 開發的企業級映象暫存器，提供圖形介面、映象掃描、存取控制、複製等功能。

```bash
# 使用 Docker Compose 部署 Harbor
wget https://github.com/goharbor/harbor/releases/download/v1.10.0/harbor-offline-installer-v1.10.0.tgz
tar xzf harbor-offline-installer-v1.10.0.tgz
cd harbor
./prepare
./install.sh
```

## 映象發布最佳實踐

1. **版本標籤**：除了 `latest`，總是使用有意義的版本標籤如 `v1.2.3` 或 `git-commit-hash`。

```bash
docker tag myapp:1.0 registry.example.com/myapp:v1.2.3
docker tag myapp:1.0 registry.example.com/myapp:latest
```

2. **多架構映象**：支援 amd64、arm64 等多種 CPU 架構。

```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:1.0 --push .
```

3. **映象說明文件**：在 Docker Hub 上提供詳細的使用說明。

## 參考資源

- https://www.google.com/search?q=Docker+私有暫存器+Registry+架設+TLS+HTTPS+設定+2016
- https://www.google.com/search?q=Docker+Hub+映象+發布+團隊+組織+權限+管理
- https://www.google.com/search?q=Harbor+映象+暫存器+企業+安裝+設定+v1.10