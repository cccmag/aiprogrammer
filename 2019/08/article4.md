# Kubernetes 1.15：Local PV GA

## 前言

Kubernetes 1.15 於 2019 年 6 月正式發布。這個版本的重點是 StatefulSet 和 Local PV 的 GA（正式可用）。

## Local PV 的穩定化

### 本地持久化儲存

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
spec:
  capacity:
    storage: 100Gi
  storageClassName: local-storage
  local:
    path: /mnt/disks/ssd1
  nodeAffinity:
    required:
      - nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
            - my-node
```

---

## StatefulSet 改進

### 增強的排序保證

StatefulSet 的有序部署和擴展得到進一步優化。

---

## 結語

Kubernetes 1.15 的 Local PV GA 對於需要高性能本地儲存的應用是重要進步。

---

**延伸閱讀**

- [Kubernetes 1.15 Release Notes](https://www.google.com/search?q=Kubernetes+1.15+release+notes)
- [Local PV Kubernetes](https://www.google.com/search?q=kubernetes+local+persistent+volume)