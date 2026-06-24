# 容器化技術實作

## 前言

本文展示 Docker 和 Kubernetes 的實作範例，涵蓋從簡單的容器化應用到複雜的編排配置。

---

## 原始碼

完整的程式實作請參考：[_code/docker_demo.py](_code/docker_demo.py) 和 [_code/k8s_demo.py](_code/k8s_demo.py)

---

## docker_demo.py：Python Docker 應用

```python
#!/usr/bin/env python3
"""Docker Demo: Containerize a Python Application"""

from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COUNTER = 0


@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Docker!',
        'version': '1.0',
    })


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


@app.route('/counter', methods=['GET', 'POST'])
def counter():
    global COUNTER

    if request.method == 'POST':
        COUNTER += 1
        logger.info(f"Counter incremented to {COUNTER}")
        return jsonify({'counter': COUNTER, 'action': 'incremented'})
    else:
        return jsonify({'counter': COUNTER})


@app.route('/reset', methods=['POST'])
def reset():
    global COUNTER
    COUNTER = 0
    logger.info("Counter reset")
    return jsonify({'counter': COUNTER, 'action': 'reset'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
```

---

## Dockerfile 示例

```dockerfile
FROM python:3.9-slim

LABEL maintainer="ai@magazine.com"
LABEL description="AI Magazine Demo Application"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 80

CMD ["python", "app.py"]
```

---

## k8s_demo.py：Kubernetes 配置生成

```python
#!/usr/bin/env python3
"""Kubernetes Demo: Generate K8s YAML configurations"""

import yaml


def generate_deployment(name, image, replicas=2):
    """Generate Kubernetes Deployment YAML"""
    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': name,
            'labels': {'app': name}
        },
        'spec': {
            'replicas': replicas,
            'selector': {
                'matchLabels': {'app': name}
            },
            'template': {
                'metadata': {
                    'labels': {'app': name}
                },
                'spec': {
                    'containers': [{
                        'name': name,
                        'image': image,
                        'ports': [{'containerPort': 80}],
                        'livenessProbe': {
                            'httpGet': {'path': '/health', 'port': 80},
                            'initialDelaySeconds': 3,
                            'periodSeconds': 3
                        },
                        'readinessProbe': {
                            'httpGet': {'path': '/health', 'port': 80},
                            'initialDelaySeconds': 5,
                            'periodSeconds': 5
                        },
                        'resources': {
                            'limits': {'memory': '256Mi', 'cpu': '500m'},
                            'requests': {'memory': '128Mi', 'cpu': '100m'}
                        }
                    }]
                }
            }
        }
    }
    return yaml.dump(deployment)


def generate_service(name, service_type='ClusterIP'):
    """Generate Kubernetes Service YAML"""
    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {'name': name},
        'spec': {
            'type': service_type,
            'selector': {'app': name},
            'ports': [{
                'protocol': 'TCP',
                'port': 80,
                'targetPort': 80
            }]
        }
    }
    return yaml.dump(service)


def generate_configmap(name, data):
    """Generate Kubernetes ConfigMap YAML"""
    configmap = {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {'name': name},
        'data': data
    }
    return yaml.dump(configmap)


def generate_ingress(name, host, service_name):
    """Generate Kubernetes Ingress YAML"""
    ingress = {
        'apiVersion': 'networking.k8s.io/v1',
        'kind': 'Ingress',
        'metadata': {
            'name': name,
            'annotations': {
                'nginx.ingress.kubernetes.io/rewrite-target': '/'
            }
        },
        'spec': {
            'rules': [{
                'host': host,
                'http': {
                    'paths': [{
                        'path': '/',
                        'pathType': 'Prefix',
                        'backend': {
                            'service': {
                                'name': service_name,
                                'port': {'number': 80}
                            }
                        }
                    }]
                }
            }]
        }
    }
    return yaml.dump(ingress)


def demo():
    print("=== Kubernetes YAML Generator ===\n")

    print("Deployment:")
    print(generate_deployment('myapp', 'myregistry/myapp:latest'))

    print("\nService:")
    print(generate_service('myapp', 'LoadBalancer'))

    print("\nConfigMap:")
    print(generate_configmap('myapp-config', {
        'DATABASE_HOST': 'db-service',
        'LOG_LEVEL': 'info'
    }))

    print("\nIngress:")
    print(generate_ingress('myapp-ingress', 'myapp.example.com', 'myapp'))


if __name__ == "__main__": demo()
```

---

## Docker Compose 完整範例

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:80"
    environment:
      - PORT=80
      - DATABASE_HOST=db
    depends_on:
      - db
      - redis
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
      restart_policy:
        condition: on-failure
        max_attempts: 3

  db:
    image: postgres:13-alpine
    volumes:
      - pg_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

  redis:
    image: redis:6-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  pg_data:
  redis_data:

secrets:
  db_password:
    file: ./db_password.txt
```

---

## 執行結果

```
=== Kubernetes YAML Generator ===

Deployment:
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: myapp
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - image: myregistry/myapp:latest
        name: myapp
        ports:
        - containerPort: 80
        ...

Service:
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: myapp
  type: ClusterIP
```

---

## 最佳實踐

### 安全最佳化

```dockerfile
# 使用非 root 用戶
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# 只複製需要的檔案
COPY --chown=appuser:appgroup . .

# 使用多階段建構
FROM python:3.9 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python", "app.py"]
```

### 效能優化

```dockerfile
# 使用 slim 版本
FROM python:3.9-slim

# 合併指令減少層數
RUN pip install --no-cache-dir \
    flask==2.0.0 \
    requests==2.26.0

# .dockerignore
__pycache__/
*.pyc
.git/
*.md
```

---

## 延伸閱讀

- [Docker Best Practices](https://www.google.com/search?q=Docker+best+practices)
- [Kubernetes Documentation](https://www.google.com/search?q=Kubernetes+official+documentation)
- [Dockerfile Reference](https://www.google.com/search?q=Dockerfile+reference)

---

*本篇文章為「AI 程式人雜誌 2016 年 12 月號」年度技術回顧補充文章。*