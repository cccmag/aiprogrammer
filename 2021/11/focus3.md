# 微服務架構與服務網格

## 微服務的核心理念

微服務架構將單體應用拆分為小型、獨立的服務，每個服務負責特定功能。這種方式提高了開發靈活性、部署獨立性和故障隔離能力。

## 微服務的優勢與挑戰

優勢：
- 獨立部署團隊協作
- 技術多樣性
- 獨立擴展
- 故障隔離

挑戰：
- 服務發現
- 網路延遲
- 分散式事務
- 監控和除錯

## 服務發現

服務需要找到彼此，有兩種模式：

### 用戶端發現

客戶端查詢服務註冊中心，選擇實例：

```python
import requests

def get_service_url(service_name):
    instances = consul.get_instances(service_name)
    return select_round_robin(instances)
```

### 服務端發現

負載平衡器或 API 閘道處理發現：

```yaml
# Kubernetes Service 自動提供 DNS 發現
# my-service.my-namespace.svc.cluster.local
```

## 負載平衡

在微服務之間分配流量：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 服務網格（Service Mesh）

服務網格為服務間通訊提供基礎設施層，常見實現包括 Istio、Linkerd。

### Istio 特性

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10
```

### mTLS 加密

服務網格預設提供相互 TLS 加密：

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
```

## 分散式追蹤

追蹤請求在多個服務間的流動：

```python
from opentracing import tracer

def handle_request(request):
    with tracer.start_span("handle_request") as span:
        span.set_tag("http.method", request.method)
        call_downstream_service()
```

## 結論

微服務和服務網格共同構成了現代雲端原生應用的基礎設施。選擇何種架構應該根據團隊能力和業務需求決定。