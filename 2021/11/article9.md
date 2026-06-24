# 成本優化與雲端資源管理

## 雲端成本為何重要

雲端採隨用隨付模式，但資源閒置或使用不當會導致不必要的開支。優化成本是雲端運維的重要課題。

## 資源標籤策略

```yaml
tags:
  Environment: Production
  Team: Platform
  CostCenter: Engineering
  Project: MyApp
```

### 使用標籤進行成本分攤

```bash
# AWS Cost Explorer
aws ce get-cost-and-usage \
  --time-period Start=2021-01-01,End=2021-02-01 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=TAG,Key=Project
```

## 右向大小調整

選擇合适的資源大小：

```yaml
# 過度配置
resources:
  requests:
    memory: "4Gi"
    cpu: "2000m"
  limits:
    memory: "8Gi"
    cpu: "4000m"

# 優化後
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Spot/Preemptible 實例

使用便宜的間斷實例：

```yaml
# AWS EKS 節點池配置
nodeGroups:
  - name: spot-nodes
    instanceType: m5.large
    spotCapacity: true
    # ...
```

適合無狀態、可容忍中斷的工作負載。

## 儲存成本優化

```bash
# 移動不需要的資料到較便宜的儲存層
# S3 Intelligent-Tiering
aws s3api put-object-storage-class \
  --bucket my-bucket \
  --key old-data/file.gz \
  --storage-class INTELLIGENT_TIERING
```

## 自動擴展

根據需求動態調整資源：

```yaml
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

## 結論

雲端成本優化是一個持續的過程。通過標籤、調整大小、使用 Spot 實例和自動擴展，可以顯著降低雲端開支。