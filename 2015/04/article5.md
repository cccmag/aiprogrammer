# NoSQL 安全性最佳實踐

## 前言

NoSQL 資料庫越來越廣泛地被用於生產環境，安全性變得至關重要。由於 NoSQL 的設計重點是效能和擴展性，安全功能有時會被忽視。本文將介紹保護 NoSQL 資料庫的最佳實踐。

## 網路安全

### 限制存取

```bash
# MongoDB：綁定到本地介面
# mongod.conf
net:
  bindIp: 127.0.0.1

# 生產環境使用防火牆
iptables -A INPUT -p tcp --dport 27017 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 27017 -j DROP
```

```bash
# Redis：綁定到指定介面
# redis.conf
bind 127.0.0.1 10.0.0.1
protected-mode yes
```

### TLS/SSL 加密

```bash
# MongoDB：啟用 TLS
# mongod.conf
net:
  ssl:
    mode: requireSSL
    PEMKeyFile: /path/to/mongodb.pem
    CAFile: /path/to/ca.pem
```

```python
# Python 客戶端使用 TLS
from pymongo import MongoClient

client = MongoClient(
    'mongodb://server:27017/',
    ssl=True,
    ssl_certfile='/path/to/client.pem',
    ssl_ca_certs='/path/to/ca.pem'
)
```

## 認證與授權

### MongoDB 認證

```javascript
// 建立管理者帳號
use admin
db.createUser({
    user: "admin",
    pwd: "strong_password_here",
    roles: [
        { role: "root", db: "admin" }
    ]
})

// 啟用認證（在 mongod.conf）
security:
  authorization: enabled

// 建立應用程式用的帳號（最小許可權原則）
use myapp
db.createUser({
    user: "myapp_user",
    pwd: "app_password_here",
    roles: [
        { role: "readWrite", db: "myapp" },
        { role: "dbAdmin", db: "myapp" }
    ]
})
```

### Redis 認證

```bash
# 設定密碼
# redis.conf
requirepass "strong_password_here"
```

```python
import redis

client = redis.Redis(host='localhost', port=6379)
client.auth('strong_password_here')
```

### Cassandra 認證

```bash
# cassandra.yaml
authenticator: PasswordAuthenticator
authorizer: CassandraAuthorizer
```

## 資料保護

### 靜態加密

```bash
# MongoDB：WiredTiger 加密
# mongod.conf
storage:
  wiredTiger:
    engineConfig:
      encryptionConfig:
        encrypt: AES256-CBC
```

### 備份加密

```python
import subprocess
import os

def encrypted_backup(mongo_uri, output_path):
    """建立加密的 MongoDB 備份"""
    password = os.environ['BACKUP_ENCRYPTION_KEY']

    # 建立加密的 tar 封存
    backup_file = '/tmp/mongo_backup.tar'

    # mongodump
    subprocess.run([
        'mongodump',
        '--uri', mongo_uri,
        '--out', '/tmp/mongo_backup'
    ])

    # 加密
    subprocess.run([
        'tar', 'cvf', backup_file, '-C', '/tmp', 'mongo_backup'
    ])

    subprocess.run([
        'openssl', 'enc', '-aes-256-cbc',
        '-in', backup_file,
        '-out', output_path,
        '-pass', f'pass:{password}'
    ])

    # 清理
    subprocess.run(['rm', '-rf', '/tmp/mongo_backup', backup_file])
```

## 應用層安全

### 輸入驗證

```python
# 防止注入攻擊
from pymongo import MongoClient
import re

client = MongoClient()
collection = client['app']['users']

def safe_find(username):
    # 白名單驗證
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValueError("Invalid username format")

    # 使用參數化查詢
    return collection.find_one({"username": username})
```

### SQL 注入防護（針對 MongoDB）

```python
# 錯誤的寫法（可能被注入）
def unsafe_query(collection, user_input):
    query = {"username": user_input}
    # 如果 user_input 是 "$gt: ''"，可能造成問題

# 正確的寫法
def safe_query(collection, user_input):
    # 確保輸入是字串類型
    if not isinstance(user_input, str):
        return None
    query = {"username": user_input}
    return collection.find_one(query)
```

## 監控與審計

### 日誌記錄

```yaml
# MongoDB 日誌配置
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  logRotate: reopen
```

```python
import logging
from pymongo import monitoring

class CommandLogger(monitoring.CommandLogger):
    def started(self, event):
        logging.info(f"Command {event.command_name} started on {event.connection_id}")

    def succeeded(self, event):
        logging.info(f"Command {event.command_name} succeeded in {event.duration_millis}ms")

    def failed(self, event):
        logging.error(f"Command {event.command_name} failed: {event.failure}")

monitoring.register(CommandLogger())
```

## 安全檢查清單

- [ ] 啟用認證
- [ ] 使用強密碼
- [ ] 限制網路存取
- [ ] 啟用 TLS/SSL
- [ ] 定期更新軟體
- [ ] 實施最小許可權原則
- [ ] 加密敏感資料
- [ ] 監控異常存取
- [ ] 定期審計日誌
- [ ] 備份並測試還原

NoSQL 資料庫的安全性需要從多個層面來考慮，從網路到應用層都需要謹慎設計。