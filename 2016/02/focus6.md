# 6. Docker Swarm 容器編排

## Swarm 模式介紹

Docker Swarm 是 Docker 原生的容器編排工具。在 Docker 1.12 中，Swarm Mode 被整合到 Docker Engine 中，無需額外安裝即可使用。Swarm 讓多台 Docker 主機形成一個叢集，統一管理容器的部署、擴展、負載平衡。

## 基本概念

**節點（Node）**：參與 Swarm 叢集的 Docker 主機。可分為 Manager 節點（負責叢集管理）與 Worker 節點（負責執行容器）。

**服務（Service）**：定義要在叢集中執行的容器。服務會自動將容器分發到多個節點上。

**任務（Task）**：服務將工作分配給多個任務，每個任務對應一個容器執行個體。

## 初始化叢集

```bash
# 初始化 Swarm，成為 Manager
docker swarm init --advertise-addr 192.168.1.100

# 檢視叢集狀態
docker node ls

# 取得 Worker 加入指令
docker swarm join-token worker

# 脫離 Swarm
docker swarm leave
```

## 部署服務

```bash
# 建立服務
docker service create --name web --replicas 3 -p 80:80 nginx

# 檢視服務
docker service ls
docker service ps web

# 檢視服務詳細資訊
docker service inspect web

# 水平擴展
docker service scale web=5

# 更新映像
docker service update --image nginx:1.13 web

# 滾動更新
docker service update --image nginx:1.14 web --update-delay 10s --update-parallelism 2
```

## 全域服務

全域服務在叢集的每個節點上都會執行一個容器，適合監控代理、防日志收集等需要每台機器都執行的場景。

```bash
docker service create \
    --mode global \
    --name monitoring-agent \
    prometheus/node-exporter
```

## 負載平衡

Swarm 提供了內建的 Ingress 負載平衡。當存取節點的發布連接埠時，Swarm 會自動將流量分散到各個容器。

```bash
# 發布連接埠
docker service create --name web --replicas 3 -p 8080:80 nginx

# 外部可透過任何節點的 IP:8080 訪問服務
# Swarm 會自動將請求分散到健康容器
```

## 健康檢查

可為服務設定健康檢查，Swarm 會自動重啟失敗的容器。

```dockerfile
# 在 Dockerfile 中定義
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost/ || exit 1
```

或在 `docker service create` 時指定：

```bash
docker service create \
    --name web \
    --health-cmd="curl -f http://localhost/" \
    --health-interval=30s \
    --health-retries=3 \
    -p 80:80 \
    nginx
```

## 資料庫的高可用性

對於需要持久化的服務（如資料庫），建議使用 `-p constraint:node==` 將容器固定到特定節點，或使用共有磁碟區。

```bash
# 使用約束將服務部署到特定節點
docker service create \
    --name db \
    --constraint 'node.role==manager' \
    -v db_data:/var/lib/postgresql/data \
    postgres:13
```

## 參考資源

- https://www.google.com/search?q=Docker+Swarm+容器編排+叢集+服務+replicas+設定+2016
- https://www.google.com/search?q=Docker+Swarm+初始化+join+node+Manager+Worker+設定
- https://www.google.com/search?q=Docker+Swarm+滾動更新+健康檢查+負載平衡+高可用性