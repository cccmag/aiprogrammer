# 機器學習中的版本控制

## 前言

機器學習專案涉及資料、模型、參數等多種變更，需要特別的版本控制策略。

---

## ML 專案的挑戰

1. **資料版本化**：訓練資料會變更
2. **模型版本化**：實驗產生大量模型
3. **超參數追蹤**：不同的實驗配置
4. **依賴管理**：框架版本衝突

---

## MLflow

MLflow 是一個開源的 ML 生命週期管理平台。

### 安裝

```bash
pip install mlflow
```

### 追蹤實驗

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

mlflow.set_experiment("classification")

with mlflow.start_run():
    # 記錄參數
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # 訓練模型
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # 記錄指標
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # 記錄模型
    mlflow.sklearn.log_model(model, "model")
```

### 查詢實驗

```bash
mlflow ui
# 在瀏覽器打開 http://localhost:5000
```

[搜尋 MLflow getting started](https://www.google.com/search?q=MLflow+getting+started)

---

## DVC (Data Version Control)

DVC 是專門設計用於資料和模型版本控制的工具。

### 安裝

```bash
pip install dvc
```

### 初始化

```bash
dvc init
git add .
git commit -m "Initialize DVC"
```

### 追蹤資料

```bash
# 新增資料檔案
dvc add data/raw.csv

# 設定遠端存儲
dvc remote add myremote s3://mybucket/data
dvc remote -d myremote

# 推送
git add data/raw.csv.dvc .gitignore
git commit -m "Add raw data"
dvc push
```

### 建立 Pipeline

```bash
# train.dvc
dvc run -n train \
  -d data/prepared.csv \
  -d src/train.py \
  -o models/model.pkl \
  python src/train.py
```

---

## Git LFS

處理大型模型檔案：

```bash
# 安裝
git lfs install

# 追蹤模型檔案
git lfs track "*.h5"
git lfs track "*.pkl"
git lfs track "*.pt"

cat .gitattributes
```

---

## 模型登錄 (Model Registry)

集中管理模型版本：

```bash
# MLflow model registry
mlflow models serve -m models:/production/1 -p 1234
```

---

## 實驗記錄範例

```python
import json
import os
from datetime import datetime

class ExperimentTracker:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.runs = []
    
    def log_run(self, params, metrics):
        run = {
            'timestamp': datetime.now().isoformat(),
            'params': params,
            'metrics': metrics
        }
        self.runs.append(run)
        
        with open(f'{self.experiment_name}_results.json', 'a') as f:
            f.write(json.dumps(run) + '\n')
    
    def get_best_run(self, metric):
        if not self.runs:
            return None
        return max(self.runs, key=lambda r: r['metrics'].get(metric, 0))
```

---

## 資料集版本化策略

### 快照策略

每個資料版本建立對應的 Git tag：

```bash
dvc add data/v1/
git add data/v1.dvc
git tag -a data-v1 -m "Dataset version 1"
```

### 差異化策略

只版本化資料的改變描述，實際資料存在外部存儲。

---

## 小結

ML 專案需要超越傳統的 Git 版本控制，結合專門的工具來管理資料、模型和實驗。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [MLflow 官方網站](https://mlflow.org/)
- [DVC 官方網站](https://dvc.org/)
- [ML version control best practices](https://www.google.com/search?q=ML+version+control+best+practices)