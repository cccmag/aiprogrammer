# 7. 安全考量與強化

## 容器安全的基本概念

容器雖然提供了程序層級的隔離，但並非完全安全。共享主機核心意味著核心漏洞可能影響所有容器。此外，映象的安全性、網路存取控制、運行時權限都是需要關注的面向。

## 映象安全

### 使用官方映象

優先使用 Docker Official Images 或可信賴的組織映象。這些映象經過安全審查，定期更新以修補漏洞。

```bash
# 官方 Python 映象
FROM python:3.9-slim

# 而非第三方作者的可能存在問題的映象
# FROM someuser/python
```

### 避免使用 latest 標籤

`latest` 標籤會自動指向最新版本，可能導致不一致的部署結果。

```dockerfile
# 不建議
FROM nginx:latest

# 建議：使用確切版本
FROM nginx:1.21.6
```

### 掃描映象漏洞

```bash
# 安裝 Anchore 進行映象掃描
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    anchore/anchore-cli:latest \
    image add myapp:1.0

docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    anchore/anchore-cli:latest \
    image vuln myapp:1.0 all
```

## 執行時安全

### 非 root 使用者執行

預設容器以 root 身份執行，這是潛在的安全風險。建議建立專用使用者。

```dockerfile
# 建立使用者
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# 切換到非 root 使用者
USER appuser

# 或在執行時指定
docker run -u 1000 myapp
```

### 限制資源使用

防止單一容器耗盡主機資源。

```bash
# 限制 CPU 與記憶體
docker run -d \
    --memory="256m" \
    --memory-swap="256m" \
    --cpus="0.5" \
    --name myapp \
    myapp
```

### 唯讀檔案系統

對於不需要寫入檔案系統的應用程式，可以設定唯讀。

```bash
docker run --read-only --name myapp myapp
```

## 網路安全

### 禁止網路特權模式

```bash
# 不建議：容器具有網路特權
docker run --privileged myapp

# 建議：只開放需要的連接埠
docker run -p 127.0.0.1:8080:80 myapp
```

### 使用網路隔離

將需要互相通信的容器放在同一網路，與其他容器隔離。

```bash
docker network create trusted_net
docker network create public_net

# 信任的服務
docker run -d --network trusted_net myapp

# 不信任的服務
docker run -d --network public_net untrustedapp
```

## 核心安全模組

### AppArmor / SELinux

啟用安全性模組來限制容器的權限。

```bash
# 使用 AppArmor 設定檔
docker run --security-opt apparmor=docker-default myapp

# 使用 SELinux 設定
docker run --security-opt label=type:container_file_t myapp
```

## Secret 管理

Swarm 提供內建的 Secret 管理機制，安全存儲敏感資訊。

```bash
# 建立 Secret
echo "mypassword" | docker secret create db_password -

# 建立服務時使用 Secret
docker service create \
    --name web \
    --secret db_password \
    -e DB_PASSWORD_FILE=/run/secrets/db_password \
    myapp
```

## 安全最佳實踐總結

1. 定期更新基礎映象與應用程式依賴
2. 掃描映象中的已知漏洞
3. 避免使用 `--privileged` 旗標
4. 以非 root 使用者執行容器程序
5. 限制容器資源使用
6. 使用網路隔離保護敏感服務
7. 啟用 Docker Content Trust 驗證映象簽名
8. 集中收集並監控容器日誌

## 參考資源

- https://www.google.com/search?q=Docker+容器安全+最佳實踐+強化+設定+2016
- https://www.google.com/search?q=Docker+映象+漏洞+掃描+Clair+Anchore+Trivy
- https://www.google.com/search?q=Docker+安全+AppArmor+SELinux+seccomp+能力+權限+限制