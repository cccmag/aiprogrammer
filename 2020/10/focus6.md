# 容器編排與 Kubernetes：Python 大規模部署

## 容器編排的概念

### 什麼是容器編排？

當應用規模擴大到需要管理數十、數百甚至數千個容器時，容器編排就變得必要：

```
手動管理 vs 編排系統：
────────────────────────────────────────────────────────

手動管理（不可擴展）：
  Container 1 ──► 手動啟動/停止
  Container 2 ──► 手動網路配置
  Container 3 ──► 手動負載平衡
  ...           ──► 不可行！

編排系統（自動化管理）：
  ┌─────────────────────────────────────────────┐
  │           Orchestrator (K8s, Swarm)          │
  │                                             │
  │   自動部署      自動擴展      自動修復       │
  │      │            │            │            │
  │      ▼            ▼            ▼            │
  │   ┌─────┐      ┌─────┐      ┌─────┐        │
  │   │ C1  │      │ C2  │      │ C3  │        │
  │   └─────┘      └─────┘      └─────┘        │
  │      │            │            │            │
  │      └────────────┼────────────┘            │
  │                   ▼                          │
  │           Service Discovery                  │
  │           Load Balancer                      │
  └─────────────────────────────────────────────┘
```

### 主要容器編排平台

- **Kubernetes**：Google 開源的事實標準
- **Docker Swarm**：Docker 原生的編排方案
- **Apache Mesos**：Twitter 等公司在使用
- **Amazon ECS/EKS**：AWS 的容器服務
- **Azure AKS**：Azure 的 Kubernetes 服務

## Kubernetes 基礎

### 核心概念

```
Kubernetes 架構：
────────────────────────────────────────────────────────

         ┌──────────────┐
         │   Control    │
         │   Plane      │
         │ (Master Node)│
         │              │
         │ ┌──────────┐ │
         │ │ API Server│ │
         │ │ Scheduler │ │
         │ │ etcd     │ │
         │ └──────────┘ │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Worker │ │ Worker │ │ Worker │
│ Node 1 │ │ Node 2 │ │ Node 3 │
│        │ │        │ │        │
│┌──────┐│ │┌──────┐│ │┌──────┐│
││ Pod  ││ ││ Pod  ││ ││ Pod  ││
│└──────┘│ │└──────┘│ │└──────┘│
│┌──────┐│ │┌──────┐│ │        │
││ Pod  ││ ││ Pod  ││ │        │
│└──────┘│ │└──────┘│ │        │
└────────┘ └────────┘ └────────┘
```

**核心資源**：
- **Pod**：Kubernetes 的基本部署單元，一個或多個容器
- **Deployment**：管理 Pod 的宣告式更新
- **Service**：網路抽象，定義 Pod 的存取方式
- **ConfigMap/Secret**：配置和敏感資料管理
- **Ingress**：HTTP/HTTPS 路由

### 基本指令

```bash
# 建立 Deployment
kubectl create deployment myapp --image=myapp:latest

# 擴展 Deployment
kubectl scale deployment myapp --replicas=3

# 查看 Pods
kubectl get pods

# 檢視日誌
kubectl logs -f pod/myapp-xxx

# 進入 Pod
kubectl exec -it pod/myapp-xxx -- /bin/bash

# 刪除資源
kubectl delete deployment myapp
```

## 在 K8s 上部署 Python 應用

### Deployment YAML

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-python-app
  labels:
    app: my-python-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-python-app
  template:
    metadata:
      labels:
        app: my-python-app
    spec:
      containers:
      - name: my-python-app
        image: myregistry/myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
```

### Service YAML

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-python-app-service
spec:
  type: LoadBalancer
  selector:
    app: my-python-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Ingress YAML

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-python-app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-python-app-service
            port:
              number: 80
```

### ConfigMap 和 Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: "INFO"
  WORKERS: "4"
```

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:pass@db:5432/myapp"
  SECRET_KEY: "my-secret-key"
```

## Helm 與 Kustomize

### Helm：Kubernetes 的套件管理

Helm 讓你可以用 Chart 的方式管理和部署應用：

```bash
# 安裝 Helm
brew install helm

# 新增 Repo
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update

# 安裝 Chart
helm install my-release stable/postgresql

# 查看 Release
helm list

# 升級
helm upgrade my-release stable/postgresql --set persistence.size=100Gi

# 刪除
helm uninstall my-release
```

### 自訂 Chart

```yaml
# values.yaml
replicaCount: 3

image:
  repository: myregistry/myapp
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80

resources:
  limits:
    memory: 256Mi
    cpu: 500m
```

```bash
# 從模板建立 Chart
helm create mychart

# 封裝 Chart
helm package mychart

# 部署本地 Chart
helm install myapp ./mychart-0.1.0.tgz
```

### Kustomize：宣告式配置管理

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- configmap.yaml

commonLabels:
  app: my-python-app

namespace: production

images:
- name: myregistry/myapp
  newTag: v1.2.3
```

```bash
# 部署
kubectl apply -k ./

# 預覽變更
kubectl diff -k ./

# 環境特定配置
kubectl apply -k ./overlays/production
```

## 自動化維運

### HPA（水平 Pod 自動擴縮）

```yaml
# hpa.yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: my-python-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-python-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 更新策略

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

## 延伸閱讀

- [Kubernetes 官方文件](https://www.google.com/search?q=Kubernetes+official+documentation)
- [Python Kubernetes 用戶端](https://www.google.com/search?q=Kubernetes+Python+client)
- [Helm 文件](https://www.google.com/search?q=Helm+Kubernetes+package+manager)
- [Kustomize 文件](https://www.google.com/search?q=Kustomize+ Kubernetes+declarative+configuration)
- [K8s 部署 Python 應用教學](https://www.google.com/search?q=deploy+Python+app+to+ Kubernetes+tutorial)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」歷史回顧系列之一。*