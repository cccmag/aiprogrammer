# Kubernetes 基礎與部署

## 前言

Kubernetes（K8s）是容器編排的標準，讓大規模容器管理變得簡單。2016 年的 Kubernetes 1.4 大幅改善了可用性。

## 核心概念

```
Pod → ReplicaSet → Deployment
         ↓
      Service → Ingress
```

## 基本資源

### Pod

```yaml
# pod.yml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
    - name: myapp
      image: myapp:1.0.0
      ports:
        - containerPort: 3000
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
```

### Deployment

```yaml
# deployment.yml
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: myapp-deployment
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
          image: myapp:1.0.0
          ports:
            - containerPort: 3000
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
```

### Service

```yaml
# service.yml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
```

### Ingress

```yaml
# ingress.yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            backend:
              serviceName: myapp-service
              servicePort: 80
```

## kubectl 常用指令

```bash
# 建立資源
kubectl create -f deployment.yml

# 列出資源
kubectl get pods
kubectl get deployments
kubectl get services

# 描述資源
kubectl describe pod myapp-pod

# 刪除資源
kubectl delete -f deployment.yml

# 擴展 Deployment
kubectl scale deployment myapp-deployment --replicas=5

# 更新映像
kubectl set image deployment/myapp myapp=myapp:2.0.0

# 查看日誌
kubectl logs -f myapp-pod

# 進入容器
kubectl exec -it myapp-pod -- /bin/bash

# 轉發連接埠
kubectl port-forward myapp-pod 8080:3000
```

## 滾動更新

```bash
# 更新 Deployment
kubectl apply -f deployment-v2.yml

# 查看更新狀態
kubectl rollout status deployment/myapp-deployment

# 回滾到上一版本
kubectl rollout undo deployment/myapp-deployment

# 回滾到特定版本
kubectl rollout undo deployment/myapp-deployment --to-revision=2
```

## ConfigMap 與 Secret

```yaml
# configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_URL: "postgres://db:5432/myapp"
  REDIS_URL: "redis://redis:6379"
```

```yaml
# secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJfc2VjcmV0  # base64 編碼
```

## 本地開發（Minikube）

```bash
# 安裝 Minikube
brew install minikube

# 啟動叢集
minikube start

# 部署應用
kubectl apply -f deployment.yml

# 開啟 Dashboard
minikube dashboard
```

## 延伸閱讀

- [Kubernetes 官方文檔](https://www.google.com/search?q=kubernetes+tutorial+2016)
- [kubectl 指令參考](https://www.google.com/search?q=kubectl+commands+2016)
- [Kubernetes 部署策略](https://www.google.com/search?q=kubernetes+deployment+strategies+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*