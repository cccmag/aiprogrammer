# 邊緣運算與混合雲架構

## 邊緣運算的興起

邊緣運算將運算能力推向網路邊緣，接近資料產生的地方。這對於需要低延遲或資料主權的應用至關重要。

## 邊緣運算的應用場景

- **物聯網**：感測器資料即時處理
- **自動駕駛**：毫秒級反應時間
- **影片處理**：減少傳輸頻寬
- **AR/VR**：低延遲體驗

## Kubernetes at the Edge

K3s 是專為邊緣設計的輕量級 K8s 發行版：

```bash
# 安裝 K3s
curl -sfL https://get.k3s.io | sh -

# 查看節點
kubectl get nodes
```

### K3s vs 標準 K8s

| 特性 | K3s | 標準 K8s |
|------|-----|----------|
| 記憶體需求 | ~512MB | ~2GB |
| 支援的架構 | 多種 | 主要 x86 |
| 容器網路介面 | Flannel | 多種 |

## 混合雲架構

混合雲結合公有雲和私有雲/本地資料中心。

### 使用場景

- 將敏感資料保留在本地
- 利用公有雲的彈性和服務
- 災難復原

### 常見模式

```yaml
# 使用 KubeFed 管理多叢集
apiVersion: core.kubefed.io/v1beta1
kind: KubeFedConfig
metadata:
  name: kubefed
spec:
  scope: Namespaced
```

## 結論

邊緣運算和混合雲是雲端運算的自然延伸。評估業務需求，選擇適合的架構模式。