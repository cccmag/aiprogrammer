# 主題總覽：Python 生態系 2020 年初

Python 是 AI 與資料科學領域的主流語言，其豐富的生態系是最大優勢。然而，面對這麼多工具與版本選擇，初學者往往無所適從。本期的主題就是幫助讀者建立對 Python 生態系的系統性理解，從而能夠自信地建置、管理與維護 Python 開發環境。

## 為什麼要關注 Python 環境管理？

在 2020 年初的 Python 生態系中，版本與套件管理的複雜度是新手面臨的首要挑戰。舉例來說，一個專案可能需要 Python 3.7、NumPy 1.17 與 TensorFlow 2.0，另一個專案可能需要 Python 3.8、NumPy 1.18 與 PyTorch 1.4。若沒有適當的環境隔離，這些相依衝突會讓開發體驗變成一場噩夢。

## 核心工具鏈

### 1. Python 版本管理
pyenv 讓開發者可以在同一台機器上安裝與切換多個 Python 版本。結合 pyenv-virtualenv 或 pyenv-conda，可以同時管理 Python 版本與虛擬環境。

### 2. 虛擬環境
venv 是 Python 3.3 內建的標準庫，virtualenv 則提供了更強大的功能。conda 不仅是虛擬環境管理工具，也是跨語言的套件管理器，對科學計算族群特別友善。

### 3. 套件管理
pip 是 Python 官方的套件管理器，2020 年初 pip 20.0 带来了諸多改進。poetry 與 pipenv 則代表了新一代的封裝與依賴管理方式。

### 4. 依賴鎖定
requirements.txt 是最廣泛使用的依賴清單格式，但其缺乏版本鎖定機制。pip-tools、poetry.lock、conda env export 提供了更穩定的環境重現能力。

## 學習路徑

建議依序閱讀 focus1 到 focus7 了解 Python 生態系的核心概念，再透過 article1 到 article10 深入實作細節。每篇文章都包含可直接執行的程式碼範例。

## 本期結構

- focus1–7：主題深入探討，涵蓋 Python 環境的各個面向
- article1–5：Python 3.8 特性與基礎環境建置
- article6–10：現代套件管理工具與 CI/CD 整合
- _code/python_env.py：Python 環境檢測腳本

## 參考資源

- https://www.google.com/search?q=Python+ecosystem+2020+virtualenv+pip+conda+Poetry+guide
- https://www.google.com/search?q=Python+3.8+new+features+walrus+operator+positional+only+parameters
- https://www.google.com/search?q=Python+dependency+management+2020+pyproject.toml+Poetry+Pipenv