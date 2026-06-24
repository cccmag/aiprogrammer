# 開源監控工具大比拼

## 前言

監控是確保系統可用性和效能的關鍵。本 文比較主流的開源監控工具。

---

## 工具總覽

| 工具 | 專注領域 | 難度 | 擴展性 |
|------|----------|------|--------|
| Nagios | 基礎設施監控 | 中 | 高 |
| Zabbix | 企業級監控 | 高 | 高 |
| Prometheus | 指標監控 | 低 | 高 |
| Grafana | 視覺化 | 低 | 高 |
| Cacti | 網路圖表 | 中 | 中 |
| Icinga | Nagios 分支 | 中 | 高 |

---

## Nagios

### 特色

- 歷史悠久，生態圈豐富
- 強大的外掛生態系統
- 高度可訂製

### 架構

```
┌─────────────┐
│ Nagios Core │ ← 主程式
└──────┬──────┘
       │
┌──────┴──────┐
│ Plugins     │ ← 監控腳本
└─────────────┘
       │
┌──────┴──────┐
│ NRPE/NSCA  │ ← 客戶端代理
└─────────────┘
```

### 設定範例

```bash
# /etc/nagios3/conf.d/host.cfg
define host {
    use                     generic-host
    host_name               web-server
    address                 192.168.1.100
    check_command           check-host-alive
    max_check_attempts      5
    notification_interval   30
}

define service {
    use                     generic-service
    host_name               web-server
    service_description     HTTP
    check_command           check_http
    check_interval          5
}
```

### 優點

- 成熟穩定
- 豐富的外掛
- 強大的社群

### 缺點

- 設定複雜
- 介面過時
- 效能有限

[搜尋 Nagios vs Zabbix](https://www.google.com/search?q=Nagios+vs+Zabbix+comparison)

---

## Zabbix

### 特色

- 企業級功能
- 內建資料庫支援
- 自動探索

### 架構

```
┌─────────────┐
│ Zabbix Server │
└──────┬──────┘
       │
┌──────┴──────┐
│ Zabbix Agent │ ← 客戶端
│ SNMP Trap    │
│ IPMI         │
└─────────────┘
```

### 優點

- 完整的監控解決方案
- 自動發現功能
- 良好的視覺化

### 缺點

- 學習曲線陡峭
- 資源消耗較高
- 複雜的升級程序

---

## Prometheus

### 特色

- 現代化的監控系統
- 基於時間序列資料
- Pull 模型

### 架構

```
┌──────────────┐
│ Prometheus   │
│ Server       │
└──────┬───────┘
       │
┌──────┴───────┐
│ Exporters    │ ← 收集指標
└──────────────┘
       │
┌──────┴───────┐
│ Grafana     │ ← 視覺化
└──────────────┘
```

### 安裝

```bash
# docker-compose.yml
version: '3'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### 查詢語言 PromQL

```promql
# CPU 使用率
rate(node_cpu_seconds_total[5m])

# 記憶體使用
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
```

### 優點

- 簡單部署
- 強大的查詢語言
- 與 Kubernetes 原生整合

### 缺點

- 長期儲存需要額外設定
- 警報功能需要 Alertmanager

---

## Grafana

### 特色

- 通用儀表板
- 支援多種資料來源
- 豐富的視覺化

### 支援的資料來源

- Prometheus
- InfluxDB
- Elasticsearch
- MySQL
- PostgreSQL
- Graphite

### Dashboard 範例

```json
{
  "title": "系統監控",
  "panels": [
    {
      "title": "CPU 使用率",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(node_cpu_seconds_total[5m])"
        }
      ]
    },
    {
      "title": "記憶體使用",
      "type": "gauge",
      "targets": [
        {
          "expr": "node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes"
        }
      ]
    }
  ]
}
```

---

## 選擇建議

| 場景 | 推薦工具 |
|------|----------|
| 簡單伺服器監控 | Prometheus + Grafana |
| 企業級需求 | Zabbix |
| 傳統 IT 環境 | Nagios |
| 容器/Kubernetes | Prometheus |
| 混合環境 | Icinga |

---

## 小結

選擇監控工具需要根據實際需求，沒有絕對的最佳方案。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Prometheus 官方網站](https://prometheus.io/)
- [Grafana 官方網站](https://grafana.com/)
- [Nagios 官方網站](https://www.google.com/search?q=Nagios+official+website)