# 主題總覽：容器化與 Docker

容器化技術徹底改变了應用程式的開發、測試、部署流程。傳統的虛擬機器技術虽然成熟，但启动速度慢、資源佔用大的問題在 DevOps 追求快速迭代的環境中显得格格不入。Docker 作為容器技術的代表作，以其輕量、快速、可移植的特性，成為現代軟體交付的標準工具。

## Docker 的核心價值

**環境一致性**：開發者在本地環境建置的容器，可以無差異地部署到測試環境、生產環境、甚至其他雲端平台。這解決了經典的「在我的機器上可以執行」的問題。

**資源效率**：容器共享主機的作業系統核心，不需要像虛擬機器那樣執行完整的作業系統。根據工作負載的特性，容器密度可以達到 VM 的 5 到 10 倍。

**快速啟動**：容器可以在數秒內啟動，適合需要快速橫向擴展的場景。搭配負載平衡器與編排工具，可實現真正的弹性運算。

**版本控制**：每個 Docker 映象都是不可變的層級結構，可以像 Git 一樣追蹤變更、版本化、回滾。

## Docker 生態系

Docker 不是單一工具，而是一個完整的生態系：

**Docker Engine**：核心的容器執行環境，負責建立與執行容器。

**Docker Hub / Docker Store**：公有映象暫存器，數十萬個預先建置的映象可供使用。

**Docker Compose**：定義與執行多容器應用程式的工具，透過 YAML 設定檔聲明服務、網路、磁碟區。

**Docker Swarm**：原生的容器編排工具，在 Docker 1.12 中整合為 Swarm Mode。

**Docker Machine**：在多個平台上自動配置 Docker 主機的工具。

## 學習路徑

建議從 focus1 了解 Docker 生態系的基本構成，接著透過 focus2 深入了解 Docker 1.10 的新功能與 Swarm Mode。focus3 到 focus5 涵蓋映象管理、網路、資料管理等實務主題，focus6 與 focus7 則進入容器編排與安全的進階領域。

## 參考資源

- https://www.google.com/search?q=Docker+容器化+基本概念+優勢+生態系+介紹+2016
- https://www.google.com/search?q=Docker+Engine+Dockerfile+Docker+Hub+Compose+Swarm+工具鏈
- https://www.google.com/search?q=容器化+vs+虛擬機+比較+差異+優勢+資源效率+啟動速度