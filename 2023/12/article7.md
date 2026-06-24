# 雲端原生技術演變

## Kubernetes 與雲端基礎設施的發展趨勢

2023 年，雲端原生技術進入了「後 Kubernetes」時代。Kubernetes 本身已成為基礎設施中的標準層，創新的重心轉向更上層的應用和更下層的硬體。邊緣運算、eBPF、WebAssembly 和平台工程成為今年的主題。

---

## Kubernetes 進入成熟期

### 版本更新

Kubernetes 在 2023 年發布了三個版本，每一版都在穩定性、安全性和可擴展性方面有所提升：

**Kubernetes 1.27（4 月）**：
- StatefulSet 的 `maxUnavailable` 功能 GA（穩定）
- `ReadWriteOncePod` 訪問模式 GA
- Container checkpointing 功能引入（用於除錯）

**Kubernetes 1.28（8 月）**：
- 混合叢集 API 引入
- Sidecar 容器改進
- 節點穩定性改進

**Kubernetes 1.29（12 月）**：
- 新的讀寫 API
- 遺留元件清理
- 叢集策略 API 的更新

### 營運成熟度

2023 年，Kubernetes 的營運工具和實踐變得更加成熟：

**Cilium 成為主流**：
- Cilium 基於 eBPF 的網路和安全解決方案在 2023 年獲得廣泛採用
- Cilium Service Mesh 模式挑戰 Istio
- Hubble 提供細粒度的網路可觀測性

**Gateway API**：
- Gateway API 在 2023 年達到 GA
- 取代 Ingress 成為 Kubernetes 的新標準 API
- 支援 HTTP、TCP、TLS、gRPC 等多種協議

**Cluster API**：
- 用宣告式 API 管理 Kubernetes 叢集的生命週期
- 支援 AWS、Azure、GCP、vSphere 等多種基礎設施

---

## eBPF 的崛起

### 什麼是 eBPF？

eBPF（extended Berkeley Packet Filter）是一項革命性的核心技術，允許使用者在 Linux 核心中安全地執行沙箱程式：

- **無需修改核心**：動態載入和卸載 eBPF 程式
- **高效能**：編譯為原生機器碼
- **安全性**：在執行前進行靜態驗證

### 2023 年 eBPF 生態

**Cilium**：
- 成為 Kubernetes 網路的事實標準
- Cilium Mesh 提供完整的服務網格功能
- Cilium Tetragon 提供執行時安全

**Falco**：
- Falco 成為 CNCF 畢業專案
- 使用 eBPF 進行核心級安全監控

**Pixie**：
- 基於 eBPF 的 Kubernetes 除錯工具
- 提供無侵入的應用監控

---

## 平台工程的興起

### 從 DevOps 到平台工程

2023 年，「平台工程」成為雲端原生領域的熱門話題。核心思想是建立一個內部開發者平台（Internal Developer Platform，IDP），抽象基礎設施的複雜性：

**為什麼需要平台工程？**
- Kubernetes 的複雜性讓普通開發者難以直接使用
- 組織需要標準化部署、監控和安全規範
- 開發者希望專注於業務邏輯而非基礎設施

### 關鍵工具

**Backstage**：
- Spotify 開源的開發者入口平台
- 2023 年成為 CNCF 孵化專案
- 整合服務目錄、文件、CI/CD

**Crossplane**：
- 基於 Kubernetes 的控制平面框架
- 將雲端資源（資料庫、佇列、儲存）管理為 Kubernetes 資源
- 支援 AWS、Azure、GCP、Upbound

**Port**、**Humanitec**、**Qovery**：新興的 IDP 平台

---

## 邊緣運算與雲端原生的融合

### 邊緣 Kubernetes

2023 年，K3s 和 MicroK8s 等輕量級 Kubernetes 發行版在邊緣運算中獲得了更多採用：

**K3s**：
- Rancher 的輕量級 Kubernetes 發行版
- 適合 IoT 和邊緣裝置
- 單一二進位檔，記憶體佔用 < 512MB

**MicroK8s**：
- Canonical 的 Kubernetes（適合邊緣和開發）
- 支援 Snap 安裝
- 最新的 1.29 版本更新

**OpenYurt**：
- 阿里巴巴開源的邊緣 Kubernetes 擴展
- 支援離線操作、邊緣節點管理

### WASM 在邊緣

WebAssembly 在 2023 年成為邊緣運算的熱門技術選擇：
- **Fermyon Spin**：WASM 微服務框架
- **Cloudflare Workers**：WASM 函數計算
- **Suborbital**：WASM 插件系統

---

## 可觀測性

### OpenTelemetry 成為標準

2023 年，OpenTelemetry 在可觀測性領域確立了主導地位：

- **Logs、Metrics、Traces 三合一**：統一的數據收集標準
- **CNCF 畢業**：2023 年從孵化階段畢業
- **廣泛採用**：AWS、Azure、GCP 都提供了原生的 OpenTelemetry 支援

### 新興工具

**Grafana Loki**：日誌聚合系統，與 Prometheus 和 Tempo 深度整合。

**Grafana Mimir**：Prometheus 的長期儲存解決方案，支援橫向擴展。

**Honeycomb**：事件驅動的可觀測性平台，支援高基數資料分析。

**SigNoz**：開源的應用性能監控平台，OpenTelemetry 原生。

---

## 成本管理

### FinOps 的普及

2023 年，雲端成本管理成為重要議題：

- **Kubecost**：Kubernetes 成本管理工具
- **VPA（Vertical Pod Autoscaler）**：自動調整 Pod 資源請求
- **Karpenter**：AWS 的節點自動擴展器，優化成本
- **Spot Instances**：使用競價實例降低運算成本

### 成本優化策略

- **Graviton（ARM）實例**：AWS Graviton 處理器比 x86 便宜 20-40%
- **保留實例與儲蓄計劃**：長期承諾換取折扣
- **自動縮放**：根據負載自動調整資源

---

## 2024 年展望

- **Kubernetes 簡化**：更多抽象層降低使用門檻
- **eBPF 擴展**：在安全、網路、儲存方面的更多應用
- **AI 與雲端原生融合**：Kubernetes 成為 AI 訓練和推理的標準平台
- **邊緣運算成熟**：更多的邊緣部署場景
- **平台工程工具標準化**

---

## 延伸閱讀

- [Kubernetes 2023 年終總結](https://www.google.com/search?q=Kubernetes+2023+year+review)
- [eBPF 2023 生態回顧](https://www.google.com/search?q=eBPF+2023+ecosystem+overview)
- [平台工程趨勢](https://www.google.com/search?q=platform+engineering+2023+trends)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」文章系列之七。*
