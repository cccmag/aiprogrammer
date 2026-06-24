# 4. 容器網路架構

## Docker 網路模型

Docker 1.10 引入的 CNM（Container Network Model）定義了網路模型的三個核心元件：

**沙盒（Sandbox）**：容器的網路命名空間，包含網路介面、路由表、DNS 設定。

**端點（Endpoint）**：連接沙盒與網路的橋樑，一個沙盒可以有多個端點連接到不同網路。

**網路（Network）**：由一群端點組成的邏輯網路，類似傳統的乙太網路交換機。

## 網路驅動類型

### Bridge 網路

預設的網路驅動，適用於單一主機上的容器通訊。Docker 會在主機上建立一個 bridge 介面，容器連接到這個 bridge 上。

```bash
# 預設 bridge（不建議在應用程式直接使用）
# 自定義 bridge
docker network create --driver bridge my_bridge

# 啟動容器並連接到自定義 bridge
docker run -d --network my_bridge --name app myapp
```

### Host 網路

容器直接使用主機的網路命名空間，沒有網路隔離。適合效能敏感的應用，但犧牲了安全性。

```bash
docker run --network host myapp
```

### Overlay 網路

跨多台 Docker 主機的網路，需要 Docker Swarm 模式。Overlay 網路使用 VXLAN 協定封裝容器之間的流量。

```bash
# 需要先初始化 Swarm
docker swarm init

# 建立 overlay 網路
docker network create --driver overlay my_overlay

# 在 Swarm 服務中使用
docker service create --name app --network my_overlay myapp
```

### Macvlan 網路

為容器分配真實的 MAC 位址，讓容器看起來像網路上的實體機器。適合需要直接被網路發現的應用。

```bash
docker network create -d macvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o parent=eth0 \
    my_macvlan
```

## 容器間通訊

同一個 bridge 網路中的容器可以透過 IP 位址相互訪問。Docker 提供內部 DNS，可以透過容器名稱解析。

```bash
# 建立網路
docker network create my_net

# 啟動兩個容器
docker run -d --network my_net --name app1 myapp
docker run -d --network my_net --name app2 myapp

# app1 可以透過 app2 這個名稱訪問 app2
docker exec app1 ping -c 1 app2
```

## 網路隔離

可以使用網路隔離防止不同應用之間的容器相互訪問。

```bash
# 建立兩個隔離的網路
docker network create frontend_net
docker network create backend_net

# 容器連接到多個網路
docker run -d --network frontend_net --network backend_net --name app myapp
```

## 對外暴露連接埠

容器預設與外部網路隔離。需要透過 `-p` 參數映射連接埠。

```bash
# 映射單一連接埠
docker run -d -p 8080:80 nginx

# 映射多個連接埠
docker run -d -p 8080:80 -p 8443:443 nginx

# 映射到主機的任意可用連接埠
docker run -d -p 80 nginx
```

## 網路疑難排解

```bash
# 檢視網路
docker network ls

# 檢視網路詳細資訊
docker network inspect my_bridge

# 檢視容器連接的網路
docker inspect -f '{{range $key, $value := .NetworkSettings.Networks}}{{$key}} {{end}}' app1

# 測試容器間連線
docker exec app1 ping -c 1 app2
docker exec app1 curl http://app2:5000
```

## 參考資源

- https://www.google.com/search?q=Docker+網路+CNM+bridge+host+overlay+macvlan+驅動+2016
- https://www.google.com/search?q=Docker+容器間+通訊+DNS+服務發現+網路隔離+設定
- https://www.google.com/search?q=Docker+網路+Overlay+VXLAN+Swarm+多主機+容器+網路