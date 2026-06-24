# 雲端原生應用架構

## 前言

雲端原生（Cloud Native）是 2016 年的重要趨勢，利用雲端平台的特性，建構可擴展、可靠的應用系統。

## 雲端原生十二要素

### 核心要素

| 要素 | 說明 | 應用 |
|------|------|------|
| 基準程式碼 | 單一碼倉庫，對應多個部署 | Git |
| 依賴 | 明確宣告並隔離依賴 | requirements.txt |
| 設定 | 將設定放在環境中 | 環境變數 |
| 後端服務 | 將後端視為附掛資源 | ConfigMap |
| 建置、發布、執行 | 嚴格分離建置與執行階段 | CI/CD Pipeline |
| 處理序 | 應用為無狀態處理序 | Stateless Design |
| 連接埠绑定 | 服務透過連接埠暴露 | Kubernetes Service |
| 併發 | 透過複製擴展 | Horizontal Pod Autoscaling |
| 易拋棄 | 快速啟動與優雅關閉 | Graceful Shutdown |
| 開發與生產一致性 | 保持所有環境相似 | Docker |
| 日誌 | 将日志视为事件流 | ELK Stack |
| 管理程序 | 將管理任務視為一次性處理 | Admin Tools |

## 微服務架構

```yaml
# docker-compose.microservices.yml
version: '3'

services:
  api-gateway:
    build: ./api-gateway
    ports:
      - "80:80"
    depends_on:
      - user-service
      - order-service
      - product-service
  
  user-service:
    build: ./user-service
    environment:
      - DATABASE_URL=postgres://db:5432/users
    deploy:
      replicas: 2
  
  order-service:
    build: ./order-service
    environment:
      - DATABASE_URL=postgres://db:5432/orders
    deploy:
      replicas: 3
  
  product-service:
    build: ./product-service
    environment:
      - CACHE_URL=redis://cache:6379
    deploy:
      replicas: 2
  
  db:
    image: postgres:9.6
  
  cache:
    image: redis:3.2-alpine
```

## 無狀態設計

```python
# stateless_service.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 使用外部 Session 儲存
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

def get_session(session_id):
    import redis
    r = redis.from_url(REDIS_URL)
    data = r.get(f'session:{session_id}')
    return json.loads(data) if data else {}

def save_session(session_id, data):
    import redis
    r = redis.from_url(REDIS_URL)
    r.setex(f'session:{session_id}', 3600, json.dumps(data))

@app.route('/api/user/<user_id>')
def get_user(user_id):
    session = get_session(request.headers.get('X-Session-ID'))
    return jsonify({
        'id': user_id,
        'session': session
    })
```

## Horizontal Pod Autoscaling

```yaml
# hpa.yml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

## 服務發現

```yaml
# service.yml (Kubernetes)
apiVersion: v1
kind: Service
metadata:
  name: user-service
  labels:
    app: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 3000
  clusterIP: None  # Headless service
```

```python
# service_discovery.py
import os

def discover_service(service_name):
    # 在 K8s 內使用 DNS
    hostname = f"{service_name}.default.svc.cluster.local"
    port = 80
    return f"http://{hostname}:{port}"

# 使用環境變數（更推薦）
SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:80')
```

## 熔斷器模式

```python
# circuit_breaker.py
from functools import wraps
import time
import requests

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'half-open'
            else:
                raise Exception("Circuit is open")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'half-open':
                self.state = 'closed'
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = 'open'
            raise
```

## 延伸閱讀

- [雲端原生架構](https://www.google.com/search?q=cloud+native+architecture+2016)
- [微服務設計模式](https://www.google.com/search?q=microservice+design+patterns+2016)
- [十二要素應用](https://www.google.com/search?q=twelve+factor+app+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*