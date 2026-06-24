# 3. 套件管理 pip 與 conda

## pip — Python 官方套件管理工具

pip 是 Python 官方推薦的套件管理器，從 PyPI 下載並安裝套件。PyPI 擁有超過 45 萬個套件，涵蓋從網頁開發到科學計算的各個領域，是 Python 生態系的核心組成部分。

```bash
# 安裝套件
pip install numpy pandas torch

# 指定版本
pip install torch==2.1.0

# 安裝特定範圍版本
pip install "torch>=2.0,<2.2"

# 從 requirements.txt 安裝
pip install -r requirements.txt

# 匯出目前環境的套件清單
pip freeze > requirements.txt
```

pip 的缺點是沒有內建的環境管理功能，需要搭配 venv 或 virtualenv 使用。此外，對於非 Python 的原生函式庫（如 CUDA 工具包）無法直接管理，這在 AI 開發中是一個明顯的限制。

## conda — 跨語言套件管理器

conda 是 Anaconda 發行的套件與環境管理工具，不僅管理 Python 套件，還能管理 R、C++ 等語言的套件，以及 CUDA、cuDNN 等系統層級的二進位檔案。這使得 conda 在 AI 領域特別受歡迎，因為它可以一次處理 Python 與 CUDA 的版本相依性，大幅降低環境建置的難度。

```bash
# 建立環境
conda create -n tf_env python=3.10

# 啟動環境
conda activate tf_env

# 安裝套件（從特定頻道）
conda install pytorch torchvision cudatoolkit -c pytorch

# 匯出環境
conda env export > environment.yml

# 從檔案重建
conda env create -f environment.yml
```

## pip vs conda 選擇指南

| 需求 | 建議 |
|------|------|
| 一般 Python 開發 | pip + venv |
| AI / 資料科學 | conda |
| 純 Python 套件 | pip |
| 需二進位相依套件（CUDA 等） | conda |
| 精確鎖定版本 | pip + pip-tools |

## 注意事項

避免在 conda 環境中頻繁使用 pip 安裝大量套件，可能導致依賴衝突。建議優先使用 conda，conda 沒有的套件再用 pip。

## 參考資源

- https://www.google.com/search?q=pip+vs+conda+Python+package+manager+difference+comparison
- https://www.google.com/search?q=conda+environment+management+tutorial+data+science+AI
- https://www.google.com/search?q=pip+install+advanced+options+requirements+file+freeze
