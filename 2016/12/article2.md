# Kubernetes 部署策略

## 前言

Kubernetes 提供了多種部署策略來滿足不同的需求。本文探討各種部署方式和滾動更新的最佳實踐。

## 常見部署策略

### 重建策略（Recreate）

```yaml
# recreate-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  strategy:
    type: Recreate
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1
```

缺點：會導致服務中斷

### 滾動更新策略（RollingUpdate）

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 最多超出預期副本數
      maxUnavailable: 0  # 不可用的副本數
```

```bash
# 手動觸發滾動更新
kubectl set image deployment/myapp myapp=myapp:v2

# 查看更新狀態
kubectl rollout status deployment/myapp

# 回滾
kubectl rollout undo deployment/myapp
```

### 藍綠部署（Blue-Green）

```yaml
# v1 (blue) - 當前版本
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: v1
  ports:
  - port: 80
    targetPort: 80

---
# deployment-v2.yaml (green)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v2
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: v2
  template:
    metadata:
      labels:
        app: myapp
        version: v2
    spec:
      containers:
      - name: myapp
        image: myapp:v2
```

```bash
# 部署 v2
kubectl apply -f deployment-v2.yaml

# 驗證 v2
kubectl get pods -l version=v2

# 切換流量到 v2
kubectl patch service myapp-service -p '{"spec":{"selector":{"version":"v2"}}}'

# 驗證成功後刪除 v1
kubectl delete deployment myapp-v1
```

### 金絲雀部署（Canary）

```yaml
# canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      track: canary
  template:
    metadata:
      labels:
        app: myapp
        track: canary
    spec:
      containers:
      - name: myapp
        image: myapp:v2
```

```bash
# 主要版本 90% 副本
kubectl scale deployment myapp --replicas=9

# 金絲雀 10% 副本
kubectl scale deployment myapp-canary --replicas=1

# 使用 Label selector 調整比例
kubectl label service myapp version=v1
kubectl label service myapp version=canary
```

## Deployment 進階配置

### 就緒探測（Readiness Probe）

```yaml
spec:
  containers:
  - name: myapp
    image: myapp:v1
    readinessProbe:
      httpGet:
        path: /ready
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
      failureThreshold: 3
```

### 存活探測（Liveness Probe）

```yaml
spec:
  containers:
  - name: myapp
    image: myapp:v1
    livenessProbe:
      httpGet:
        path: /health
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 10
      failureThreshold: 3
```

### 啟動探測（Startup Probe）

```yaml
spec:
  containers:
  - name: myapp
    image: myapp:v1
    startupProbe:
      httpGet:
        path: /health
        port: 80
      failureThreshold: 30
      periodSeconds: 10
```

## 配置管理

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: "info"
  DATABASE_HOST: "db-service"
```

```yaml
# 使用 ConfigMap
spec:
  containers:
  - name: myapp
    envFrom:
    - configMapRef:
        name: myapp-config
```

### Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=  # base64 編碼
```

## 水平自動擴縮

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
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

```bash
kubectl autoscale deployment myapp --cpu-percent=70 --min=2 --max=10
kubectl get hpa
```

## 災難恢復

### 備份策略

```bash
# 備份 etcd
ETCDCTL_API=3 etcdctl snapshot save backup.db

# 還原
ETCDCTL_API=3 etcdctl snapshot restore backup.db
```

### 跨區域部署

```yaml
# node-affinity 示例
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-east-1a
```

## 小結

選擇合適的部署策略取決於您的需求：快速回滾、金絲雀測試、零停機更新。Kubernetes 提供了靈活工具來實現這些策略，結合健康檢查、資源限制和自動擴縮，可以構建高可用的服務。

---

**延伸閱讀**

- [Kubernetes Deployment Strategies](https://www.google.com/search?q=Kubernetes+deployment+strategies)
- [Rolling Update Documentation](https://www.google.com/search?q=Kubernetes+rolling+update)
- [Canary Deployment](https://www.google.com/search?q=canary+deployment+Kubernetes)