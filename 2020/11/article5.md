# 服務網格與 Istio

## 前言

服務網格（Service Mesh）是管理服務間通訊的基礎設施層，Istio 是最受歡迎的開源服務網格實現。

## 核心功能

```
Istio 功能：
────────────────────────────────

1. 流量管理
   └── 智慧路由、負載均衡、熔斷

2. 可觀測性
   └── 追蹤、監控、日誌聚合

3. 安全
   └── mTLS 加密、身分驗證、授權

4. 策略控制
   └── 流量限制、配額管理
```

## 流量管理

```yaml
# VirtualService 範例
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - match:
    - headers:
        cookie:
          regex: ".*customer_type=premium.*"
    route:
    - destination:
        host: my-service-premium
        subset: v2
  - route:
    - destination:
        host: my-service
        subset: v1
```

## 延伸閱讀

- [Istio 官方網站](https://www.google.com/search?q=Istio+service+mesh+official)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*