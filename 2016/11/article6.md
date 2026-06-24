# 環境管理策略

## 前言

環境管理是 DevOps 的核心挑戰之一。如何在開發、測試、正式環境之間保持一致性，同時又能靈活配置？

## 環境類型

| 環境 | 用途 | 特性 |
|------|------|------|
| Local | 開發 | 快速迭代、本機資源 |
| Dev | 整合測試 | 接近正式、對外隔離 |
| Staging | UAT | 與正式相同配置 |
| Production | 正式服務 | 高可用、安全 |

## 環境變數管理

### 開發環境

```bash
# .env.development
DATABASE_URL=postgres://localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379
LOG_LEVEL=debug
DEBUG=true
```

### 正式環境

```bash
# .env.production
DATABASE_URL=postgres://prod-db:5432/myapp
REDIS_URL=redis://prod-cache:6379
LOG_LEVEL=info
DEBUG=false
```

### Python 載入設定

```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    env = os.environ.get('APP_ENV', 'development')
    
    database_url = os.environ.get('DATABASE_URL', '')
    redis_url = os.environ.get('REDIS_URL', '')
    log_level = os.environ.get('LOG_LEVEL', 'info')
    
    @classmethod
    def from_env(cls):
        return cls(
            database_url=os.environ.get('DATABASE_URL', ''),
            redis_url=os.environ.get('REDIS_URL', ''),
            log_level=os.environ.get('LOG_LEVEL', 'info')
        )

class DevelopmentConfig(Config):
    debug = True

class ProductionConfig(Config):
    debug = False
```

## Docker 環境隔離

```yaml
# docker-compose.dev.yml
version: '3'

services:
  app:
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://db:5432/myapp
    volumes:
      - ./src:/app/src

---

# docker-compose.prod.yml
version: '3'

services:
  app:
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://prod-db:5432/myapp
    restart: unless-stopped
    read_only: true
```

## 設定管理工具

### Consul

```python
# config_from_consul.py
import consul

c = consul.Consul()

# 讀取設定
c.kv.get('myapp/database_url')

# 監聽變更
def handle_change(index):
    index, data = c.kv.get('myapp/config', index=index)
    if data:
        config = json.loads(data['Value'])
        update_app_config(config)
    return index

watch_index = None
while True:
    watch_index = handle_change(watch_index)
    time.sleep(5)
```

### etcd

```bash
# etcd 指令
etcdctl set /myapp/config '{"database": "postgres"}'
etcdctl get /myapp/config
```

## 秘密管理

### Vault

```bash
# 寫入秘密
vault write secret/myapp/db_password value=super_secret

# 讀取秘密
vault read secret/myapp/db_password
```

```python
# vault_client.py
import hvac

def get_secret(path):
    client = hvac.Client(url='http://vault:8200')
    client.token = os.environ['VAULT_TOKEN']
    result = client.read(path)
    return result['data']

db_password = get_secret('secret/myapp/db_password')
```

## 環境一致性策略

### 不可變基礎設施

伺服器一經部署就不修改，更新時建立新伺服器替換。

```bash
# 建立新伺服器（使用 Packer）
packer build -var="version=2.0.0" template.json

# Terraform 部署新實例
terraform apply -var="ami=new_version_ami"
```

### 金絲雀部署

```yaml
# canary-deployment.yml
apiVersion: flagger.app/v1alpha1
kind: Canary
spec:
  targetRef:
    apiVersion: apps/apps/v1
    kind: Deployment
    name: myapp
  analysis:
    interval: 1m
    threshold: 5
    stepWeight: 20
    maxWeight: 80
```

## 延伸閱讀

- [環境管理策略](https://www.google.com/search?q=environment+management+devops+2016)
- [秘密管理工具](https://www.google.com/search?q=secrets+management+2016)
- [不可變基礎設施](https://www.google.com/search?q=immutable+infrastructure+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*