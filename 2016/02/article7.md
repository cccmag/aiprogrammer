# 跨主機網路 overlay

## Overlay 網路原理

Overlay 網路是 Docker Swarm 實現跨主機容器通訊的基礎。它使用 VXLAN 協定，在底層網路之上建立一個虛擬的二層網路。

### 封裝與路由

當容器 A（主機 1）要與容器 B（主機 2）通訊時：

1. 容器 A 產生乙太網路框架（包含目標 MAC、來源 MAC、IP）
2. VXLAN 將這個框架封裝成 UDP 封包（使用 VTEP 的 IP）
3. 透過底層網路傳輸到目標主機
4. 目標主機解封裝，取出原始框架交給容器 B

### VTEP（VXLAN Tunnel End Point）

每台 Docker 主機都有一個 VTEP，負責封裝與解封裝 VXLAN 流量。VTEP 有兩個介面：
- 實體網路介面：連接到基礎網路
- VXLAN 介面：連接到 overlay 網路

## 初始化 Swarm

Overlay 網路需要 Swarm 模式才能運作：

```bash
# 初始化 Swarm
docker swarm init --advertise-addr 192.168.1.100

# 檢視加入指令（含 Token）
docker swarm join-token worker
docker swarm join-token manager

# 將其他節點加入叢集
docker swarm join --token SWMTKN-1-xxxxx 192.168.1.100:2377
```

## 建立 Overlay 網路

```bash
# 建立可附加的 overlay 網路（支援叢集外的容器）
docker network create -d overlay --attachable my_overlay

# 建立普通的 overlay 網路（僅用於 Swarm 服務）
docker network create -d overlay my_overlay
```

## 服務發現

在 overlay 網路中，服務名稱會自動註冊到內部 DNS。叢集內的任何容器都可以透過服務名稱解析到服務的虛擬 IP。

```bash
# 建立服務
docker service create --name api --network my_overlay api-image

# 另一個服務可以透過 api 這個名稱訪問
docker service create --name web --network my_overlay --env "API_HOST=api" web-image
```

## 部署多節點服務

```bash
# 建立具有 3 個副本的服務
docker service create --name web \
    --replicas 3 \
    --network my_overlay \
    -p 80:80 \
    nginx

# 檢視服務分布
docker service ps web

# 結果可能類似：
# ID             NAME      IMAGE  NODE      DESIRED STATE
# abc123         web.1     nginx  node-1    Running
# def456         web.2     nginx  node-2    Running
# ghi789         web.3     nginx  node-3    Running
```

## 負載平衡

Swarm 提供了兩層負載平衡：

**入口負載平衡（Ingress Load Balancing）**：外部流量透過任何節點的 published port 進入，由 Swarm 自動分散到健康容器。

**服務層級負載平衡（Service-level LB）**：叢集內的容器可透過服務名稱訪問服務，DNS 解析到服務的 VIP，流量透過 Swarm 的 IPVS 負載平衡分發。

## 網路隔離

使用 network overlay 的 `internal` 選項建立隔離的 overlay 網路：

```bash
# 建立隔離的 overlay（不連接到外部網路）
docker network create -d overlay --internal my_private_net
```

## 故障排除

```bash
# 檢視節點狀態
docker node ls

# 檢視網路詳細資訊
docker network inspect my_overlay

# 檢視服務日誌
docker service logs web

# 在特定節點上執行容器除錯
docker run --rm -it --network my_overlay --entrypoint sh myapp
```

## 效能考量

Overlay 網路有額外的封裝開銷：
- 每個封包增加 50 bytes（VXLAN header）
- 需要額外的 CPU 進行封裝/解封裝
- 對延遲敏感的應用可能需要考虑直接路由或 macvlan

## 參考資源

- https://www.google.com/search?q=Docker+overlay+VXLAN+網路+原理+跨主機+容器+通訊+2016
- https://www.google.com/search?q=Docker+Swarm+overlay+網路+設定+服務發現+負載平衡
- https://www.google.com/search?q=Docker+overlay+效能+延遲+封裝+開銷+最佳化