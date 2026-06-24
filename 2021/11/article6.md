# 服務發現與負載平衡

## 服務發現的重要性

在微服務架構中，服務需要找到彼此。服務發現自動化這個過程，無需手動配置 IP 位址或主機名。

## Kubernetes 中的服務發現

### DNS

Kubernetes 提供叢集內部的 DNS 服務：

```bash
# 服務建立後會自動註冊 DNS
# my-service.my-namespace.svc.cluster.local
```

### 環境變數

Kubelet 為每個 Pod 注入環境變數：

```bash
# 例如對於名為 "redis-master" 的服務
REDIS_MASTER_SERVICE_HOST=10.0.0.100
REDIS_MASTER_SERVICE_PORT=6379
```

## Service 類型

### ClusterIP（預設）

僅叢集內部存取：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
```

### NodePort

暴露節點連接埠：

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8000
    nodePort: 30080
```

### LoadBalancer

使用雲端負載平衡器：

```yaml
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
```

## Ingress

HTTP/HTTPS 路由：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

## 負載平衡策略

### Round Robin

輪流分配請求，最簡單的策略。

### 最少連線

將請求發送到連線數最少的實例。

### IP Hash

根據客戶端 IP 決定伺服器，保證同一客戶端 consistently 到同一伺服器。

### 權重

根據權重比例分配流量，用於 canary 部署。

## 結論

服務發現和負載平衡是微服務架構的基礎設施。正確的配置能提高系統的可用性和效能。