# 2. Docker 1.10 新功能詳解

## Docker 1.10 概述

Docker 1.10 是 2016 年初最重要的版本更新，帶來多項長期等待的功能。這個版本的開發重點在於增強容器的安全性、網路功能、以及映象管理能力。

## Swarm Mode

Docker 1.12 將 Swarm Mode 整合進 Docker Engine 本身，這裡我們說的是 1.10 版本中為即將到來的整合做準備的相關改進。Swarm Mode 讓多台 Docker 主機可以形成一個叢集，統一管理容器的部署與調度。

### 初始化 Swarm

```bash
# 初始化 Swarm（，成為 Manager）
docker swarm init --advertise-addr 192.168.1.100

# 加入 Worker 節點
docker swarm join --token SWMTKN-1-xxxxx 192.168.1.100:2377

# 檢視節點狀態
docker node ls
```

### 部署服務

```bash
# 建立服務
docker service create --name web --replicas 3 -p 80:80 nginx

# 檢視服務
docker service ls
docker service ps web

# 擴展服務
docker service scale web=5

# 更新服務
docker service update --image nginx:1.13 web
```

## 網路驅動重構

Docker 1.10 對網路系統進行了大規模重構，引入了 CNM（Container Network Model）與新的 IP Address Management（IPAM）插件系統。

### 內建網路驅動

**bridge**：預設的網路驅動，為單一主機上的容器提供網路隔離。

**host**：移除容器與主機之間的網路隔離，容器直接使用主機的網路堆疊。

**overlay**：跨多台 Docker 主機的網路，支援 Swarm Mode 的服務發現。

**macvlan**：為容器分配 MAC 位址，使其在網路上看起來像傳統的實體機器。

```bash
# 建立自定義 bridge 網路
docker network create --driver bridge my_bridge

# 建立 overlay 網路（需要 Swarm 模式）
docker network create --driver overlay my_overlay

# 在指定網路中啟動容器
docker run -d --network my_bridge --name app myapp
```

## 內容位址儲存（Content Addressable Storage）

Docker 1.10 採用內容位址儲存來管理映象層級。每個映象層都有一個根據內容計算的 SHA256 雜湊值作為唯一識別碼。這提升了映象的安全性與效能：

- 映象層不會重複儲存，節省磁碟空間
- 可驗證映象層的完整性，防止篡改
- 提高映象拉取與推送的效率

## 服務發現

在 Swarm 模式下，每個服務都會被自動賦予一個虛擬 IP（VIP），並透過內部 DNS 進行服務發現。容器可以透過服務名稱訪問其他服務，DNS 會自動解析到正確的容器 IP。

```bash
# 建立服務並指定網路
docker service create --name api --network my_overlay api-image

# 另一個服務可以透過服務名走訪
docker service create --name web --network my_overlay --env "API_HOST=api" web-image
```

## 日誌驅動改進

Docker 1.10 支援更多的日誌驅動，包括 syslog、journald、gelf、fluentd。使用者可選擇將容器日誌發送到統一的日誌收集系統。

```bash
# 啟動容器並指定日誌驅動
docker run -d --log-driver=syslog --log-opt syslog-address=tcp://logserver:514 myapp

# 設定 Docker Daemon 預設日誌驅動
echo '{"log-driver": "json-file", "log-opts": {"max-size": "10m", "max-file": "3"}}' > /etc/docker/daemon.json
```

## 參考資源

- https://www.google.com/search?q=Docker+1.10+新功能+Swarm+Mode+overlay+network+CNM+2016
- https://www.google.com/search?q=Docker+Swarm+初始化+服務+部署+scale+update+教學
- https://www.google.com/search?q=Docker+內容位址儲存+CAS+映象層+sha256+安全性