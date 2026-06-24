# 本期焦點

## DevOps 與自動化部署

### 引言

DevOps 不僅是工具鏈的集合，更是一種文化與實踐的轉變。它打破了開發（Dev）與維運（Ops）之間的壁壘，通過自動化流程、持續整合與持續交付，讓軟體從開發到上線的過程更加快速且可靠。

本期將從七個面向深入探討 DevOps 與自動化部署：

- **文化與實踐**：DevOps 的核心理念與組織變革
- **容器化**：Docker 作爲現代部署的基石
- **多容器編排**：Docker Compose 管理複雜服務
- **CI/CD 管線**：自動化構建、測試與部署
- **GitHub Actions**：實戰自動化工作流程
- **監控與日誌**：系統的可觀測性
- **IaC**：基礎設施即程式碼的宣言

---

## 大綱

- [程式：devops_demo.js — DevOps 自動化流程模擬](focus_code.md)
   - 模擬 Docker 構建流程
   - CI 管線階段模擬
   - 部署策略演示

1. [DevOps 文化與實踐](focus1.md)
   - 三大支柱：文化、自動化、度量
   - CALMS 框架
   - 傳統維運的困境

2. [Docker 容器化](focus2.md)
   - 映像、容器、倉庫
   - Dockerfile 最佳實踐
   - 多階段構建

3. [Docker Compose 多容器](focus3.md)
   - 服務定義與編排
   - 網路與卷管理
   - 環境變數與配置

4. [CI/CD 管線設計](focus4.md)
   - 持續整合 vs 持續交付
   - 管線階段劃分
   - 品質閘道

5. [GitHub Actions 實戰](focus5.md)
   - 工作流語法
   - 矩陣構建
   - 自訂 Action

6. [監控與日誌管理](focus6.md)
   - 可觀測性三大支柱
   - Prometheus + Grafana
   - ELK 日誌堆疊

7. [基礎設施即程式碼](focus7.md)
   - Terraform 核心概念
   - 聲明式 vs 命令式
   - 狀態管理

---

## DevOps 工具鏈全景

```
開發 → 構建 → 測試 → 部署 → 監控
 │       │       │       │       │
 Git    Docker  CI/CD   K8s     Prometheus
 │       │       │       │       │
PR     Docker  GitHub  Docker  Grafana
Review  Compose Actions Compose  ELK
```

## 濃縮回顧

### 從傳統維運到 DevOps

傳統軟體開發中，開發團隊寫完程式後將程式碼「丟過牆」給維運團隊部署。這種模式導致了溝通成本高、部署頻率低、問題定位慢等問題。

DevOps 的核心思想是讓開發和維運團隊緊密協作，通過自動化工具鏈消除手動操作。這不僅加快了交付速度，也提高了系統的穩定性。

### DevOps 的關鍵原則

1. **自動化一切**：重複性工作都應自動化
2. **持續反饋**：快速獲得程式碼品質和系統狀態的反饋
3. **共享責任**：開發者也應關心部署和運維
4. **基礎設施即程式碼**：用程式碼管理基礎設施
5. **不可變基礎設施**：伺服器創建後不修改，直接替換

### 容器化帶來的變革

Docker 容器化是 DevOps 實踐中的關鍵技術。容器提供了輕量級、一致的執行環境，解決了「在我機器上可以運行」的經典問題。

| 面向 | 傳統方式 | 容器化 |
|------|---------|--------|
| 環境一致性 | ❌ 環境差異 | ✅ 一致環境 |
| 啟動速度 | 分鐘級 | 秒級 |
| 資源開銷 | 高（VM） | 低（容器） |
| 部署單元 | 程式碼 + 配置 | 映像 |

---

**下一步**：[程式實作](focus_code.md) → [DevOps 文化與實踐](focus1.md)

## 延伸閱讀

- [DevOps 官方指南](https://www.google.com/search?q=DevOps+guide+2024)
- [Docker 文件](https://www.google.com/search?q=Docker+documentation)
- [GitHub Actions 文件](https://www.google.com/search?q=GitHub+Actions+documentation)
