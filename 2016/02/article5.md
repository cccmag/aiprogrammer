# 資源限制與監控

## 為什麼需要資源限制

在共享主機環境中，若某個容器無限制使用資源，會影響同一主機上其他容器的效能。設定資源限制可確保所有容器公平地共享主機資源。

## 記憶體限制

```bash
# 設定硬上限
docker run -d --name myapp --memory="256m" myapp

# 設定記憶體 + swap 總上限
docker run -d --name myapp --memory="256m" --memory-swap="512m" myapp

# 設定軟上限（可突破，但會被惩罚）
docker run -d --name myapp --memory="128m" --memory-reservation="64m" myapp
```

## CPU 限制

```bash
# 限制 CPU 核心數
docker run -d --name myapp --cpus="0.5" myapp

# 限制特定 CPU 核心
docker run -d --name myapp --cpuset-cpus="0,1" myapp

# 設定 CPU  Shares（相對比重，預設 1024）
docker run -d --name myapp --cpu-shares="512" myapp
```

## 區塊 IO 限制

```bash
# 限制讀寫速率（每秒位元組）
docker run -d --name myapp \
    --device-read-bps /dev/sda:1mb \
    --device-write-bps /dev/sda:1mb \
    myapp

# 限制 IOPS
docker run -d --name myapp \
    --device-read-iops /dev/sda:100 \
    --device-write-iops /dev/sda:100 \
    myapp
```

## 設定檔

在 `/etc/docker/daemon.json` 中設定預設限制：

```json
{
    "default-ulimits": {
        "memlock": {
            "Name": "memlock",
            "Soft": -1,
            "Hard": -1
        }
    },
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}
```

```bash
sudo systemctl restart docker
```

## 監控工具

### docker stats

即時查看容器資源使用：

```bash
# 即時統計
docker stats

# 只看特定容器
docker stats myapp

# 無色彩輸出（適合 Script）
docker stats --no-stream myapp
```

### Prometheus + Grafana

Prometheus 是最受歡迎的开源監控系統，可收集 Docker 指標並視覺化。

```yaml
# docker-compose.yml
version: "3.8"
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secret

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
```

### cAdvisor

Google 開發的容器監控工具，可收集 Docker 容器的資源使用資料。

```bash
docker run \
    --volume=/:/rootfs:ro \
    --volume=/var/run:/var/run:ro \
    --volume=/sys:/sys:ro \
    --volume=/var/lib/docker/:/var/lib/docker:ro \
    --publish=8080:8080 \
    --detach=true \
    --name=cadvisor \
    gcr.io/cadvisor/cadvisor:latest
```

## 自動重啟政策

設定容器崩潰時的自動重啟行為：

```bash
# 關閉自動重啟（預設）
docker run --restart=no myapp

# 失敗時重啟
docker run --restart=on-failure myapp

# 任何退出時重啟
docker run --restart=always myapp

# 限制重啟次數（5 分鐘內最多 3 次）
docker run --restart=on-failure:3 myapp
```

## 資源不足的徵兆

- OOMKilled：容器因記憶體不足被核心終止
- CPU throttling：容器 CPU 使用被節流
- IO wait：高磁碟 IO 延遲
- Network packet loss：網路封包遺失

發現這些徵兆時，應調整資源限制或優化應用程式效能。

## 參考資源

- https://www.google.com/search?q=Docker+資源限制+記憶體+CPU+IO+設定+教學+2016
- https://www.google.com/search?q=Docker+監控+cadvisor+Prometheus+Grafana+安裝+設定
- https://www.google.com/search?q=Docker+stats+容器+資源使用+統計+查詢+方法