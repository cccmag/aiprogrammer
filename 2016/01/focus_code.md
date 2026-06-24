# 程式碼說明 — 雲端環境檢測腳本

## 功能概述

`_code/cloud_check.py` 是一個跨平台的雲端環境檢測腳本，協助使用者快速確認雲端 CLI 工具的安裝狀態與設定。本腳本不需要任何第三方套件，僅使用 Python 標準函式庫。

## 功能模組說明

### 1. AWS CLI 檢測

透過 `aws --version` 指令確認 AWS CLI 是否已安裝，並檢查 `AWS_ACCESS_KEY_ID` 與 `AWS_SECRET_ACCESS_KEY` 環境變數是否已設定。環境變數存在但值為空字串可能是設定不完整的徵兆。

### 2. GCP CLI 檢測

透過 `gcloud --version` 確認 Google Cloud SDK 是否已安裝。檢查 `GOOGLE_APPLICATION_CREDENTIALS` 環境變數指向的服務帳號金鑰檔案是否存在。

### 3. Azure CLI 檢測

透過 `azure --version`（傳統 CLI）或 `az --version`（新 CLI）確認 Azure CLI 是否已安裝。檢查登入狀態。

### 4. Terraform 檢測

透過 `terraform --version` 確認基礎設施即程式碼工具是否可用。

## 執行方式

```bash
cd _code
python3 cloud_check.py
```

## 輸出範例

```
====================================================
雲端環境檢測工具
====================================================

[1] AWS CLI
    狀態: 已安裝
    版本: aws-cli/1.10.12 Python/3.5.1 linux/4.4.0
    憑證: 已設定

[2] Google Cloud SDK
    狀態: 未安裝

[3] Azure CLI
    狀態: 已安裝
    版本: azure-cli (0.10.4)

[4] Terraform
    狀態: 已安裝
    版本: Terraform v0.7.0

====================================================
檢測完成
====================================================
```

## 自行擴展

本腳本架構簡單，可輕易擴展加入其他雲端平台的檢測邏輯，例如 DigitalOcean、Heroku 等。建議在新增檢測模組時，遵循現有的函式命名與回傳格式保持一致性。

## 參考資源

- https://www.google.com/search?q=AWS+CLI+install+configuration+check+Python+script
- https://www.google.com/search?q=GCP+Google+Cloud+SDK+authentication+service+account+check
- https://www.google.com/search?q=Terraform+infrastructure+as+code+check+installed+version