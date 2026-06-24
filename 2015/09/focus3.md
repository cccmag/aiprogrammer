# DNS 運作原理

DNS（Domain Name System）是網際網路的電話簿，將網域名稱轉換為 IP 位址。

---

## DNS 層級架構

```
根網域 (.) 
    │
    ├── com, org, net, edu, gov, tw, cn, jp...
    │     │
    │     └── example.com
    │           │
    │           ├── www.example.com
    │           ├── mail.example.com
    │           └── api.example.com
    │
    └── cn, tw, jp...
          │
          └── nqu.edu.tw
                 │
                 └── csie.nqu.edu.tw
```

---

## DNS 伺服器類型

### 1. 根伺服器 (Root Server)

- 全球共 13 組根伺服器（A-M）
- 儲存頂級網域（TLD）伺服器位址

### 2. 頂級網域伺服器 (TLD Server)

管理 .com, .org, .net, .tw 等頂級網域。

### 3. 授權網域伺服器 (Authoritative Server)

儲存特定網域的 DNS 記錄。

### 4. 遞迴解析器 (Recursive Resolver)

代表客戶端查詢的伺服器，通常由 ISP 或第三方提供。

---

## DNS 查詢流程

### 完整查詢

```
用戶端
    │
    ▼
1. 查詢本地快取（瀏覽器/系統）
    │
    ▼
2. 遞迴解析器（8.8.8.8 或 10.0.0.1）
    │
    ▼
3. 根伺服器 → TLD 伺服器 → 授權伺服器
    │
    ▼
4. 傳回 IP 位址
    │
    ▼
用戶端
```

### 具體範例：查詢 www.example.com

```
步驟 1: 查詢根伺服器
"www.example.com 的 IP 是什麼？"
根伺服器回應："我不知道，但我知道 .com 的 TLD 伺服器在哪裡"

步驟 2: 查詢 .com TLD 伺服器
"www.example.com 的 IP 是什麼？"
TLD 伺服器回應："我不知道，但我知道 example.com 的 NS 伺服器"

步驟 3: 查詢 example.com 授權伺服器
"www.example.com 的 IP 是什麼？"
授權伺服器回應："是 93.184.216.34"
```

---

## DNS 記錄類型

### A 記錄

```bash
# 網域名稱 → IPv4
www.example.com.    IN  A       93.184.216.34
```

### AAAA 記錄

```bash
# 網域名稱 → IPv6
www.example.com.    IN  AAAA    2606:2800:220:1::
```

### CNAME 記錄

```bash
# 網域名稱別名
blog.example.com.   IN  CNAME   www.example.com.
```

### MX 記錄

```bash
# 郵件交換伺服器
example.com.        IN  MX      10 mail1.example.com.
example.com.        IN  MX      20 mail2.example.com.
```

### NS 記錄

```bash
# 名稱伺服器
example.com.        IN  NS      ns1.example.com.
example.com.        IN  NS      ns2.example.com.
```

### TXT 記錄

```bash
# 文字記錄，常用於驗證和 SPF
example.com.        IN  TXT     "v=spf1 include:_spf.example.com ~all"
```

---

## DNS 查詢工具

### nslookup

```bash
nslookup example.com
nslookup -type=MX example.com
```

### dig

```bash
dig example.com
dig @8.8.8.8 example.com A
dig @8.8.8.8 example.com MX
```

### drill

```bash
drill example.com
drill -T example.com  # 追蹤查詢過程
```

---

## DNS 快取

### 瀏覽器快取

每個瀏覽器有自己的 DNS 快取策略（通常 1-5 分鐘）。

### 作業系統快取

```bash
# 清除 macOS DNS 快取
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# 清除 Linux DNS 快取
sudo systemd-resolve --flush-caches

# 清除 Windows DNS 快取
ipconfig /flushdns
```

### DNS 伺服器快取

通常根據 TTL（Time To Live）值快取。

---

## TTL

```bash
# 設定 TTL
example.com.    IN  A       93.184.216.34
                IN  TTL     3600  # 1 小時
```

### 最佳實踐

- 正常營運時：設定較長的 TTL（數小時到一天）
- 預期變更前：先降低 TTL，變更後再提高
- 緊急變更：設定很短的 TTL

---

## 安全考量

### DNSSEC

```bash
# 數位簽章保護 DNS 資料
example.com.    IN  DNSKEY  257 3 13 ABCDEF...
```

### DNS 攻擊

- **DNS 挾持**：偽造 DNS 回應
- **DNS 放大**：利用開放 DNS 伺服器發動 DDoS
- **快取污染**：注入錯誤的 DNS 記錄

### 對應措施

- 使用可信的 DNS 伺服器（如 8.8.8.8、1.1.1.1）
- 啟用 DNSSEC
- 使用 DNS-over-HTTPS (DoH)

[搜尋 DNS security best practices](https://www.google.com/search?q=DNS+security+best+practices)

---

## 小結

DNS 是網路基礎設施的關鍵組件，了解其運作原理能幫助你更好地理解網路和除錯問題。

---

*作者：AI 程式人團隊*