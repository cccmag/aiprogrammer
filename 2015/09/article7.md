# 負載平衡器工作原理

## 前言

負載平衡器是現代網路架構的核心元件，負責分配流量到多個伺服器。

---

## 負載平衡器類型

### 硬體負載平衡器

- 專用設備（如 F5、A10）
- 高效能、高可靠性
- 昂貴

### 軟體負載平衡器

- Nginx、HAProxy、Envoy
- 彈性、成本低
- 適合雲端環境

### 雲端負載平衡器

- AWS ELB、Azure Load Balancer、GCP Cloud Load Balancing
- 托管服務、自動擴展

---

## 負載平衡演算法

### 1. Round Robin

輪流分配，適合伺服器規格相同。

```
請求 1 ──> Server A
請求 2 ──> Server B
請求 3 ──> Server C
請求 4 ──> Server A
```

### 2. Weighted Round Robin

根據權重分配。

```
Server A (權重 3) ──> 處理 3 個請求
Server B (權重 2) ──> 處理 2 個請求
Server C (權重 1) ──> 處理 1 個請求
```

### 3. Least Connections

分配給連線數最少的。

```
Server A: 10 連線
Server B: 5 連線  ← 下一個請求導向這裡
Server C: 8 連線
```

### 4. IP Hash

根據來源 IP 決定伺服器。

```python
# 同一 IP 永遠導向同一伺服器
server_index = hash(source_ip) % num_servers
```

### 5. Least Response Time

分配給響應時間最短的。

---

## 健康檢查

### TCP 檢查

```bash
# 檢查連接埠是否開放
telnet server 80
```

### HTTP 檢查

```bash
# 檢查 HTTP 回應
curl -I http://server/health
```

### 自訂檢查

```nginx
upstream backend {
    server server1.example.com;
    server server2.example.com;
    
    health_check uri=/health.php match=ok;
}

match ok {
    status 200;
    header Content-Type = text/html;
    body ~ "OK";
}
```

---

## Nginx 負載平衡設定

```nginx
upstream backend {
    # 負載平衡配置
    server 10.0.0.1:8080 weight=3;
    server 10.0.0.2:8080 weight=2;
    server 10.0.0.3:8080 backup;  # 備用
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        
        # 健康檢查
        proxy_connect_timeout 5s;
        proxy_next_upstream error timeout;
        
        # 標頭轉發
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## HAProxy 設定

```
global
    log localhost local0
    maxconn 4096

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http-in
    bind *:80
    default_backend servers

backend servers
    balance roundrobin
    option httpchk GET /health
    server s1 10.0.0.1:8080 check inter 2000 rise 2 fall 3
    server s2 10.0.0.2:8080 check inter 2000 rise 2 fall 3
```

---

## 會話保持

### Cookie 方式

```nginx
upstream backend {
    ip_hash;
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
}
```

### Cookie 插入

```nginx
upstream backend {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
}

server {
    listen 80;
    
    # 插入 session cookie
    proxy_set_header Cookie "session_id=abc123";
}
```

---

## 高可用性

### Keepalived + LVS

```bash
# keepalived.conf
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    virtual_ipaddress {
        192.168.1.100
    }
}
```

### DNS 高可用

```
www.example.com ──> 負載平衡器 IP 1
                  ──> 負載平衡器 IP 2
```

[搜尋 load balancer architecture](https://www.google.com/search?q=load+balancer+architecture+design)

---

## 小結

負載平衡是建立可擴展、高可用系統的關鍵，了解不同的演算法和架構能幫助你設計更好的系統。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Nginx 負載平衡文档](https://www.google.com/search?q=Nginx+load+balancing)
- [HAProxy 官方文檔](https://www.google.com/search?q=HAProxy+documentation)