# 雲端監控與日記管理

## 可觀測性三大支柱

雲端原生應用的監控離不開三個維度：
- **指標（Metrics）**：數值化的度量
- **日誌（Logs）**：事件記錄
- **追蹤（Traces）**：請求路徑

## Prometheus

Prometheus 是雲端原生監控的事實標準：

```yaml
# 部署 Prometheus
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        args:
          - '--config.file=/etc/prometheus/prometheus.yml'
        ports:
        - containerPort: 9090
```

### 監控應用

```python
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.route('/api/data')
def handle_request():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/data').inc()
    with REQUEST_LATENCY.time():
        # 處理請求
        return result
```

## Grafana

Grafana 是指標視覺化工具：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
```

## ELK Stack

Elasticsearch、Logstash、Kibana 構成完整的日誌解決方案：

```yaml
# Elasticsearch
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
spec:
  serviceName: elasticsearch
  replicas: 3
  # ...
```

### Fluentd 日誌收集

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
    </source>
    <match>
      @type elasticsearch
      host elasticsearch.logging
      port 9200
    </match>
```

## Jaeger 分散式追蹤

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:latest
        ports:
        - containerPort: 16686
```

### 在應用中使用

```python
from opentracing import tracer

def handle_request(request):
    with tracer.start_active_span('process-request') as scope:
        scope.span.log_kv({'event': 'start', 'request_id': request.id})
        result = process(request)
        scope.span.log_kv({'event': 'end'})
        return result
```

## 結論

完善的監控和日誌管理是雲端原生應用運維的基礎。投資在可觀測性基礎設施，能及早發現問題、減少故障排除時間。