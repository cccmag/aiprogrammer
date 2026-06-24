# Kubernetes 1.17：Custom Resources v1

## 前言

Kubernetes 1.17 於 2019 年 12 月發布，Custom Resources Definition (CRD) v1 達到了正式穩定狀態。

## CRD v1

### 創建自定義資源

```yaml
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

---

## 結語

CRD v1 的GA標誌著 Kubernetes 擴展性的成熟，允許開發者定義自己的資源類型。

---

**延伸閱讀**

- [Kubernetes 1.17 CRD](https://www.google.com/search?q=Kubernetes+1.17+CRD+v1)