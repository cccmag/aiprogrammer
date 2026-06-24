# HTTPS 與 TLS 設定

## 為什麼需要 HTTPS

HTTP 是明文協定，傳輸過程中任何人都可以監聽或篡改。特別是：
- 公共 WiFi 網路容易被窃聽
- ISP 或路由器可能注入廣告
- 中間人攻擊（MITM）可以假冒伺服器

HTTPS 通過 TLS 加密通訊，提供了：
- **加密**：保護資料不被窺探
- **身份驗證**：確認伺服器身份
- **完整性**：防止資料被篡改

## 取得 TLS 憑證

### Let's Encrypt（免費）

Let's Encrypt 是 Mozilla 贊助的免費 CA，支援自動化申請與更新：

```bash
# 安裝 certbot
sudo apt-get install certbot python-certbot-nginx

# 申請憑證（Nginx 外掛）
sudo certbot --nginx -d example.com -d www.example.com

# 自動更新測試
sudo certbot renew --dry-run
```

### 憑證檔案結構

```
/etc/letsencrypt/live/example.com/
    fullchain.pem    # 完整憑證鏈
    privkey.pem      # 私鑰
    cert.pem         # 伺服器憑證
    chain.pem       # 中間憑證
```

## Nginx TLS 設定

### 基本設定

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # TLS 版本
    ssl_protocols TLSv1.2 TLSv1.3;

    # 密碼套件
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';

    # 使用伺服器端密碼偏好
    ssl_prefer_server_ciphers on;

    # session 快取
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
}
```

### HSTS（HTTP Strict Transport Security）

強制瀏覽器使用 HTTPS：

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

`preload` 允許提交到 HSTS Preload List，瀏覽器會內建記住只能使用 HTTPS 存取。

### OCSP Stapling

減少客戶端的 CA 查詢延遲：

```nginx
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
```

## Apache TLS 設定

```apache
<VirtualHost *:443>
    ServerName example.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.com/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/example.com/chain.pem

    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
</VirtualHost>
```

## 前向保密（Forward Secrecy）

確保即使私鑰被竊，過去的通訊記錄也無法被解密。需要使用短暫的 Diffie-Hellman 金鑰交換（ECDHE）：

```nginx
ssl_ecdh_curve secp384r1;
```

## 混合內容處理

HTTPS 頁面不應包含 HTTP 資源：

```html
<!-- 檢測並自動升級 -->
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
```

使用開發者工具檢查混合內容警告：

```
Mixed Content: The page at 'https://example.com' was loaded over HTTPS,
but requested an insecure resource 'http://example.com/script.js'.
```

## 強制 HTTP 轉 HTTPS

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## 測試 TLS 配置

使用 SSL Labs 的線上工具或本地工具：

```bash
# 安裝 testssl.sh
docker run --rm -ti drwetter/testssl.sh https://example.com
```

## 參考資源

- https://www.google.com/search?q=HTTPS+TLS+SSL+憑證+設定+Nginx+Apache+Let's+Encrypt+2016
- https://www.google.com/search?q=HSTS+Strict+Transport+Security+設定+preload+安全
- https://www.google.com/search?q=前向保密+Forward+Secrecy+ECDHE+TLS+配置+方法