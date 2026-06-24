# 雲端的安全性：安全挑戰與解決方案

## 雲端安全的重要性

2007 年，隨著企業開始將資料和應用遷移到雲端，安全成為首要考量。

### 安全威脅

```
雲端安全威脅：
──────────────
1. 資料外洩
2. 帳戶綁架
3. 內部威脅
4. API 安全漏洞
5. 拒絕服務攻擊
6. 依賴供應商的風險
```

## 安全策略

### 1. 資料加密

```python
# S3 伺服器端加密
import boto.s3
from boto.s3.key import Key

bucket = conn.get_bucket('my-bucket')
key = bucket.new_key('sensitive.txt')
key.set_contents_from_string(
    encrypted_data,
    encrypt_key=True  # S3 自動加密
)
```

### 2. 傳輸加密

```python
# HTTPS 傳輸
# S3 提供安全端點
# https://my-bucket.s3.amazonaws.com/path

# 使用 TLS/SSL
import ssl
# 確保所有 API 呼叫使用 HTTPS
```

### 3. 存取控制

```python
# IAM（Identity and Access Management）概念
# 2007 年的 AWS 沒有完整 IAM，使用 S3 ACL

# S3 ACL 範例
bucket.set_acl('private')  # 只有擁有者
key.set_acl('public-read')  # 公開讀取
```

### 4. 身份驗證

```python
# AWS 認證
# 使用 Access Key 和 Secret Key

import boto
conn = boto.connect_s3('ACCESS_KEY', 'SECRET_KEY')

# 建議使用 IAM Role（後來的功能）
# 避免在程式碼中儲存憑證
```

## 合規性

### 雲端合規挑戰

```bash
# 主要合規問題
# 1. 資料主權
# 2. 隱私權法規（HIPAA, SOX, PCI-DSS）
# 3. 審計要求
# 4. 資料在地化
```

## 結語

雲端安全需要「共享責任模型」——雲端供應商負責基礎設施安全，客戶負責應用和資料安全。

---

## 延伸閱讀

- [cloud+computing+security+2007](https://www.google.com/search?q=cloud+computing+security+2007)

---