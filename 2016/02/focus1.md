# 1. Docker 生態系概述

## Docker 簡史

Docker 由 dotCloud 公司在 2013 年開源。dotCloud 成立於 2010 年，原本是一家平台即服務（PaaS）供應商，在營運過程中累積了豐富的容器技術經驗。2013 年他們決定將內部的容器技術開源，這就是 Docker 的誕生。隨後 dotCloud 更名為 Docker Inc.，專注於 Docker 產品與生態系的發展。

## Docker 的三大核心概念

**映象（Image）**：唯讀的模板，包含了執行應用程式所需的作業系統、函式庫、程式碼、依賴。映象是分層的，每一層代表 Dockerfile 中的一個指令。

**容器（Container）**：映象的執行實例。可以把容器想像成一個執行中的程序，加上自己的檔案系統、網路、程序空間。容器是隔離的，但可以通過設定與主機或網路互通。

**暫存器（Registry）**：儲存與分發映象的服務。Docker Hub 是最大的公有暫存器。企業通常會架設私有暫存器來存放內部應用程式映象。

## Docker Engine 架構

Docker Engine 採用客戶端-伺服器架構：

**Docker Daemon（dockerd）**：背景服務程序，負責管理映象、容器、網路、磁碟區等物件。

**Docker Client（docker）**：命令列工具，與 Daemon 溝通的客戶端。

**REST API**：Daemon 暴露的程式化介面，客戶端與其他工具透過 REST API 與 Daemon 溝通。

```
Client (docker CLI) <---> REST API <---> Daemon (dockerd)
                                         |
                                    Containerd
                                         |
                                      runc
```

## 主要元件

**containerd**：容器執行時管理工具，負責容器的生命週期管理（啟動、停止、暫停、刪除）。

**runc**：OCI 規範的參考實作，負責真正建立與執行容器。

**Dockerfile**：文字格式的指令檔案，定義如何從一個基礎映象逐步建置出應用程式映象。

## Docker 的應用場景

**開發環境**：開發團隊可以透過 Dockerfile 定義一致的開發環境，新成員只需執行 `docker-compose up` 就能立即開始工作。

**測試與 CI/CD**：自動化測試環境可快速建置與銷毀，確保每次測試都在乾淨的環境中執行。

**部署與擴展**：容器化的應用程式可以在任何支援 Docker 的環境中執行，實現真正的「建置一次，處處執行」。

**微服務架構**：每個微服務包裝成獨立的容器，獨立部署與擴展，是目前最流行的容器使用模式。

## 參考資源

- https://www.google.com/search?q=Docker+歷史+起源+dotCloud+2013+發展+生態系
- https://www.google.com/search?q=Docker+Engine+架構+Daemon+Client+containerd+runc+OCI
- https://www.google.com/search?q=Docker+映象+容器+暫存器+核心概念+運作原理