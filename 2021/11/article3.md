# Kubernetes 部署實戰

## 本地開發環境

### Minikube

在本地運行 Kubernetes：

```bash
# 安裝
brew install minikube

# 啟動
minikube start

# 查看狀態
minikube status

# 存取 dashboard
minikube dashboard
```

### kubectl 基本操作

```bash
# 獲取叢集資訊
kubectl cluster-info

# 列出所有 Pod
kubectl get pods

# 列出所有資源
kubectl get all

# 描述資源
kubectl describe pod myapp-pod

# 刪除資源
kubectl delete pod myapp-pod
```

## 部署應用

### 基本流程

```bash
# 創建 deployment
kubectl create deployment myapp --image=myapp:latest

# 暴露服務
kubectl expose deployment myapp --port=8000 --type=LoadBalancer

# 擴展
kubectl scale deployment myapp --replicas=3

# 查看部署
kubectl get deployments
kubectl get pods
kubectl get services
```

## YAML 資源檔案

deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
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
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests:
            memory: "64Mi"
            cpu: "250m"
```

套用配置：

```bash
kubectl apply -f deployment.yaml
```

## 故障排除

```bash
# 查看日誌
kubectl logs myapp-pod
kubectl logs -f myapp-pod --previous

# 進入容器
kubectl exec -it myapp-pod -- /bin/bash

# 轉發連接埠
kubectl port-forward myapp-pod 8080:8000

# 診斷
kubectl get events
kubectl describe pod myapp-pod
```

## 配置管理

ConfigMap：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: "info"
  DATABASE_HOST: "db-service"
```

Secret：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
stringData:
  API_KEY: "secret-key"
```

在 Pod 中使用：

```yaml
env:
- name: LOG_LEVEL
  valueFrom:
    configMapKeyRef:
      name: myapp-config
      key: LOG_LEVEL
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: myapp-secret
      key: API_KEY
```

## 結論

Kubernetes 功能強大但概念繁多。從基本操作開始，逐步深入，是掌握它的最佳路徑。