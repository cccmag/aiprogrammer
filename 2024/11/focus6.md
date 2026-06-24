# 監控與日誌管理

## 可觀測性三大支柱

### 前言

在 DevOps 實踐中，部署完成不是終點，而是監控的起點。可觀測性（Observability）是理解系統內部狀態的關鍵能力。本節將探討監控與日誌管理的核心概念與工具。

### 可觀測性三大支柱

**1. 指標（Metrics）**

指標是數值化的時間序列數據，反映系統的健康狀態：

```javascript
// 使用 prom-client 定義指標
const client = require('prom-client');
const counter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests'
});

const gauge = new client.Gauge({
  name: 'memory_usage_bytes',
  help: 'Current memory usage'
});

const histogram = new client.Histogram({
  name: 'http_request_duration_ms',
  help: 'Request duration in ms',
  buckets: [50, 100, 200, 500, 1000]
});
```

**2. 日誌（Logs）**

日誌是結構化的事件記錄，用於問題排查和審計：

```javascript
// 使用 pino 進行結構化日誌記錄
const pino = require('pino');
const logger = pino({
  level: process.env.LOG_LEVEL || 'info'
});

logger.info({ userId: 123, action: 'login' }, '用戶登入');
logger.error({ err, requestId: 'abc' }, '請求處理失敗');
```

**3. 追蹤（Traces）**

追蹤記錄請求在分散式系統中的完整路徑：

```javascript
const opentelemetry = require('@opentelemetry/api');
const tracer = opentelemetry.trace.getTracer('my-service');

async function handleRequest(req, res) {
  const span = tracer.startSpan('handle-request');
  span.setAttribute('user.id', req.userId);
  // 業務邏輯
  span.end();
}
```

### Prometheus + Grafana

**Prometheus** 是開源的監控系統和時間序列資料庫：

```yaml
# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

**Grafana** 提供儀表板視覺化：

```javascript
// Node.js 應用的 Prometheus 端點
const express = require('express');
const client = require('prom-client');
const app = express();

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```

### ELK 日誌堆疊

ELK（Elasticsearch、Logstash、Kibana）是經典的日誌管理方案：

```yaml
services:
  elasticsearch:
    image: elasticsearch:8
    environment:
      - discovery.type=single-node

  logstash:
    image: logstash:8
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: kibana:8
    ports:
      - "5601:5601"
```

### 警報與通知

設置閾值警報，在異常發生時即時通知：

```yaml
# prometheus-alert.yml
groups:
  - name: alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "錯誤率超過 5%"
```

### 小結

監控與日誌管理是 DevOps 可觀測性的基礎。通過 Prometheus、Grafana 和 ELK 等工具組合，團隊可以即時掌握系統狀態，快速定位問題，確保服務的穩定運行。

---

**下一步**：[基礎設施即程式碼](focus7.md)

## 延伸閱讀

- [Prometheus 文件](https://www.google.com/search?q=Prometheus+documentation)
- [Grafana 入門](https://www.google.com/search?q=Grafana+getting+started)
- [ELK Stack 指南](https://www.google.com/search?q=ELK+Stack+tutorial)
