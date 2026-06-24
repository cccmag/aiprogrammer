# 程式碼說明 — focus_code.md

## 概述

本期範例程式碼位於 `_code/cloud.py`，展示雲端原生架構的核心概念和模擬實現。涵蓋容器編排、服務發現、負載平衡等核心概念的教學實現。程式碼使用純 Python，幫助讀者建立雲端原生架構的直覺。

## 元件說明

### `Container`

模擬 Docker 容器的概念，包含映像檔、狀態和資源限制。每個容器代表一個隔離的執行環境。

### `Service`

實現 Kubernetes Service 的核心思想：為 Pod 提供穩定的網路端點和負載平衡。自動追蹤healthy的容器實例。

### `ServiceDiscovery`

DNS 风格的服務發現機制，允許服務通過名稱找到彼此。這是微服務架構的基礎設施。

### `LoadBalancer`

實現基本的負載平衡演算法（Round Robin）。將客戶端請求分發到多個容器實例，確保資源合理利用。

### `SimpleOrchestrator`

模擬簡化的容器編排器，負責調度容器到可用的「節點」。展示編排系統的基本運作原理。

## 執行程式

```bash
cd _code
bash test.sh
```

`test.sh` 使用 `set -x` 顯示執行過程並呼叫 `python3 cloud.py`。`demo()` 函式展示完整流程：創建容器、編排部署、服務發現、負載平衡，驗證雲端原生概念的正確運作。

## 參考資源

- Kubernetes 官方文件：https://www.google.com/search?q=Kubernetes+documentation
- Docker 官方文件：https://www.google.com/search?q=Docker+documentation
- Cloud Native Computing Foundation：https://www.google.com/search?q=CNCF+cloud+native