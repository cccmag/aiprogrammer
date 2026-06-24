# DVC 資料版本控制

## 前言

資料版本控制是 AI 專案管理的痛點。傳統 Git 不擅長處理大型檔案，而 DVC（Data Version Control）填補了這個空白。DVC 讓資料集和模型像程式碼一樣可以版本化管理、回滾和協作。

## DVC 核心概念

DVC 在 Git 之上建立了一個資料追蹤層。它不儲存資料本身，而是儲存資料檔案的指標（指紋），實際資料儲存在遠端儲存（S3、GCS、MinIO 等）。

```python
# 初始化 DVC
# $ dvc init

# 追蹤資料目錄
# $ dvc add data/raw/

""" dvc add 會產生 .dvc 檔案記錄資料的 MD5 雜湊 """

import os
import hashlib
import json

def compute_md5(filepath: str) -> str:
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def create_dvc_file(data_path: str, output: str):
    """模擬 DVC 的 .dvc 檔案結構"""
    entries = []
    for root, _, files in os.walk(data_path):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, data_path)
            entries.append({
                "md5": compute_md5(full),
                "path": rel,
                "size": os.path.getsize(full),
            })
    with open(output, "w") as fp:
        json.dump({"md5": hashlib.md5(data_path.encode()).hexdigest(), "entries": entries}, fp)
    print(f"已產生 {output}")

create_dvc_file("./data/raw", "data_raw.dvc")
```

## 版本管理實戰

DVC 讓資料集版本切換如同 Git 分支一樣簡單：

```bash
# $ git checkout v1.0
# $ dvc checkout
# 以上指令會將資料恢復到 v1.0 對應的版本
```

```python
""" 從 Python 使用 DVC API """
import dvc.api
import pandas as pd

# 指定版本讀取資料
with dvc.api.open(
    "data/processed/train.parquet",
    repo=".",
    rev="experiment-1"
) as fd:
    df = pd.read_parquet(fd)
    print(f"載入資料形狀: {df.shape}")
```

## DVC Pipeline

DVC 還能定義資料管線，自動追蹤資料血緣：

```python
# dvc.yaml
stages:
  clean:
    cmd: python src/clean.py data/raw data/clean
    deps:
      - src/clean.py
      - data/raw
    outs:
      - data/clean
  train:
    cmd: python src/train.py data/clean model.pkl
    deps:
      - src/train.py
      - data/clean
    outs:
      - model.pkl
    metrics:
      - metrics.json:
          cache: false
```

```python
# $ dvc repro
# 自動檢測依賴變化，只重新執行必要的步驟
```

## 結語

DVC 是 MLOps 工具箱中不可或缺的一環。它將資料版本管理納入熟悉的 Git 工作流程，讓團隊可以輕鬆重現實驗結果、追蹤資料變更，並與 CI/CD 管線整合。

---

**延伸閱讀**

- [DVC 官方文件](https://www.google.com/search?q=DVC+data+version+control+documentation)
- [DVC Pipelines 指南](https://www.google.com/search?q=DVC+pipeline+tutorial)
- [MLOps 資料版本管理實踐](https://www.google.com/search?q=MLOps+data+version+control+best+practices)
