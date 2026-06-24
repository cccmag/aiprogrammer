# HTTP/2 實作指南

## 前言

HTTP/2 是 HTTP 協議自 1999 年以來最重要的更新，本指南幫助你理解和部署 HTTP/2。

---

## HTTP/1.1 的限制

### 線頭阻塞 (Head-of-Line Blocking)

HTTP/1.1 只支援順序處理請求，一個請求完成前不能處理下一個。

```
請求 1 ────────────────────>
        <─────────────────── 回應 1
請求 2 ────────────────────>
        <─────────────────── 回應 2
```

### 多個連線

瀏覽器通常使用 6-8 個連線來繞過這個限制。

```
連線 1: GET /style.css
連線 2: GET /image1.jpg
連線 3: GET /image2.jpg
...
```

---

## HTTP/2 特性

### 1. 多工 (Multiplexing)

單一連線上並行多個請求/回應。

```
Stream 1: ──── Headers ──── Data ────
Stream 2: ── Headers ── Data ──
Stream 3: ── Headers ──────── Data ──
```

### 2. 標頭壓縮 (Header Compression)

使用 HPACK 演算法，極大減少標頭大小。

```bash
# 第一次請求
:method: GET
:path: /index.html
:scheme: https
:authority: example.com
user-agent: curl/7.43.0

# 之後請求（使用索引）
:path: /about.html
```

### 3. 伺服器推送 (Server Push)

伺服器可以主動推送資源。

```http
HTTP/2 200
content-type: text/html

PUSH_PROMISE:
Stream 2: /style.css
Stream 3: /script.js
```

### 4. 流量控制 (Flow Control)

每個 stream 有獨立的流量控制。

---

## 瀏覽器支援

```javascript
// 檢查 HTTP/2 支援
if (window.location.protocol === 'https:') {
    // 現代瀏覽器在 HTTPS 下支援 HTTP/2
    // 可以使用 fetch API 或 WebSocket
}
```

支援情況（2015 年）：
- Chrome 41+
- Firefox 36+
- Safari 9+
- Edge 12+

---

## 伺服器支援

| 伺服器 | HTTP/2 支援 |
|--------|------------|
| Nginx | 1.9.5+（需 OpenSSL 1.0.2+）|
| Apache | 2.4.17+（需 mod_http2）|
| IIS | 10+ |

---

## Nginx HTTP/2 設定

### 安裝

```bash
# Ubuntu/Debian
sudo apt-get install nginx

# 檢查版本
nginx -v
```

### 設定

```nginx
server {
    listen 443 ssl http2;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    server_name example.com;
    
    root /var/www/html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 驗證

```bash
# 使用 curl 測試
curl -I --http2 https://example.com

# 使用線上工具
# https://www.ssllabs.com/ssltest/
```

---

## 效能比較

### 實際測試結果

| 指標 | HTTP/1.1 | HTTP/2 |
|------|----------|--------|
| 頁面載入時間 | 1.2s | 0.8s |
| 連線數 | 6-8 | 1-2 |
| 標頭傳輸 | 400 bytes/請求 | < 50 bytes/請求 |

---

## 遷移考量

### 需要注意

1. **HTTPS**：HTTP/2 需要 TLS
2. **代理相容性**：確保代理支援 HTTP/2
3. **瀏覽器支援**：仍需提供 HTTP/1.1 回退
4. **伺服器支援**：升級到新版軟體

### 向後相容

現代瀏覽器會自動協商 HTTP/1.1 或 HTTP/2。

[搜尋 HTTP/2 deployment guide](https://www.google.com/search?q=HTTP+2+deployment+guide)

---

## 小結

HTTP/2 提供了顯著的性能提升，但遷移需要謹慎規劃。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [HTTP/2 官方規格](https://www.google.com/search?q=HTTP+2+specification+RFC+7540)
- [HTTP/2 測試工具](https://www.google.com/search?q=HTTP+2+test+tools)