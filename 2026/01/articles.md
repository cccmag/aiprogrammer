# 文章索引

## 程式開發實戰 (article1–5)

這五篇文章專注於 Python 開發環境的基礎建置與 GPU 加速設定。

| # | 主題 | 說明 |
|---|------|------|
| 1 | [pyenv 與 virtualenv](article1.md) | Python 版本管理與虛擬環境的實戰搭配，包含 pyenv 安裝、版本切換與虛擬環境建立 |
| 2 | [pip 進階使用](article2.md) | 依賴鎖定、離線安裝、私有套件源與 pip-tools 進階技巧 |
| 3 | [Conda 環境管理](article3.md) | 跨語言套件管理、環境匯出與重現、conda 與 pip 的混合使用策略 |
| 4 | [NVIDIA 驅動與 CUDA 安裝](article4.md) | 從顯示驅動安裝到 CUDA 工具包與 cuDNN 的完整流程 |
| 5 | [PyTorch GPU 驗證](article5.md) | 多種方法確認 GPU 加速正常運作，含效能基準測試 |

## AI 應用實戰 (article6–10)

這五篇文章涵蓋容器化、遠端開發與完整專案範本。

| # | 主題 | 說明 |
|---|------|------|
| 6 | [Docker 基本指令](article6.md) | 映像管理、容器操作、GPU 傳遞與資料掛載 |
| 7 | [Dockerfile 撰寫指南](article7.md) | 多階段建置、Docker 快取最佳化與最佳實踐 |
| 8 | [docker-compose 多容器](article8.md) | 多服務協作、資料持久化與 GPU 資源配置 |
| 9 | [VS Code 遠端開發](article9.md) | Remote SSH、Dev Containers 與遠端 Jupyter 整合 |
| 10 | [完整 AI 專案範本](article10.md) | 從目錄結構到自動化建置的完整實例 |

## 閱讀建議

初學者建議從 article1 開始依序閱讀。已有基礎的讀者可直接跳到感興趣的主題。所有程式碼範例皆可在 `_code/` 目錄中找到對應的實作。

本期也提供了整合環境檢測腳本 `_code/ai_env.py`，可在完成環境建置後執行，一鍵確認所有元件是否正常運作。
