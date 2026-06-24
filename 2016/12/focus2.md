# 主題二：Kubernetes 生態系統

## 什麼是 Kubernetes？

Kubernetes（又稱 K8s）是一個開源的容器編排平台，用於自動化容器化應用程式的部署、擴縮和管理。由 Google 開發並於 2015 年捐贈給 CNCF。

### Kubernetes 核心價值

```
Kubernetes 提供：
├── 自動化部署和副本管理
├── 服務發現和負載均衡
├── 自我修復（自動重啟、重新排程）
├── 水平擴縮
├── 組態管理和密鑰管理
└── 儲存編排
```

## Kubernetes 架構

```
┌─────────────────────────────────────────────────────────────┐
│                      Kubernetes Cluster                      │
│                                                              │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │   Master Node   │    │   Worker Node   │                 │
│  │  ┌───────────┐  │    │  ┌───────────┐  │                 │
│  │  │   API     │  │    │  │   kubelet  │  │                 │
│  │  │  Server   │  │    │  │   kube-    │  │                 │
│  │  └───────────┘  │    │  │   proxy   │  │                 │
│  │  ┌───────────┐  │    │  └───────────┘  │                 │
│  │  │ Scheduler│  │    │  ┌───────────┐  │                 │
│  │  └───────────┘  │    │  │  Container │  │                 │
│  │  ┌───────────┐  │    │  │   Runtime  │  │                 │
│  │  │Controller│  │    │  └───────────┘  │                 │
│  │  │ Manager   │  │    │                  │                 │
│  │  └───────────┘  │    └─────────────────┘                 │
│  └─────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## 核心概念

### Pod

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
```

```bash
kubectl apply -f pod.yaml
kubectl get pods
kubectl describe pod nginx-pod
kubectl delete pod nginx-pod
```

### ReplicaSet

```yaml
# replicaset.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicas
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
```

```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl rollout status deployment/nginx-deployment
kubectl rollout undo deployment/nginx-deployment
```

### Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

```bash
kubectl expose deployment nginx-deployment --port=80 --type=LoadBalancer
kubectl get services
kubectl describe service nginx-service
```

## Python 客戶端

```python
from kubernetes import client, config

def main():
    # 載入 kubeconfig
    config.load_kube_config()

    # 建立 API 客戶端
    v1 = client.CoreV1Api()

    # 列出所有 pods
    pods = v1.list_pod_for_all_namespaces()
    for pod in pods.items:
        print(f"{pod.metadata.namespace}: {pod.metadata.name}")

    # 建立 namespace
    namespace = client.V1Namespace()
    namespace.metadata = client.V1ObjectMeta(name="myapp")
    v1.create_namespace(namespace)

    # 刪除 pod
    v1.delete_namespaced_pod("nginx-pod", "default")


if __name__ == "__main__":
    main()
```

## ConfigMap 和 Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_HOST: "localhost"
  LOG_LEVEL: "info"
```

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=
```

```python
# 在 Pod 中使用
# configMapRef 或 envFrom
```

## Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-service
            port:
              number: 80
```

## Helm：Kubernetes Package Manager

```bash
# 安裝 Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

# 新增 chart 倉庫
helm repo add stable https://charts.helm.sh/stable

# 搜尋 chart
helm search repo nginx

# 安裝 chart
helm install my-nginx stable/nginx-ingress

# 查看 release
helm list
helm status my-nginx

# 升級
helm upgrade my-nginx stable/nginx-ingress

# 卸載
helm uninstall my-nginx
```

## Python 應用程式部署完整範例

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: python-app
  template:
    metadata:
      labels:
        app: python-app
    spec:
      containers:
      - name: web
        image: myregistry/python-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secret
              key: DB_PASSWORD
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: python-app-service
spec:
  type: LoadBalancer
  selector:
    app: python-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

## 小結

Kubernetes 已經成為容器編排的事實標準。透過其豐富的功能——包括自動化部署、服務發現、負載均衡、自我修復和水平擴縮——Kubernetes 大幅簡化了雲端原生應用的管理和擴展。

理解 Kubernetes 的核心概念和操作，是現代雲端開發者的必備技能。

---

**延伸閱讀**

- [Kubernetes Documentation](https://www.google.com/search?q=Kubernetes+official+documentation)
- [kubectl Reference](https://www.google.com/search?q=kubectl+cheat+sheet)
- [Kubernetes Best Practices](https://www.google.com/search?q=Kubernetes+best+practices)