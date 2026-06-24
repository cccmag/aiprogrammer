# Docker 1.9 網路革新

## 主要新功能

Docker 1.9 帶來了完整的網路功能：

- **Overlay Network**：跨主機網路
- **Swarm Discovery**：服務發現
- **Network IPAM**：IP 位址管理

## Overlay Network

```bash
# 建立 overlay 網路
docker network create --driver overlay my-network

# 使用網路
docker service create --name web \
  --network my-network \
  nginx
```

## Docker Swarm

```bash
# 初始化 Swarm
docker swarm init

# 加入節點
docker swarm join --token <token>

# 部署服務
docker stack deploy -c docker-compose.yml myapp
```

## 網路驅動程式

| 驅動 | 用途 |
|------|------|
| bridge | 單一主機 |
| host | 直接使用主機網路 |
| overlay | 多主機叢集 |
| macvlan | 直接賦予 MAC |

## 小結

Docker 1.9 解決了容器跨主機通訊的問題。

---

## 延伸閱讀

- [Docker 1.9 Release Notes](https://www.google.com/search?q=Docker+1.9+release+notes)
- [Docker Networking Guide](https://www.google.com/search?q=Docker+networking+tutorial)