# 災難復原與高可用性設計

## 高可用性的定義

高可用（HA）系統能夠在元件故障時繼續提供服務。衡量標準是正常運行時間百分比：99.9%（三個九）= 每年約 8.5 小時停機。

## 冗餘設計

### 多副本部署

```yaml
spec:
  replicas: 3
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - myapp
          topologyKey: kubernetes.io/hostname
```

### 多可用區部署

```yaml
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: myapp
```

## 健康檢查

### 存活探針（Liveness Probe）

確認容器是否存活：

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
  failureThreshold: 3
```

### 就緒探針（Readiness Probe）

確認容器是否就緒處理流量：

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

## 資源限制

防止單一元件耗盡資源：

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "250m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

## 災難復原規劃

### 備份策略

```bash
# 資料庫備份
pg_dump -h db-host -U dbuser mydb > backup.sql

# Kubernetes 資源備份（Velero）
velero backup create my-backup --include-namespaces myapp
```

### 復原程序

1. 驗證備份完整性
2. 建立新的命名空間
3. 恢復資源
4. 驗證服務正常

## 結論

高可用性和災難復原需要提前規劃和持續維護。投資在這些領域，能在災難發生時大幅減少損失。