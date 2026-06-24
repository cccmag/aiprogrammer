# 7. AI 專案目錄結構

## 標準專案配置

一個良好的 AI 專案目錄結構能提升團隊協作效率與程式碼可維護性。以下是參考知名專案 cookiecutter-data-science 與實際經驗總結的推薦配置：

```
project/
├── data/                    # 資料集（加入 .gitignore）
│   ├── raw/                 # 原始資料，唯讀
│   ├── processed/           # 預處理後的資料
│   └── external/            # 外部資料來源
├── notebooks/               # Jupyter Notebooks 探索與原型
│   ├── 01-eda.ipynb         # 探索性資料分析
│   └── 02-model-prototype.ipynb
├── src/                     # 可重複使用的原始碼
│   ├── data/                # 資料下載與預處理
│   ├── features/            # 特徵工程
│   ├── models/              # 模型定義
│   └── visualization/       # 可視化函式
├── tests/                   # 單元測試
│   └── test_model.py
├── configs/                 # 設定檔
│   └── config.yaml
├── docker/                  # Docker 相關檔案
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/                 # 輔助腳本
│   └── setup.sh
├── requirements.txt         # pip 依賴
├── environment.yml          # conda 環境設定
├── setup.py                 # 套件安裝
├── .gitignore
└── README.md
```

## 設定管理

使用 YAML 設定檔管理超參數與路徑，避免將設定寫死在程式碼中：

```python
import yaml
from pathlib import Path

with open("configs/config.yaml") as f:
    config = yaml.safe_load(f)

data_dir = Path(config["paths"]["data_dir"])
batch_size = config["training"]["batch_size"]
learning_rate = config["training"]["learning_rate"]
```

## 版本控制注意事項

- 虛擬環境目錄（`.venv/`, `env/`）加入 `.gitignore`
- 資料集不提交到 Git（使用 DVC 管理）
- 模型檢查點（`.ckpt`, `.pth`）不提交
- 記錄實驗的目錄（`logs/`, `runs/`）不提交

## 參考資源

- https://www.google.com/search?q=cookiecutter+data+science+project+template+structure
- https://www.google.com/search?q=AI+machine+learning+project+directory+organization+best+practices
- https://www.google.com/search?q=Python+AI+project+gitignore+data+management
