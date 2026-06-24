# TLS 協定導論

## 網際網路的安全基石

TLS（Transport Layer Security）是保護網際網路通訊的事實標準。從網路購物到電子郵件，從社交媒體到線上銀行，TLS 在幕後保護著我們的資料安全。

TLS 的前身是 SSL（Secure Sockets Layer），由 Netscape 在 1994 年設計。SSL 1.0 從未公開，SSL 2.0 於 1995 年發布但存在嚴重安全缺陷。SSL 3.0（1996 年）成為現代 TLS 的基礎。

2000 年代後，TLS 由 IETF 標準化：
- **TLS 1.0**（1999 年）：相當於 SSL 3.1，只做了少量修改
- **TLS 1.1**（2006 年）：增加了 CBC 保護和 IV 改進
- **TLS 1.2**（2008 年）：大幅更新，引入 AEAD 密碼
- **TLS 1.3**（2018 年）：重大重構，簡化握手並移除不安全選項

## TLS 1.3 握手詳解

TLS 1.3 將握手從 TLS 1.2 的 2-RTT 減少到 1-RTT（首次連接）或 0-RTT（恢復會話）。

### 首次連接（1-RTT）

```
Client                               Server
  |-------- ClientHello ----------->|
  |  (TLS 版本, 密碼套件, 金鑰共享)    |
  |                                  |
  |<------ ServerHello --------------|
  |  (選取版本, 密碼套件, 金鑰共享)    |
  |<------ EncryptedExtensions ------|
  |<------ Certificate --------------|
  |<------ CertificateVerify --------|
  |<------ Finished -----------------|
  |                                  |
  |-------- Finished --------------->|
  |                                  |
  |<========== 加密通訊 ==============>|
```

ClientHello 中包含了客戶端的金鑰共享值（Key Share），這使得伺服器可以在第一個回應中就計算出共享金鑰。這就是 1-RTT 的關鍵。

### 0-RTT

如果客戶端之前連線過同一伺服器，可以使用 Session Ticket 或 PSK 實現 0-RTT：

```
Client                               Server
  |-------- ClientHello ----------->|
  |  (PSK + 0-RTT data)             |
  |<------ ServerHello --------------|
  |<------ 加密通訊 ------------------|
```

0-RTT 資料存在重放攻擊風險，因此僅適用於冪等操作（如 HTTP GET）。

## 密碼套件選擇

TLS 1.3 大幅簡化了密碼套件，僅支援 5 個：

| 套件 | 加密 | HKDF |
|:---|:---|:---|
| TLS_AES_128_GCM_SHA256 | AES-128-GCM | SHA256 |
| TLS_AES_256_GCM_SHA384 | AES-256-GCM | SHA384 |
| TLS_CHACHA20_POLY1305_SHA256 | ChaCha20-Poly1305 | SHA256 |
| TLS_AES_128_CCM_SHA256 | AES-128-CCM | SHA256 |
| TLS_AES_128_CCM_8_SHA256 | AES-128-CCM-8 | SHA256 |

所有 TLS 1.3 密碼套件都提供：
- **AEAD**：認證加密，同時提供機密性和完整性
- **前向安全性**：使用 ECDHE 金鑰交換
- **HKDF**：基於 HMAC 的金鑰推導

## 金鑰排程

TLS 1.3 使用 HKDF 進行金鑰推導。從 PSK（預共享金鑰）或 ECDHE 輸出開始，經過 HKDF-Extract 和 HKDF-Expand，生成多個金鑰：

- **客戶端寫金鑰**：加密從客戶端到伺服器的資料
- **伺服器寫金鑰**：加密從伺服器到客戶端的資料
- **應用程式金鑰**：保護應用層資料

## 常見攻擊與防護

### POODLE（2014）

針對 SSL 3.0 的 CBC 填充攻擊。結果：所有主流瀏覽器和伺服器禁用 SSL 3.0。

### Heartbleed（2014）

OpenSSL 的緩衝區讀取越界漏洞，可能洩露伺服器記憶體中的私鑰。結果：OpenSSL 緊急修補，數百萬伺服器更新。

### Logjam（2015）

針對 DHE 金鑰交換的降級攻擊。結果：瀏覽器和伺服器提高 DH 參數的最小長度。

### CRIME/BREACH（2012-2013）

利用 TLS 壓縮洩露訊息的壓縮比資訊。結果：TLS 壓縮被禁用。

## TLS 的未來

**TLS 1.4** 正在草案階段，預計將引入：
- 更強的隱私保護（隱藏 SNI）
- 更快的握手
- 後量子密碼學支援

## 延伸閱讀

- [TLS 1.3 RFC 8446](https://www.google.com/search?q=TLS+1.3+RFC+8446)
- [TLS 握手詳解](https://www.google.com/search?q=TLS+handshake+explained+in+detail)
- [Heartbleed 漏洞](https://www.google.com/search?q=Heartbleed+OpenSSL+bug)
- [TLS 1.3 vs 1.2 比較](https://www.google.com/search?q=TLS+1.3+vs+TLS+1.2+differences)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
