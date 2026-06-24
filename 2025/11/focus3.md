# API 閘道與負載平衡

## 流量管理與路由

當系統從單一伺服器擴展到多台伺服器時，第一個需要解決的問題是：請求應該發送到哪台伺服器？API 閘道和負載平衡器就是解決這個問題的核心元件。

---

## API Gateway 模式

API Gateway 是系統的單一入口點，負責路由、認證、限流等橫切關注點。

```
                    ┌──────────────┐
                    │   Clients    │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ API Gateway  │
                    │ (認證/限流/路由)│
                    └──────┬───────┘
                    ┌──────┼───────┐
                    │      │       │
              ┌─────▼┐ ┌──▼───┐ ┌─▼────┐
              │Service│ │Service│ │Service│
              │ A    │ │ B    │ │ C    │
              └──────┘ └──────┘ └──────┘
```

### API Gateway 的主要功能

**請求路由**：根據路徑、標頭、方法轉發到對應服務

```
/user/* → User Service
/order/* → Order Service
/product/* → Product Service
```

**認證授權**：統一處理身分驗證和權限檢查

**限流（Rate Limiting）**：防止惡意請求或流量暴增

```
每秒限制：1000 請求 / IP
突發限制：2000 請求（短時間可超過）
```

**協議轉換**：將外部請求轉換為內部服務的協議格式

### 常見 API Gateway 方案

| 方案 | 語言 | 特點 |
|------|------|------|
| Kong | Lua/Go | 外掛生態豐富 |
| Tyk | Go | 支援多協議 |
| AWS API Gateway | 託管 | 內建 AWS 服務整合 |
| Envoy | C++ | Service Mesh 原生 |

---

## 負載平衡策略

### 輪詢（Round-Robin）

將請求依序分配給後端伺服器。

```python
# 輪詢實作（參考 _code/system_design.py）
servers = ["srv-a", "srv-b", "srv-c"]
index = 0
for request in requests:
    server = servers[index % len(servers)]
    index += 1
    send_to(server, request)
```

**適用場景**：伺服器配置相同，請求處理時間相近

### 最少連接（Least Connections）

將請求分配給當前活躍連接數最少的伺服器。

**適用場景**：請求處理時間差異大（例如有些請求含大量計算）

### IP Hash

根據客戶端 IP 的 Hash 值分配伺服器。

```
hash(ip) % N = server_index
```

**適用場景**：需要 Session 黏性（Sticky Session）時

### 加權分配（Weighted）

為效能不同的伺服器設定不同權重。

```
srv-a（32 cores）權重 4
srv-b（16 cores）權重 2
srv-c（8 cores） 權重 1

在 7 個請求中：
  srv-a 處理 4 個
  srv-b 處理 2 個
  srv-c 處理 1 個
```

---

## 反向代理

反向代理（Reverse Proxy）是負載平衡器的常見實作方式之一。

```
┌─────────┐      ┌──────────────┐      ┌──────────┐
│  Client  │─────►│ Reverse Proxy │─────►│ Backend  │
│          │      │ (Nginx/Caddy) │      │ Servers  │
└─────────┘      └──────────────┘      └──────────┘
```

### 反向代理 vs 正向代理

```
正向代理：
  Client ──→ Proxy ──→ Internet
  （代理客戶端，隱藏客戶端 IP）

反向代理：
  Client ──→ Proxy ──→ Backend Servers
  （代理伺服器，隱藏伺服器細節）
```

### Nginx 的範例設定

```
http {
    upstream backend {
        server 10.0.0.1:8080 weight=3;
        server 10.0.0.2:8080 weight=2;
        server 10.0.0.3:8080;
    }

    server {
        listen 80;
        location /api/ {
            proxy_pass http://backend;
        }
    }
}
```

---

## 健康檢查

負載平衡器需要知道哪些伺服器是健康的。

### 被動健康檢查

監控請求失敗率，如果錯誤率超過閾值則暫時移除伺服器。

```
連續 5 次 5xx 錯誤 → 標記為不健康
等待 30 秒後重試 → 恢復正常則重新加入
```

### 主動健康檢查

定期向伺服器發送健康檢查請求。

```
每 10 秒發送 GET /health
預期回覆：200 OK，body: {"status": "healthy"}
連續 3 次失敗 → 移除
```

---

## 限流策略

### 令牌桶（Token Bucket）

最常用的限流演算法。

```
初始化：桶容量 1000，每秒填入 100 個令牌
請求來臨：消耗一個令牌
桶空時：請求排隊或拒絕
```

### 滑動視窗（Sliding Window）

在時間視窗內限制請求數。

```
視窗大小：1 秒
視窗內最大請求數：100
將 1 秒分成 10 個 100ms 的區塊
每個區塊記錄請求數
滑動時丟棄過期區塊的計數
```

---

## 實戰注意事項

- **負載平衡器單點故障**：部署多個負載平衡器，用 DNS Round-Robin 或 Anycast
- **SSL Termination**：在負載平衡器解密 HTTPS，內部使用 HTTP 通信
- **WebSocket 支援**：確保負載平衡器支援長連接
- **分散式追蹤**：注入 Trace ID 以便跨服務追蹤

---

## 延伸閱讀

- [API Gateway Pattern](https://www.google.com/search?q=API+gateway+pattern+microservices)
- [Nginx Load Balancing](https://www.google.com/search?q=nginx+load+balancing+configuration)
- [Rate Limiting Algorithms](https://www.google.com/search?q=rate+limiting+algorithms+token+bucket)

---

*本篇文章為「AI 程式人雜誌 2026 年 11 月號」系統設計系列之三。*
