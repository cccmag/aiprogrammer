# 程式碼說明 — 環境檢測腳本

## 功能概述

`_code/ai_env.py` 是一個單一檔案的全方位環境檢測腳本，幫助開發者在設定完開發環境後快速確認各項元件的狀態。腳本不需要任何第三方套件，僅使用 Python 標準函式庫即可執行，在任何 Python 環境中都能直接使用。

## demo() 函數說明

`demo()` 函數依序執行以下四個檢測項目：

### 1. Python 版本檢查
確認當前 Python 直譯器的版本（例如 3.10.12）、實作方式（CPython、PyPy 等）以及系統架構（x86_64、arm64）。這對於確認套件相容性非常重要，例如某些套件在 arm64 架構（如 Apple Silicon）上需要使用特定版本。

### 2. 虛擬環境資訊
透過比較 `sys.prefix` 與 `sys.base_prefix` 來判斷是否在虛擬環境中執行。顯示虛擬環境的路徑，方便確認使用的是否為正確的環境，避免意外安裝到全域 Python。

### 3. GPU / CUDA 檢查
使用 `subprocess` 呼叫 `nvidia-smi` 來檢測 NVIDIA GPU 型號與驅動版本。若 `nvcc` 可用則一併顯示 CUDA 工具包版本。若 `nvidia-smi` 無法執行（例如沒有 NVIDIA GPU 或驅動未安裝），腳本會優雅地處理錯誤並顯示明確的提示訊息。

### 4. Docker 資訊
檢查 Docker 是否安裝及運行中，並統計目前運行中的容器數量。這有助於確認 Docker 服務狀態是否正常。

## 執行方式

```bash
cd _code
python3 ai_env.py
```

或使用測試腳本：

```bash
cd _code
bash test.sh
```

## 輸出範例

在完整的 GPU 環境中，輸出類似：

```
========================================================
AI 開發環境檢測工具
========================================================

[1] Python 版本
    Python 3.10.12
    實作: CPython
    架構: x86_64

[2] 虛擬環境
    狀態: 啟用中
    路徑: /home/user/project/.venv

[3] GPU / CUDA
    GPU: NVIDIA RTX 4090, 560.94
    CUDA: release 12.6

[4] Docker
    Docker: Docker version 27.0.3
    運行中容器: 2

========================================================
檢測完成
========================================================
```

## 參考資源

- https://www.google.com/search?q=Python+check+CUDA+GPU+availability+nvidia-smi+subprocess+script
- https://www.google.com/search?q=Python+subprocess+check+Docker+installed+running+version
- https://www.google.com/search?q=Python+sys+prefix+base+prefix+virtual+environment+detection+method
