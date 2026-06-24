# 監控與日誌管理

## 前言

監控與日誌是維運的雙眼。2016 年的監控趨勢是容器化、微服務友好的解決方案。

## 監控架構

```
應用 → Metrics → Prometheus → Alertmanager → 通知
                      ↓
                   Grafana → 視覺化儀表板

應用 → Logs → Fluentd → Elasticsearch → Kibana
```

## Prometheus 設定

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['myapp:3000']
    metrics_path: '/metrics'
```

```yaml
# deployment with prometheus annotations
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 3000
```

## 應用指標端點

```python
# metrics_endpoint.py
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

@app.route('/api/users')
def get_users():
    with REQUEST_LATENCY.labels(method='GET', endpoint='/api/users').time():
        users = fetch_users()
        REQUEST_COUNT.labels(method='GET', endpoint='/api/users', status=200).inc()
        return jsonify(users)
```

## 日誌收集架構

```python
# structured_logging.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
        }
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        return json.dumps(log_data)

# 使用
logger = logging.getLogger('myapp')
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

## ELK Stack 設定

```yaml
# docker-compose.elk.yml
version: '3'

services:
  elasticsearch:
    image: elasticsearch:5.0
    environment:
      - discovery.type=single-node
    volumes:
      - es_data:/usr/share/elasticsearch/data
  
  logstash:
    image: logstash:5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
  
  kibana:
    image: kibana:5.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  es_data:
```

```conf
# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
  }
  date {
    match => ["timestamp", "ISO8601"]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "myapp-%{+YYYY.MM.dd}"
  }
}
```

## 警報規則

```yaml
# alert_rules.yml
groups:
  - name: myapp_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
```

## 分散式追蹤

```python
# tracing.py
from flask import Flask, request
import time
import uuid

app = Flask(__name__)

@app.before_request
def before():
    request.id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request.start_time = time.time()

@app.after_request
def after(response):
    duration = time.time() - request.start_time
    response.headers['X-Request-ID'] = request.id
    response.headers['X-Response-Time'] = str(duration)
    
    # 發送到追蹤系統
    trace_data = {
        'request_id': request.id,
        'method': request.method,
        'path': request.path,
        'duration': duration,
        'status': response.status_code
    }
    # 發送至 Zipkin/Jaeger
    return response
```

## 延伸閱讀

- [Prometheus 監控](https://www.google.com/search?q=prometheus+monitoring+tutorial+2016)
- [ELK Stack 教學](https://www.google.com/search?q=elk+stack+tutorial+2016)
- [分散式追蹤](https://www.google.com/search?q=distributed+tracing+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*