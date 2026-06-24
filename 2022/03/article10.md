# 資料科學專案結構

## 混亂是生產力的殺手

每一位資料科學家都曾經歷過這樣的場景：專案開始時只有一個 Jupyter Notebook，幾個月後 Notebook 已經有上千個儲存格，變數命名混亂，沒有人能重現結果。本文介紹如何建立一個可維護、可重現的資料科學專案。

## 專案目錄結構

一個良好組織的資料科學專案應遵循以下結構：

```
project_name/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── data/
│   ├── raw/           # 原始資料（不可修改）
│   ├── processed/     # 處理後的資料
│   └── external/      # 外部資料
├── notebooks/         # Jupyter notebooks
│   ├── 01-exploration.ipynb
│   ├── 02-feature-engineering.ipynb
│   └── 03-modeling.ipynb
├── src/               # 可重用的 Python 模組
│   ├── __init__.py
│   ├── data/
│   │   ├── make_dataset.py
│   │   └── preprocessing.py
│   ├── features/
│   │   └── build_features.py
│   └── models/
│       ├── train_model.py
│       └── predict_model.py
├── reports/           # 報告與簡報
│   ├── figures/
│   └── reports/
├── configs/           # 設定檔
│   └── config.yaml
└── tests/             # 測試
    ├── test_data.py
    └── test_models.py
```

## Notebook vs 腳本

Notebook 適合探索，腳本適合生產：

```
探索階段 → Jupyter Notebook
             │
             ▼
定型階段 → Python 腳本（src/）
             │
             ▼
生產階段 → API/排程任務
```

**Notebook 的使用原則**：
- 依序編號：`01-`, `02-`, `03-`
- 每個 notebook 有明確目的
- 結束時清理不必要的儲存格
- 關鍵結果輸出到 reports/

## 配置管理

```yaml
# configs/config.yaml
data:
  raw_path: "data/raw/train.csv"
  processed_path: "data/processed/"

features:
  numeric: ["age", "income"]
  categorical: ["dept", "city"]
  target: "churn"

model:
  type: "random_forest"
  params:
    n_estimators: 100
    max_depth: 10
    random_state: 42
```

```python
import yaml

with open("configs/config.yaml") as f:
    config = yaml.safe_load(f)

model_params = config["model"]["params"]
```

## 可重現性

```bash
# 建立獨立的虛擬環境
python -m venv .venv
source .venv/bin/activate

# 固定所有相依套件版本
pip freeze > requirements.txt
```

使用 Docker 確保完全可重現：

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
COPY configs/ configs/
CMD ["python", "src/models/train_model.py"]
```

## 版本控制

```bash
# data 資料夾通常用 DVC 管理
dvc init
dvc add data/raw/train.csv

# 程式碼用 Git
git add src/ notebooks/ configs/
git commit -m "Add feature engineering pipeline"
```

## 測試策略

```python
# tests/test_preprocessing.py
import pytest
import pandas as pd
from src.features.build_features import create_features

def test_create_features():
    data = pd.DataFrame({
        "x": [1, 2, 3],
        "y": [4, 5, 6],
    })
    result = create_features(data)
    assert "x_y_ratio" in result.columns
    assert len(result) == 3
```

## 延伸閱讀

- [Cookiecutter Data Science](https://www.google.com/search?q=Cookiecutter+Data+Science)
- [MLflow 專案管理](https://www.google.com/search?q=MLflow+project+management)
- [DVC 資料版本控制](https://www.google.com/search?q=DVC+data+version+control)
