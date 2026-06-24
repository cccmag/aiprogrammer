# 6. 傳輸層安全

## HTTP 的安全問題

HTTP 協定傳輸的資料是明文的，任何人都可以透過網路監聽竊取傳輸內容。這對於敏感資料（如密碼、信用卡號）是無法接受的。

## HTTPS 的作用

HTTPS = HTTP + TLS（Transport Layer Security）。TLS 提供了：

**加密**：傳輸內容被加密，即使被攔截也無法解讀

**身份驗證**：確認網站的身份，防止假冒

**完整性**：偵測傳輸過程中的篡改

## TLS 憑證

TLS 使用數位憑證來驗證網站身份。憑證由可信的憑證授權中心（CA）簽發。

### 憑證類型

**DV（Domain Validation）**：僅驗證網域所有權，最快，適用於一般網站

**OV（Organization Validation）**：驗證組織身份，適用于企業

**EV（Extended Validation）**：最嚴格的驗證，瀏覽器位址列會顯示組織名稱，適合金融機構

### 免費憑證

Let's Encrypt 提供免費的 DV 憑證，支援自動化申請與更新：

```bash
# 使用 certbot 取得憑證
certbot certonly --webroot -w /var/www/html -d example.com -d www.example.com

# 或使用 DNS 驗證
certbot certonly --manual --preferred-challenges dns -d example.com
```

## TLS 設定

### 建議的 TLS 配置

```nginx
# Nginx TLS 配置
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
```

### 停用 SSLv2 / SSLv3

SSLv2 和 SSLv3 有已知漏洞，應完全停用：

```
ssl_protocols TLSv1.2 TLSv1.3;  # 只允許 TLS
```

## HSTS（HTTP Strict Transport Security）

強制瀏覽器使用 HTTPS 連線：

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

設定後，瀏覽器會在指定時間內（此處為一年）只透過 HTTPS 訪問該網站。

## 憑證釘扎（Certificate Pinning）

將網站的合法憑證資訊寫入應用程式，防止 CA 被入侵後發行偽造憑證：

```python
# Android App 的 Certificate Pinning（使用 OkHttp）
OkHttpClient client = new OkHttpClient.Builder()
    .certificatePinner(new CertificatePinner.Builder()
        .add("example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
        .build())
    .build();
```

## 前向保密（Forward Secrecy）

即使伺服器的私鑰被竊取，過去的通訊記錄也無法被解密。這需要使用短暫的 Diffie-Hellman（ECDHE）金鑰交換：

```nginx
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
ssl_prefer_server_ciphers on;
```

## 混合內容問題

HTTPS 頁面不應該載入 HTTP 資源，否則會被中間人攻擊：

```html
<!-- 不安全 -->
<script src="http://example.com/script.js"></script>

<!-- 安全 -->
<script src="https://example.com/script.js"></script>
```

使用 CSP 檢測混合內容：

```html
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
```

## TLS 終止

對於大型系統，TLS 加密通常在負載平衡器或專用的 TLS 終止代理處理，而非應用程式伺服器。這樣可以：

- 減輕應用程式伺服器的計算負擔
- 集中管理 TLS 設定
- 簡化憑證管理

## 參考資源

- https://www.google.com/search?q=HTTPS+TLS+SSL+加密+設定+HSTS+憑證+2016
- https://www.google.com/search?q=Let's+Encrypt+免費+SSL+憑證+申請+certbot+設定
- https://www.google.com/search?q=TLS+HTTPS+安全+配置+nginx+Apache+前向保密+混合內容