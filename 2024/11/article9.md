# ELK 日誌系統

## 1. 引言

ELK Stack（Elasticsearch、Logstash、Kibana）是目前最流行的開源日誌管理解決方案。它提供日誌收集、儲存、分析和視覺化的一站式服務。本文將介紹如何在 Docker 環境中部署和使用 ELK 日誌系統。

## 2. ELK 架構概覽

```
應用程式 → Filebeat → Logstash → Elasticsearch → Kibana
   │                                    │
   └──────── 直接寫入 ─────────────────┘
```

- **Filebeat**：輕量級日誌收集器，安裝在應用端
- **Logstash**：日誌解析和轉換管道
- **Elasticsearch**：分散式搜尋和分析引擎
- **Kibana**：資料視覺化儀表板

## 3. Docker Compose 部署

```yaml
version: '3.8'

services:
  elasticsearch:
    image: elasticsearch:8.15.0
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - esdata:/usr/share/elasticsearch/data

  logstash:
    image: logstash:8.15.0
    ports:
      - "5000:5000"
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: kibana:8.15.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

volumes:
  esdata:
```

## 4. Logstash 配置

```ruby
# logstash.conf
input {
  beats {
    port => 5000
  }
}

filter {
  # 解析 JSON 格式的日誌
  if [@metadata][type] == "json" {
    json {
      source => "message"
    }
  }
  
  # 解析 Nginx 日誌
  if [service] == "nginx" {
    grok {
      match => {
        "message" => "%{COMBINEDAPACHELOG}"
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

## 5. Node.js 結構化日誌

```javascript
const pino = require('pino');

// 建立日誌實例
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-elasticsearch',
    options: {
      node: 'http://localhost:9200',
      index: 'app-logs',
      'es-version': 8
    }
  }
});

// 使用結構化日誌
logger.info({ userId: 123, action: 'purchase' }, '用戶完成購買');
logger.error({ err, orderId: 'ORD-456' }, '訂單處理失敗');
```

## 6. Filebeat 配置

```yaml
# filebeat.yml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    processors:
      - add_docker_metadata:
          host: "unix:///var/run/docker.sock"

output.logstash:
  hosts: ["logstash:5000"]
```

## 7. Kibana 儀表板

在 Kibana 中可以建立：
- **即時日誌儀表板**：顯示最近 15 分鐘的日誌量
- **錯誤率儀表板**：按服務分類的錯誤率趨勢
- **API 響應時間**：各端點的響應時間分佈
- **地理分布**：用戶請求的地理來源

## 8. 結語

ELK Stack 為 DevOps 團隊提供了強大的日誌管理能力。通過結構化日誌記錄和即時的日誌分析，團隊可以快速定位問題、分析系統行為，並建立有效的警報機制。
