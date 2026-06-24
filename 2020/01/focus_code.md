# 程式碼說明 — Python 環境檢測腳本

## 功能概述

`_code/python_env.py` 是一個單一檔案的 Python 環境檢測腳本，幫助開發者快速確認 Python 環境的狀態。腳本不需要任何第三方套件，僅使用 Python 標準函式庫即可執行。

## demo() 函數說明

`demo()` 函數依序執行以下四個檢測項目：

### 1. Python 版本檢查
確認當前 Python 直譯器的版本（例如 3.8.1）、實作方式（CPython、PyPy 等）以及作業系統平台。這對於確認套件相容性非常重要，例如某些套件在 macOS 上需要特別設定。

### 2. 虛擬環境檢測
透過比較 `sys.prefix` 與 `sys.base_prefix` 來判斷是否在虛擬環境中執行。若兩者相同，表示在全域 Python 中執行；若不同，則表示已啟動虛擬環境。

### 3. 已安裝熱門套件檢查
嘗試匯入幾個常見的資料科學套件（NumPy、Pandas、Matplotlib、Requests），並顯示其版本資訊。這可以快速確認科學計算生態系是否完整安裝。

### 4. pip 與套件管理器資訊
顯示 pip 版本與已安裝套件數量，幫助確認套件管理的狀態。

## 執行方式

```bash
cd _code
python3 python_env.py
```

或使用測試腳本：

```bash
cd _code
bash test.sh
```

## 輸出範例

```
============================================================
Python 環境檢測工具
============================================================

[1] Python 版本
    Python 3.8.1
    實作: CPython
    平台: macOS-10.15.7-x86_64

[2] 虛擬環境
    狀態: 啟用中
    路徑: /Users/user/project/.venv

[3] 熱門套件
    NumPy: 1.18.1
    Pandas: 1.0.3
    Matplotlib: 3.1.3
    Requests: 未安裝

[4] pip 管理
    pip 20.0.1
    已安裝套件: 47

============================================================
檢測完成
============================================================
```

## 參考資源

- https://www.google.com/search?q=Python+check+environment+information+sys.prefix+platform+script
- https://www.google.com/search?q=Python+check+installed+packages+version+import+demo