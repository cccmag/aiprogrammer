# Kubernetes 容器編排詳解

## Kubernetes 概述

Kubernetes（K8s）是一個開源的容器編排平台，自動化容器化應用程式的部署、擴展和管理。它已成為雲端原生計算的基石。

## 核心概念

### Pod

Pod 是 Kubernetes 的基本部署單元，一個 Pod 可以包含一個或多個緊密耦合的容器：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp
    image: myapp:latest
    ports:
    - containerPort: 8000
```

### ReplicaSet

確保指定數量的 Pod 副本始終運行：

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
```

### Deployment

提供聲明式的 Pod 更新：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v2
```

## Service

為 Pod 提供穩定的網路端點：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## ConfigMap 與 Secret

管理配置和敏感資訊：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_HOST: "db-service"
  LOG_LEVEL: "info"
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
stringData:
  API_KEY: "secret-key-here"
```

## 命名空間（Namespace）

邏輯隔離資源：

```bash
kubectl create namespace myapp-namespace
kubectl get namespaces
```

## 日常操作

```bash
# 部署應用
kubectl apply -f deployment.yaml

# 查看資源
kubectl get pods -n myapp-namespace
kubectl describe pod myapp-pod

# 擴展應用
kubectl scale deployment myapp-deployment --replicas=5

# 檢視日誌
kubectl logs -f myapp-pod

# 轉發連接埠
kubectl port-forward myapp-pod 8080:8000
```

## 結論

Kubernetes 雖然學習曲線較陡，但其强大的功能和靈活性使其成為大規模容器部署的首選解決方案。