# 網路安全基礎

網路安全是保護系統和資料免受未授權存取的重要領域。

---

## 常見威脅

### 1. 竊聽 (Eavesdropping)

在網路傳輸過程中攔截資料。

```bash
# 使用 wireshark 抓包
sudo wireshark -i eth0 -k
```

### 2. 偽裝 (Impersonation)

偽造身份進行欺騙。

### 3. 竄改 (Tampering)

修改傳輸中的資料。

### 4. 否認 (Repudiation)

否認曾經執行過的動作。

---

## 密碼學基礎

### 對稱加密

同一把金鑰加密和解密。

```
明文 ──>[金鑰]──> 密文 ──>[金鑰]──> 明文
```

常用演算法：AES、DES、3DES、Blowfish

### 非對稱加密

公鑰加密，私鑰解密。

```
明文 ──>[公鑰]──> 密文 ──>[私鑰]──> 明文
```

常用演算法：RSA、ECC、Diffie-Hellman

### 雜湊函數

單向函數，不可逆。

```
資料 ──>[SHA-256]──> 雜湊值
```

常用演算法：SHA-256、SHA-512、MD5（不安全）

---

## TLS/SSL

### TLS 握手過程

```
用戶端                      伺服器
  │                          │
  │────── ClientHello ──────>│
  │     (支援的密碼套件)      │
  │     (TLS 版本)           │
  │                          │
  │<───── ServerHello ───────│
  │     (選擇的密碼套件)      │
  │                          │
  │<───── Certificate ───────│
  │     (伺服器憑證)          │
  │                          │
  │<───── ServerHelloDone ───│
  │                          │
  │────── ClientKeyExchange ─>│
  │     (預備主密鑰)          │
  │                          │
  │────── ChangeCipherSpec ─>│
  │────── Finished ─────────>│
  │                          │
  │<───── ChangeCipherSpec ───│
  │<───── Finished ───────────│
  │                          │
  │     加密的 HTTP 資料      │
```

### 密碼套件 (Cipher Suite)

```
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
   │      │    │       │    │
   │      │    │       │    └── Hash 演算法
   │      │    │       └────── 加密演算法 (AES-256-GCM)
   │      │    └───────────── 金鑰交換 (ECDHE)
   │      └────────────────── 憑證類型 (RSA)
   └───────────────────────── 協定版本 (TLS)
```

---

## 憑證

### 憑證結構

```json
{
  "subject": {
    "CN": "example.com",
    "O": "Example Inc",
    "C": "US"
  },
  "issuer": {
    "CN": "DigiCert SHA2 Extended Validation Server CA",
    "O": "DigiCert Inc",
    "C": "US"
  },
  "validity": {
    "notBefore": "2025-01-01",
    "notAfter": "2026-01-01"
  },
  "publicKey": "..."
}
```

### 憑證鏈

```
根憑證 (Root CA)
    │
    ▼
中繼憑證 (Intermediate CA)
    │
    ▼
伺服器憑證 (Server Certificate)
```

### 建立自有 CA

```bash
# 1. 建立私鑰
openssl genrsa -out ca.key 4096

# 2. 建立自我簽署憑證
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt

# 3. 為客戶端頒發憑證
openssl genrsa -out client.key 4096
openssl req -new -key client.key -out client.csr
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt
```

---

## 安全傳輸實作

### HTTPS 設定 (Nginx)

```nginx
server {
    listen 443 ssl http2;
    
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # 安全的 SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers on;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;
}
```

### Python HTTPS 客戶端

```python
import ssl
import socket

# 建立 SSL 上下文
context = ssl.create_default_context()

# 連接 HTTPS 伺服器
conn = context.wrap_socket(socket.socket(), 
                            server_hostname='example.com')
conn.connect(('example.com', 443))

# 獲取憑證資訊
cert = conn.getpeercert()
print(cert)
```

---

## 密碼最佳實踐

### 密碼儲存

```python
# 錯誤：儲存明文密碼
# user.password = "plaintext"

# 正確：使用 bcrypt
import bcrypt

password = "user_password"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# 儲存 hashed

# 驗證
bcrypt.checkpw(password.encode(), hashed)
```

### 金鑰管理

```bash
# 不要在程式碼中硬編碼金鑰
# 環境變數
export SECRET_KEY="your-secret-key"

# 金鑰管理服務
# AWS KMS, HashiCorp Vault
```

---

## 小結

網路安全是一個複雜的領域，需要持續關注和更新知識。

---

*作者：AI 程式人團隊*