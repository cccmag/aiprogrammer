# 文章索引

## 容器化實戰（article1–5）

這五篇文章專注於 Docker 的進階應用，包括 Docker Compose、私有暫存器、網路驅動、資料磁碟區、以及資源監控。

| # | 主題 | 說明 |
|---|------|------|
| 1 | [Docker Compose 多容器應用](article1.md) | 使用 YAML 定義多容器應用，一鍵啟動完整開發環境 |
| 2 | [登錄與私有暫存器](article2.md) | Docker Hub 設定、私有暫存器架設、映象發布流程 |
| 3 | [網路驅動與 CNM](article3.md) | 深入了解 bridge、host、overlay、macvlan 網路驅動 |
| 4 | [磁碟區與資料持久化](article4.md) | Named Volume、Bind Mount、tmpfs 與資料備份還原 |
| 5 | [資源限制與監控](article5.md) | CPU、記憶體限制、容器監控工具與警示設定 |

## 進階應用實戰（article6–10）

這五篇文章涵蓋 CI/CD 整合、跨主機網路、資料庫容器化、日誌管理、進入點腳本。

| # | 主題 | 說明 |
|---|------|------|
| 6 | [CI/CD 整合 Docker](article6.md) | Jenkins、Travis CI 與 Docker 的整合流程 |
| 7 | [跨主機網路 overlay](article7.md) | Overlay 網路原理、Swarm 模式下的網路設定 |
| 8 | [容器化資料庫應用](article8.md) | PostgreSQL、MySQL、MongoDB 的容器化部署與資料持久化 |
| 9 | [日誌管理與驅動](article9.md) | 集中式日誌收集、ELK Stack 整合、日誌驅動設定 |
| 10 | [進入點腳本實作](article10.md) | ENTRYPOINT 與 CMD 的差異、進入點腳本範例 |

## 閱讀建議

初學者建議從 article1 開始了解 Docker Compose，這是管理多容器應用的最佳工具。已有基礎的讀者可直接跳到感興趣的主題深入閱讀。

本期提供的 `_code/docker_manage.py` 腳本可用於日常的容器管理操作。