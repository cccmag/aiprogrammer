# 傳輸層安全性

傳輸層安全性確保資料在網路傳輸過程中的機密性和完整性。

---

## TLS 1.2 與 TLS 1.3

### TLS 1.2 握手

```
用戶端                      伺服器
  │                          │
  │────── ClientHello ──────>│
  │                          │
  │<───── ServerHello ───────│
  │<───── Certificate ───────│
  │<───── ServerKeyExchange ─>│
  │<───── ServerHelloDone ───│
  │                          │
  │────── ClientKeyExchange ─>│
  │────── ChangeCipherSpec ─>│
  │────── Finished ─────────>│
  │                          │
  │<───── ChangeCipherSpec ───│
  │<───── Finished ───────────│
  │                          │
  │       加密資料            │
```

### TLS 1.3 改進

- **簡化握手**：從 2-RTT 降到 1-RTT
- **移除不安全加密演算法**：MD5、SHA-1、RC4 等
- **前向保密 (PFS)**：強制使用 Diffie-Hellman

### TLS 1.3 握手

```
用戶端                      伺服器
  │                          │
  │────── ClientHello ──────>│  (包含 DH 參數)
  │                          │
  │<───── ServerHello ───────│  (選擇 DH 參數)
  │<───── {Certificate} ─────│
  │<───── {CertificateVerify} │
  │<───── {Finished} ─────────│
  │                          │
  │────── {Finished} ───────>│
  │                          │
  │       加密資料            │
```

---

## 憑證管理

### 免費憑證：Let's Encrypt

```bash
# 安裝 certbot
sudo apt-get install certbot python3-certbot-nginx

# 取得憑證
sudo certbot certonly --nginx -d example.com -d www.example.com

# 自動續期
sudo certbot renew --dry-run
```

### 憑證類型

| 類型 | 驗證等级 | 顯示 |
|------|----------|------|
| DV (Domain Validation) | 僅驗證網域 | 鎖頭 |
| OV (Organization Validation) | 驗證組織 | 鎖頭 + 組織名稱 |
| EV (Extended Validation) | 嚴格驗證 | 綠色名稱列 |

---

## HTTPS 實作

### Apache

```apache
<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/html
    
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/example.com.crt
    SSLCertificateKeyFile /etc/ssl/private/example.com.key
    SSLCertificateChainFile /etc/ssl/certs/ca-bundle.crt
    
    # 安全設定
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
</VirtualHost>
```

### Nginx

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # 安全設定
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

---

## 安全 Headers

### 重要 Headers

```http
# 防止 XSS
Content-Security-Policy: default-src 'self'

# 防止點擊劫持
X-Frame-Options: DENY

# 防止 MIME 類型 sniffing
X-Content-Type-Options: nosniff

# 引用來源策略
Referrer-Policy: strict-origin-when-cross-origin

# XSS 保護
X-XSS-Protection: 1; mode=block
```

### Python Flask 設定

```python
from flask import Flask

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
```

---

## 憑證固定 (Certificate Pinning)

### HTTP Public Key Pinning (已廢棄)

由於 HPKP 的風險，已被大多數瀏覽器廢棄。

### 現代做法：Trust on First Use (TOFU)

```python
# 首次連線時儲存憑證指紋
import hashlib
import sqlite3

def store_certificate_fingerprint(host, cert):
    fingerprint = hashlib.sha256(cert).hexdigest()
    db = sqlite3.connect('trusted_certs.db')
    db.execute('INSERT INTO certs (host, fingerprint) VALUES (?, ?)',
               (host, fingerprint))
    db.commit()

def verify_certificate(host, cert):
    fingerprint = hashlib.sha256(cert).hexdigest()
    db = sqlite3.connect('trusted_certs.db')
    row = db.execute('SELECT fingerprint FROM certs WHERE host = ?',
                     (host,)).fetchone()
    return row and row[0] == fingerprint
```

---

## 測試 SSL/TLS

### SSL Labs

線上工具：https://www.ssllabs.com/ssltest/

### 命令列工具

```bash
# 使用 openssl 測試
openssl s_client -connect example.com:443

# 顯示憑證資訊
openssl s_client -connect example.com:443 -showcerts

# 測試特定 TLS 版本
openssl s_client -tls1_2 -connect example.com:443

# 檢查憑證過期
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

[搜尋 SSL TLS testing tools](https://www.google.com/search?q=SSL+TLS+testing+tools)

---

## 小結

傳輸層安全是保護網路通訊的關鍵，需要正確配置和持續監控。

---

*作者：AI 程式人團隊*