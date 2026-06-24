# Kubernetes 1.16：Custom Resources 與 CSI

## 前言

Kubernetes 1.16 於 2019 年 9 月正式發布。這個版本包含了多項重要的 GA（正式可用）功能，特別是 Custom Resources 和 Container Storage Interface (CSI) 的持續改進。

## Custom Resources (CRD) GA

### 什麼是 Custom Resources？

Custom Resources 是 Kubernetes 擴展 API 的方式，允許開發者定義自己的資源類型：

```yaml
# 定義一個自定義資源 CronTab
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  names:
    kind: CronTab
    plural: crontabs
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
```

### 1.16 的改進

```yaml
# 使用自定義資源
apiVersion: stable.example.com/v1
kind: CronTab
metadata:
  name: my-crontab
spec:
  cronSpec: "* * * * */5"
  image: my-cron-image
```

---

## CSI 持續改進

### Container Storage Interface

CSI 是 Kubernetes 與外部儲存系統交互的標準介面：

```go
// CSI Driver 介面
type NodeServiceCapability interface {
    // 捲輯加
    NodeStageVolume() {}
    // 捲掛載
    NodePublishVolume() {}
}
```

### 新支援的 CSI 功能

```yaml
# 區塊儲存
apiVersion: v1
kind: PersistentVolume
spec:
  capacity:
    storage: 10Gi
  storageClassName: fast-storage
  persistentVolumeReclaimPolicy: Retain
  csi:
    driver: pd.csi.storage.gke.io
    volumeHandle: "projects/PROJECT/zones/us-central1-a/disks/pd-name"
```

---

## Scheduling Framework Alpha

### 新增的調度功能

```go
// Scheduling Framework 的 Plugin 介面
type PreFilterPlugin interface {
    PreFilter(ctx context.Context, state *CycleState, p *v1.Pod) *Status
}

type FilterPlugin interface {
    Filter(ctx context.Context, state *CycleState, p *v1.Pod, nodeInfo *NodeInfo) *Status
}
```

---

## 其他重要更新

### RuntimeClass 和 PodTopologySpread GA

```yaml
apiVersion: v1
kind: Pod
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: my-app
```

### 結語

Kubernetes 1.16 標誌著 CRD 和 CSI 的成熟，為雲原生應用提供了更穩定的擴展基礎。

---

**延伸閱讀**

- [Kubernetes 1.16 Release Notes](https://www.google.com/search?q=Kubernetes+1.16+release+notes)
- [Custom Resources Definition](https://www.google.com/search?q=Kubernetes+CRD+custom+resources)
- [CSI Documentation](https://www.google.com/search?q=Kubernetes+CSI+storage)