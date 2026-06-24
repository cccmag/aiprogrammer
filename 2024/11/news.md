# 本月新知

## 2024 年 11 月 DevOps 與自動化技術動態

### Docker 與容器技術

**Docker 25 發布：效能大幅提升**

Docker 於 2024 年 10 月發布 25 版，帶來多項重大改進。新版本採用改良後的儲存驅動程式，映像構建速度提升 40%，啟動時間縮短 30%。Docker Compose v3 正式支援 GPU 資源分配，讓 AI/ML 工作負載的容器化部署更加順暢。

**containerd 2.0 成爲行業標準**

CNCF 的 containerd 專案發布 2.0 版，成爲 Kubernetes 容器運行時的預設選擇。新版本引入了簡化的命名空間管理和增強的映像拉取效能，並完全棄用了舊版的 Docker Shim。

### CI/CD 與 DevOps 工具

**GitHub Actions 工作流程快取改進**

GitHub 宣布 Actions 的快取機制大幅改進，支援跨分支快取共享和精細化的快取金鑰策略。這對於具有大型依賴項的專案顯著減少了 CI 執行時間。同時，GitHub 推出了 Actions 工作流程的 AI 輔助除錯功能。

**GitLab 16.8：整合的 DevOps 平台**

GitLab 16.8 發布，強化了其 DevOps 平台的整合能力。新功能包括與 Kubernetes 的深度整合、內建的基礎設施即程式碼（IaC）掃描器，以及 AI 生成的管線配置建議。

**Jenkins 社群推出現代化 UI**

老牌 CI/CD 工具 Jenkins 發布了基於 React 重新設計的現代化 UI，同時保留了對既有外掛的完整相容性。新 UI 支援暗色模式、更直觀的管線視覺化。

### 監控與可觀測性

**OpenTelemetry 成爲 CNCF 畢業專案**

OpenTelemetry 正式從 CNCF 孵化器畢業，成爲監控和可觀測性的事實標準。多數主流廠商（Datadog、New Relic、Grafana）已全面支援 OTLP 協定。

**Grafana 11：整合的觀測平台**

Grafana 11 發布，整合了 Prometheus、Loki 和 Tempo 為單一觀測平台。新的「Explore 2.0」介面讓開發者可以同時査看指標、日誌和追蹤數據。

### 基礎設施即程式碼

**Terraform 1.8 支援 provider-defined 函式**

HashiCorp Terraform 1.8 發布，引入了 provider-defined 函式功能，讓 provider 開發者可以定義可在 HCL 中直接呼叫的函式。同時 Terraform 加強了模組版本管理。

**Pulumi 推出 AI 輔助基礎設施生成**

Pulumi 發布了 Copilot 功能，使用 AI 將自然語言描述轉換爲基礎設施程式碼。開發者可以用「建立一個三節點的 Kubernetes 叢集」這樣的描述生成完整的 Pulumi 程式。

### AI 與 DevOps 的融合

**AI 輔助部署分析**

多家廠商推出了 AI 輔助的部署分析工具，可以自動檢測部署異常、預測潛在的服務中斷，並提供回滾建議。這些工具基於歷史部署數據訓練，能發現人眼難以察覺的模式。

**LLM 自動生成 Dockerfile 和 CI 配置**

新的 AI 工具可以根據專案描述自動生成 Dockerfile 和 CI/CD 配置檔案。OpenAI 的 Codex CLI 和 GitHub Copilot 都新增了「生成 Dockerfile」的功能。

### 業界動態

- **AWS 宣布 ECS 全面支援 Fargate 無伺服器容器**：不再需要管理底層伺服器
- **Kubernetes 1.31 發布**：Sidecar 容器正式穩定，改善了服務網格部署體驗
- **HashiCorp 被 IBM 收購**：Terraform 和 Vault 的未來發展引起社群關注
- **Systemd 整合容器管理**：Systemd 新增對 Docker 和 podman 容器的原生管理功能
