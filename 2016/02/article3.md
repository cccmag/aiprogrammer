# 網路驅動與 CNM

## CNM 詳解

CNM（Container Network Model）是 Docker 提出的網路模型規範，定義了容器網路的三個核心元件：

**Network Sandbox**：隔離的網路命名空間，包含網卡、路由表、DNS 配置。與 Linux 的網路命名空間對應。

**Endpoint**：連接 Sandbox 到 Network 的橋樑。一個 Sandbox 可以有多個 Endpoint，連接到不同的網路。

**Network**：邏輯的網路交換機，一組 Endpoints 形成一個廣播域。

## bridge 驅動

bridge 是預設的網路驅動，適用於單一主機上的容器通訊。

```bash
# 建立自定義 bridge
docker network create --driver bridge my_bridge

# 啟動時指定網路
docker run -d --network my_bridge --name app myapp

# 動態將容器連接到網路
docker network connect my_bridge app2

# 斷開連接
docker network disconnect my_bridge app2
```

## host 驅動

使用 host 驅動，容器直接使用主機的網路命名空間，沒有隔離。

```bash
docker run --network host myapp
```

**優點**：網路效能最好，沒有額外的封裝開銷。
**缺點**：犧牲安全性，容器應用之間無法隔離，連接埠衝突風險高。

## overlay 驅動

overlay 網路支援跨多台 Docker 主機的容器通訊，是 Swarm Mode 的基礎。

```bash
# 初始化 Swarm
docker swarm init

# 建立 overlay 網路
docker network create --driver overlay --attachable my_overlay

# 建立服務
docker service create --name web --network my_overlay nginx
```

Overlay 網路使用 VXLAN 協定，將容器網路封裝在主機網路中傳輸。

## macvlan 驅動

macvlan 為每個容器分配真實的 MAC 位址，使其在網路上呈現為獨立的實體機器。

```bash
docker network create -d macvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    --ip-range=192.168.1.200/29 \
    -o parent=eth0 \
    my_macvlan

docker run --network my_macvlan --name app myapp
```

適用於需要直接被網路發現的應用（如監控系統）或需要固定 IP 的場景。

## none 驅動

完全禁用網路，適用於不需要網路連接的批次處理任務。

```bash
docker run --network none mybatch
```

## 服務發現機制

在自定義網路中，Docker 提供內建 DNS，可透過容器名稱解析 IP。

```bash
# 建立網路
docker network create my_net

# 啟動兩個容器
docker run -d --network my_net --name api myapi
docker run -d --network my_net --name web myweb

# web 可以透過 api 這個名稱訪問 API 服務
docker exec web ping -c 1 api
```

## DNS 設定

```bash
# 指定 DNS 伺服器
docker run --dns=8.8.8.8 --dns=8.8.4.4 myapp

# 新增主機映射
docker run --add-host=myhost:192.168.1.100 myapp

# 使用 /etc/hosts 中的別名
docker run --network-alias=api myapp
```

## 網路效能比較

| 驅動 | 適用場景 | 效能 | 隔離性 |
|------|---------|------|--------|
| bridge | 單主機容器通訊 | 中等 | 良好 |
| host | 效能敏感應用 | 最高 | 無 |
| overlay | 多主機 Swarm | 中等 | 良好 |
| macvlan | 網路發現應用 | 最高 | 良好 |

## 參考資源

- https://www.google.com/search?q=Docker+CNM+Container+Network+Model+bridge+host+overlay+macvlan+2016
- https://www.google.com/search?q=Docker+overlay+VXLAN+網路+原理+ Swarm+多主機
- https://www.google.com/search?q=Docker+DNS+服務發現+容器名稱+解析+設定