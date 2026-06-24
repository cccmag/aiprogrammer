# 日誌管理與驅動

## Docker 日誌架構

Docker  daemon 接收來自容器的 stdout 與 stderr 輸出，並將其寫入日誌檔案或發送到日誌收集系統。每個容器都有一個獨立的日誌檔案。

```bash
# 查看容器日誌
docker logs mycontainer

# 即時追蹤日誌
docker logs -f mycontainer

# 查看最後 100 行
docker logs --tail 100 mycontainer
```

## 日誌驅動

Docker 支援多種日誌驅動，可在 `/etc/docker/daemon.json` 中設定。

### json-file（預設）

```json
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}
```

- `max-size`：單一日誌檔案的最大大小
- `max-file`：保留的日誌檔案數量

### syslog

將日誌發送到 syslog 系統：

```json
{
    "log-driver": "syslog",
    "log-opts": {
        "syslog-address": "tcp://logserver:514"
    }
}
```

### journald

將日誌發送到 systemd journal：

```json
{
    "log-driver": "journald"
}
```

查看 journald 日誌：

```bash
journalctl -u docker.service CONTAINER_NAME=mycontainer
```

### fluentd

將日誌發送到 Fluentd：

```json
{
    "log-driver": "fluentd",
    "log-opts": {
        "fluentd-address": "fluentdhost:24224",
        "fluentd-tag": "docker.mycontainer"
    }
}
```

### gelf

將日誌發送到 Graylog 或 Logstash：

```json
{
    "log-driver": "gelf",
    "log-opts": {
        "gelf-address": "udp://graylog:12201"
    }
}
```

## 在容器層級設定日誌驅動

可覆寫 Docker Daemon 的預設設定：

```bash
docker run -d \
    --log-driver=json-file \
    --log-opt max-size=5m \
    --log-opt max-file=5 \
    --name myapp \
    myapp
```

## 集中式日誌收集架構

### ELK Stack（Elasticsearch + Logstash + Kibana）

```
Docker Containers --> Fluentd --> Elasticsearch --> Kibana
                     (日誌收集)   (儲存搜尋)      (視覺化)
```

### 部署 ELK Stack

```yaml
version: "3.8"
services:
  elasticsearch:
    image: elasticsearch:7.13.0
    environment:
      - discovery.type=single-node
    volumes:
      - es_data:/usr/share/elasticsearch/data

  logstash:
    image: logstash:7.13.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: kibana:7.13.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  fluentd:
    image: fluent/fluentd:v1.12-1
    volumes:
      - ./fluent.conf:/fluentd/etc/fluent.conf
    depends_on:
      - logstash

volumes:
  es_data:
```

### Fluentd 設定

```conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match docker.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  logstash_prefix docker
</match>
```

## 應用程式日誌最佳實踐

1. **結構化日誌**：使用 JSON 格式輸出日誌，方便解析與搜尋。

```python
import json
import sys

def log(level, message, **kwargs):
    print(json.dumps({
        "level": level,
        "message": message,
        **kwargs
    }), file=sys.stdout)
```

2. **不要輸出敏感資訊**：密碼、API Key、信用卡號等不應出現在日誌中。

3. **設定適當的日誌層級**：DEBUG、INFO、WARN、ERROR，避免輸出過多無用的資訊。

## 參考資源

- https://www.google.com/search?q=Docker+日誌+驅動+syslog+journald+fluentd+gelf+設定+2016
- https://www.google.com/search?q=Docker+ELK+Stack+Logstash+Kibana+Elasticsearch+集中式+日誌
- https://www.google.com/search?q=Fluentd+Docker+日誌+收集+ELK+整合+設定